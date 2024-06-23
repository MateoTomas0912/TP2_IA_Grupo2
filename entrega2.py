from simpleai.search import CspProblem, backtrack, min_conflicts, MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE
from itertools import combinations

def armar_nivel(colores, contenidos_parciales):
    #Numero de frascos dependiendo los colores
    cant_frascos = len(colores)

    #cant_frascos = 4 --> variables = [(0,0),(0,1),...,(3,3)] --> [(numFrasco,numSegmento),...]

    variables = [(frasco, pos) for frasco in range(cant_frascos) for pos in range(4)]

    dominios = {variable: colores[:] for variable in variables}

    # Aplicar contenidos parciales: si una posición tiene un color definido, su dominio se reduce a ese color
    for frasco, contenido in enumerate(contenidos_parciales):
        for pos, color in enumerate(contenido):
            if color:  # Si hay un color definido en esa posición
                dominios[(frasco, pos)] = [color]

    restricciones = []

    # Todos los frascos tienen capacidad de 4 segmentos. --> cuando se crea, se crean de 4 segmentos
    # Todos los frascos deben llenarse hasta el tope.
    def frascos_llenos(variables, values):
        return all(values)

    for frasco in range(cant_frascos):
        frasco_vars = [(frasco, pos) for pos in range(4)]
        restricciones.append((frasco_vars, frascos_llenos))

    # No puede haber más de 4 segmentos de un mismo color, de lo contrario no se podría resolver el juego.
    def no_mas_de_cuatro_segmentos(variables, values):
        conteo_colores = {color: 0 for color in colores}
        for value in values:
            conteo_colores[value] += 1
        return all(conteo_colores[color] <= 4 for color in colores)

    for frasco1, frasco2, frasco3, frasco4, frasco5 in combinations(variables, 5):
        restricciones.append(((frasco1, frasco2, frasco3, frasco4, frasco5), no_mas_de_cuatro_segmentos))



    # Ningún frasco debe comenzar resuelto. Es decir, ningún frasco debe tener 4 segmentos del mismo color.
    def no_frasco_resuelto(variables, values):
        return len(set(values)) > 1

    for frasco in range(cant_frascos):
        frasco_vars = [(frasco, pos) for pos in range(4)]
        restricciones.append((frasco_vars, no_frasco_resuelto))

    # Ningún color puede comenzar con todos sus segmentos en el fondo de frascos, porque se trataría de una situación excesivamente difícil de resolver.
    def no_color_completo_en_fondo(variables, values):
        conteo_fondo = {color: 0 for color in colores}
        for value in values:
            conteo_fondo[value] += 1
        return all(conteo_fondo[color] < 4 for color in colores)

    frasco_fondo = []

    for frasco in range(cant_frascos):
        frasco_vars = [(frasco, pos) for pos in range(4)]
        frasco_fondo.append(frasco_vars[0])

    restricciones.append((frasco_fondo, no_color_completo_en_fondo))

    # Si dos frascos son adyacentes, deben compartir al menos un color.
    def frascos_adyacentes_comparten_color(variables, values):
        frasco1_values = values[:4]
        frasco2_values = values[4:]
        return len(set(frasco1_values) & set(frasco2_values)) > 0

    for frasco in range(cant_frascos - 1):
        frasco_vars1 = [(frasco, pos) for pos in range(4)]
        frasco_vars2 = [(frasco + 1, pos) for pos in range(4)]
        restricciones.append((frasco_vars1 + frasco_vars2, frascos_adyacentes_comparten_color))

    # Si dos frascos son adyacentes, no pueden tener más de 6 colores diferentes entre ambos, para evitar situaciones demasiado complejas.
    def frascos_adyacentes_no_mas_de_seis_colores(variables, values):
        return len(set(values)) <= 6

    for frasco in range(cant_frascos - 1):
        frasco_vars1 = [(frasco, pos) for pos in range(4)]
        frasco_vars2 = [(frasco + 1, pos) for pos in range(4)]
        restricciones.append((frasco_vars1 + frasco_vars2, frascos_adyacentes_no_mas_de_seis_colores))

    # No puede haber dos frascos exactamente iguales.

    def frascos_diferentes(variables, values):
        frasco1_values = values[:4]
        frasco2_values = values[4:]
        return frasco1_values != frasco2_values

    for frasco1, frasco2 in combinations(range(cant_frascos), 2):
        frasco_vars1 = [(frasco1, pos) for pos in range(4)]
        frasco_vars2 = [(frasco2, pos) for pos in range(4)]
        restricciones.append((frasco_vars1 + frasco_vars2, frascos_diferentes))


    #return dominios
    # Crear y resolver el problema
    problema = CspProblem(variables, dominios, restricciones)
    #solucion = min_conflicts(problema, iterations_limit=47000)
    solucion = backtrack(problema, variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                         value_heuristic=LEAST_CONSTRAINING_VALUE)

    # Convertir la solución en el formato esperado
    resultado = []
    for frasco in range(cant_frascos):
        frasco_values = [solucion[(frasco, pos)] for pos in range(4)]
        resultado.append(tuple(frasco_values))

    return resultado



# Ejemplo de uso
if __name__ == "__main__":
    frascos = armar_nivel(
                colores=["rojo", "verde", "azul", "celeste", "lila", "naranja", "amarillo", "verde_oscuro"],
                contenidos_parciales=[("rojo", "verde_oscuro", "verde_oscuro", "verde_oscuro"),
                                      ("celeste", "azul", "azul",),
                                      ("naranja", "verde_oscuro", "verde", "azul"),
                                      ("amarillo", "amarillo",),
                                      ("celeste",),]
    )

    for frasco in frascos:
        print(*frasco)

    apariciones_colores = {}
    for combinacion in frascos:
        for color in combinacion:
            if color not in apariciones_colores:
                apariciones_colores[color] = 0
            apariciones_colores[color] += 1
    print(apariciones_colores)
    total = 0
    for color in apariciones_colores:
        total += apariciones_colores[color]
    print (total)
