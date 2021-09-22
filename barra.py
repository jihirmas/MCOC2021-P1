import numpy as np

from constantes import g_, ρ_acero, E_acero


class Barra(object):

    """Constructor para una barra"""
    def __init__(self, ni, nj, seccion, color=np.random.rand(3)):
        super(Barra, self).__init__()
        self.ni = ni
        self.nj = nj
        self.seccion = seccion
        self.color = color


    def obtener_conectividad(self):
        return [self.ni, self.nj]
    

    def calcular_largo(self, reticulado):
         """Devuelve el largo de la barra. 
         xi : Arreglo numpy de dimenson (3,) con coordenadas del nodo i
         xj : Arreglo numpy de dimenson (3,) con coordenadas del nodo j
         """
         ni=self.ni
         nj=self.nj
         
         ni=reticulado.xyz[ni,:]
         nj=reticulado.xyz[nj,:]    
         
         largo = abs(ni-nj)
         return np.sqrt(np.dot(largo,largo))
     
     
        
     
        

    def calcular_peso(self, reticulado):
       """Devuelve el largo de la barra. 
       xi : Arreglo numpy de dimenson (3,) con coordenadas del nodo i
       xj : Arreglo numpy de dimenson (3,) con coordenadas del nodo j
       """
       
       """Implementar"""    
       Area = self.seccion.area()
       largo = self.calcular_largo(reticulado)
       ro = ρ_acero
       return Area*largo*ro*g_
   




    def obtener_rigidez(self, ret):
        
        
        L=self.calcular_largo(ret)
        
        xi = ret.obtener_coordenada_nodal(self.ni)
        xj = ret.obtener_coordenada_nodal(self.nj) 
        
        Lx=abs((xi[0]-xj[0]))
        Ly=abs((xi[1]-xj[1]))
        Lz=abs((xi[2]-xj[2]))
        
        cosθx= Lx/L
        cosθy=Ly/L
        cosθz=Lz/L
        
        
        T = np.array([[-cosθx,-cosθy,-cosθz,cosθx,cosθy,cosθz]])
        
        
        ke=self.seccion.area()*E_acero/L*(T.T@T)
        
        return ke
    

    def obtener_vector_de_cargas(self, ret):
        
        
        W = self.calcular_peso(ret)

        return -W/2*np.array([0,1,0,0,1,0])
        
        

    def obtener_fuerza(self, ret):
        
        L=self.calcular_largo(ret)
        
        xi = ret.obtener_coordenada_nodal(self.ni)
        xj = ret.obtener_coordenada_nodal(self.nj) 
        
        Lx=abs((xi[0]-xj[0]))
        Ly=abs((xi[1]-xj[1]))
        Lz=abs((xi[2]-xj[2]))
        
        cosθx= Lx/L
        cosθy=Ly/L
        cosθz=Lz/L
        
        T = np.array([-cosθx,-cosθy,-cosθz,cosθx,cosθy,cosθz])
        A = self.seccion.area()
        u = ret.u
        ni=self.ni
        nj=self.nj
        u_e = np.array([u[3*ni],u[3*ni+1],u[3*ni+2],u[3*nj],u[3*nj+1],u[3*nj+2]])
        se= A*E_acero/L*T@u_e
        return se




    def chequear_diseño(self, Fu, ret, ϕ=0.9):
        
        """Implementar"""	
        
        return 0





    def obtener_factor_utilizacion(self, Fu, ϕ=0.9):
        
        """Implementar"""	
        
        return 0


    def rediseñar(self, Fu, ret, ϕ=0.9):
        
        """Implementar"""	
        
        return 0

