# Importamos librerías necesarias
from numpy import *
import sympy as sp

# Creamos una nueva función con sus "argumentos".


def Riemann(Fun_Riemann, LimInferior, LimSuperior, SubInt):

    # Calculamos la longitud de los subintervalos.
    dx = (LimSuperior-LimInferior)/SubInt

    # Definimos x como variable
    x = sp.symbols('x')

    # Usando lamdbify convertimos la función almacenada en f en una función de Python que tiene como argumento x.
    fx = sp.lambdify(x, Fun_Riemann)

    # Definimos  "Resultado" donde vamos a almacenar el resultado de la suma. Evaluamos de una vez para x_0.
    Resultado = fx(LimInferior)

    # Hacemos un ciclo  for para evaluar la función de x_1 hasta x_SubInt.
    for i in range(1, SubInt):
        Resultado += fx(LimInferior + i*dx)

    # Multiplicamos el resultado por dx.
    Resultado *= dx
    Resultado = "El resultado usando la Suma de Riemann hacia adelante para las condiciones dadas es: " + \
        str(Resultado)

    # Devolvemos el valor de Resultado. Ósea la suma calculada númericamente.
    return Resultado
