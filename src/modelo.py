import numpy as np
from src.constantes import (
    TMAX, ROCE, ALFA, BETA, GAMMA, DELTA, SIGMA, A, PI, OMEGA,
    T0, H0, P0, T_INICIAL, T_FINAL
)


def R(t, A_val=A):
    return ROCE + A_val * np.cos(OMEGA * t - PI)


def ecuaciones_diferenciales(t, T, H, P, A_val=A, beta=BETA, gamma=GAMMA, sigma=SIGMA):
    deltaT = R(t, A_val) * T * (1.0 - T / TMAX) - ALFA * H
    deltaH = beta * (T ** 2) - gamma * H * P
    deltaP = DELTA * (H ** 2) - sigma * P
    return deltaT, deltaH, deltaP


def euler(h, A_val=A, beta=BETA, gamma=GAMMA, sigma=SIGMA):
    pasos_segun_h = int(round((T_FINAL - T_INICIAL) / h))

    t = np.linspace(T_INICIAL, pasos_segun_h * h, pasos_segun_h + 1)
    T = np.zeros(pasos_segun_h + 1)
    H = np.zeros(pasos_segun_h + 1)
    P = np.zeros(pasos_segun_h + 1)

    T[0] = T0
    H[0] = H0
    P[0] = P0

    R_vec = R(t, A_val)

    for n in range(pasos_segun_h):
        Tn = T[n]
        Hn = H[n]
        Pn = P[n]

        if abs(Tn) > 1e6 or abs(Hn) > 1e6 or abs(Pn) > 1e6:
            T[n + 1:] = np.nan
            H[n + 1:] = np.nan
            P[n + 1:] = np.nan
            break

        deltaT = R_vec[n] * Tn * (1.0 - Tn / TMAX) - ALFA * Hn
        deltaH = beta * (Tn ** 2) - gamma * Hn * Pn
        deltaP = DELTA * (Hn ** 2) - sigma * Pn

        T[n + 1] = Tn + h * deltaT
        H[n + 1] = Hn + h * deltaH
        P[n + 1] = Pn + h * deltaP

    return t, T, H, P


def calcular_indicadores_ultimo_ciclo(t, T, H, P):
    if np.isnan(T).any() or np.isnan(H).any() or np.isnan(P).any():
        return None
    if np.max(np.abs(T)) > 100.0 or np.max(np.abs(H)) > 100.0 or np.max(np.abs(P)) > 100.0:
        return None
    if np.min(T) < -0.5:
        return None

    mask_ultimo = (t >= 48.0 - 1e-9) & (t <= 60.0 + 1e-9)
    mask_previo = (t >= 36.0 - 1e-9) & (t <= 48.0 + 1e-9)

    t_ult = t[mask_ultimo]
    T_ult = T[mask_ultimo]
    P_ult = P[mask_ultimo]

    T_prev = T[mask_previo]
    P_prev = P[mask_previo]

    if len(P_ult) == len(P_prev):
        diff_rel_P = np.max(np.abs(P_ult - P_prev)) / (np.max(P_ult) + 1e-9)
        diff_rel_T = np.max(np.abs(T_ult - T_prev)) / (np.max(T_ult) + 1e-9)
        es_repetitivo = (diff_rel_P < 0.05) and (diff_rel_T < 0.05)
    else:
        es_repetitivo = False

    P_max = float(np.max(P_ult))
    P_min = float(np.min(P_ult))
    P_med = float(np.mean(P_ult))

    if P_med <= 1e-9:
        return None

    SP = (P_max - P_min) / P_med

    idx_T_max = int(np.argmax(T_ult))
    idx_P_max = int(np.argmax(P_ult))

    t_T_max = float(t_ult[idx_T_max])
    t_P_max = float(t_ult[idx_P_max])

    delta_t_TP = t_P_max - t_T_max
    if delta_t_TP < 0.0:
        delta_t_TP += 12.0

    return {
        "SP": SP,
        "delta_t_TP": delta_t_TP,
        "P_max": P_max,
        "P_min": P_min,
        "P_med": P_med,
        "t_T_max": t_T_max,
        "t_P_max": t_P_max,
        "T_max": float(T_ult[idx_T_max]),
        "es_repetitivo": es_repetitivo,
    }
