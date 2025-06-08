# este modulo contiene funciones para simular un Autómata de Pila Determinista (APD)


# esta funcion simula un Autómata de Pila Determinista (APD) paso a paso
# mostrando el estado actual, la pila y las transiciones realizadas
# y determina si la palabra es aceptada o rechazada según el tipo de aceptación
def simular_apd(transiciones, estado_inicial, estados_finales, palabra, tipo_aceptacion):
    estado_actual = estado_inicial
    pila = ['Z']
    entrada = list(palabra) + ['ε']
    i = 0

    print("\nSimulación paso a paso:")
    while i < len(entrada):
        simbolo_entrada = entrada[i]
        cima_pila = pila[-1] if pila else 'ε'
        clave = (estado_actual, simbolo_entrada, cima_pila)

        if clave in transiciones:
            nuevo_estado, nuevos_simbolos = transiciones[clave]
            print(f"δ({estado_actual}, {simbolo_entrada}, {cima_pila}) → ({nuevo_estado}, {''.join(nuevos_simbolos) or 'ε'})")
            estado_actual = nuevo_estado
            pila.pop()
            for s in reversed(nuevos_simbolos):
                if s != 'ε':
                    pila.append(s)
            if simbolo_entrada != 'ε':
                i += 1
        else:
            print(f"No hay transición definida para ({estado_actual}, {simbolo_entrada}, {cima_pila})")
            break

    print(f"\nEstado final alcanzado: {estado_actual}")
    print(f"Pila final: {pila}")

    if tipo_aceptacion == 'estado_final':
        if estado_actual in estados_finales:
            print("La palabra fue ACEPTADA por estado final.")
            return True
        else:
            print("La palabra fue RECHAZADA.")
            return False
    elif tipo_aceptacion == 'pila_vacia':
        if pila == [] or pila == ['Z']:
            print("La palabra fue ACEPTADA por pila vacía.")
            return True
        else:
            print("La palabra fue RECHAZADA (la pila no está vacía).")
            return False
