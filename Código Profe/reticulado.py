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
        self.cargas = {}
        self.restricciones = {}
        self.Ndimensiones = 3
        self.has_solution = False

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
        if n >= self.Nnodos:
            return 
        return self.xyz[n, :]

    def calcular_peso_total(self):
        peso = 0.
        for b in self.barras:
            peso += b.calcular_peso(self)
        return peso

    def obtener_nodos(self):
        return self.xyz[0:self.Nnodos,:].copy()

    def obtener_barras(self):
        return self.barras








    def agregar_restriccion(self, nodo, gdl, valor=0.0):

        if nodo not in self.restricciones:
            self.restricciones[nodo] = [[gdl, valor]]
        else:
            self.restricciones[nodo].append([gdl, valor])


    def agregar_fuerza(self, nodo, gdl, valor):
        """
        Agrega una fuerza al sistema en el 'nodo', 
        y 'gdl' especificados con el 'valor' dado. 
        """
        if nodo not in self.cargas:
            self.cargas[nodo] = [[gdl, valor]]
        else:
            self.cargas[nodo].append([gdl, valor])


    def ensamblar_sistema(self, factor_peso_propio=[0., 0., 0.], factor_cargas=0.):
        
        Ngdl = self.Nnodos * self.Ndimensiones

        self.K = np.zeros((Ngdl,Ngdl), dtype=np.double)
        self.f = np.zeros((Ngdl), dtype=np.double)
        self.u = np.zeros((Ngdl), dtype=np.double)

        #Iterar sobre las barras:
        for i,b in enumerate(self.barras):
            ke = b.obtener_rigidez(self)
            fe = b.obtener_vector_de_cargas(self,factor_peso_propio) 

            # print(f"i = {i} fe = {fe}")

            ni, nj = b.obtener_conectividad()


            #MDR
            if self.Ndimensiones == 2:
                d = [2*ni, 2*ni+1 , 2*nj, 2*nj+1]
            else:
                d = [3*ni, 3*ni+1, 3*ni+2 , 3*nj, 3*nj+1, 3*nj+2]

            for i in range(self.Ndimensiones*2):
                p = d[i]
                for j in range(self.Ndimensiones*2):
                    q = d[j]
                    self.K[p,q] += ke[i,j]
                self.f[p] += fe[i]


        for nodo in self.cargas:
            for carga in self.cargas[nodo]:
                gdl = carga[0]
                valor = carga[1]

                self.gdl_global = self.Ndimensiones*nodo + gdl
                self.f[self.gdl_global] = factor_cargas*valor



    def resolver_sistema(self):

        # 0 : Aplicar restricciones
        Ngdl = self.Nnodos * self.Ndimensiones
        self.gdl_libres = np.arange(Ngdl)
        self.gdl_restringidos = []

        #Pre-llenar el vector u

        for nodo in self.restricciones:
            for restriccion in self.restricciones[nodo]:
                gdl = restriccion[0]
                valor = restriccion[1]

                self.gdl_global = self.Ndimensiones*nodo + gdl
                self.u[self.gdl_global] = valor

                self.gdl_restringidos.append(self.gdl_global)

        # con self.gdl_restringidos encuentro  self.gdl_libres
        self.gdl_restringidos = np.array(self.gdl_restringidos)
        self.gdl_libres = np.setdiff1d(self.gdl_libres, self.gdl_restringidos)


        #1 Particionar:


        self.Kff = self.K[np.ix_(self.gdl_libres, self.gdl_libres)]
        Kfc = self.K[np.ix_(self.gdl_libres, self.gdl_restringidos)]
        Kcf = Kfc.T
        Kcc = self.K[np.ix_(self.gdl_restringidos, self.gdl_restringidos)]
 
        uf = self.u[self.gdl_libres]
        uc = self.u[self.gdl_restringidos]

        ff = self.f[self.gdl_libres]
        fc = self.f[self.gdl_restringidos]

        # Solucionar Kff uf = ff
        uf = solve(self.Kff, ff - Kfc @ uc)

        self.u[self.gdl_libres] = uf

        self.has_solution = True

    def obtener_desplazamiento_nodal(self, n):
        if self.Ndimensiones == 2:
            dofs = [2*n, 2*n+1]
        elif self.Ndimensiones == 3:
            dofs = [3*n, 3*n+1, 3*n+2]
        else:
            print(f"Error en numero de dimensiones. Ndimensiones = {self.Ndimensiones == 2} ")

        return self.u[dofs]


    def obtener_fuerzas(self):
        
        fuerzas = np.zeros((len(self.barras)), dtype=np.double)
        for i,b in enumerate(self.barras):
            fuerzas[i] = b.obtener_fuerza(self)

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



    def chequear_diseño(self, Fu, ϕ=0.9, silence=False):
        cumple = True
        for i,b in enumerate(self.barras):
            if not b.chequear_diseño(Fu[i], self, ϕ, silence=silence):
                if not silence:
                    print(f"----> Barra {i} no cumple algun criterio. ")
                cumple = False
        return cumple












    def __str__(self):
        s = "nodos:\n"
        for n in range(self.Nnodos):
            s += f"  {n} : ( {self.xyz[n,0]}, {self.xyz[n,1]}, {self.xyz[n,2]}) \n "
        s += "\n\n"

        s += "barras:\n"
        for i, b in enumerate(self.barras):
            n = b.obtener_conectividad()
            s += f" {i} : [ {n[0]} {n[1]} ] \n"
        s += "\n\n"
        
        s += "restricciones:\n"
        for nodo in self.restricciones:
            s += f"{nodo} : {self.restricciones[nodo]}\n"
        s += "\n\n"
        
        s += "cargas:\n"
        for nodo in self.cargas:
            s += f"{nodo} : {self.cargas[nodo]}\n"
        s += "\n\n"

        if self.has_solution:
            s += "desplazamientos:\n"
            if self.Ndimensiones == 2:
                uvw = self.u.reshape((-1,2))
                for n in range(self.Nnodos):
                    s += f"  {n} : ( {uvw[n,0]}, {uvw[n,1]}) \n "
            if self.Ndimensiones == 3:
                uvw = self.u.reshape((-1,3))
                for n in range(self.Nnodos):
                    s += f"  {n} : ( {uvw[n,0]}, {uvw[n,1]}, {uvw[n,2]}) \n "
        s += "\n\n"

        if self.has_solution:
            f = self.obtener_fuerzas()
            s += "fuerzas:\n"
            for b in range(len(self.barras)):
                s += f"  {b} : {f[b]}\n"
        s += "\n"
        s += f"Ndimensiones = {self.Ndimensiones}"

        return s



    def guardar(self, nombre):
        import h5py

        fid = h5py.File(nombre, "w")

        fid["xyz"] = self.xyz

        Nbarras = len(self.barras)
        barras = np.zeros((Nbarras,2), dtype=np.int32)
        secciones = fid.create_dataset("secciones", shape=(Nbarras,1), dtype=h5py.string_dtype())

        for i, b in enumerate(self.barras):
            barras[i,0] = b.ni
            barras[i,1] = b.nj
            secciones[i] = b.seccion.nombre()

        fid["barras"] = barras

        data_rest = fid.create_dataset("restricciones", (1,2), maxshape=(None,2), dtype=np.int32)
        data_rest_val = fid.create_dataset("restricciones_val", (1,), maxshape=(None,), dtype=np.double)
        nr = 0
        for nodo in  self.restricciones:
            for gdl, val in self.restricciones[nodo]:
                data_rest.resize((nr+1,2))
                data_rest_val.resize((nr+1,))
                data_rest[nr, 0] = nodo
                data_rest[nr, 1] = gdl
                data_rest_val[nr] = val
                nr += 1


        data_cargas = fid.create_dataset("cargas", (1,2), maxshape=(None,2), dtype=np.int32)
        data_cargas_val = fid.create_dataset("cargas_val", (1,), maxshape=(None,), dtype=np.double)
        nr = 0
        for nodo in  self.cargas:
            for gdl, val in self.cargas[nodo]:
                data_cargas.resize((nr+1,2))
                data_cargas_val.resize((nr+1,))
                data_cargas[nr, 0] = nodo
                data_cargas[nr, 1] = gdl
                data_cargas_val[nr] = val
                nr += 1


    def abrir(self, nombre):
        import h5py
        from secciones import SeccionICHA
        from barra import Barra

        fid = h5py.File(nombre, "r")

        xyz = fid["xyz"][:,:]

        Nnodos = xyz.shape[0]

        for i in range(Nnodos):
            self.agregar_nodo(xyz[i,0], xyz[i,1], xyz[i,2])

        barras = fid["barras"]
        secciones = fid["secciones"]
        cargas = fid["cargas"]
        cargas_val = fid["cargas_val"]
        restricciones = fid["restricciones"]
        restricciones_val = fid["restricciones_val"]

        Nbarras = fid["barras"].shape[0]

        dict_secciones = {}

        for i in range(Nbarras):
            ni = barras[i,0]
            nj = barras[i,1]

            den = secciones[i][0]

            if not den in dict_secciones:
                dict_secciones[den] = SeccionICHA(den)

            self.agregar_barra(Barra(ni,nj,dict_secciones[den]))
            

        for i in range(restricciones.shape[0]):
            nodo = restricciones[i,0]
            gdl = restricciones[i,1]
            val = restricciones_val[i]

            self.agregar_restriccion(nodo, gdl, val)

        for i in range(cargas.shape[0]):
            nodo = cargas[i,0]
            gdl = cargas[i,1]
            val = cargas_val[i]

            self.agregar_fuerza(nodo, gdl, val)

