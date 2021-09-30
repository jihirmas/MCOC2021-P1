from numpy import pi, sqrt, nan
from numpy.random import rand
from constantes import g_, ρ_acero, mm_
 
class Circular(object):
    """define una seccion Circular"""

    def __init__(self, D, Dint, color=rand(3)):
        super(Circular, self).__init__()
        self.D = D
        self.Dint = Dint
        self.color = color  #color para la seccion

    def area(self):
        return pi*(self.D**2 - self.Dint**2)/4

    def peso(self):
        return self.area()*ρ_acero*g_

    def inercia_xx(self):
        return pi*(self.D**4 - self.Dint**4)/4

    def inercia_yy(self):
        return self.inercia_xx()

    def nombre(self):
        return f"O{self.D*1e3:.0f}x{self.Dint*1e3:.0f}"

    def __str__(self):
        return f"Seccion Circular {self.nombre()}"


        
#Mas adelante, no es para P1E1

from pandas import read_excel

class SeccionICHA(object):
    """Lee la tabla ICHA y genera una seccion apropiada"""

    def __init__(self, denominacion, base_datos="Perfiles ICHA.xlsx", debug=False, color=rand(3)):
        super(SeccionICHA, self).__init__()
        self.denominacion = denominacion
        self.color = color  #color para la seccion

        if denominacion[0:2] == "HR" or denominacion[0] == "W":
            tab = "HR"
            tipo = "HR"
        elif denominacion[0] == "H":
            tab = "H"
            tipo = "H"
        elif denominacion[0:2] == "[]":
            tab = "Cajon"
            tipo = "[]"
        elif denominacion[0] == "o":
            tab = "Circulares Menores"
            tipo = "o"
        elif denominacion[0] == "O":
            tab = "Circulares Mayores"
            tipo = "O"
        else:
            print(f"Tipo de seccion {denominacion} no soportada. Intentar H, HR, [], o u O")
            self.invalid_section()

        found = False

        xls = read_excel(base_datos,
        engine="openpyxl",
        sheet_name=tab,
        header=11)

        if debug:
            print("======xls=======")
            print(xls)
            print("======xls=======")


        if tipo == "H" or tipo == "HR":
            Nregistros = len(xls["A"])-2
            for i_fila in range(Nregistros):
                
                df = xls.loc[i_fila+2,["d","bf","peso","A","Ix/10⁶","Iy/10⁶",]]
                if debug:
                    print("======df=======")
                    print(df)
                    print("======df=======")

                if df.isnull().values.any():
                    #Saltarse valores inexistentes
                    continue

                d = df["d"]
                bf = df["bf"]
                w = df["peso"]
                den = f'{tipo}{d}x{bf}x{w}'

                if den == self.denominacion:
                    found = True
                    self.d = df["d"]
                    self.bf = df["bf"]
                    self.w = df["peso"]
                    self.A = df["A"]*mm_**2
                    self.Ixx = df["Ix/10⁶"]*1e6**mm_**4
                    self.Iyy = df["Iy/10⁶"]*1e6**mm_**4
                    # self.denominacion = denominacion
                    print(f"{den} encontrada. A={self.A} Ix={self.Ixx} Iy={self.Iyy} ")

        if tipo == "[]":
            Nregistros = len(xls["A"])-2
            for i_fila in range(Nregistros):
                
                df = xls.loc[i_fila+2,["D","B","peso","A","Ix/10⁶","Iy/10⁶",]]
                if debug:
                    print("======df=======")
                    print(df)
                    print("======df=======")

                if df.isnull().values.any():
                    #Saltarse valores inexistentes
                    continue

                D = df["D"]
                B = df["B"]
                W = df["peso"]
                den = f'{tipo}{D}x{B}x{W}'

                if den == self.denominacion:
                    found = True
                    self.D = df["D"]
                    self.B = df["B"]
                    self.w = df["peso"]
                    self.A = df["A"]*mm_**2
                    self.Ixx = df["Ix/10⁶"]*1e6**mm_**4
                    self.Iyy = df["Iy/10⁶"]*1e6**mm_**4
                    # self.denominacion = denominacion
                    print(f"{den} encontrada. A={self.A} Ix={self.Ixx} Iy={self.Iyy} ")

        if not found:
            print(f"Tipo de seccion {denominacion} no encontrada en base de datos")
            self.invalid_section()
        
    def area(self):
        return self.A

    def peso(self):
        return self.w

    def inercia_xx(self):
        return self.Ixx

    def inercia_yy(self):
        return self.Iyy

    def invalid_section(self):
        self.A = nan
        self.peso = nan
        self.Ixx = nan
        self.Iyy = nan

    def nombre(self):
        return self.denominacion

    def __str__(self):
        s = f"Seccion ICHA {self.denominacion}\n"
        s += f"  Area : {self.A}\n"
        s += f"  peso : {self.peso}\n"
        s += f"  Ixx  : {self.Ixx}\n"
        s += f"  Iyy  : {self.Iyy}\n"
        return s
