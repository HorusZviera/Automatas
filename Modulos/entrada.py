# este modulo contiene funciones para solicitar datos al usuario

# esta funcion solicita el alfabeto al usuario
def solicitar_alfabeto():
    while True:
        alfabeto = input("Ingrese el alfabeto separado por comas (ej: a,b,c): ")
        simbolos = [s.strip() for s in alfabeto.split(',') if s.strip() != '']
        if simbolos:
            if all(len(s) == 1 for s in simbolos):
                return simbolos
            else:
                print("Cada símbolo del alfabeto debe tener solo 1 carácter.")
        else:
            print("El alfabeto no puede estar vacío.")

# esta funcion solicita el estado inicial al usuario
def solicitar_estado_inicial(alfabeto):
    while True:
        estado = input("Ingrese el estado inicial: ").strip()
        if not estado:
            print("El estado inicial no puede estar vacío.")
        elif estado in alfabeto:
            print("El estado inicial no puede ser un símbolo del alfabeto.")
        else:
            return estado

# esta funcion solicita los estados finales al usuario
def solicitar_estados_finales(alfabeto):
    while True:
        estados = input("Ingrese los estados finales separados por comas (ej: qf,q2): ")
        estados_list = [s.strip() for s in estados.split(',') if s.strip() != '']
        if not estados_list:
            print("Debe ingresar al menos un estado final.")
        elif any(e in alfabeto for e in estados_list):
            print("Los estados finales no pueden ser símbolos del alfabeto.")
        else:
            return list(set(estados_list))

# esta funcion solicita una palabra al usuario
def solicitar_palabra(alfabeto):
    while True:
        palabra = input("Ingrese la palabra a analizar (use solo símbolos del alfabeto): ").strip()
        if all(c in alfabeto for c in palabra):
            return palabra
        else:
            print("La palabra contiene símbolos no definidos en el alfabeto.")

# esta funcion muestra un menu para seleccionar el tipo de aceptacion del APD
def menu_tipo_aceptacion():
    print("\nSeleccione el tipo de aceptación del APD:")
    print("1. Por estado final")
    print("2. Por pila vacía")
    while True:
        opcion = input("Ingrese 1 o 2: ").strip()
        if opcion == '1':
            return 'estado_final'
        elif opcion == '2':
            return 'pila_vacia'
        else:
            print("Opción inválida. Intente de nuevo.")
