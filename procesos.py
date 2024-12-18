import os
import random


class Proceso:
    def __init__(self, pid, nombre, estado, prioridad, tiempo_llegada, tiempo_ejecucion):
        self.pid = pid
        self.nombre = nombre
        self.estado = estado
        self.prioridad = int(prioridad)
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_ejecucion = tiempo_ejecucion
        self.tiempo_restante = tiempo_ejecucion
        self.tiempo_finalizacion = 0
        self.tiempo_espera = 0
        self.tiempo_respuesta = -1

    def __str__(self):
        return f"PID: {self.pid}, Nombre: {self.nombre}, Estado: {self.estado}, Prioridad: {self.prioridad}"


def obtener_procesos():
    procesos = []
    proc_dir = "/proc"
    tiempo_llegada = 0

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

                tiempo_llegada += random.randint(0, 3)
                tiempo_ejecucion = random.randint(1, 20)

                procesos.append(Proceso(pid, nombre, estado, prioridad, tiempo_llegada, tiempo_ejecucion))
            except FileNotFoundError:
                continue

    return procesos


def eliminar_proceso(procesos, pid):
    for proceso in procesos:
        if proceso.pid == pid:
            procesos.remove(proceso)
            return True
    return False


def agregar_proceso(procesos, pid, nombre, estado, prioridad, tiempo_llegada, tiempo_ejecucion):
    nuevo_proceso = Proceso(pid, nombre, estado, prioridad, tiempo_llegada, tiempo_ejecucion)
    procesos.append(nuevo_proceso)
