class Billetera:
    def __init__(self, nombre:str, mostrar_nombre:bool, saldo:float, icono:str):
        self.nombre = nombre
        self.mostrar_nombre = mostrar_nombre
        self.saldo = saldo
        self.icono = icono
    
    def suma_saldo(self, cant):
        self.saldo += cant

    def resta_saldo(self, cant):
        self.saldo -= cant

    def mover_saldo(self, cant, objetivo):
        self.saldo -= cant
        objetivo.suma_saldo(cant)
