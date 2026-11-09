import os
import math
import numpy as np
import matplotlib.pyplot as plt
from src.modelo import euler


def ejecutar_punto_a(guardar_graficos=True, carpeta_salida="graficos"):
    h_ref = 0.001
    t_ref, T_ref, H_ref, P_ref = euler(h_ref)

    print("\n--- PARTE 1 - Punto A ---")
    print(f"Simulacion de referencia completada con {len(t_ref)} puntos.")
    print(f"Valores finales a los 60 meses: T={T_ref[-1]:.4f} C, H={H_ref[-1]:.4f}, P={P_ref[-1]:.4f}")

    plt.figure(figsize=(10, 6))
    plt.plot(t_ref, T_ref, label="Temperatura T(t) [C]", color="tab:red")
    plt.plot(t_ref, H_ref, label="Humedad H(t) [u.h.]", color="tab:blue")
    plt.plot(t_ref, P_ref, label="Nubosidad/Precipitacion P(t) [u.p.]", color="tab:green")
    plt.title("Parte 1 - Punto A: Solucion de referencia (h_ref = 0.001 meses)")
    plt.xlabel("Tiempo t [meses]")
    plt.ylabel("Nivel")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()

    if guardar_graficos:
        os.makedirs(carpeta_salida, exist_ok=True)
        plt.savefig(os.path.join(carpeta_salida, "parte1_punto_a.png"), dpi=150)
    plt.show()

    return t_ref, T_ref, H_ref, P_ref


def ejecutar_punto_b(t_ref, T_ref, guardar_graficos=True, carpeta_salida="graficos"):
    h_inicial = 0.005
    cant_pasos = 5
    pasos_h = [h_inicial * (2 ** i) for i in range(cant_pasos)]
    error_absoluto = []

    print("\n--- PARTE 1 - Punto B ---")
    for h in pasos_h:
        t_h, T_h, _, _ = euler(h)
        T_ref_interpolado = np.interp(t_h, t_ref, T_ref)
        error_max = np.max(np.abs(T_ref_interpolado - T_h))
        error_absoluto.append(error_max)
        print(f"h = {h:.4f} mes | Pasos: {len(t_h) - 1:5d} | Error max T: {error_max:.6f} C")

    plt.figure(figsize=(10, 6))
    plt.plot(pasos_h, error_absoluto, "o-", color="tab:red", linewidth=2, markersize=6, label="Err(h)")
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Parte 1 - Punto B: Error maximo absoluto en T(t) vs Paso temporal h")
    plt.xlabel("Paso temporal h [meses]")
    plt.ylabel("Error maximo absoluto Err(h) [C]")
    plt.grid(True, which="both", linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()

    if guardar_graficos:
        os.makedirs(carpeta_salida, exist_ok=True)
        plt.savefig(os.path.join(carpeta_salida, "parte1_punto_b.png"), dpi=150)
    plt.show()

    return pasos_h, error_absoluto


def ejecutar_punto_c(pasos_h, error_absoluto):
    ordenes_p = []
    print("\n--- PARTE 1 - Punto C ---")
    for i in range(len(error_absoluto) - 1):
        err_h = error_absoluto[i]
        err_2h = error_absoluto[i + 1]
        p = math.log(err_2h / err_h) / math.log(2.0)
        ordenes_p.append(p)
        print(f"Entre h={pasos_h[i]:.4f} y 2h={pasos_h[i + 1]:.4f} -> Orden p: {p:.4f}")
    return ordenes_p


def ejecutar_punto_d(t_ref, T_ref, pasos_h, error_absoluto, guardar_graficos=True, carpeta_salida="graficos"):
    pasos_exploracion = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.00, 1.15, 1.20, 1.25, 1.30]
    h_estables = []
    err_estables = []

    print("\n--- PARTE 1 - Punto D ---")
    for h_prueba in pasos_exploracion:
        t_p, T_p, _, _ = euler(h_prueba)
        if np.isnan(T_p).any() or np.isinf(T_p).any() or np.max(np.abs(T_p)) > 100.0:
            print(f"h = {h_prueba:.4f} mes -> CONVERGENCIA FALLIDA (solucion inestable)")
        else:
            T_ref_interp = np.interp(t_p, t_ref, T_ref)
            err_max = np.max(np.abs(T_ref_interp - T_p))
            h_estables.append(h_prueba)
            err_estables.append(err_max)
            print(f"h = {h_prueba:.4f} mes -> Acotada | Error max T: {err_max:.6f} C")

    _, axes = plt.subplots(1, 2, figsize=(14, 5))

    recta_teorica = [error_absoluto[0] * (h / pasos_h[0]) for h in h_estables]
    axes[0].plot(h_estables, err_estables, "o-", color="tab:red", label="Err(h) real")
    axes[0].plot(h_estables, recta_teorica, "--", color="black", label="Tendencia lineal O(h)")
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_title("Punto D: Quiebre de proporcionalidad Err(h) vs h")
    axes[0].set_xlabel("Paso temporal h [meses]")
    axes[0].set_ylabel("Error max absoluto en T(t) [C]")
    axes[0].grid(True, which="both", linestyle="--", alpha=0.7)
    axes[0].legend()

    t_125, T_125, _, _ = euler(1.25)
    axes[1].plot(t_ref, T_ref, label="Referencia (h = 0.001)", color="black", linewidth=1.5)
    axes[1].plot(t_125, T_125, "o--", label="Paso limite (h = 1.25)", color="tab:orange", markersize=4)
    axes[1].set_title("Punto D: Degradacion al borde de inestabilidad")
    axes[1].set_xlabel("Tiempo t [meses]")
    axes[1].set_ylabel("Temperatura T(t) [C]")
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[1].legend()

    plt.tight_layout()
    if guardar_graficos:
        os.makedirs(carpeta_salida, exist_ok=True)
        plt.savefig(os.path.join(carpeta_salida, "parte1_punto_d.png"), dpi=150)
    plt.show()


def correr_parte1(guardar_graficos=True, carpeta_salida="graficos"):
    t_ref, T_ref, _, _ = ejecutar_punto_a(guardar_graficos, carpeta_salida)
    pasos_h, error_absoluto = ejecutar_punto_b(t_ref, T_ref, guardar_graficos, carpeta_salida)
    ejecutar_punto_c(pasos_h, error_absoluto)
    ejecutar_punto_d(t_ref, T_ref, pasos_h, error_absoluto, guardar_graficos, carpeta_salida)
