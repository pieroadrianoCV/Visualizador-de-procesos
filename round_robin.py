from collections import deque
import matplotlib.pyplot as plt


def graficar_gantt_progresivo_en_ventana(gantt_chart, num_cpus, fig, ax, procesos_por_ventana, ventana_actual):
    """
    Función para generar el diagrama de Gantt de manera progresiva, con límite de procesos por ventana.

    Args:
        gantt_chart (list): Lista de tuplas con formato (time, pid, cpu) que representa la ejecución de los procesos.
        num_cpus (int): Número de CPUs disponibles.
        fig (Figure): Figura de matplotlib que contiene el gráfico.
        ax (Axes): Ejes de matplotlib para el gráfico.
        procesos_por_ventana (int): Número máximo de procesos por ventana.
        ventana_actual (int): Número de la ventana actual.
    """
    # Limpiar los ejes para actualizar la gráfica
    ax.clear()
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']

    # Dibujar el gráfico con un límite de procesos
    gantt_chart_filtrado = gantt_chart[
                           ventana_actual * procesos_por_ventana: (ventana_actual + 1) * procesos_por_ventana]

    for (time, pid, cpu) in gantt_chart_filtrado:
        ax.broken_barh([(time, 1)], (cpu * 10, 9), facecolors=colors[int(pid) % len(colors)])
        ax.text(time + 0.5, cpu * 10 + 4.5, f"{pid}", color='white', ha='center', va='center', fontsize=8)

    # Configurar etiquetas y detalles del gráfico
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("CPU")
    ax.set_yticks([i * 10 + 4.5 for i in range(num_cpus)])
    ax.set_yticklabels([f"CPU {i}" for i in range(num_cpus)])
    ax.grid(True)
    plt.title(f"Diagrama de Gantt - Round Robin SMP (Ventana {ventana_actual + 1})")

    # Dibujar el gráfico
    fig.canvas.draw()
    plt.pause(0.1)  # Pausa para que la animación sea visible

def simulador(procesos, quantum, num_cpus):
    tiempo_actual = 0
    cola = deque()
    finalizados = []
    indice_procesos = 0
    n = len(procesos)
    cpus = [None] * num_cpus
    tiempo_restante_cpu = [0] * num_cpus

    gantt_chart = []
    fig, ax = plt.subplots(figsize=(10, 6))

    # Número máximo de procesos por ventana (según altura mínima de 5 mm por barra)
    procesos_por_ventana = 200
    ventana_actual = 0

    while len(finalizados) < n or any(cpus) or cola:
        while indice_procesos < n and procesos[indice_procesos].tiempo_llegada <= tiempo_actual:
            cola.append(procesos[indice_procesos])
            indice_procesos += 1

        for i in range(num_cpus):
            if cpus[i]:
                tiempo_restante_cpu[i] -= 1
                cpus[i].tiempo_restante -= 1

                gantt_chart.append((tiempo_actual - 1, cpus[i].pid, i))

                if cpus[i].tiempo_restante == 0:
                    cpus[i].tiempo_finalizacion = tiempo_actual
                    cpus[i].tiempo_espera = cpus[i].tiempo_finalizacion - cpus[i].tiempo_llegada - cpus[i].tiempo_ejecucion
                    finalizados.append(cpus[i])
                    cpus[i] = None
                elif tiempo_restante_cpu[i] == 0:
                    cola.append(cpus[i])
                    cpus[i] = None

        for i in range(num_cpus):
            if cpus[i] is None and cola:
                proceso = cola.popleft()
                cpus[i] = proceso
                tiempo_restante_cpu[i] = min(quantum, proceso.tiempo_restante)
                if proceso.tiempo_respuesta == -1:
                    proceso.tiempo_respuesta = tiempo_actual - proceso.tiempo_llegada

        # Controlar cuántos procesos se han graficado en la ventana actual
        if len(gantt_chart) > (ventana_actual + 1) * procesos_por_ventana:
            ventana_actual += 1
            fig, ax = plt.subplots(figsize=(10, 6))  # Crear una nueva ventana

        graficar_gantt_progresivo_en_ventana(gantt_chart, num_cpus, fig, ax, procesos_por_ventana, ventana_actual)
        tiempo_actual += 1

    total_espera = sum(p.tiempo_espera for p in finalizados)
    total_respuesta = sum(p.tiempo_respuesta for p in finalizados)
    tiempo_espera_promedio = total_espera / n
    tiempo_respuesta_promedio = total_respuesta / n

    finalizados.sort(key=lambda proceso: int(proceso.pid))
    print("\nResultados de la simulación:")
    print(
        f"{'Proceso':<10}{'Nombre':<40}{'Llegada':<10}{'Ejecución':<10}{'Finalización':<15}{'Espera':<10}{'Respuesta':<10}")
    for p in finalizados:
        print(
            f"{p.pid:<10}{p.nombre:<40}{p.tiempo_llegada:<10}{p.tiempo_ejecucion:<10}{p.tiempo_finalizacion:<15}{p.tiempo_espera:<10}{p.tiempo_respuesta:<10}")

    print(f"\nTiempo de espera promedio: {tiempo_espera_promedio:.2f}")
    print(f"Tiempo de respuesta promedio: {tiempo_respuesta_promedio:.2f}")

    plt.show()
