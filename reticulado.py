
import numpy as np
from scipy.linalg import solve

class Reticulado(object):
    """Define un reticulado"""
    __NNodosInit__ = 1

    def __init__(self):
        super(Reticulado, self).__init__()
        self.xyz = np.zeros((Reticulado.__NNodosInit__,3), dtype=np.double)
        self.Nnodos = 0
        self.barras = []
        self.Ndimensiones = 3
        self.cargas = {}
        self.restricciones = {}
        

    def agregar_nodo(self, x, y, z=0):
        if self.Nnodos+1 > Reticulado.__NNodosInit__:
            self.xyz.resize((self.Nnodos+1,3))
        self.xyz[self.Nnodos,:] = [x, y, z]
        self.restricciones[self.Nnodos]=[] 
        self.cargas[self.Nnodos]=[]  
        self.Nnodos += 1





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
        
        fcp=factor_peso_propio
        ponderador=[fcp[0],fcp[1],fcp[2],fcp[0],fcp[1],fcp[2]] 
        
        for barr in self.barras:
            
            ni,nj = barr.obtener_conectividad()
            k_chica= barr.obtener_rigidez(self)
            f_chica= np.array([x*y for x,y in zip( barr.obtener_vector_de_cargas(self) ,ponderador)])
            
            pos_i= [ni*3,ni*3+1, ni*3+2 ,nj*3,nj*3+1,nj*3+2]
                
            for i in range(self.Ndimensiones*2):
                p = pos_i[i]

                for j in range(self.Ndimensiones*2):
                    q = pos_i[j]
                    self.K[p,q] += k_chica[i,j]

                self.f[p] += f_chica[i]
                
        for i in range(self.Nnodos):
            for car in self.cargas[i]:
                if len(car) > 0:
                    self.f[i*3+car[0]] = car[1]
        self.F = self.f
        
    def resolver_sistema(self):
        
        # 0 : Aplicar restricciones
        Ngdl = self.Nnodos * self.Ndimensiones
        gdl_libres = np.arange(Ngdl)
        gdl_restringidos = []

        #Pre-llenar el vector u

        for nodo in self.restricciones:
            for restriccion in self.restricciones[nodo]:
                gdl = restriccion[0]
                valor = restriccion[1]

                gdl_global = self.Ndimensiones*nodo + gdl
                self.u[gdl_global] = valor

                gdl_restringidos.append(gdl_global)

        # con gdl_restringidos encuentro  gdl_libres
        gdl_restringidos = np.array(gdl_restringidos)
        gdl_libres = np.setdiff1d(gdl_libres, gdl_restringidos)

    
        for nodo in self.cargas:
            for carga in self.cargas[nodo]:
                gdl = carga[0]
                valor = carga[1]

                gdl_global = self.Ndimensiones*nodo + gdl
                self.f[gdl_global] = valor

        #1 Particionar:
        """
        Kff = self.K[np.ix_(gdl_libres, gdl_libres)]
        Kcc = self.K[np.ix_(gdl_restringidos, gdl_restringidos)]
        Kcf = self.K[np.ix_(gdl_restringidos, gdl_libres)]
        Kfc = self.K[np.ix_(gdl_libres, gdl_restringidos)]
 
        uf = self.u[gdl_libres]
        uc = self.u[gdl_restringidos]

        ff = self.f[gdl_libres] - Kfc@uc
        fc = self.f[gdl_restringidos]

        # Solucionar Kff uf = ff

        self.u[gdl_libres] = solve(Kff, ff)
        R = Kcf@uf+Kcc@uc-fc
        """
        Kff = self.K[np.ix_(gdl_libres, gdl_libres)]
        Kfc = self.K[np.ix_(gdl_libres, gdl_restringidos)]
        Kcf = Kfc.T
        Kcc = self.K[np.ix_(gdl_restringidos, gdl_restringidos)]
 
        uf = self.u[gdl_libres]
        uc = self.u[gdl_restringidos]

        ff = self.f[gdl_libres]
        fc = self.f[gdl_restringidos]

        # Solucionar Kff uf = ff
        
        uf = solve(Kff, ff - Kfc @ uc)
        R = Kcf@uf+Kcc@uc-fc
        self.R = R
        self.Kff = Kff
        self.Kcc = Kcc
        self.Kfc = Kfc
        self.Kcf = Kcf
        self.u[gdl_libres] = uf
        lis = []
        # for i in range(self.__NNodosInit__):
        #     lis.append(i)
        # for i in range(self.Nnodos):
        #     lis.remove(i)
        # self.xyz = np.delete(self.xyz,lis,axis=0)
        
        return 0

    def obtener_desplazamiento_nodal(self, n):
        
        dofs = [3*n, 3*n+1, 3*n+2]
        return self.u[dofs]
        # return 0


    def obtener_fuerzas(self):
        
        fuerzas = np.zeros(len(self.barras))
        contador = 0
        for i in self.barras:
            fuerzas[contador] = i.obtener_fuerza(self)
            contador += 1

        return fuerzas



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
        s += "restricciones:\n"
        for nodo in self.restricciones:
            if len(self.restricciones[nodo]) != 0:
                s += f"    {nodo} : {self.restricciones[nodo]}\n"
        s += "\n\n"
        
        contador = 0
        for nodo in self.cargas:
            if len(self.cargas[nodo]) != 0:
                contador += 1
        if contador != 0:
            s += "cargas:\n"
            for nodo in self.cargas:
                if len(self.cargas[nodo]) != 0:
                    s += f"    {nodo} : {self.cargas[nodo]}\n"
            s += "\n\n"

        s += "desplazamientos:\n"
        for n in range(self.Nnodos):
            s += f"    {n} : ( {self.obtener_desplazamiento_nodal(n)}) \n "
        s += "\n\n"


        f = self.obtener_fuerzas()
        s += "fuerzas:\n"
        for b in range(len(self.barras)):
            s += f"    {b} : {f[b]}\n"
        s += "\n"
        return s