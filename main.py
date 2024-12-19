from procesos import obtener_procesos, agregar_proceso, eliminar_proceso
from interfaz_grafica import ProcesoGUI
from shortest_job import simulador_sjf


if __name__ == "__main__":
    quantum = 3
    num_cpus = 4

    # Inicializar la GUI
    gui = ProcesoGUI(simulador_sjf, quantum, num_cpus)
    gui.run()