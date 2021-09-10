
import numpy as np
from scipy.linalg import solve

class Reticulado(object):
    """Define un reticulado"""
    __NNodosInit__ = 100

    def __init__(self):
        super(Reticulado, self).__init__()
        self.xyz = np.zeros((Reticulado.__NNodosInit__,3), dtype=np.double)
        self.Nnodos = 0
        self.barras = []
        self.Ndimensiones = 2
        self.cargas = {}
        self.restricciones = {}
        

    def agregar_nodo(self, x, y, z=0):
        if self.Nnodos+1 > Reticulado.__NNodosInit__:
            self.xyz.resize((self.Nnodos+1,3))
        self.xyz[self.Nnodos,:] = [x, y, z]
        self.Nnodos += 1
        if z != 0.:
            self.Ndimensiones = 3
            



    def agregar_barra(self, barra):
        self.barras.append(barra)
        


    def obtener_coordenada_nodal(self, n):
        
        return self.xyz[n,:]


    def calcular_peso_total(self):
        
        peso_total=0
        for i in self.barras:
            peso_total+= i.calcular_peso(self)
        return peso_total



    def obtener_nodos(self):
        
        return self.xyz

    def obtener_barras(self):
        
        return self.barras



    def agregar_restriccion(self, nodo, gdl, valor=0.0):
        
        """Implementar"""	
        
        return 0

    def agregar_fuerza(self, nodo, gdl, valor):
        
        """Implementar"""	
        
        return 0


    def ensamblar_sistema(self):
        
        """Implementar"""	
        
        return 0



    def resolver_sistema(self):
        
        """Implementar"""	
        
        return 0

    def obtener_desplazamiento_nodal(self, n):
        
        """Implementar"""	
        
        return 0


    def obtener_fuerzas(self):
        
        """Implementar"""	
        
        return 0


    def obtener_factores_de_utilizacion(self, f):
        
        """Implementar"""	
        
        return 0

    def rediseñar(self, Fu, ϕ=0.9):
        
        """Implementar"""	
        
        return 0



    def chequear_diseño(self, Fu, ϕ=0.9):
        
        """Implementar"""	
        
        return 0







    def __str__(self):
        NODOS = self.obtener_nodos()
        s = "nodos:"
        s += "\n"
        for i in range(self.Nnodos):
            s += "     "+str(i)+" : "+str(tuple(NODOS[i]))+"\n"
        BARRAS = self.obtener_barras()
        s += "\n"
        s += "\n"
        s += "barras:\n"
        for j in range(len(BARRAS)):
            s += "     "+str(j)+" : "+"[ "+str(BARRAS[j].ni)+" "+str(BARRAS[j].nj)+" ]"+"\n"
        s += "\n"
        return s