def solicitar_transiciones():
    print("\nIngrese las transiciones del APD una por una.")
    print("Formato: estado,entrada,tope_pila => nuevo_estado,símbolos_a_apilar")
    print("Ejemplo: q0,a,Z => q1,AZ")
    print("Use 'ε' para representar vacío (sin leer símbolo o sin apilar).")
    print("Escriba 'fin' para terminar de ingresar transiciones.")

    transiciones = {}

    while True:
        entrada = input("Transición: ").strip()
        if entrada.lower() == 'fin':
            break

        try:
            izquierda, derecha = entrada.split("=>")
            izquierda = izquierda.strip()
            derecha = derecha.strip()

            estado, simbolo, tope = [s.strip() for s in izquierda.split(",")]
            nuevo_estado, apilar = [s.strip() for s in derecha.split(",")]

            clave = (estado, simbolo, tope)
            valor = (nuevo_estado, list(apilar) if apilar != 'ε' else [])

            transiciones[clave] = valor

        except ValueError:
            print("Formato inválido. Intenta de nuevo.")

    return transiciones
