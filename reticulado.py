
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
        
        if nodo not in self.restricciones:
            self.restricciones[nodo] = [[gdl, valor]]
        else:
            self.restricciones[nodo].append([gdl, valor])


    def agregar_fuerza(self, nodo, gdl, valor):
        
        if nodo not in self.cargas:
            self.cargas[nodo] = [[gdl, valor]]
        else:
            self.cargas[nodo].append([gdl, valor])

    def ensamblar_sistema(self, factor_peso_propio=0.):
        if factor_peso_propio==0.:
            factor_peso_propio=[0.,0.,0.]
        
        tamano=self.Nnodos*self.Ndimensiones
        self.K=np.zeros((tamano,tamano),dtype=np.double)
        self.f=np.zeros(tamano)
        self.u = np.zeros((tamano), dtype=np.double)
        for barr in self.barras:
            
            ni,nj = barr.obtener_conectividad()
            k_chica= barr.obtener_rigidez(self)
            
            
            peso_barra= barr.calcular_peso(self)

            self.agregar_fuerza(ni,1,-peso_barra/2.0*factor_peso_propio[1])
            self.agregar_fuerza(nj,1,-peso_barra/2.0*factor_peso_propio[1])
            f_chica= barr.obtener_fuerza(self)
            

            
            if self.Ndimensiones ==2:
                pos_i= [ni*2,ni*2+1,nj*2,nj*2+1]
            elif self.Ndimensiones ==3:
                pos_i= [ni*3,ni*3+1, ni*3+2 ,nj*3,nj*3+1,nj*3+2]
                
            for i in range(self.Ndimensiones*2):
                p = pos_i[i]

                for j in range(self.Ndimensiones*2):
                    q = pos_i[j]
                    self.K[p,q] += k_chica[i,j]
                self.f[p] = f_chica[i]



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