# TpMode2c2026
Repositorio para el TP de modelacion numerica (Tarela), 2c2026.

## Algunas cositas que me sugirio la ia, para poner en el informe (acordarse poner que ia usamos):


### Definicion de variables: 
Cambiar el nombre de algunos simbolos que estaban mal (por ejemplo uno se llamaba SIGMA y yo le puse TITA)

### Construccion de Ecuaciones (delta): 
En principio habiamos planteado tres ecuaciones distintas para cada delta.
Nos sugirio tener una unica funcion en donde se calculan las 3 por separado y luego se devuelven sus resultados, nos parecio mas practico asi que utilizamos esta funcion.

### Construccion de ecuacion de Euler:
Nos recomendo utilizar numpy para que a la hora de ejecutar las simulaciones, las listas propias de python pueden ser lentas (aca podriamos mencionar que es algo que vimos en fundamentos de la programacion ).
Numpy maneja arreglos de vectores en C, con iteraciones mas rapidas.

Aparte nos menciono que es el estandar para pasar datos directamente a funciones que grafican.