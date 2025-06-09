import tkinter as tk

class Gui():
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Simulador APD")
		self.root.geometry("500x600")

		# Variables de control
		self.stack_vacio = tk.BooleanVar(value=False)

		# Crear los elementos de la GUI
		self.crear_widgets()

		self.root.mainloop()

	def crear_widgets(self):
		# Alfabeto
		tk.Label(self.root, text="Ingrese el alfabeto (ej: ['a','b']):").pack()
		self.alfabeto_txt = tk.Text(self.root, height=2, width=50)
		self.alfabeto_txt.pack()

		# Transiciones
		tk.Label(self.root, text="Ingrese las transiciones (ej: [('q0','a','Z',['q1','AZ'])]):").pack()
		self.transiciones_txt = tk.Text(self.root, height=5, width=50)
		self.transiciones_txt.pack()

		# Estado inicial
		tk.Label(self.root, text="Estado inicial (ej: q0):").pack()
		self.estado_inicial_txt = tk.Entry(self.root, width=50)
		self.estado_inicial_txt.pack()

		# Estado final
		tk.Label(self.root, text="Estado final (si corresponde, ej: qf):").pack()
		self.estado_final_txt = tk.Entry(self.root, width=50)
		self.estado_final_txt.pack()

		# Palabras de entrada
		tk.Label(self.root, text="Palabras de entrada (ej: ['ab', 'abb']):").pack()
		self.palabras_txt = tk.Text(self.root, height=3, width=50)
		self.palabras_txt.pack()

		# Acepta por stack vacío o estado final (Checkbutton)
		self.acepta_stack_vacio_chk = tk.Checkbutton(
			self.root, 
			text="Aceptar por stack vacío (desmarcar si acepta por estado final)", 
			variable=self.stack_vacio
		)
		self.acepta_stack_vacio_chk.pack()

		# Botón para procesar palabras (la lógica APD se implementa aparte)
		tk.Button(self.root, text="Procesar Palabras", command=self.procesar).pack(pady=10)

		# Salida
		self.resultado_lbl = tk.Label(self.root, text="", fg="blue")
		self.resultado_lbl.pack()

	def procesar(self):
		# Por ahora solo captura las entradas y las muestra en consola
		alfabeto = self.alfabeto_txt.get("1.0", "end-1c")
		transiciones = self.transiciones_txt.get("1.0", "end-1c")
		estado_inicial = self.estado_inicial_txt.get()
		estado_final = self.estado_final_txt.get()
		palabras = self.palabras_txt.get("1.0", "end-1c")
		acepta_stack_vacio = self.stack_vacio.get()

		print("Alfabeto:", alfabeto)
		print("Transiciones:", transiciones)
		print("Estado inicial:", estado_inicial)
		print("Estado final:", estado_final)
		print("Palabras:", palabras)
		print("Acepta por stack vacío:", acepta_stack_vacio)

		self.resultado_lbl.config(text="Datos capturados. (Aquí mostrarías si acepta o no)")

# Ejecutar GUI
Gui()
