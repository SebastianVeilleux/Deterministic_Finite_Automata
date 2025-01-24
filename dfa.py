def clasificar_caracter(caracter):
    if caracter.isdigit():
        return "digito"
    elif caracter.isalpha():
        return "letra"
    elif caracter == "_":
        return "guion_bajo"
    elif caracter == "=":
        return "asignacion"
    elif caracter == "+":
        return "suma"
    elif caracter == "-":
        return "resta"
    elif caracter == "*":
        return "multiplicacion"
    elif caracter == "/":
        return "division"
    elif caracter == "^":
        return "potencia"
    elif caracter == "(":
        return "parentesis_abre"
    elif caracter == ")":
        return "parentesis_cierra"
    elif caracter == ".":
        return "punto"
    elif caracter.lower() == "e":
        return "exponente"
    elif caracter.isspace():
        return "espacio"
    else:
        return "otro"

def procesar_cadena(cadena, transiciones):
    estado_actual = "qstart"
    token_actual = ""
    tokens = []

    for caracter in cadena:
        clasificacion = clasificar_caracter(caracter)

        if clasificacion in transiciones[estado_actual]:
            estado_siguiente = transiciones[estado_actual][clasificacion]

            if estado_siguiente == "qend":
                tokens.append((token_actual, estado_actual))
                estado_actual = "qstart"
                token_actual = ""

                # Reprocesar el caracter actual desde el estado inicial
                if clasificacion in transiciones[estado_actual]:
                    estado_actual = transiciones[estado_actual][clasificacion]
                    token_actual += caracter
            else:
                estado_actual = estado_siguiente
                token_actual += caracter
        else:
            # Si el caracter no encaja, finalizamos el token actual
            if token_actual:
                tokens.append((token_actual, estado_actual))
            estado_actual = "qstart"
            token_actual = ""

            # Reprocesar el caracter actual desde el estado inicial
            if clasificacion in transiciones[estado_actual]:
                estado_actual = transiciones[estado_actual][clasificacion]
                token_actual += caracter

    # Agregar el último token si existe
    if token_actual:
        tokens.append((token_actual, estado_actual))

    return tokens

def lexer_aritmetico(archivo):
    transiciones = {
        "qstart": {
            "digito": "qint",
            "letra": "qvar",
            "guion_bajo": "qvar",
            "asignacion": "qass",
            "suma": "qsum",
            "resta": "qsub",
            "multiplicacion": "qmul",
            "division": "qdiv",
            "potencia": "qpow",
            "parentesis_abre": "qop",
            "parentesis_cierra": "qcl",
            "espacio": "qstart",
            "otro": "qstart",
        },
        "qint": {
            "digito": "qint",
            "punto": "qfloat",
            "exponente": "qexp",
            "otro": "qend",
        },
        "qfloat": {
            "digito": "qfloat",
            "exponente": "qexp",
            "otro": "qend",
        },
        "qexp": {
            "digito": "qexpnum",
            "resta": "qexpsign",
            "otro": "qstart",
        },
        "qexpsign": {
            "digito": "qexpnum",
            "otro": "qstart",
        },
        "qexpnum": {
            "digito": "qexpnum",
            "otro": "qend",
        },
        "qvar": {
            "letra": "qvar",
            "digito": "qvar",
            "guion_bajo": "qvar",
            "otro": "qend",
        },
        "qass": {"otro": "qend"},
        "qsum": {"otro": "qend"},
        "qsub": {"otro": "qend"},
        "qmul": {"otro": "qend"},
        "qdiv": {
            "division": "qcom",
            "otro": "qend",
        },
        "qpow": {"otro": "qend"},
        "qop": {"otro": "qend"},
        "qcl": {"otro": "qend"},
        "qcom": {"otro": "qcom"},
    }

    tipos_tokens = {
        "qint": "Entero",
        "qfloat": "Real",
        "qexpnum": "Real",
        "qvar": "Variable",
        "qass": "Asignación",
        "qsum": "Suma",
        "qsub": "Resta",
        "qmul": "Multiplicación",
        "qdiv": "División",
        "qpow": "Potencia",
        "qop": "Paréntesis que abre",
        "qcl": "Paréntesis que cierra",
        "qcom": "Comentario",
    }

    with open(archivo, "r") as file:
        for linea in file:
            tokens = procesar_cadena(linea.strip(), transiciones)
            for token, estado in tokens:
                tipo = tipos_tokens.get(estado, "Desconocido")
                print(f"Token: {token}, Tipo: {tipo}")

# Prueba con un archivo de entrada
lexer_aritmetico("expresiones.txt")
