import matplotlib.pyplot as plt
import math
import portion as rango
import numpy as np

#Constantes:
Tmax = 4.0 
ROCE = 0.30
ALFA = 0.05 
BETA = 0.20
GAMMA = 0.10
DELTA = 0.40
SIGMA = 0.70
A = 0.45
PI = math.pi
OMEGA = (2*PI)/12

#Condiciones iniciales
T0 = 1.0
H0 = 0.0
P0 = 0.0

#para intervalo 0 ≤ t ≤ 60 meses
t0 = 0.0 #vendria a ser el mes cero 
t60 = 60.0

#Ecuaciones:

def R(t):
    return ROCE + A*math.cos(OMEGA*t-PI)

def ecuaciones_diferenciales(t,T, H, P):

    deltaT = R(t)*T*(1-T/Tmax) - ALFA * H

    deltaH = BETA*(T**2) - GAMMA*H*P

    deltaP = DELTA*(H**2) - SIGMA*P

    return deltaT,deltaH,deltaP




