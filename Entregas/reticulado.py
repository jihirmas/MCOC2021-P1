import numpy as np
from scipy.linalg import solve
import h5py as h5
from barra import Barra
from constantes import g_, ρ_acero, E_acero
from secciones import SeccionICHA

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

    def ensamblar_sistema(self, factor_peso_propio=[0., 0., 0.],factor_cargas=0.):
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
            
            
            f_chica= barr.obtener_vector_de_cargas(self)
            if factor_peso_propio == [0.,0.,0.]:
                f_chica = np.zeros(self.Ndimensiones*2)
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
        self.gdl_libres = gdl_libres
        # lis = []
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


    def obtener_factores_de_utilizacion(self, f, ϕ=0.9):
        
        FU = np.zeros((len(self.barras)), dtype=np.double)
        for i,b in enumerate(self.barras):
            FU[i] = b.obtener_factor_utilizacion(f[i], ϕ)

        return FU


    def rediseñar(self, Fu, ϕ=0.9):
        for i,b in enumerate(self.barras):
           print(f"\n\nBarra {i}")
           b.rediseñar(Fu[i], self, ϕ)
    
    def guardar(self, nombre):
        
        metadatos =h5.File(nombre,"w")
        
        xyz_prima= np.zeros((self.Nnodos,3))
        for i in range(self.Nnodos):
            xyz_prima[i,:]=self.xyz[i,:]
            
        metadatos["xyz"]= xyz_prima
        
        barras_prima= np.zeros((len(self.barras),2),dtype=np.int32)
        for i,barr in enumerate(self.barras):
            barras_prima[i,:]= [barr.ni,barr.nj]
            
        metadatos["barras"]= barras_prima
        
        secciones_prima = np.zeros((len(self.barras),1),dtype=h5.string_dtype())
        for i,barr in enumerate(self.barras):
            secciones_prima[i]= barr.seccion.nombre()
        metadatos["secciones"]= secciones_prima
        
        restricciones_prima= []
        restricciones_val  = []
        for i,res in enumerate(self.restricciones):
            for j in self.restricciones[res]:
                restricciones_prima.append([i,j[0]])
                restricciones_val .append(j[1])
        restricciones_prima= np.array(restricciones_prima,dtype=h5.string_dtype())
        restricciones_val= np.array(restricciones_val,dtype=h5.string_dtype())
        
        metadatos["restricciones"]= restricciones_prima
        metadatos["restricciones_val"]= restricciones_val
        
        cargas_prima= []
        cargas_val  = []
        for i,car in enumerate(self.cargas):
            for j in self.cargas[car]:
                cargas_prima.append([i,j[0]])
                cargas_val.append(j[1])
        cargas_prima= np.array(cargas_prima,dtype=h5.string_dtype())
        cargas_val= np.array(cargas_val,dtype=h5.string_dtype())
        
        metadatos["cargas"]= cargas_prima
        metadatos["cargas_val"]= cargas_val
        
        metadatos.close()

    def abrir(self, nombre):
        
        metadatos =h5.File(nombre,"r")
        
        xyz_prima = metadatos["xyz"]
        barras_prima = metadatos["barras"]
        secciones_prima = metadatos["secciones"]
        restricciones_prima = metadatos["restricciones"]
        restricciones_val = metadatos["restricciones_val"]
        cargas_prima = metadatos["cargas"]
        cargas_val = metadatos["cargas_val"]

        for i in xyz_prima:
            self.agregar_nodo(i[0],i[1],i[2])                            
        
        for i, barr in enumerate(barras_prima):
            self.agregar_barra(Barra(np.int32(barr[0]),np.int32(barr[1]),SeccionICHA(secciones_prima[i][0]),color=np.random.rand(3)))
        
        for i, res in enumerate(restricciones_prima):           
            self.agregar_restriccion(np.int32(res[0]),np.int32(res[1]),np.int32(restricciones_val[i]))
        
        for i, car in enumerate(cargas_prima):           
            self.agregar_fuerza( np.int32(car[0]),np.float32(car[1]),np.float32(cargas_val[i]))
        
        
        metadatos.close()



    def chequear_diseño(self, Fu, ϕ=0.9):
        cumple = True
        for i,b in enumerate(self.barras):
            if not b.chequear_diseño(Fu[i], self, ϕ):
                print(f"----> Barra {i} no cumple algun criterio. ")
                cumple = False
        return cumple







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