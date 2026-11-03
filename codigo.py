import math
import numpy as np
import matplotlib.pyplot as plt

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

#Euler explícito:
# yₙ₊₁ = yₙ + h f(tₙ, yₙ)
#En codigo:

def euler(h):
    # h vendria a ser el paso fijo
    # y pasos_segun_h son la cant. de pasos a iterar segun el paso fijo (osea h)

    pasos_segun_h = int((t60 - t0) / h)

    t = np.zeros(pasos_segun_h+1)
    T = np.zeros(pasos_segun_h+1)
    H = np.zeros(pasos_segun_h+1)
    P = np.zeros(pasos_segun_h+1)

    t[0] = t0
    T[0] = T0
    H[0] = H0
    P[0] = P0

    for n in range(pasos_segun_h):
        deltaT, deltaH, deltaP = ecuaciones_diferenciales(t[n], T[n], H[n], P[n])

        T[n +1] = T[n] + h *deltaT
        H[n +1] = H[n] + h *deltaH
        P[n +1] = P[n] + h *deltaP

        t[n+1] = t[n] + h

    return t,T,H,P


#Punto A
#referencia usada para los graficos https://matplotlib.org/stable/tutorials/pyplot.html

h_ref = 0.001

t_ref, T_ref, H_ref, P_ref = euler(h_ref)

print(f"(A) Simulación de referencia completada con {len(t_ref)} puntos.") 
print(f"(A) Valores finales a los 60 meses: T={T_ref[-1]:.3f} °C," f" H={H_ref[-1]:.3f}, P={P_ref[-1]:.3f}")

#grafico:

plt.figure(figsize=(10, 6))
plt.plot(t_ref, T_ref, label='Temperatura T(t) [°C]', color='tab:red')
plt.plot(t_ref, H_ref, label='Humedad H(t) [u.h.]', color='tab:blue')
plt.plot(t_ref, P_ref, label='Nubosidad P(t) [u.p.]', color='tab:green')

plt.title('Punto A: (h_ref = 0.001 meses)') 
plt.xlabel('Tiempo t [meses]') 
plt.ylabel('Nivel') 
plt.grid(True, linestyle='--', alpha=0.7) 
plt.legend() 
plt.tight_layout() 
plt.show()




#Punto B

h_inicial = 0.005
cant_pasos = 5

pasos_h = [h_inicial * (2**i) for i in range (cant_pasos)]

error_absoluto = []

print("\n Punto B")

for h in pasos_h:
    t_h, T_h, H_h, P_h = euler(h)

    T_ref_interpolado = np.interp(t_h, t_ref, T_ref) #

    error_max = np.max(np.abs(T_ref_interpolado - T_h))
    error_absoluto.append(error_max)
    
    print(f"h = {h:.4f} mes | Pasos: {len(t_h)-1:5d} | Error max T: {error_max:.6f}")

#grafico:

plt.figure(figsize=(10, 6)) 
plt.plot( pasos_h, error_absoluto, 'o-', color='tab:red', linewidth=2, markersize=6, label='Err(h)', ) 
plt.xscale('log')
plt.yscale('log') 
plt.title('Punto B: Error max Absoluto en T(t) vs Paso Temporal h') 
plt.xlabel('Paso temporal h [meses]') 
plt.ylabel('Error max Absoluto Err(h) [°C]') 
plt.grid(True, which='both', linestyle='--', alpha=0.7) 
plt.legend() 
plt.tight_layout() 
plt.show()