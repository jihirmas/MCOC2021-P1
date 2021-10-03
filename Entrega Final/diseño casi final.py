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

seccc = ['[]400×200×45.6', '[]400×200×36.7', '[]400×200×27.7', '[]400×200×18.6', '[]400×150×41.7', '[]400×150×33.6', '[]400×150×25.4', '[]400×150×17.0', '[]400×100×37.8', '[]400×100×30.5', '[]400×100×23.0', '[]400×100×15.5', '[]350×200×41.7', '[]350×200×33.6', '[]350×200×25.4', '[]350×200×17.0', '[]350×150×37.8', '[]350×150×30.5', '[]350×150×23.0', '[]350×150×15.5', '[]350×100×33.9', '[]350×100×27.3', '[]350×100×20.7', '[]350×100×13.9', '[]300×200×37.8', '[]300×200×30.5', '[]300×200×23.0', '[]300×200×15.5', '[]300×150×33.9', '[]300×150×27.3', '[]300×150×20.7', '[]300×150×13.9', '[]300×100×29.9', '[]300×100×24.2', '[]300×100×18.3', '[]300×100×12.3', '[]300×75×28.0', '[]300×75×22.6', '[]300×75×17.1', '[]300×75×11.5', '[]300×50×26.0', '[]300×50×21.0', '[]300×50×16.0', '[]300×50×10.8', '[]250×200×33.9', '[]250×200×27.3', '[]250×200×20.7', '[]250×200×13.9', '[]250×150×29.9', '[]250×150×24.2', '[]250×150×18.3', '[]250×150×12.3', '[]250×100×26.0', '[]250×100×21.0', '[]250×100×16.0', '[]250×100×10.8', '[]250×75×24.1', '[]250×75×19.5', '[]250×75×14.8', '[]250×75×10.0', '[]250×50×22.1', '[]250×50×17.9', '[]250×50×13.6', '[]250×50×9.2', '[]200×200×29.9', '[]200×200×24.2', '[]200×200×18.3', '[]200×200×12.3', '[]200×150×26.0', '[]200×150×21.0', '[]200×150×16.0', '[]200×150×10.8', '[]200×100×22.1', '[]200×100×17.9', '[]200×100×13.6', '[]200×100×9.2', '[]200×75×20.1', '[]200×75×16.3', '[]200×75×12.4', '[]200×75×8.4', '[]200×70×23.3', '[]200×70×19.7', '[]200×70×16.0', '[]200×50×18.2', '[]200×50×14.8', '[]200×50×11.2', '[]200×50×7.6', '[]150×150×22.1', '[]150×150×17.9', '[]150×150×13.6', '[]150×150×9.2', '[]150×100×18.2', '[]150×100×14.8', '[]150×100×11.2', '[]150×100×7.6', '[]150×75×16.2', '[]150×75×13.2', '[]150×75×10.1', '[]150×75×6.8', '[]150×50×16.7', '[]150×50×14.2', '[]150×50×11.6', '[]150×50×8.9', '[]150×50×6.0', '[]135×135×23.3', '[]135×135×19.7', '[]135×135×16.0', '[]120×60×14.9', '[]120×60×12.7', '[]120×60×10.4', '[]120×60×8.0', '[]100×100×16.7', '[]100×100×14.2', '[]100×100×11.6', '[]100×100×8.9', '[]100×100×6.0', '[]100×75×12.3', '[]100×75×10.1', '[]100×75×7.7', '[]100×75×5.3', '[]100×50×12.0', '[]100×50×10.3', '[]100×50×8.5', '[]100×50×6.5', '[]100×50×4.5', '[]80×40×8.0', '[]80×40×6.6', '[]80×40×5.1', '[]80×40×3.5', '[]75×75×12.0', '[]75×75×10.3', '[]75×75×8.5', '[]75×75×6.5', '[]75×75×4.5', '[]70×30×5.3', '[]70×30×4.2', '[]70×30×2.9', '[]60×40×6.4', '[]60×40×5.3', '[]60×40×4.2', '[]60×40×2.9', '[]60×40×2.2', '[]50×50×7.3', '[]50×50×6.4', '[]50×50×5.3', '[]50×50×4.2', '[]50×50×2.9', '[]50×50×2.2', '[]50×30×3.2', '[]50×30×2.3', '[]50×30×1.8', '[]50×30×1.2', '[]50×20×2.0', '[]50×20×1.5', '[]50×20×1.0', '[]40×40×4.8', '[]40×40×4.1', '[]40×40×3.2', '[]40×40×2.3', '[]40×40×1.8', '[]40×40×1.2', '[]40×30×2.0', '[]40×30×1.5', '[]40×30×1.0', '[]40×20×1.7', '[]40×20×1.3', '[]40×20×0.9', '[]30×30×1.7', '[]30×30×1.3', '[]30×30×0.9', '[]30×20×1.3', '[]30×20×1.0', '[]30×20×0.7', '[]25×25×1.3', '[]25×25×1.0', '[]25×25×0.7', '[]25×15×1.0', '[]25×15×0.8', '[]25×15×0.6', '[]20×20×1.0', '[]20×20×0.8', '[]20×20×0.6', '[]20×10×0.6', '[]20×10×0.4', '[]15×15×0.6', '[]15×15×0.4', '[]12×12×0.3']
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

ret.agregar_nodo(l1[17][0],0,l1[17][1])
ret.agregar_nodo(l1[17][0],4,l1[17][1])
ret.agregar_nodo(l1[18][0],0,l1[18][1])
ret.agregar_nodo(l1[18][0],4,l1[18][1])
ret.agregar_nodo(l1[17][0],0,l1[17][1]+6)
ret.agregar_nodo(l1[17][0],4,l1[17][1]+6)
ret.agregar_nodo(l1[18][0],0,l1[18][1]+6-(l1[18][1]-l1[17][1]))
ret.agregar_nodo(l1[18][0],4,l1[18][1]+6-(l1[18][1]-l1[17][1]))
ret.agregar_nodo(l1[17][0],0,l1[17][1]+6+6)
ret.agregar_nodo(l1[17][0],4,l1[17][1]+6+6)
ret.agregar_nodo(l1[18][0],0,l1[18][1]+12-(l1[18][1]-l1[17][1]))
ret.agregar_nodo(l1[18][0],4,l1[18][1]+12-(l1[18][1]-l1[17][1]))
#Secciones de las barras
nodostodos = ret.obtener_nodos()
seccion_grande = SeccionICHA("[]300×150×33.9", color="#3A8431")#, debug=True)
seccion_chica = SeccionICHA("[]80×40×8.0", color="#A3500B")
# seccion_grande = SeccionICHA("[]300x150x33.9", color="#3A8431")#, debug=True)
# seccion_chica = SeccionICHA("[]80x40x8.0", color="#A3500B")
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

# seccion_grande = SeccionICHA("[]100x100x16.7", color="#3A8431")#, debug=True)
seccion_grande = SeccionICHA("[]100×100×16.7", color="#3A8431")#, debug=True)
ret.agregar_barra(Barra(67,69, seccion_grande))
ret.agregar_barra(Barra(69,68, seccion_grande))
ret.agregar_barra(Barra(68,66, seccion_grande))
ret.agregar_barra(Barra(66,67, seccion_grande))
ret.agregar_barra(Barra(66,63, seccion_grande))
ret.agregar_barra(Barra(67,62, seccion_grande))
ret.agregar_barra(Barra(66,64, seccion_grande))
ret.agregar_barra(Barra(68,62, seccion_grande))
ret.agregar_barra(Barra(69,64, seccion_grande))
ret.agregar_barra(Barra(68,65, seccion_grande))
ret.agregar_barra(Barra(69,63, seccion_grande))
ret.agregar_barra(Barra(67,65, seccion_grande))
ret.agregar_barra(Barra(68,64, seccion_grande))
ret.agregar_barra(Barra(69,65, seccion_grande))
ret.agregar_barra(Barra(67,63, seccion_grande))
ret.agregar_barra(Barra(66,62, seccion_grande))

ret.agregar_barra(Barra(70,67, seccion_grande))
ret.agregar_barra(Barra(71,66, seccion_grande))
ret.agregar_barra(Barra(70,68, seccion_grande))
ret.agregar_barra(Barra(72,66, seccion_grande))
ret.agregar_barra(Barra(72,69, seccion_grande))
ret.agregar_barra(Barra(73,68, seccion_grande))
ret.agregar_barra(Barra(73,67, seccion_grande))
ret.agregar_barra(Barra(71,69, seccion_grande))
ret.agregar_barra(Barra(70,71, seccion_grande))
ret.agregar_barra(Barra(71,73, seccion_grande))
ret.agregar_barra(Barra(73,72, seccion_grande))
ret.agregar_barra(Barra(72,70, seccion_grande))
ret.agregar_barra(Barra(70,66, seccion_grande))
ret.agregar_barra(Barra(72,68, seccion_grande))
ret.agregar_barra(Barra(73,69, seccion_grande))
ret.agregar_barra(Barra(71,67, seccion_grande))

ret.agregar_barra(Barra(8,70, seccion_grande))
ret.agregar_barra(Barra(8,71, seccion_grande))
ret.agregar_barra(Barra(70,49, seccion_grande))
ret.agregar_barra(Barra(49,71, seccion_grande))
ret.agregar_barra(Barra(9,70, seccion_grande))
ret.agregar_barra(Barra(9,71, seccion_grande))
ret.agregar_barra(Barra(50,71, seccion_grande))
ret.agregar_barra(Barra(50,70, seccion_grande))
ret.agregar_barra(Barra(9,72, seccion_grande))
ret.agregar_barra(Barra(9,73, seccion_grande))
ret.agregar_barra(Barra(50,72, seccion_grande))
ret.agregar_barra(Barra(50,73, seccion_grande))
ret.agregar_barra(Barra(10,72, seccion_grande))
ret.agregar_barra(Barra(10,73, seccion_grande))
ret.agregar_barra(Barra(51,72, seccion_grande))
ret.agregar_barra(Barra(51,73, seccion_grande))
ll1 = ret.obtener_barras()
# Crear restricciones
for nodo in [0,41]:
 	ret.agregar_restriccion(nodo, 0, 0)
 	ret.agregar_restriccion(nodo, 1, 0)
 	ret.agregar_restriccion(nodo, 2, 0)

for nodo in [20,61,62,63,64,65]:
    ret.agregar_restriccion(nodo, 0, 0)
    ret.agregar_restriccion(nodo, 1, 0)
    ret.agregar_restriccion(nodo, 2, 0)



#Visualizar y comprobar las secciones
opciones_barras = {
	# "ver_secciones_en_barras": True,
	"color_barras_por_seccion": True,
}
ver_reticulado_3d(ret,opciones_barras=opciones_barras)
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

factores_de_utilizacion = ret.obtener_factores_de_utilizacion(fu, ϕ=0.9)
barras_a_cambiar = ret.obtener_barras()
cont = 0
for i in range(0,len(factores_de_utilizacion)):
    if i < 175:
        k = seccc.index("[]300×150×33.9")
    else: 
        seccion_grande = SeccionICHA("[]100×100×16.7", color="#3A8431")#, debug=True)
    ret.resolver_sistema()
    factores_de_utilizacion = ret.obtener_factores_de_utilizacion(fu, ϕ=0.9)
    for j in range(k,k+1):#len(seccc)):
        # cont+=1
        # print("HHH    "+str(i)+"    "+str(j))
        if cont > 50:
            break
        if factores_de_utilizacion[i]<=0.01:
            # print("entre")
            # print(factores_de_utilizacion[i])
            barras_a_cambiar[i].seccion = SeccionICHA(seccc[j], color="#3A8431")#, debug=True)
        else:
            barras_a_cambiar[i].seccion = SeccionICHA(seccc[j-1], color="#3A8431")#, debug=True)
            break
    if cont > 50:
            break
        
barras_a_cambiar[8].seccion = SeccionICHA("[]300×150×33.9", color="#3A8431")
barras_a_cambiar[9].seccion = SeccionICHA("[]300×150×33.9", color="#3A8431")
for i in range(21,38):
    barras_a_cambiar[i].seccion = SeccionICHA("[]300×150×33.9", color="#3A8431")
barras_a_cambiar[47].seccion = SeccionICHA("[]300×150×33.9", color="#3A8431")
barras_a_cambiar[48].seccion = SeccionICHA("[]300×150×33.9", color="#3A8431")




ret.resolver_sistema()
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


ver_reticulado_3d(ret, 
 	opciones_nodos=opciones_nodos, 
 	opciones_barras=opciones_barras,
 	titulo="Factor Utilizacion")


ret.guardar("Puente Grupo 0 casi listo.h5")