from src.parte1 import correr_parte1
from src.parte2 import correr_parte2


def main():
    carpeta_graficos = "graficos"
    guardar = True

    print("Iniciando simulaciones del TP de Modelacion Numerica...")
    correr_parte1(guardar_graficos=guardar, carpeta_salida=carpeta_graficos)
    correr_parte2(h_p2=0.005, guardar_graficos=guardar, carpeta_salida=carpeta_graficos)
    print("\nEjecucion finalizada. Los graficos se guardaron en la carpeta 'graficos/'.")


if __name__ == "__main__":
    main()
