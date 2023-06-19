import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox

class VentanaPrincipal(tk.Tk):

    def __init__(self):
        super().__init__()
        # Icono y propiedades de la ventana principal.
        self.iconbitmap('icos/icon.ico')
        self.font = ('Arial', 20)
        self.title("Finn")
        self.geometry("800x500")
        self.configure(background='#ecfcff')
        self.resizable(False, False)

        # Total frame.
        self.tot = tk.StringVar()
        self.fr_tot = tk.Frame(self, borderwidth=2, relief='groove', width=700, height=45, background='#cff9ff')
        self.lb_tot = tk.Label(self.fr_tot, textvariable=self.tot, font=self.font, background='#cff9ff')
        self.lb_tot_tx = tk.Label(self.fr_tot, text='Total', font=self.font, background='#cff9ff')
        # Total estimado frame.
        self.tot_es = tk.StringVar()
        self.fr_tot_es = tk.Frame(self, borderwidth=2, relief='groove', width=700, height=45, background='#dffff5')
        self.lb_tot_es = tk.Label(self.fr_tot_es, textvariable=self.tot_es, font=self.font, background='#dffff5')
        self.lb_tot_es_tx = tk.Label(self.fr_tot_es, text='Total Estimado', font=self.font, background='#dffff5')
        # Conteo para saber donde ira cada Frame.
        self.fila = 0
        # Auxiliar para saber si se debe reiniciar la entrada.
        self.last_ent = ''
        # Ventana de seleccion al mover saldo.
        self.bg_obj = '#cfebff'
        self.obj_win = tk.Toplevel()
        self.obj_win.resizable(False, False)
        self.obj_win.geometry('180x160')
        self.lb_obj_fr = tk.Frame(self.obj_win, width=150, relief='groove', borderwidth=2, background=self.bg_obj)
        self.lb_obj = tk.Label(self.lb_obj_fr, text='Selecciona el destino', font=('Arial', 12), background=self.bg_obj)
        self.obj_win.withdraw()
        self.obj_fr = tk.Frame(self.obj_win, borderwidth=2, relief='groove', width=300)
        self.btn_obj_cncl = tk.Button(self.obj_win, text='Cancelar', command=lambda: self.obj_win.withdraw(), background='#ffeaea', borderwidth=2, height=1, width=24, relief='groove')
        self.btn_obj_cncl.grid(column=0, row=2, padx=0, pady=1)
        self.obj_fr.grid(column=0, row=1, pady=(0,1))
        self.lb_obj.grid(column=0, row=0, padx=10, pady=10)
        self.lb_obj_fr.grid(column=0, row=0, padx=1, pady=(1,0))
        
    # /-----/ Cargar imagenes /-----/
    def cargar_imagen(self, ruta, x, y):
        imagen = Image.open(ruta)
        imagen = imagen.resize((x, y), Image.ANTIALIAS)
        imagen = ImageTk.PhotoImage(imagen)
        return imagen  
    # /-------------//---------------/


    # /-----/ Creacion Frames /-----/
    def new_frame(self, bill):

        # Extraer iconos y formatear saldos.
        img_path = bill.icono
        tv_saldo = tk.StringVar()
        tv_saldo.set(self.formatear(bill.saldo))

        # Restriccion para el input.
        def restrict(char):
            if char.isdigit() or (char in ['$', ',']):
                return True
            else:
                return False
        # Formateo del input
        def format_entry(entry):
            val = entry.get()
            if self.last_ent != val:
                val = self.inverse_formatear(val)
                val = int(val)
                val = self.formatear(val)
                entry.delete(0, tk.END)
                entry.insert(0, val)
            self.last_ent = val
            
        # Elementos para cada billetera.
        # Frame
        frame = tk.Frame(self, borderwidth=2, relief='groove', width=700, height=80, background='#ecf6ff')
        frame.grid_propagate(0)
        frame.grid_columnconfigure(0, weight=1)
        # Icono
        ico = self.cargar_imagen(img_path, 60, 60)
        lb_img = tk.Label(frame, image=ico, background='#ecf6ff')
        lb_img.image = ico
        # Botones
        btn_add = tk.Button(frame, text='+', width=2, background='#CAFFB4', borderwidth=2)
        btn_rm = tk.Button(frame, text='-', width=2, background='#e48a8a', borderwidth=2)
        btn_pas = tk.Button(frame, text='↻', width=2, background='#fff5d5', borderwidth=2)
        btn_obj = tk.Button(self.obj_fr, text=bill.nombre, background='#ecf7ff', borderwidth=2, height=1, width=24, relief='groove')
        # propiedades On Hover y On Leave
        btn_add.bind('<Enter>', lambda event: btn_add.config(background='#51FF2B'))
        btn_add.bind('<Leave>', lambda event: btn_add.config(background='#CAFFB4'))

        btn_rm.bind('<Enter>', lambda event: btn_rm.config(background='#FF0000'))
        btn_rm.bind('<Leave>', lambda event: btn_rm.config(background='#e48a8a'))

        btn_pas.bind('<Enter>', lambda event: btn_pas.config(background='#FFEF2C'))
        btn_pas.bind('<Leave>', lambda event: btn_pas.config(background='#fff5d5'))

        btn_obj.bind('<Enter>', lambda event: btn_obj.config(background='#b3dbff'))
        btn_obj.bind('<Leave>', lambda event: btn_obj.config(background='#ecf7ff'))
        # Saldo
        lb_text = tk.Label(frame, textvariable=tv_saldo, font=self.font, background='#ecf6ff')
        # Entrada
        tv_en = tk.StringVar()
        tv_en.set('$')
        ent = tk.Entry(frame,font=('Arial', 11), width=15)
        ent.config(validate="key", validatecommand=(frame.register(restrict), "%S"), background='#cadae9', textvariable=tv_en)
        tv_en.trace("w", lambda n, i, m, tv_en=tv_en: format_entry(ent))
        # Grid
        # pady para el primer frame.
        if (self.fila == 0):
            pady1 = 30
            pady2 = 1
        else:
            pady1, pady2 = 1, 1

        frame.grid(column=0, row=self.fila, padx=45, pady=(pady1, pady2))
        lb_text.grid(column=0, row=0, padx=50)
        lb_img.grid(column=1, row=0, padx=(0, 20), pady=10)
        btn_add.grid(column=2, row=0, padx=(20, 6))
        btn_rm.grid(column=3, row=0, padx=6)
        btn_pas.grid(column=4, row=0, padx=(6, 20))
        ent.grid(column=5, row=0, padx=(0,20))
        # Nuevo indice para nuevas filas.
        self.fila += 1
        # Retorna los objetos creados, mas la billetera con la que fueron creados.
        return {
            'marco':frame, 
            'lb_img':lb_img, 
            'lb_text':{
                'lb':lb_text,
                'tv':tv_saldo
                },
            'botones':{
                'add': btn_add,
                'rm': btn_rm,
                'pas': btn_pas,
                'obj': btn_obj
            },
            'entry':{
                'tv': tv_en,
                'ent': ent
            },
            'bill':bill
        }
    # /-------------//---------------/


    # /------/ Interactuar con objetos /------/

    # Formatear cadenas de entero 100000000 texto a $100,000,000.
    def formatear(self, cad):
        return "${:,.0f}".format(cad)
    # Volver cadena de la forma $100,000,000 a entero 100000000.
    def inverse_formatear(self, cad):
        unf_cad = cad.replace(',', '').replace('$', '')
        return int(unf_cad)

    # Activar y desactivar botones
    def enable_btn(self, btn):
        btn.config(state=tk.NORMAL)
    def disable_btn(self, btn):
        btn.config(state=tk.DISABLED)

    # Mostrar la ventana de opciones para mover saldo, olvida los botones si G es False.
    def show_obj_win(self, opts, g=True):
        if g:
            for btn in opts:
                btn.grid()
            self.obj_win.deiconify()
        else:
            for btn in opts:
                btn.grid_forget()
            self.obj_win.withdraw()
    
    # Actualizar text variables.
    def update_elms(self, tv, new):
        if type(new) == int:
            new = self.formatear(new)
        tv.set(new)

    # Obtener la entrada de un entry y formatearla.
    def get_ent(self, ent):
        text = ent.get()
        text = self.inverse_formatear(text)
        return text
    # /-------------------//----------------------/


    # /------/ Interfaz base /------/
    def crear_interfaz(self, tot, tot_es):
        # Grid total
        self.tot.set(self.formatear(tot))
        self.fr_tot.grid(row=self.fila, pady= 1, padx=45)
        self.fr_tot.grid_propagate(0)
        self.fr_tot.grid_columnconfigure(0, weight=1)
        self.lb_tot.grid(column=0 ,padx=50)
        self.lb_tot_tx.grid(column=1, row=0, padx=(280, 30))

        self.fila += 1
        # Grid total estimado
        self.tot_es.set(self.formatear(tot_es))
        self.fr_tot_es.grid(row=self.fila, pady= (1, 0), padx=45)
        self.fr_tot_es.grid_propagate(0)
        self.fr_tot_es.grid_columnconfigure(0, weight=1)
        self.lb_tot_es.grid(column=0 ,padx=50)
        self.lb_tot_es_tx.grid(column=1, row=0, padx=(160, 30))

        self.fila += 1
        # Botones
        btn_bg = '#f0f8ff'
        self.btn_frame = tk.Frame(self, background='#ecfcff')
        self.btn_undo = tk.Button(self.btn_frame, relief='groove', text='Deshacer ⬅',font=('Arial', 10), width=14, height=1, background=btn_bg, borderwidth=2)
        self.btn_save = tk.Button(self.btn_frame, relief='groove', text='Guardar 💾',font=('Arial', 10), width=14, height=1, background=btn_bg, borderwidth=2)        
        self.btn_gastos_mes = tk.Button(self.btn_frame, relief='groove', text='Gastos Mes 📅',font=('Arial', 10), width=15, height=1, background=btn_bg, borderwidth=2)
        self.btn_gastos = tk.Button(self.btn_frame, relief='groove', text='Compras 🛒',font=('Arial', 10), width=14, height=1, background=btn_bg, borderwidth=2)
        self.btn_hist = tk.Button(self.btn_frame, relief='groove', text='Historial 📝',font=('Arial', 10), width=14, height=1, background=btn_bg, borderwidth=2)

        # Aplicamos propiedades de on hover y on leave a los botones
        def on_hover(event, button, hover_color):
            if button['state'] == tk.NORMAL:
                button.config(background=hover_color)
        def on_leave(event, button, default_color):
            button.config(background=default_color)
        hv_color = '#CDFDFF'
        def apply_hover(btns, hv_bg, df_bg):
            for btn in btns:
                btn.bind('<Enter>', lambda event, btn=btn: on_hover(event, btn, hv_bg))
                btn.bind('<Leave>', lambda event, btn=btn: on_leave(event, btn, df_bg))

        apply_hover((self.btn_undo, self.btn_save, self.btn_gastos_mes, self.btn_gastos, self.btn_hist), hv_color, btn_bg)
        apply_hover([self.btn_obj_cncl], '#ff8279', '#ffeaea')
        
        # Grid
        self.btn_undo.grid(row=0, column=0, padx=8, pady=(30,1))
        self.btn_save.grid(row=0, column=1, padx=8, pady=(30,1))
        self.btn_gastos_mes.grid(row=0, column=2, padx=8, pady=(30,1))
        self.btn_gastos.grid(row=0, column=3, padx=8, pady=(30,1))
        self.btn_hist.grid(row=0, column=4, padx=8, pady=(30,1))
        self.btn_frame.grid(row=self.fila)
        # Desactivar save y undo
        self.btn_save.config(state=tk.DISABLED)
        self.btn_undo.config(state=tk.DISABLED)



        # ///
        self.fr_tot_es.grid_forget()
        self.btn_gastos.grid_forget()
        self.btn_gastos_mes.grid_forget()
        self.btn_hist.grid_forget()
    # /-------------//---------------/

    def on_closing(self):
        result = messagebox.askyesnocancel("Confirmación", "¿Desea guardar los cambios antes de salir?")
        if result is True:
            return True
        elif result is False:
            self.destroy()  
        else:
            pass  
