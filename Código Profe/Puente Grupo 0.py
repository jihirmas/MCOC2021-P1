# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 19:03:14 2021

@author: jihir
"""

from reticulado import Reticulado
from barra import Barra
from graficar3d import ver_reticulado_3d
from constantes import *
from math import sqrt
from secciones1 import SeccionICHA


#Inicializar modelo
ret = Reticulado()
nodos = []
archivo = open("posibles-apoyos-2021.txt")
c = 0
l1 = []
for i in archivo:
    l = (i.split(" "))
    l1.append([float(l[0]),float(l[1])])
    # print(c,'{0:.10f}'.format(l[0]),'{0:.10f}'.format(l[1]))
    # print(c,float(l[0]),float(l[1]))
    c+=1
archivo.close()
nodos.append([l1[7][0],l1[7][1]])
for i in range(19):
    nodos.append([l1[7][0]+6*(i+1),l1[7][1]])
nodos.append([l1[28][0],l1[28][1]])
ypuntas = l1[0][1]-(5)
for i in range(19):
    nodos.append([l1[7][0]+6*(i+1)-3,ypuntas])
nodos.append([nodos[19][0]+nodos[20][0]/2-nodos[19][0]/2,ypuntas])
lista_nodos = nodos
cont = 0
for x in lista_nodos:
    if cont<21:
        ret.agregar_nodo(x[0],0,x[1])
    else:
        ret.agregar_nodo(x[0],2,x[1])
    cont +=1
cont = 0
for x in lista_nodos:
    if cont<21:
        ret.agregar_nodo(x[0],4,x[1])
    else:
        pass
    cont += 1
#Secciones de las barras

seccion_grande = SeccionICHA("[]350x150x37.8", color="#3A8431")#, debug=True)
seccion_chica = SeccionICHA("[]80x40x8.0", color="#A3500B")


#Crear y agregar las barras
h=0
for x in range(20):
  ret.agregar_barra(Barra(h,h+1, seccion_grande)) #0
  h+=1
hh=21
for x in range(19):
   ret.agregar_barra(Barra(hh,hh+1, seccion_grande)) #0
   hh+=1
hh=41
for x in range(20):
   ret.agregar_barra(Barra(hh,hh+1, seccion_grande)) #0
   hh+=1
for i in range(20):
    ret.agregar_barra(Barra(0+i, 21+i, seccion_grande)) #0
    ret.agregar_barra(Barra(21+i,1+i, seccion_grande)) #0
for i in range(20):
    ret.agregar_barra(Barra(21+i, 41+i, seccion_grande)) #0
    ret.agregar_barra(Barra(21+i,42+i, seccion_grande)) #0
for i in range(20):
    ret.agregar_barra(Barra(0+i, 42+i, seccion_grande)) #0
    ret.agregar_barra(Barra(41+i,1+i, seccion_grande)) #0

# Crear restricciones
for nodo in [0,41]:
 	ret.agregar_restriccion(nodo, 0, 0)
 	ret.agregar_restriccion(nodo, 1, 0)
 	ret.agregar_restriccion(nodo, 2, 0)

for nodo in [20,61]:
    ret.agregar_restriccion(nodo, 0, 0)
    ret.agregar_restriccion(nodo, 1, 0)
    ret.agregar_restriccion(nodo, 2, 0)
    
ret.agregar_restriccion(31, 2, 0)
ret.agregar_restriccion(31, 1, 0)
ret.agregar_restriccion(32, 2, 0)
ret.agregar_restriccion(32, 1, 0)


#Visualizar y comprobar las secciones
opciones_barras = {
	# "ver_secciones_en_barras": True,
	"color_barras_por_seccion": True,
}
ver_reticulado_3d(ret,opciones_barras=opciones_barras)

# exit(0)



#Resolver el problema peso_propio
ret.ensamblar_sistema(factor_peso_propio=[0.,0.,-1.], factor_cargas=0.0)
ret.resolver_sistema()
f_D = ret.obtener_fuerzas()

L = 6.*m_
# H = 6.*m_
B = 4.*m_

q = 400*kgf_/m_**2

F = B*L*q
L1 = 3.48
F1 = B*L1*q
#Agregar fuerzas tablero
ret.agregar_fuerza(0, 2, -F/4)
# print(f"{0}: {-F/4} {ret.obtener_coordenada_nodal(0)}")
for i in range(1,19):
    ret.agregar_fuerza(i, 2, -F/2)
    # print(f"{i}: {-F/2} {ret.obtener_coordenada_nodal(i)}")
ret.agregar_fuerza(19, 2, -F/4+-F1/4) 
# print(f"{19}: {-F/4+-F1/4} {ret.obtener_coordenada_nodal(19)}")  
ret.agregar_fuerza(20, 2, -F1/4)
# print(f"{20}: {-F1/4} {ret.obtener_coordenada_nodal(20)}")

ret.agregar_fuerza(41, 2, -F/4)
# print(f"{41}: {-F/4} {ret.obtener_coordenada_nodal(41)}")
for i in range(42,60):
    # print(f"{i}: {-F/2} {ret.obtener_coordenada_nodal(i)}")
    ret.agregar_fuerza(i, 2, -F/2)
    
ret.agregar_fuerza(60, 2, -F/4+-F1/4)  
# print(f"{60}: {-F/4+-F1/4} {ret.obtener_coordenada_nodal(60)}")
ret.agregar_fuerza(61, 2, -F1/4)
# print(f"{61}: {-F1/4}, {ret.obtener_coordenada_nodal(61)}")

# print(ret.obtener_nodos())

#Resolver el problema peso_propio
ret.ensamblar_sistema(factor_peso_propio=[0.,0.,0], factor_cargas=1.0)
ret.resolver_sistema()
f_L = ret.obtener_fuerzas()

#Visualizar f_L en el reticulado
opciones_nodos = {
	"usar_posicion_deformada": False,
}

opciones_barras = {
	"color_barras_por_dato": True,
	"ver_dato_en_barras" : True,
	"dato":f_L
}

# ver_reticulado_3d(ret, 
# 	opciones_nodos=opciones_nodos, 
# 	opciones_barras=opciones_barras,
# 	titulo="Carga Viva")


#Visualizar f_L en el reticulado
opciones_nodos = {
	"usar_posicion_deformada": False,
}

opciones_barras = {
	"color_barras_por_dato": True,
	"ver_dato_en_barras" : True,
	"dato":f_D
}

# ver_reticulado_3d(ret, 
# 	opciones_nodos=opciones_nodos, 
# 	opciones_barras=opciones_barras,
# 	titulo="Carga Muerta")


#Calcular carga ultima (con factores de mayoracion)
fu = 1.2*f_D + 1.6*f_L



#Visualizar combinacion en el reticulado
opciones_nodos = {
	"usar_posicion_deformada": False,
}

opciones_barras = {
	"color_barras_por_dato": True,
	"ver_dato_en_barras" : True,
	"dato":fu
}

# ver_reticulado_3d(ret, 
# 	opciones_nodos=opciones_nodos, 
# 	opciones_barras=opciones_barras,
# 	titulo="1.2D + 1.6L")





cumple = ret.chequear_diseño(fu, ϕ=0.9)

if cumple:
	print(":)  El reticulado cumple todos los requisitos")
else:
	print(":(  El reticulado NO cumple todos los requisitos")

#Calcular factor de utilizacion para las barras
factores_de_utilizacion = ret.obtener_factores_de_utilizacion(fu, ϕ=0.9)


#Visualizar FU en el reticulado
opciones_nodos = {
	"usar_posicion_deformada": False,
	# "factor_amplificacion_deformada": 1.,
}

opciones_barras = {
	"color_barras_por_dato": True,
	"ver_dato_en_barras" : True,
	"dato":factores_de_utilizacion
}


# ver_reticulado_3d(ret, 
# 	opciones_nodos=opciones_nodos, 
# 	opciones_barras=opciones_barras,
# 	titulo="Factor Utilizacion")


ret.guardar("Puente Grupo 0.h5")