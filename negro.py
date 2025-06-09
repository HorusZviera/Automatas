import tkinter as tk

# Clase lógica APD
class APDSimulator:
    def __init__(self, alfabeto, transiciones, estado_inicial, estados_finales, tipo_aceptacion):
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales
        self.tipo_aceptacion = tipo_aceptacion

    def simular(self, palabra):
        estado_actual = self.estado_inicial
        pila = ['Z']
        entrada = list(palabra) + ['ε']
        i = 0
        log = []

        while i < len(entrada):
            simbolo_entrada = entrada[i]
            cima_pila = pila[-1] if pila else 'ε'
            clave = (estado_actual, simbolo_entrada, cima_pila)

            if clave in self.transiciones:
                nuevo_estado, nuevos_simbolos = self.transiciones[clave]
                log.append(f"δ({estado_actual}, {simbolo_entrada}, {cima_pila}) → ({nuevo_estado}, {''.join(nuevos_simbolos) or 'ε'})")
                estado_actual = nuevo_estado
                pila.pop()
                for s in reversed(nuevos_simbolos):
                    if s != 'ε':
                        pila.append(s)
                if simbolo_entrada != 'ε':
                    i += 1
            else:
                log.append(f"No hay transición definida para ({estado_actual}, {simbolo_entrada}, {cima_pila})")
                break

        log.append(f"Estado final alcanzado: {estado_actual}")
        log.append(f"Pila final: {pila}")

        aceptada = False
        if self.tipo_aceptacion == 'estado_final':
            aceptada = estado_actual in self.estados_finales
            log.append("Aceptada por estado final." if aceptada else "Rechazada por estado final.")
        elif self.tipo_aceptacion == 'pila_vacia':
            aceptada = pila == [] or pila == ['Z']
            log.append("Aceptada por pila vacía." if aceptada else "Rechazada, pila no vacía.")

        return aceptada, '\n'.join(log)

# Clase GUI
class APDGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulador APD")
        self.root.geometry("600x650")

        self.stack_vacio = tk.BooleanVar(value=False)

        self.crear_widgets()
        self.root.mainloop()

    def crear_widgets(self):
        # Alfabeto
        tk.Label(self.root, text="Alfabeto (ej: ['a','b']):").pack()
        self.alfabeto_txt = tk.Text(self.root, height=2, width=60)
        self.alfabeto_txt.pack()

        # Transiciones
        tk.Label(self.root, text="Transiciones (ej: q0,a,Z => q1,AZ:").pack()
        self.transiciones_txt = tk.Text(self.root, height=5, width=60)
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
        tk.Label(self.root, text="Palabras (ej: ['ab', 'abb']):").pack()
        self.palabras_txt = tk.Text(self.root, height=3, width=60)
        self.palabras_txt.pack()

        # Aceptación por stack vacío o estado final
        self.acepta_stack_vacio_chk = tk.Checkbutton(
            self.root, text="Aceptar por pila vacía (desmarcar si es por estado final)", 
            variable=self.stack_vacio
        )
        self.acepta_stack_vacio_chk.pack()

        # Botón procesar
        tk.Button(self.root, text="Procesar Palabras", command=self.procesar).pack(pady=10)

        # Resultado
        self.resultado_txt = tk.Text(self.root, height=15, width=70, fg="blue")
        self.resultado_txt.pack()

    def procesar(self):
        try:
            alfabeto = eval(self.alfabeto_txt.get("1.0", "end-1c"))
            transiciones_input = eval(self.transiciones_txt.get("1.0", "end-1c"))
            estado_inicial = self.estado_inicial_txt.get().strip()
            estados_finales = [e.strip() for e in self.estado_final_txt.get().split(',') if e.strip()]
            palabras = eval(self.palabras_txt.get("1.0", "end-1c"))
            tipo_aceptacion = 'pila_vacia' if self.stack_vacio.get() else 'estado_final'

            # Transiciones en diccionario
            transiciones = {
                (t[0], t[1], t[2]): (t[3][0], list(t[3][1])) for t in transiciones_input
            }

            sim = APDSimulator(alfabeto, transiciones, estado_inicial, estados_finales, tipo_aceptacion)

            self.resultado_txt.delete("1.0", "end")

            for palabra in palabras:
                aceptada, log = sim.simular(palabra)
                resultado = f"Palabra: '{palabra}' → {'ACEPTADA' if aceptada else 'RECHAZADA'}\n{log}\n{'-'*60}\n"
                self.resultado_txt.insert("end", resultado)

        except Exception as e:
            self.resultado_txt.delete("1.0", "end")
            self.resultado_txt.insert("end", f"Error en los datos ingresados:\n{e}")

# Ejecutar GUI
if __name__ == "__main__":
    APDGui()
