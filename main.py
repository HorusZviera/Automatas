from entrada import (
    solicitar_alfabeto,
    solicitar_estado_inicial,
    solicitar_estados_finales,
    solicitar_palabra,
    menu_tipo_aceptacion
)
from transiciones import solicitar_transiciones
from simulador import simular_apd

def main():
    alfabeto = solicitar_alfabeto()
    estado_inicial = solicitar_estado_inicial()
    estados_finales = solicitar_estados_finales()
    transiciones = solicitar_transiciones()
    palabra = solicitar_palabra(alfabeto)

    print(f"\nAlfabeto: {alfabeto}")
    print(f"Estado inicial: {estado_inicial}")
    print(f"Estados finales: {estados_finales}")
    print(f"Palabra a analizar: {palabra}")

    print("\nTransiciones ingresadas:")
    for (estado, entrada, tope), (nuevo_estado, apilar) in transiciones.items():
        apilar_str = ''.join(apilar) if apilar else 'ε'
        print(f"δ({estado}, {entrada}, {tope}) → ({nuevo_estado}, {apilar_str})")

    tipo_aceptacion = menu_tipo_aceptacion()
    simular_apd(transiciones, estado_inicial, estados_finales, palabra, tipo_aceptacion)

if __name__ == "__main__":
    main()
