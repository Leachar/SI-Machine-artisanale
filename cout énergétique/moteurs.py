# Programme pour l'énergie des moteurs :

import sympy as sp


L = []     #liste des longueurs des barres 
w = []      #liste des vitesses angulaires des barres 
m = 45      #masse d'un moteur (en grammes)

def equations_mouvement(L, w):
    t = sp.Symbol('t')
    x = 0
    y = 0
    
    for i in range(len(L)):
        x += L[i] * sp.cos(w[i] * t)
        y += L[i] * sp.sin(w[i] * t)
        
    return x, y

for i in range len(L) : 
    Ec = 1/2*m*


