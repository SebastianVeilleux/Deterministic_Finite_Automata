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
            "guion_bajo": "qerror", 
            "asignacion": "qass",
            "suma": "qsum",
            "resta": "qsub",
            "multiplicacion": "qmul",
            "division": "qdiv",
            "potencia": "qpow",
            "parentesis_abre": "qop",
            "parentesis_cierra": "qcl",
            "espacio": "qstart",
            "otro": "qerror",
        },
        "qint": {
            "digito": "qint",
            "punto": "qfloat",
            "exponente": "qexp",
            "letra": "qerror", 
            "guion_bajo": "qerror",
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
            "otro": "qerror", 
        },
        "qexpsign": {
            "digito": "qexpnum",
            "otro": "qerror",  
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
        "qerror": {}, 
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

# archivo de entrada
lexer_aritmetico("expresiones.txt")