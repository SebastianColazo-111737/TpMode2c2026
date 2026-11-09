import math

# Parametros nominales del modelo
TMAX = 4.0
ROCE = 0.30
ALFA = 0.05
BETA = 0.20
GAMMA = 0.10
DELTA = 0.40
SIGMA = 0.70
A = 0.45

PI = math.pi
OMEGA = (2.0 * PI) / 12.0

# Condiciones iniciales
T0 = 1.0
H0 = 0.0
P0 = 0.0

# Intervalo de integracion (0 <= t <= 60 meses)
T_INICIAL = 0.0
T_FINAL = 60.0
