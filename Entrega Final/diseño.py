# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 20:05:44 2021

@author: jihir
"""
import matplotlib.pyplot as plt
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

# plt.hlines(y=y1,xmin=x1,xmax=x2,linewidth=2.5,zorder=1)


nodos = []
nodos.append([l1[7][0],l1[7][1]])
for i in range(19):
    nodos.append([l1[7][0]+6*(i+1),l1[7][1]])
nodos.append([l1[28][0],l1[28][1]])
ypuntas = l1[0][1]-(3*3**0.5)
for i in range(19):
    nodos.append([l1[7][0]+6*(i+1)-3,ypuntas])
nodos.append([nodos[19][0]+nodos[20][0]/2-nodos[19][0]/2,ypuntas])




barras = []
for i in range(20):
    barras.append([nodos[i],nodos[i+1]])
for i in range(21,40):
    barras.append([nodos[i],nodos[i+1]])
for i in range(20):
    barras.append([nodos[i],nodos[i+20+1]])
for i in range(20):
    barras.append([nodos[i],nodos[i+19+1]])

for i in nodos:
    plt.scatter(i[0],i[1],marker="o",color="black",linewidths=0.001)
plt.scatter(0, 0, )
for i in barras:
    x = [i[0][0],i[1][0]]
    y = [i[0][1],i[1][1]]
    plt.plot(x,y,linewidth=3,color="red")
plt.show()

print(nodos[40][0]-nodos[39][0])