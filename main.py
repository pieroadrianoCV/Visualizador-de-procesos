from procesos import obtener_procesos, agregar_proceso, eliminar_proceso
from interfaz_grafica import ProcesoGUI
from round_robin import simulador


if __name__ == "__main__":
    quantum = 3
    num_cpus = 4

    # Inicializar la GUI
    gui = ProcesoGUI(simulador, quantum, num_cpus)
    gui.run()