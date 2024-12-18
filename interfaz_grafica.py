import tkinter as tk
from tkinter import ttk, messagebox
from procesos import obtener_procesos, agregar_proceso, eliminar_proceso


class ProcesoGUI:
    def __init__(self, simulador_func, quantum, num_cpus):
        self.simulador = simulador_func
        self.quantum = quantum
        self.num_cpus = num_cpus
        self.procesos = obtener_procesos()

        self.root = tk.Tk()
        self.root.title("Simulador de Planificación de CPU")
        self.setup_gui()

    def setup_gui(self):
        # Frame principal
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Tabla de procesos
        self.tree = ttk.Treeview(frame, columns=("PID", "Nombre", "Prioridad", "Llegada", "Ejecución"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.update_tree()

        # Controles
        controls = tk.Frame(frame)
        controls.pack(pady=10)

        # Entradas para agregar procesos
        tk.Label(controls, text="PID:").grid(row=0, column=0, padx=5)
        self.pid_entry = tk.Entry(controls)
        self.pid_entry.grid(row=0, column=1)

        tk.Label(controls, text="Nombre:").grid(row=1, column=0, padx=5)
        self.nombre_entry = tk.Entry(controls)
        self.nombre_entry.grid(row=1, column=1)

        tk.Label(controls, text="Prioridad:").grid(row=2, column=0, padx=5)
        self.prioridad_entry = tk.Entry(controls)
        self.prioridad_entry.grid(row=2, column=1)

        tk.Label(controls, text="Tiempo Llegada:").grid(row=3, column=0, padx=5)
        self.llegada_entry = tk.Entry(controls)
        self.llegada_entry.grid(row=3, column=1)

        tk.Label(controls, text="Tiempo Ejecución:").grid(row=4, column=0, padx=5)
        self.ejecucion_entry = tk.Entry(controls)
        self.ejecucion_entry.grid(row=4, column=1)

        # Botones para agregar y eliminar procesos
        tk.Button(controls, text="Agregar", command=self.add_proceso).grid(row=5, column=0, pady=5)
        tk.Button(controls, text="Eliminar por PID", command=self.delete_proceso).grid(row=5, column=1, pady=5)

        # Botón de simulación
        tk.Button(frame, text="Ejecutar Simulación", command=self.run_simulation).pack(pady=10)

    def update_tree(self):
        """
        Actualiza la tabla de procesos con la lista actual de procesos.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        for proceso in self.procesos:
            self.tree.insert("", "end", values=(proceso.pid, proceso.nombre, proceso.prioridad, proceso.tiempo_llegada, proceso.tiempo_ejecucion))

    def add_proceso(self):
        """
        Agrega un proceso a la lista basado en los valores ingresados por el usuario.
        """
        try:
            pid = int(self.pid_entry.get())
            nombre = self.nombre_entry.get()
            prioridad = int(self.prioridad_entry.get())
            tiempo_llegada = int(self.llegada_entry.get())
            tiempo_ejecucion = int(self.ejecucion_entry.get())

            # Agregar proceso a la lista
            agregar_proceso(self.procesos, pid, nombre, "Nuevo", prioridad, tiempo_llegada, tiempo_ejecucion)
            # Reordenar la lista de procesos por PID
            self.procesos.sort(key=lambda p: int(p.pid))

            self.update_tree()

            # Limpiar entradas
            self.pid_entry.delete(0, tk.END)
            self.nombre_entry.delete(0, tk.END)
            self.prioridad_entry.delete(0, tk.END)
            self.llegada_entry.delete(0, tk.END)
            self.ejecucion_entry.delete(0, tk.END)

            messagebox.showinfo("Proceso Agregado", f"Proceso con PID {pid} agregado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese datos válidos.")

    def delete_proceso(self):
        """
        Elimina un proceso de la lista basado en el PID ingresado.
        """
        try:
            pid = self.pid_entry.get()
            if eliminar_proceso(self.procesos, pid):
                self.update_tree()
                messagebox.showinfo("Proceso Eliminado", f"Proceso con PID {pid} eliminado correctamente.")
            else:
                messagebox.showerror("Error", f"No se encontró un proceso con PID {pid}.")

            # Limpiar entrada de PID
            self.pid_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un PID válido.")

    def run_simulation(self):
        """
        Ejecuta la simulación con los procesos actuales, quantum y número de CPUs.
        """
        self.simulador(self.procesos, self.quantum, self.num_cpus)
        messagebox.showinfo("Simulación Completa", "La simulación se ejecutó correctamente.")

    def run(self):
        """
        Inicia la interfaz gráfica.
        """
        self.root.mainloop()

