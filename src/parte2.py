import os
import numpy as np
import matplotlib.pyplot as plt
from src.constantes import A, BETA, GAMMA, SIGMA
from src.modelo import euler, calcular_indicadores_ultimo_ciclo


def ejecutar_punto_2a(h_p2=0.005, guardar_graficos=True, carpeta_salida="graficos"):
    t_nom, T_nom, H_nom, P_nom = euler(h_p2)
    ind_nom = calcular_indicadores_ultimo_ciclo(t_nom, T_nom, H_nom, P_nom)

    print("\n--- PARTE 2 - Punto A (Parametros Nominales) ---")
    print(f"Paso seleccionado: h = {h_p2} meses")
    print(f"P_max = {ind_nom['P_max']:.4f} u.p. (en t = {ind_nom['t_P_max']:.2f} meses)")
    print(f"P_min = {ind_nom['P_min']:.4f} u.p.")
    print(f"P_med = {ind_nom['P_med']:.4f} u.p.")
    print(f"t_T,max = {ind_nom['t_T_max']:.2f} meses (T_max = {ind_nom['T_max']:.4f} C)")
    print(f"Severidad estacional (SP) = {ind_nom['SP']:.4f}")
    print(f"Desfase temp-precipitacion (delta_t_TP) = {ind_nom['delta_t_TP']:.4f} meses")

    mask_48_60 = (t_nom >= 48.0 - 1e-9) & (t_nom <= 60.0 + 1e-9)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].plot(t_nom, T_nom, label="T(t) [C]", color="tab:red")
    axes[0].plot(t_nom, H_nom, label="H(t) [u.h.]", color="tab:blue")
    axes[0].plot(t_nom, P_nom, label="P(t) [u.p.]", color="tab:green")
    axes[0].axvspan(48, 60, color="gray", alpha=0.15, label="Ultimo ciclo (48-60 m)")
    axes[0].set_title("Parte 2 - Punto A: Evolucion completa (0 a 60 meses)")
    axes[0].set_xlabel("Tiempo t [meses]")
    axes[0].set_ylabel("Nivel")
    axes[0].grid(True, linestyle="--", alpha=0.7)
    axes[0].legend()

    axes[1].plot(t_nom[mask_48_60], T_nom[mask_48_60], label="T(t) [C]", color="tab:red")
    axes[1].plot(t_nom[mask_48_60], H_nom[mask_48_60], label="H(t) [u.h.]", color="tab:blue")
    axes[1].plot(t_nom[mask_48_60], P_nom[mask_48_60], label="P(t) [u.p.]", color="tab:green")
    axes[1].axvline(ind_nom["t_T_max"], color="tab:red", linestyle=":", label=f"t_T,max = {ind_nom['t_T_max']:.2f} m")
    axes[1].axvline(ind_nom["t_P_max"], color="tab:green", linestyle=":", label=f"t_P,max = {ind_nom['t_P_max']:.2f} m")
    axes[1].set_title("Parte 2 - Punto A: Ultimo ciclo anual (48 <= t <= 60 meses)")
    axes[1].set_xlabel("Tiempo t [meses]")
    axes[1].set_ylabel("Nivel")
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[1].legend()

    plt.tight_layout()
    if guardar_graficos:
        os.makedirs(carpeta_salida, exist_ok=True)
        plt.savefig(os.path.join(carpeta_salida, "parte2_punto_a.png"), dpi=150)
    plt.show()

    return (t_nom, T_nom, H_nom, P_nom), ind_nom


def ejecutar_punto_2b(h_p2=0.005, guardar_graficos=True, carpeta_salida="graficos"):
    n_puntos = 25
    rangos_parametros = {
        "A": np.linspace(0.25, 0.60, n_puntos),
        "beta": np.linspace(0.10, 0.30, n_puntos),
        "gamma": np.linspace(0.05, 0.20, n_puntos),
        "sigma": np.linspace(0.40, 1.00, n_puntos),
    }

    etiquetas = {
        "A": "Amplitud estacional A [1/mes]",
        "beta": "Eficiencia de evaporacion beta [u.h./(mes C^2)]",
        "gamma": "Consumo de humedad gamma [1/(mes u.p.)]",
        "sigma": "Tasa de disipacion sigma [1/mes]",
    }

    resultados = {}
    print("\n--- PARTE 2 - Punto B (Sensibilidad Individual) ---")

    for nombre_param, valores_q in rangos_parametros.items():
        lista_sp = []
        lista_dt = []

        for q in valores_q:
            kwargs = {"A_val": A, "beta": BETA, "gamma": GAMMA, "sigma": SIGMA}
            if nombre_param == "A":
                kwargs["A_val"] = q
            else:
                kwargs[nombre_param] = q

            t_sim, T_sim, H_sim, P_sim = euler(h_p2, **kwargs)
            ind = calcular_indicadores_ultimo_ciclo(t_sim, T_sim, H_sim, P_sim)

            if ind is not None:
                lista_sp.append(ind["SP"])
                lista_dt.append(ind["delta_t_TP"])
            else:
                lista_sp.append(np.nan)
                lista_dt.append(np.nan)

        resultados[nombre_param] = (valores_q, np.array(lista_sp), np.array(lista_dt))
        print(
            f"Parametro {nombre_param:5s}: "
            f"SP va de {lista_sp[0]:.4f} a {lista_sp[-1]:.4f} | "
            f"delta_t_TP va de {lista_dt[0]:.4f} a {lista_dt[-1]:.4f} meses"
        )

    fig, axes = plt.subplots(2, 4, figsize=(18, 8))
    for col, nombre_param in enumerate(["A", "beta", "gamma", "sigma"]):
        valores_q, arr_sp, arr_dt = resultados[nombre_param]

        axes[0, col].plot(valores_q, arr_sp, "o-", color="tab:blue", markersize=4)
        axes[0, col].set_title(f"SP vs {nombre_param}")
        axes[0, col].set_xlabel(etiquetas[nombre_param])
        axes[0, col].set_ylabel("Severidad Estacional SP")
        axes[0, col].grid(True, linestyle="--", alpha=0.7)

        axes[1, col].plot(valores_q, arr_dt, "s-", color="tab:orange", markersize=4)
        axes[1, col].set_title(f"Desfase delta_t_TP vs {nombre_param}")
        axes[1, col].set_xlabel(etiquetas[nombre_param])
        axes[1, col].set_ylabel("Desfase delta_t_TP [meses]")
        axes[1, col].grid(True, linestyle="--", alpha=0.7)

    plt.suptitle("Parte 2 - Punto B: Sensibilidad parametrica individual", fontsize=14)
    plt.tight_layout()
    if guardar_graficos:
        os.makedirs(carpeta_salida, exist_ok=True)
        plt.savefig(os.path.join(carpeta_salida, "parte2_punto_b.png"), dpi=150)
    plt.show()

    return resultados


def ejecutar_punto_2c(h_p2=0.005):
    print("\n--- PARTE 2 - Punto C (Busqueda en grilla de maxima severidad SP) ---")

    grilla_A = np.linspace(0.25, 0.60, 8)
    grilla_beta = np.linspace(0.10, 0.30, 9)
    grilla_gamma = np.linspace(0.05, 0.20, 7)
    grilla_sigma = np.linspace(0.40, 1.00, 7)

    mejor_escenario = None
    mejor_SP = -1.0

    for val_A in grilla_A:
        for val_beta in grilla_beta:
            for val_gamma in grilla_gamma:
                for val_sigma in grilla_sigma:
                    t_g, T_g, H_g, P_g = euler(
                        h_p2, A_val=val_A, beta=val_beta, gamma=val_gamma, sigma=val_sigma
                    )
                    ind_g = calcular_indicadores_ultimo_ciclo(t_g, T_g, H_g, P_g)

                    if ind_g is not None and ind_g["es_repetitivo"]:
                        if ind_g["SP"] > mejor_SP:
                            mejor_SP = ind_g["SP"]
                            mejor_escenario = {
                                "A": val_A,
                                "beta": val_beta,
                                "gamma": val_gamma,
                                "sigma": val_sigma,
                                "indicadores": ind_g,
                                "series": (t_g, T_g, H_g, P_g),
                            }

    print("Combinacion optima encontrada (acotada y repetitiva):")
    print(
        f"  A = {mejor_escenario['A']:.4f}, "
        f"beta = {mejor_escenario['beta']:.4f}, "
        f"gamma = {mejor_escenario['gamma']:.4f}, "
        f"sigma = {mejor_escenario['sigma']:.4f} "
        f"-> SP = {mejor_SP:.4f}"
    )
    return mejor_escenario


def ejecutar_punto_2d(series_nom, ind_nom, mejor_escenario, h_p2=0.005, guardar_graficos=True, carpeta_salida="graficos"):
    t_nom, T_nom, H_nom, P_nom = series_nom
    ind_opt = mejor_escenario["indicadores"]
    t_opt, T_opt, H_opt, P_opt = mejor_escenario["series"]

    t_max_p, T_max_p, H_max_p, P_max_p = euler(
        h_p2, A_val=0.60, beta=0.30, gamma=0.20, sigma=1.00
    )
    ind_todos_max = calcular_indicadores_ultimo_ciclo(t_max_p, T_max_p, H_max_p, P_max_p)

    print("\n--- PARTE 2 - Punto D (Comparacion Caso Nominal vs Maxima Severidad) ---")
    print(f"{'Indicador':<18} | {'Caso Nominal':<15} | {'Max Severidad':<15} | {'Todos en Maximo':<15}")
    print("-" * 72)
    print(f"{'A [1/mes]':<18} | {A:<15.4f} | {mejor_escenario['A']:<15.4f} | {0.60:<15.4f}")
    print(f"{'beta':<18} | {BETA:<15.4f} | {mejor_escenario['beta']:<15.4f} | {0.30:<15.4f}")
    print(f"{'gamma':<18} | {GAMMA:<15.4f} | {mejor_escenario['gamma']:<15.4f} | {0.20:<15.4f}")
    print(f"{'sigma [1/mes]':<18} | {SIGMA:<15.4f} | {mejor_escenario['sigma']:<15.4f} | {1.00:<15.4f}")
    print("-" * 72)
    print(f"{'SP':<18} | {ind_nom['SP']:<15.4f} | {ind_opt['SP']:<15.4f} | {ind_todos_max['SP']:<15.4f}")
    print(f"{'delta_t_TP [mes]':<18} | {ind_nom['delta_t_TP']:<15.4f} | {ind_opt['delta_t_TP']:<15.4f} | {ind_todos_max['delta_t_TP']:<15.4f}")
    print(f"{'P_max [u.p.]':<18} | {ind_nom['P_max']:<15.4f} | {ind_opt['P_max']:<15.4f} | {ind_todos_max['P_max']:<15.4f}")
    print(f"{'P_min [u.p.]':<18} | {ind_nom['P_min']:<15.4f} | {ind_opt['P_min']:<15.4f} | {ind_todos_max['P_min']:<15.4f}")
    print(f"{'P_med [u.p.]':<18} | {ind_nom['P_med']:<15.4f} | {ind_opt['P_med']:<15.4f} | {ind_todos_max['P_med']:<15.4f}")

    mask_48_60 = (t_nom >= 48.0 - 1e-9) & (t_nom <= 60.0 + 1e-9)
    fig, axes = plt.subplots(2, 2, figsize=(15, 9))

    axes[0, 0].plot(t_nom, T_nom, label="T(t) Nominal", color="tab:red", linestyle="--")
    axes[0, 0].plot(t_opt, T_opt, label="T(t) Max SP", color="tab:red", linewidth=1.8)
    axes[0, 0].plot(t_nom, H_nom, label="H(t) Nominal", color="tab:blue", linestyle="--")
    axes[0, 0].plot(t_opt, H_opt, label="H(t) Max SP", color="tab:blue", linewidth=1.8)
    axes[0, 0].set_title("Punto D: T(t) y H(t) en 60 meses (Nominal vs Max SP)")
    axes[0, 0].set_xlabel("Tiempo t [meses]")
    axes[0, 0].set_ylabel("Nivel")
    axes[0, 0].grid(True, linestyle="--", alpha=0.7)
    axes[0, 0].legend()

    axes[0, 1].plot(t_nom, P_nom, label=f"P(t) Nominal (SP={ind_nom['SP']:.2f})", color="tab:green", linestyle="--")
    axes[0, 1].plot(t_opt, P_opt, label=f"P(t) Max SP (SP={ind_opt['SP']:.2f})", color="darkgreen", linewidth=1.8)
    axes[0, 1].set_title("Punto D: Precipitacion P(t) en 60 meses (Nominal vs Max SP)")
    axes[0, 1].set_xlabel("Tiempo t [meses]")
    axes[0, 1].set_ylabel("Precipitacion P(t) [u.p.]")
    axes[0, 1].grid(True, linestyle="--", alpha=0.7)
    axes[0, 1].legend()

    axes[1, 0].plot(t_nom[mask_48_60], T_nom[mask_48_60], label="T(t) Nominal", color="tab:red", linestyle="--")
    axes[1, 0].plot(t_opt[mask_48_60], T_opt[mask_48_60], label="T(t) Max SP", color="tab:red", linewidth=2)
    axes[1, 0].plot(t_nom[mask_48_60], H_nom[mask_48_60], label="H(t) Nominal", color="tab:blue", linestyle="--")
    axes[1, 0].plot(t_opt[mask_48_60], H_opt[mask_48_60], label="H(t) Max SP", color="tab:blue", linewidth=2)
    axes[1, 0].set_title("Punto D: Ultimo ciclo anual (48 <= t <= 60 meses) - T y H")
    axes[1, 0].set_xlabel("Tiempo t [meses]")
    axes[1, 0].set_ylabel("Nivel")
    axes[1, 0].grid(True, linestyle="--", alpha=0.7)
    axes[1, 0].legend()

    axes[1, 1].plot(t_nom[mask_48_60], P_nom[mask_48_60], label="P(t) Nominal", color="tab:green", linestyle="--")
    axes[1, 1].plot(t_opt[mask_48_60], P_opt[mask_48_60], label="P(t) Max SP", color="darkgreen", linewidth=2)
    axes[1, 1].axhline(ind_nom["P_med"], color="tab:green", linestyle=":", alpha=0.8, label="P_med Nominal")
    axes[1, 1].axhline(ind_opt["P_med"], color="darkgreen", linestyle=":", alpha=0.8, label="P_med Max SP")
    axes[1, 1].set_title("Punto D: Ultimo ciclo anual (48 <= t <= 60 meses) - P(t)")
    axes[1, 1].set_xlabel("Tiempo t [meses]")
    axes[1, 1].set_ylabel("Precipitacion P(t) [u.p.]")
    axes[1, 1].grid(True, linestyle="--", alpha=0.7)
    axes[1, 1].legend()

    plt.tight_layout()
    if guardar_graficos:
        os.makedirs(carpeta_salida, exist_ok=True)
        plt.savefig(os.path.join(carpeta_salida, "parte2_punto_d.png"), dpi=150)
    plt.show()


def correr_parte2(h_p2=0.005, guardar_graficos=True, carpeta_salida="graficos"):
    series_nom, ind_nom = ejecutar_punto_2a(h_p2, guardar_graficos, carpeta_salida)
    ejecutar_punto_2b(h_p2, guardar_graficos, carpeta_salida)
    mejor_escenario = ejecutar_punto_2c(h_p2)
    ejecutar_punto_2d(series_nom, ind_nom, mejor_escenario, h_p2, guardar_graficos, carpeta_salida)
