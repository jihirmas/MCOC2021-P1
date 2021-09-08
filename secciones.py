from numpy import pi, sqrt
from constantes import g_, ρ_acero
 
class Circular(object):
    """define una seccion Circular"""

    def __init__(self, D, Dint):
        super(Circular, self).__init__()
        """Implementar"""	

    def area(self):
        A = (((self.D)**2)*pi/4) - (((self.Dint)**2)*pi/4)
            
        
        return A

    def peso(self):

        
        """Implementar"""	
        
        return 0

    def inercia_xx(self):

        
        """Implementar"""	
        
        return 0

    def inercia_yy(self):

        
        """Implementar"""	
        
        return 0


