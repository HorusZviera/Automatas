import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class APDSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulador de Autómata Pushdown Determinista")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables del APD
        self.transitions = {}
        self.initial_state = ""
        self.accept_by_empty_stack = True
        self.final_states = set()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = tk.Label(main_frame, text="Simulador de Autómata Pushdown Determinista", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame para configuración del APD
        config_frame = ttk.LabelFrame(main_frame, text="Configuración del APD", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 1. Transiciones
        ttk.Label(config_frame, text="1. Transiciones (formato: estado_origen,símbolo_entrada,símbolo_pila → estado_destino,símbolos_push):").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Área de texto para transiciones con scroll
        self.transitions_text = scrolledtext.ScrolledText(config_frame, height=8, width=80)
        self.transitions_text.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Ejemplo de transiciones
        example_transitions = """q0,a,Z → q0,aZ
q0,a,a → q0,aa
q0,b,a → q1,ε
q1,b,a → q1,ε
q1,ε,Z → q2,Z"""
        self.transitions_text.insert(tk.END, example_transitions)
        
        # 2. Estado inicial
        ttk.Label(config_frame, text="2. Estado inicial:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.initial_state_entry = ttk.Entry(config_frame, width=20)
        self.initial_state_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        self.initial_state_entry.insert(0, "q0")
        
        # 3. Tipo de aceptación
        ttk.Label(config_frame, text="3. Tipo de aceptación:").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        self.accept_type = tk.StringVar(value="empty_stack")
        
        accept_frame = ttk.Frame(config_frame)
        accept_frame.grid(row=3, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Radiobutton(accept_frame, text="Por pila vacía", variable=self.accept_type, 
                       value="empty_stack", command=self.toggle_final_states).pack(side=tk.LEFT)
        ttk.Radiobutton(accept_frame, text="Por estado final", variable=self.accept_type, 
                       value="final_state", command=self.toggle_final_states).pack(side=tk.LEFT, padx=(10, 0))
        
        # 4. Estados finales (solo si acepta por estado final)
        self.final_states_label = ttk.Label(config_frame, text="4. Estados finales (separados por coma):")
        self.final_states_label.grid(row=4, column=0, sticky=tk.W, pady=(10, 0))
        
        self.final_states_entry = ttk.Entry(config_frame, width=30)
        self.final_states_entry.grid(row=4, column=1, sticky=tk.W, padx=(10, 0))
        self.final_states_entry.insert(0, "q2")
        
        # Inicialmente ocultar estados finales
        self.toggle_final_states()
        
        # Botón para cargar APD
        load_button = ttk.Button(config_frame, text="Cargar APD", command=self.load_apd)
        load_button.grid(row=5, column=0, columnspan=2, pady=(15, 0))
        
        # Separador
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        # Frame para simulación
        sim_frame = ttk.LabelFrame(main_frame, text="Simulación", padding="10")
        sim_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 5. Palabra de entrada
        ttk.Label(sim_frame, text="5. Palabra de entrada:").grid(row=0, column=0, sticky=tk.W)
        self.input_word_entry = ttk.Entry(sim_frame, width=30, font=("Courier", 12))
        self.input_word_entry.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        self.input_word_entry.insert(0, "aabb")
        
        # Botón para simular
        simulate_button = ttk.Button(sim_frame, text="Simular", command=self.simulate)
        simulate_button.grid(row=0, column=2, padx=(10, 0))
        
        # Área de resultados
        result_frame = ttk.LabelFrame(main_frame, text="Resultado", padding="10")
        result_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=10, width=80, 
                                                    font=("Courier", 10))
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar redimensionamiento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # Instrucciones iniciales
        self.show_instructions()
        
    def show_instructions(self):
        instructions = """INSTRUCCIONES DE USO:

1. TRANSICIONES: Ingrese las transiciones en el formato:
   estado_origen,símbolo_entrada,símbolo_pila → estado_destino,símbolos_push
   
   - Use 'ε' para epsilon (cadena vacía)
   - Use 'Z' para el símbolo inicial de la pila
   - Ejemplo: q0,a,Z → q0,aZ (lee 'a', con 'Z' en la pila, va a q0 y apila 'aZ')

2. ESTADO INICIAL: El estado donde comienza la ejecución (ej: q0)

3. TIPO DE ACEPTACIÓN:
   - Por pila vacía: acepta cuando la pila está vacía
   - Por estado final: acepta cuando llega a un estado final

4. ESTADOS FINALES: Solo si acepta por estado final (ej: q1,q2)

5. PALABRA DE ENTRADA: La cadena a procesar (ej: aabb)

Ejemplo cargado: APD que acepta el lenguaje {a^n b^n | n ≥ 1}
"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, instructions)
        
    def toggle_final_states(self):
        if self.accept_type.get() == "final_state":
            self.final_states_label.grid()
            self.final_states_entry.grid()
        else:
            self.final_states_label.grid_remove()
            self.final_states_entry.grid_remove()
            
    def parse_transitions(self, text):
        """Parsea las transiciones desde el texto"""
        transitions = {}
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            try:
                # Separar por la flecha 
                left, right = line.split('→')
                left = left.strip()
                right = right.strip()
                
                # Parsear lado izquierdo (estado,input,stack)
                parts = left.split(',')
                if len(parts) != 3:
                    raise ValueError(f"Formato incorrecto en: {line}")
                
                state, input_symbol, stack_symbol = [p.strip() for p in parts]
                
                # Parsear lado derecho (next_state,push_symbols)
                right_parts = right.split(',', 1)
                if len(right_parts) != 2:
                    raise ValueError(f"Formato incorrecto en: {line}")
                
                next_state, push_symbols = [p.strip() for p in right_parts]
                
                # Convertir epsilon
                if input_symbol == 'ε':
                    input_symbol = ''
                if stack_symbol == 'ε':
                    stack_symbol = ''
                if push_symbols == 'ε':
                    push_symbols = ''
                
                key = (state, input_symbol, stack_symbol)
                transitions[key] = (next_state, push_symbols)
                
            except Exception as e:
                raise ValueError(f"Error en línea '{line}': {str(e)}")
        
        return transitions
    
    # Esta funcion carga la configuración del APD desde los campos de entrada
    def load_apd(self):
        """Carga la configuración del APD"""
        try:
            # Parsear transiciones
            transitions_text = self.transitions_text.get(1.0, tk.END)
            self.transitions = self.parse_transitions(transitions_text)
            
            # Estado inicial
            self.initial_state = self.initial_state_entry.get().strip()
            if not self.initial_state:
                raise ValueError("El estado inicial no puede estar vacío")
            
            # Tipo de aceptación
            self.accept_by_empty_stack = (self.accept_type.get() == "empty_stack")
            
            # Estados finales
            if not self.accept_by_empty_stack:
                final_states_text = self.final_states_entry.get().strip()
                if not final_states_text:
                    raise ValueError("Debe especificar estados finales")
                self.final_states = set([s.strip() for s in final_states_text.split(',')])
            else:
                self.final_states = set()
            
            # Mostrar confirmación
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "✓ APD cargado exitosamente\n\n")
            self.result_text.insert(tk.END, f"Estado inicial: {self.initial_state}\n")
            self.result_text.insert(tk.END, f"Acepta por: {'pila vacía' if self.accept_by_empty_stack else 'estado final'}\n")
            if not self.accept_by_empty_stack:
                self.result_text.insert(tk.END, f"Estados finales: {', '.join(self.final_states)}\n")
            self.result_text.insert(tk.END, f"Transiciones cargadas: {len(self.transitions)}\n\n")
            self.result_text.insert(tk.END, "Ahora puede ingresar palabras para simular.\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar APD: {str(e)}")
    
    # Funcion que simula el APD con la palabra de entrada
    def simulate(self):
        """Simula el APD con la palabra de entrada"""
        if not self.transitions:
            messagebox.showwarning("Advertencia", "Primero debe cargar un APD")
            return
        
        input_word = self.input_word_entry.get()
        
        # Inicializar estado de la simulación
        current_state = self.initial_state
        stack = ['Z']  # Pila inicial con símbolo Z
        input_index = 0
        steps = []
        
        # Registro del paso inicial
        steps.append({
            'step': 0,
            'state': current_state,
            'input_remaining': input_word,
            'stack': stack.copy(),
            'action': 'Estado inicial'
        })
        
        step_count = 0
        max_steps = 1000
        
        while step_count < max_steps:
            step_count += 1
            
            # Verificar condiciones de aceptación
            if self.accept_by_empty_stack and len(stack) == 0:
                steps.append({
                    'step': step_count,
                    'state': current_state,
                    'input_remaining': input_word[input_index:],
                    'stack': stack.copy(),
                    'action': '¡ACEPTADO! (Pila vacía)'
                })
                break
            
            if not self.accept_by_empty_stack and current_state in self.final_states and input_index == len(input_word):
                steps.append({
                    'step': step_count,
                    'state': current_state,
                    'input_remaining': '',
                    'stack': stack.copy(),
                    'action': '¡ACEPTADO! (Estado final)'
                })
                break
            
            # Buscar transición aplicable
            transition_found = False
            
            # Intentar transición con símbolo de entrada
            if input_index < len(input_word):
                input_symbol = input_word[input_index]
                stack_top = stack[-1] if stack else ''
                
                key = (current_state, input_symbol, stack_top)
                if key in self.transitions:
                    next_state, push_symbols = self.transitions[key]
                    
                    # Aplicar transición
                    if stack:
                        stack.pop()  # Quitar símbolo de la pila
                    
                    # Apilar nuevos símbolos (de derecha a izquierda)
                    if push_symbols:
                        for symbol in reversed(push_symbols):
                            stack.append(symbol)
                    
                    input_index += 1
                    current_state = next_state
                    transition_found = True
                    
                    steps.append({
                        'step': step_count,
                        'state': current_state,
                        'input_remaining': input_word[input_index:],
                        'stack': stack.copy(),
                        'action': f'Transición: lee "{input_symbol}", apila "{push_symbols if push_symbols else "ε"}"'
                    })
            
            # Si no hay transición con símbolo, intentar transición epsilon
            if not transition_found:
                stack_top = stack[-1] if stack else ''
                
                key = (current_state, '', stack_top)
                if key in self.transitions:
                    next_state, push_symbols = self.transitions[key]
                    
                    # Aplicar transición epsilon
                    if stack:
                        stack.pop()
                    
                    if push_symbols:
                        for symbol in reversed(push_symbols):
                            stack.append(symbol)
                    
                    current_state = next_state
                    transition_found = True
                    
                    steps.append({
                        'step': step_count,
                        'state': current_state,
                        'input_remaining': input_word[input_index:],
                        'stack': stack.copy(),
                        'action': f'Transición ε: apila "{push_symbols if push_symbols else "ε"}"'
                    })
            
            # Si no se encontró transición, terminar
            if not transition_found:
                steps.append({
                    'step': step_count,
                    'state': current_state,
                    'input_remaining': input_word[input_index:],
                    'stack': stack.copy(),
                    'action': 'RECHAZADO (No hay transición aplicable)'
                })
                break
        
        # Verificar si se agotaron los pasos
        if step_count >= max_steps:
            steps.append({
                'step': step_count,
                'state': current_state,
                'input_remaining': input_word[input_index:],
                'stack': stack.copy(),
                'action': 'RECHAZADO (Demasiados pasos - posible bucle)'
            })
        self.display_results(input_word, steps)
    

    # Esta funcion muestra los resultados de la simulación en el área de texto final
    def display_results(self, input_word, steps):
        """Muestra los resultados de la simulación"""
        self.result_text.delete(1.0, tk.END)
        
        final_step = steps[-1]
        accepted = 'ACEPTADO' in final_step['action']
        
        self.result_text.insert(tk.END, f"SIMULACIÓN DE LA PALABRA: '{input_word}'\n")
        self.result_text.insert(tk.END, "=" * 60 + "\n\n")
        
        result_text = "✓ PALABRA ACEPTADA" if accepted else "✗ PALABRA RECHAZADA"
        self.result_text.insert(tk.END, f"RESULTADO: {result_text}\n\n")
        
        self.result_text.insert(tk.END, "PASOS DE LA SIMULACIÓN:\n")
        self.result_text.insert(tk.END, "-" * 60 + "\n")
        
        for step in steps:
            stack_str = ''.join(reversed(step['stack'])) if step['stack'] else '∅'
            self.result_text.insert(tk.END, 
                f"Paso {step['step']:2d}: Estado={step['state']:4s} | "
                f"Entrada restante='{step['input_remaining']:10s}' | "
                f"Pila={stack_str:10s} | {step['action']}\n")
        
        self.result_text.insert(tk.END, "\n" + "=" * 60 + "\n")
        self.result_text.insert(tk.END, f"RESULTADO FINAL: {result_text}\n")
        
        self.result_text.see(tk.END)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    simulator = APDSimulator()
    simulator.run()