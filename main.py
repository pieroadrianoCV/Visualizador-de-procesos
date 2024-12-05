import os
import random

class Proceso:
    def __init__(self, pid, nombre, estado, prioridad):
        self.pid = pid
        self.nombre = nombre
        self.estado = estado
        self.prioridad = int(prioridad)

    def __str__(self):
        return f"PID: {self.pid}, Nombre: {self.nombre}, Estado: {self.estado}, Prioridad: {self.prioridad}"

def obtener_procesos():
    procesos = []
    proc_dir = "/proc"
    
    for entry in os.listdir(proc_dir):
        if entry.isdigit():
            pid = entry
            try:
                with open(f"{proc_dir}/{pid}/comm", "r") as comm_file:
                    nombre = comm_file.readline().strip()
                
                with open(f"{proc_dir}/{pid}/stat", "r") as stat_file:
                    stat_data = stat_file.readline().split()
                    estado = stat_data[2]
                    prioridad = stat_data[17]
                
                procesos.append(Proceso(pid, nombre, estado, prioridad))
            except FileNotFoundError:
                continue
    
    return procesos

def crear_proceso_simulado(nombre=None, prioridad=None):
    pid = os.fork()

    if pid == 0:
        # Proceso hijo
        print(f"Proceso hijo creado. PID: {os.getpid()}")
        os._exit(0)

    else:
        # Proceso padre
        nombre = nombre or f"Proceso_{pid}"
        prioridad = prioridad if prioridad is not None else random.randint(1, 20)
        estado = "R" 
        return Proceso(pid, nombre, estado, prioridad)

def eliminar_proceso(lista_procesos, pid):
    proceso_a_eliminar = next((proc for proc in lista_procesos if proc.pid == pid), None)

    if proceso_a_eliminar:
        try:
            os.kill(pid, 9)
            print(f"Proceso con PID {pid} eliminado del sistema operativo.")
        except ProcessLookupError:
            print(f"El proceso con PID {pid} ya no existía en el sistema operativo.")

        lista_procesos = [proc for proc in lista_procesos if proc.pid != pid]
    else:
        print(f"No se encontró el proceso con PID {pid}.")

    return lista_procesos

#if __name__ == "__main__":
#    procesos = obtener_procesos()
#
#   for proc in procesos:
#        print(proc)

if __name__ == "__main__":
    procesos = []

    # Crear 3 procesos simulados
    for _ in range(3):
        proceso = crear_proceso_simulado()
        procesos.append(proceso)

    print("\nProcesos creados:")
    for proc in procesos:
        print(proc)

    # Eliminar el segundo proceso
    pid_a_eliminar = procesos[1].pid
    procesos = eliminar_proceso(procesos, pid_a_eliminar)

    print("\nProcesos restantes:")
    for proc in procesos:
        print(proc)

