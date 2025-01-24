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

    i = 0
    while i < len(cadena):
        caracter = cadena[i]
        clasificacion = clasificar_caracter(caracter)

        if estado_actual == "qcom":
            # Capturar el resto de la línea como un comentario
            token_actual += cadena[i:]
            tokens.append((token_actual, estado_actual))
            break

        if clasificacion in transiciones.get(estado_actual, {}):
            estado_siguiente = transiciones[estado_actual][clasificacion]

            if estado_siguiente == "qend":
                tokens.append((token_actual, estado_actual))
                estado_actual = "qstart"
                token_actual = ""

                if clasificacion in transiciones.get(estado_actual, {}):
                    estado_actual = transiciones[estado_actual][clasificacion]
                    token_actual += caracter
            else:
                estado_actual = estado_siguiente
                token_actual += caracter
        else:
            if clasificacion == "otro" or estado_actual == "qerror":
                print(f"Error: Caracter no reconocido '{caracter}' en la línea '{cadena.strip()}'")

            if token_actual:
                tokens.append((token_actual, estado_actual))
            estado_actual = "qstart"
            token_actual = ""

            if clasificacion in transiciones.get(estado_actual, {}):
                estado_actual = transiciones[estado_actual][clasificacion]
                token_actual += caracter

        i += 1

    if token_actual and estado_actual != "qcom":
        tokens.append((token_actual, estado_actual))

    return tokens

def lexer_aritmetico(archivo):
    transiciones = {
        "qstart": {
            "digito": "qint",
            "letra": "qvar",
            "guion_bajo": "qerror",  # Error: variable no puede iniciar con "_"
            "asignacion": "qass",
            "suma": "qsum",
            "resta": "qsub",
            "multiplicacion": "qmul",
            "division": "qdiv",
            "potencia": "qpow",
            "parentesis_abre": "qop",
            "parentesis_cierra": "qcl",
            "espacio": "qstart",
            "otro": "qerror",  # Caracter inválido
        },
        "qint": {
            "digito": "qint",
            "punto": "qfloat",
            "exponente": "qexp",
            "letra": "qerror",  # Error: número no puede mezclarse con letras
            "guion_bajo": "qerror",  # Error: número no puede mezclarse con "_"
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
            "otro": "qerror",  # Error: exponente debe ser un número
        },
        "qexpsign": {
            "digito": "qexpnum",
            "otro": "qerror",  # Error: signo debe ir seguido de número
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
            "division": "qcom",  # Comentario al detectar "//"
            "otro": "qend",
        },
        "qpow": {"otro": "qend"},
        "qop": {"otro": "qend"},
        "qcl": {"otro": "qend"},
        "qcom": {"otro": "qcom"},  # Permanecer en comentario
        "qerror": {},  # Estado de error: no transiciones válidas
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
        "qerror": "Error",
    }

    with open(archivo, "r") as file:
        for linea in file:
            tokens = procesar_cadena(linea.strip(), transiciones)
            for token, estado in tokens:
                tipo = tipos_tokens.get(estado, "Desconocido")
                if tipo == "Error":
                    print(f"Error: Token inválido '{token}' en la línea '{linea.strip()}'")
                elif tipo == "Desconocido":
                    print(f"Advertencia: Token desconocido '{token}' encontrado.")
                else:
                    print(f"Token: {token}, Tipo: {tipo}")

# Prueba con un archivo de entrada
lexer_aritmetico("expresiones.txt")