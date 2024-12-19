from interfaz_grafica import ProcesoGUI

if __name__ == "__main__":
    # Parámetros del simulador
    quantum = 3
    num_cpus = 4

    # Iniciar la interfaz gráfica
    gui = ProcesoGUI(quantum, num_cpus)
    gui.run()
