from collections import deque
import matplotlib.pyplot as plt

def graficar_gantt_progresivo_en_ventana(gantt_chart, num_cpus, fig, ax, procesos_por_ventana, ventana_actual):
    """
    Función para generar el diagrama de Gantt de manera progresiva, con límite de procesos por ventana.
    """
    ax.clear()
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']
    gantt_chart_filtrado = gantt_chart[
                           ventana_actual * procesos_por_ventana: (ventana_actual + 1) * procesos_por_ventana]

    for (time, pid, cpu) in gantt_chart_filtrado:
        ax.broken_barh([(time, 1)], (cpu * 10, 9), facecolors=colors[int(pid) % len(colors)])
        ax.text(time + 0.5, cpu * 10 + 4.5, f"{pid}", color='white', ha='center', va='center', fontsize=8)

    ax.set_xlabel("Tiempo")
    ax.set_ylabel("CPU")
    ax.set_yticks([i * 10 + 4.5 for i in range(num_cpus)])
    ax.set_yticklabels([f"CPU {i}" for i in range(num_cpus)])
    ax.grid(True)
    plt.title(f"Diagrama de Gantt - Shortest Job First (Ventana {ventana_actual + 1})")
    fig.canvas.draw()
    plt.pause(0.1)

def simulador_sjf(procesos, quantum ,num_cpus):
    """
    Simulador para el algoritmo Shortest Job First (SJF).
    """
    tiempo_actual = 0
    cola = []
    finalizados = []
    indice_procesos = 0
    n = len(procesos)
    cpus = [None] * num_cpus

    gantt_chart = []
    fig, ax = plt.subplots(figsize=(10, 6))
    procesos_por_ventana = 200
    ventana_actual = 0

    while len(finalizados) < n or any(cpus) or cola:
        while indice_procesos < n and procesos[indice_procesos].tiempo_llegada <= tiempo_actual:
            cola.append(procesos[indice_procesos])
            indice_procesos += 1

        # Ordenar la cola por tiempo de ejecución restante
        cola.sort(key=lambda p: p.tiempo_restante)

        for i in range(num_cpus):
            if cpus[i]:
                cpus[i].tiempo_restante -= 1
                gantt_chart.append((tiempo_actual, cpus[i].pid, i))

                if cpus[i].tiempo_restante == 0:
                    cpus[i].tiempo_finalizacion = tiempo_actual + 1
                    cpus[i].tiempo_espera = cpus[i].tiempo_finalizacion - cpus[i].tiempo_llegada - cpus[i].tiempo_ejecucion
                    finalizados.append(cpus[i])
                    cpus[i] = None

        for i in range(num_cpus):
            if cpus[i] is None and cola:
                proceso = cola.pop(0)
                cpus[i] = proceso
                if proceso.tiempo_respuesta == -1:
                    proceso.tiempo_respuesta = tiempo_actual - proceso.tiempo_llegada

        if len(gantt_chart) > (ventana_actual + 1) * procesos_por_ventana:
            ventana_actual += 1
            fig, ax = plt.subplots(figsize=(10, 6))

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
