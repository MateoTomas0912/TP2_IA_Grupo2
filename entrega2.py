from simpleai.search import CspProblem, backtrack


def generar_rellenos(colores, length):
    if length == 0:
        return [[]]
    else:
        rellenos = []
        for color in colores:
            for resto in generar_rellenos(colores, length - 1):
                rellenos.append([color] + resto)
        return rellenos


def no_mas_de_cuatro_segmentos(colores):
    def restriccion(variables, values):
        conteo_colores = {color: 0 for color in colores}
        for value in values:
            for segmento in value:
                conteo_colores[segmento] += 1
        return all(conteo_colores[color] <= 4 for color in colores)

    return restriccion


def ningun_frasco_resuelto(variables, values):
    return all(len(set(value)) > 1 for value in values)


def color_no_en_fondo(colores, n):
    def restriccion(variables, values):
        conteo_fondo = {color: 0 for color in colores}
        for value in values:
            conteo_fondo[value[0]] += 1
        return all(conteo_fondo[color] < n for color in colores)

    return restriccion


def adyacentes_comparten_color(variables, values):
    for i in range(len(values) - 1):
        if not set(values[i]).intersection(values[i + 1]):
            return False
    return True


def adyacentes_max_seis_colores(variables, values):
    for i in range(len(values) - 1):
        if len(set(values[i]).union(values[i + 1])) > 6:
            return False
    return True


def frascos_no_iguales(variables, values):
    return len(values) == len(set(values))


def armar_nivel(colores, contenidos_parciales):
    # Número de frascos y colores
    n = len(colores)

    # Variables y dominios
    variables = [f'frasco_{i}' for i in range(n)]
    dominios = {}

    for i in range(n):
        if i < len(contenidos_parciales):
            # Frasco con contenido parcial
            dominios[variables[i]] = [contenidos_parciales[i] + tuple(resto)
                                      for resto in generar_rellenos(colores, 4 - len(contenidos_parciales[i]))]
        else:
            # Frasco sin contenido parcial
            dominios[variables[i]] = [tuple(relleno) for relleno in generar_rellenos(colores, 4)]

    # Restricciones
    restricciones = [
        (variables, no_mas_de_cuatro_segmentos(colores)),
        (variables, ningun_frasco_resuelto),
        (variables, color_no_en_fondo(colores, n)),
        (variables, adyacentes_comparten_color),
        (variables, adyacentes_max_seis_colores),
        (variables, frascos_no_iguales),
    ]

    # Crear y resolver el problema
    problema = CspProblem(variables, dominios, restricciones)
    solucion = backtrack(problema)

    # Convertir la solución en el formato esperado
    resultado = [solucion[var] for var in variables]
    return resultado


# Ejemplo de uso
frascos = armar_nivel(
    colores=["rojo", "verde", "azul", "amarillo"],
    contenidos_parciales=[
        ("verde", "azul", "rojo", "rojo"),
        ("verde", "rojo")
    ]
)

print(frascos)
