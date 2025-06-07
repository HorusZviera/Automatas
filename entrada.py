def solicitar_alfabeto():
    while True:
        alfabeto = input("Ingrese el alfabeto separado por comas (ej: a,b,c): ")
        simbolos = [s.strip() for s in alfabeto.split(',') if s.strip() != '']
        if simbolos:
            if all(len(s) == 1 for s in simbolos):
                return simbolos
            else:
                print("❌ Cada símbolo del alfabeto debe tener solo 1 carácter.")
        else:
            print("❌ El alfabeto no puede estar vacío.")

def solicitar_estado_inicial():
    while True:
        estado = input("Ingrese el estado inicial: ").strip()
        if estado:
            return estado
        else:
            print("❌ El estado inicial no puede estar vacío.")

def solicitar_estados_finales():
    while True:
        estados = input("Ingrese los estados finales separados por comas (ej: qf,q2): ")
        estados_list = [s.strip() for s in estados.split(',') if s.strip() != '']
        if estados_list:
            return list(set(estados_list))
        else:
            print("❌ Debe ingresar al menos un estado final.")

def solicitar_palabra(alfabeto):
    while True:
        palabra = input("Ingrese la palabra a analizar (use solo símbolos del alfabeto): ").strip()
        if all(c in alfabeto for c in palabra):
            return palabra
        else:
            print("La palabra contiene símbolos no definidos en el alfabeto.")

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
