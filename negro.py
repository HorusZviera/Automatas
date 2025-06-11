import tkinter as tk
import ast

# Clase lógica APD
class APDSimulator:
    def __init__(self, alfabeto, transiciones, estado_inicial, estados_finales, tipo_aceptacion):
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales
        self.tipo_aceptacion = tipo_aceptacion

    def simular(self, palabra):
        pila = ['Z']  # Símbolo inicial de pila
        estado = self.estado_inicial
        log = f"Inicio en estado {estado} con pila: {pila}\n"

        i = 0
        while True:
            simbolo = palabra[i] if i < len(palabra) else 'ε'
            tope_pila = pila[-1] if pila else 'ε'

            clave = (estado, simbolo, tope_pila)
            clave_epsilon = (estado, 'ε', tope_pila)

            if clave in self.transiciones:
                nuevo_estado, nuevos_simbolos = self.transiciones[clave]
                pila.pop()
                for s in reversed(nuevos_simbolos):
                    if s != 'ε':
                        pila.append(s)
                estado = nuevo_estado
                log += f"Transición con ({simbolo}) → {estado}, pila: {pila}\n"
                if simbolo != 'ε':
                    i += 1

            elif clave_epsilon in self.transiciones:
                nuevo_estado, nuevos_simbolos = self.transiciones[clave_epsilon]
                pila.pop()
                for s in reversed(nuevos_simbolos):
                    if s != 'ε':
                        pila.append(s)
                estado = nuevo_estado
                log += f"Transición con (ε) → {estado}, pila: {pila}\n"

            else:
                break

            if i > len(palabra):
                break

        aceptada = False
        if self.tipo_aceptacion == 'estado_final':
            aceptada = estado in self.estados_finales
        elif self.tipo_aceptacion == 'pila_vacia':
            aceptada = pila == []

        return aceptada, log


# Clase GUI
class APDGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulador APD")
        self.root.geometry("600x680")

        self.stack_vacio = tk.BooleanVar(value=False)

        self.crear_widgets()
        self.root.mainloop()

    def crear_widgets(self):
        # Alfabeto
        tk.Label(self.root, text="Alfabeto (ej: ['a','b']):").pack()
        self.alfabeto_txt = tk.Text(self.root, height=2, width=60)
        self.alfabeto_txt.pack()

        # Transiciones
        tk.Label(self.root, text="Transiciones (ej: (q0,a,Z) => (q0,AZ))").pack()
        self.transiciones_txt = tk.Text(self.root, height=6, width=60)
        self.transiciones_txt.pack()

        # Estado inicial
        tk.Label(self.root, text="Estado inicial (ej: q0):").pack()
        self.estado_inicial_txt = tk.Entry(self.root, width=60)
        self.estado_inicial_txt.pack()

        # Estados finales
        tk.Label(self.root, text="Estados finales separados por coma (ej: qf,q2):").pack()
        self.estado_final_txt = tk.Entry(self.root, width=60)
        self.estado_final_txt.pack()

        # Palabras
        tk.Label(self.root, text="Palabras (ej: ['ab', 'aabb']):").pack()
        self.palabras_txt = tk.Text(self.root, height=3, width=60)
        self.palabras_txt.pack()

        # Aceptación por pila vacía o estado final
        self.acepta_stack_vacio_chk = tk.Checkbutton(
            self.root, text="Aceptar por pila vacía (desmarcar para estado final)",
            variable=self.stack_vacio
        )
        self.acepta_stack_vacio_chk.pack()

        # Botón procesar
        tk.Button(self.root, text="Procesar Palabras", command=self.procesar).pack(pady=10)

        # Resultado
        self.resultado_txt = tk.Text(self.root, height=17, width=70, fg="blue")
        self.resultado_txt.pack()

    def parsear_transiciones(self, texto):
        """

        """

        transiciones = {}
        lineas = texto.strip().split('\n') # toma todas las lineas del input, estas estan separadas asi: '(q0, a, Z) => (q0, AZ)', '(q0, a, A) => (q0, AA)', por cada salto de linea las separa y les elimina el espacio de la ultima linea. Lineas es un array.
        for linea in lineas:
            if '=>' in linea:
                izquierda, derecha = linea.split('=>') # Separa el texto por '=>' en dos arrays. Queda asi: derecha:['(q0, a, Z)'], izquierda:['(q0, AZ)']
                estado, simbolo, tope_pila = [x.strip() for x in izquierda.strip('() ').split(',')] # separa las palabras por ',', les quita los parentesis y asigna cada valor de x a las variables 
                nuevo_estado, nuevos_simbolos = [x.strip() for x in derecha.strip('() ').split(',')] # Hace lo mismo que arriba, pero con la parte derecha
                transiciones[(estado, simbolo, tope_pila)] = (nuevo_estado, list(nuevos_simbolos)) # Genera el diccionario con los valores  de la forma: {('q0', 'a', 'Z'): ('q0', ['A', 'Z']), ('q0', 'a', 'A'): ('q0', ['A', 'A'])}
        return transiciones

    def procesar(self):
        try:
            alfabeto = ast.literal_eval(self.alfabeto_txt.get("1.0", "end-1c")) # Toma el alfabeto de la forma ['a','b']
            transiciones_input = self.transiciones_txt.get("1.0", "end-1c") # Toma el lafabeto, al ejecutar la fui hay un ejemplo
            transiciones = self.parsear_transiciones(transiciones_input) # Funcion para pasear las transiciones 
            estado_inicial = self.estado_inicial_txt.get().strip()
            estados_finales = [e.strip() for e in self.estado_final_txt.get().split(',') if e.strip()]
            palabras = ast.literal_eval(self.palabras_txt.get("1.0", "end-1c")) # Palabras a evaluar
            tipo_aceptacion = 'pila_vacia' if self.stack_vacio.get() else 'estado_final'

            simulador = APDSimulator(alfabeto, transiciones, estado_inicial, estados_finales, tipo_aceptacion) # Crea la clase con las variable

            self.resultado_txt.delete("1.0", "end")

            for palabra in palabras: # por cara palabra del array ejecuta la funcion y evalua 
                aceptada, log = simulador.simular(palabra)
                resultado = f"Palabra: '{palabra}' ➡️ {'Aceptada [+]' if aceptada else 'Rechazada [!]'}\n{log}\n{'-'*60}\n"
                self.resultado_txt.insert("end", resultado)

        except Exception as e:
            self.resultado_txt.delete("1.0", "end")
            self.resultado_txt.insert("end", f"[!] Error en los datos ingresados:\n{e}")


# Ejecutar GUI
if __name__ == "__main__": 
    APDGui()
