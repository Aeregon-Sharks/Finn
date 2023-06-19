import json
from model.billetera import Billetera

class Controlador():
    def __init__(self, vista):

        # Cargar datos
        try:
            with open('data/data.json', 'r') as f:
                self.data = json.load(f)
        except:
            self.data = [{"nombre": "Efectivo", 
                      "mostrar_nombre": False, 
                      "saldo": 0, 
                      "icono": "icos/ef.png"}, 
                      {"nombre": "Movil", 
                       "mostrar_nombre": False, 
                       "saldo": 0, 
                       "icono": "icos/mov.png"}, 
                       {"nombre": "Tarjeta", 
                        "mostrar_nombre": False, 
                        "saldo": 0, 
                        "icono": "icos/tar.png"}, 
                        {"nombre": "Paypal", 
                         "mostrar_nombre": False, 
                         "saldo": 0, 
                         "icono": "icos/pay.png"}]
            with open('data/data.json', 'w') as f:
                json.dump(self.data, f)

        self.vista = vista
        # Memoria de cambios
        self.hist_mem = []
        # Frames de cada billetera para operar con ellos
        self.bill_frames = {}
        self.pre_load_bills()
        # Obtener el total y crear la interfaz base con el
        self.total = self.get_total()
        vista.crear_interfaz(self.total , 1_200_000)
        # Funcionalidad para cada boton
        self.func_botones()
        # Funcionalidad ventanas
        self.func_Tk()
    
    def pre_load_bills(self):
        # Se carga cada bill que habia en el archivo data
        for bill in self.data:
            # Se extraen sus porpiedades para un objeto Billetera, se agrega a bill_frames creando un frame nuevo para ese objeto.
            bill_temp = Billetera(bill['nombre'], bill['mostrar_nombre'], bill['saldo'], bill['icono'])
            self.bill_frames[bill_temp.nombre] = self.vista.new_frame(bill_temp)

    def func_botones(self):
        # Funciones de botones CRUD en cada FRAME, y boton obj. Entramos en cada bill_frame y extraemos cada boton y billetera correspondiente.
        for frame_data in self.bill_frames.values():
            # Botones actuales
            botones = frame_data['botones']
            # Billetera actual
            bill = frame_data['bill']
            # Agregar funcionalidad crud a cada boton
            botones['add'].config(command=lambda b=bill: self.sumar_saldo(b))
            botones['rm'].config(command=lambda b=bill: self.restar_saldo(b))
            botones['pas'].config(command=lambda b=bill: self.mover_saldo(b))
            # Boton objetivo que tendra el nombre de la billetera para cuando se quiera pasar saldo a ella
            botones['obj'].config(command=lambda n=bill.nombre: self.obj_select(n))
        # Funciones de botones en interfaz
        self.vista.btn_undo.config(command=lambda: self.undo())
        self.vista.btn_save.config(command=lambda: self.save())
        self.vista.btn_gastos_mes.config(command=lambda: self.show_gastos_mes())
        self.vista.btn_gastos.config(command=lambda: self.show_gastos())
        self.vista.btn_hist.config(command=lambda: self.show_hist())

    def func_Tk(self):
        self.vista.protocol("WM_DELETE_WINDOW", self.verify_changes)
    
    def verify_changes(self):
        state_save = self.vista.btn_save.cget("state")
        if state_save == "normal":
            save = self.vista.on_closing()
            if save:
                self.save()
                self.vista.destroy()
        else:
            self.vista.destroy()

    def obj_select(self, name=None):
        # Se muestran las opciones disponibles para mover el dinero, no se muestra la misma billetera de la cual se va a sacar dinero
        self.vista.show_obj_win(self.opts, False)
        # Si hay algun nombre de billetera, es porque ya hubo un target, entonces se inicia el proceso para mover saldo
        if name:
            # primera billetera, text variable, y se guarda hist para ver si se agrega al historial
            b1 = self.bill_frames[name]['bill']
            tv1 = self.bill_frames[name]['lb_text']['tv']
            hist1 = (b1.saldo, b1.nombre)
            # Se suma saldo a la billetera objetivo (name)
            b1.suma_saldo(self.cantidad)
            # Segunda billetera, se guarda en hist2 para ver si se agrega al historial
            b2 = self.bill_frames[self.ignor]['bill']
            tv2 = self.bill_frames[self.ignor]['lb_text']['tv']
            hist2 = (b2.saldo, b2.nombre, True)
            # Se resta saldo a la billetera origen (self.ignor) la cual se ignoraba y no se mostraba en las opciones
            b2.resta_saldo(self.cantidad)
            # Actualizar vista con nuevos saldos
            self.vista.update_elms(tv1, b1.saldo)
            self.vista.update_elms(tv2, b2.saldo)
            # Verificar el historial, agregar elementos a él, y activar botones guardar y deshacer
            if not self.verif_hist_mem():
                self.hist_mem.pop(0)
                self.hist_mem.pop(0)
                if self.hist_mem[0][-1] == True:
                    self.hist_mem.pop(0)

            self.hist_mem.append(hist1)
            self.hist_mem.append(hist2)

            self.vista.enable_btn(self.vista.btn_save)
            self.vista.enable_btn(self.vista.btn_undo)

    def sumar_saldo(self, bill):
        # Entry, text variable del entry y del frame, junto a la cantidad a sumar
        ent = self.bill_frames[bill.nombre]['entry']['ent']
        tv_ent = self.bill_frames[bill.nombre]['entry']['tv']
        tv = self.bill_frames[bill.nombre]['lb_text']['tv']
        cantidad = self.vista.get_ent(ent)
        # Historial
        hist = (bill.saldo, bill.nombre)
        # Se suma la cantidad a la billetera
        bill.suma_saldo(cantidad)
        # Actualizar Vista, Entry y Total.
        self.vista.update_elms(tv, bill.saldo)
        tv_ent.set('$')
        self.upd_total()

        # Verificar el historial, agregar elementos a él, y activar botones guardar y deshacer
        if not self.verif_hist_mem():
            self.hist_mem.pop(0)
            if self.hist_mem[0][-1] == True:
                self.hist_mem.pop(0)
        self.hist_mem.append(hist)
        self.vista.enable_btn(self.vista.btn_save)
        self.vista.enable_btn(self.vista.btn_undo)

    def restar_saldo(self, bill):
        # Entry, text variable del entry y del frame, junto a la cantidad a restar
        ent = self.bill_frames[bill.nombre]['entry']['ent']
        tv_ent = self.bill_frames[bill.nombre]['entry']['tv']
        tv = self.bill_frames[bill.nombre]['lb_text']['tv']
        cantidad = self.vista.get_ent(ent)
        # Historial
        hist = (bill.saldo, bill.nombre)
        # Se resta la cantidad de la billetera
        bill.resta_saldo(cantidad)
        # Actualizar Vista, Entry y Total.
        self.vista.update_elms(tv, bill.saldo)
        tv_ent.set('$')
        self.upd_total()
        # Verificar el historial, agregar elementos a él, y activar botones guardar y deshacer
        if not self.verif_hist_mem():
            self.hist_mem.pop(0)
            if self.hist_mem[0][-1] == True:
                self.hist_mem.pop(0)
        self.hist_mem.append(hist)
        self.vista.enable_btn(self.vista.btn_save)
        self.vista.enable_btn(self.vista.btn_undo)

    def mover_saldo(self, bill):
        # Entrada, text variable de la entrada y cantidad a mover. Cantidad en variable global para usarse luego en el menu de selección de objetivo
        ent = self.bill_frames[bill.nombre]['entry']['ent']
        tv_ent = self.bill_frames[bill.nombre]['entry']['tv']
        self.cantidad = self.vista.get_ent(ent)
        # Se cambia el comportamiento de la ventana para que al cerrarse olvide los botones
        self.vista.obj_win.protocol("WM_DELETE_WINDOW", lambda: self.obj_select())
        # Billetera a ignorar entre las opciones, y a su vez, billetera origen
        self.ignor = bill.nombre
        # Opciones
        self.opts = []
        for obj in self.bill_frames.values():
            # Todas las que no sean la origen
            if obj['bill'].nombre != self.ignor:
                self.opts.append(obj['botones']['obj'])
        # Se muestra la nueva ventana para elegir un objetivo con las opciones
        self.vista.show_obj_win(self.opts)
        # Reiniciar entry
        tv_ent.set('$')

    # Obtener el total
    def get_total(self):
        # La suma de todas las bill_frames en la posicion 'bill' para bill en sus llaves
        total = sum(self.bill_frames[bill]['bill'].saldo for bill in self.bill_frames.keys())
        return total
    # Actualizar el total
    def upd_total(self):
        # Se obtiene el total y se actualiza en la vista
        total = self.get_total()
        self.vista.update_elms(self.vista.tot, total)

    # Deshacer
    def undo(self):
        # Se quita el ultimo elemento del historial
        last = self.hist_mem.pop()
        # El nombre de la billetera que se modificó es el segundo elemento
        bill_n = last[1]
        # Se obtiene la text variable que debemos modificar
        tv = self.bill_frames[bill_n]['lb_text']['tv']
        # Si el ultimo cambio tiene 3 de longitud, es porque fue un 'mover saldo'. Por lo que se requieren 2 cambios
        if len(last) == 3:
            # Segundos elementos del historial
            last_2 = self.hist_mem.pop()
            bill_n_2 = last_2[1]
            tv_2 = self.bill_frames[bill_n_2]['lb_text']['tv']
            # Se actualizan los segundos elementos visuales y la billetera
            self.vista.update_elms(tv_2, last_2[0])
            self.bill_frames[bill_n_2]['bill'].saldo = last_2[0]
        # Se actualizan los primeros elementos visuales y la billetera
        self.vista.update_elms(tv, last[0])
        self.bill_frames[bill_n]['bill'].saldo = last[0]
        # Se actualiza el total
        self.upd_total()
        # Si no hay mas en la memoria, se desactiva el boton de deshacer
        if len(self.hist_mem) == 0:
            self.vista.disable_btn(self.vista.btn_undo)
        # Se activa el boton de guardar
        self.vista.enable_btn(self.vista.btn_save)

    # Guardar cambios
    def save(self):
        new_data = []
        # Entrar en cada billetera y enumerarla para guardar en el JSON nuevo los datos
        for bill in self.bill_frames.values():
            # se guarda cada billetera y sus propiedades en cada posicion de la lista data
            new_data.append({"nombre":bill['bill'].nombre, "mostrar_nombre":bill['bill'].mostrar_nombre, "saldo":bill['bill'].saldo, "icono":bill['bill'].icono})
        # Se guarda la lista de Diccionarios
        with open('data/data.json', 'w') as f:
            json.dump(new_data, f)
        # Se desactiva el boton de guardar
        self.vista.disable_btn(self.vista.btn_save)

    # Mostrar gastos mensuales
    def show_gastos_mes(self):
        pass

    # Mostrar gastos
    def show_gastos(self):
        pass

    # Mostrar historial
    def show_hist(self):
        print(self.hist_mem)
    # Verificar si la memoria tiene muchas cosas
    def verif_hist_mem(self):
        return len(self.hist_mem) < 30