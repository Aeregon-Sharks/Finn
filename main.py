from controller.controlador import Controlador
from view.VentanaPrincipal import VentanaPrincipal

if __name__=='__main__':
    vista = VentanaPrincipal()
    controlador = Controlador(vista)
    vista.mainloop()