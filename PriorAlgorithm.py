from collections import deque
from processos import *
import matplotlib.pyplot as plt

def simulador_prioridad_smp(procesos, num_cpus):
  tiempo_actual = 0
  cola = []  # Cola de procesos listos, ordenada por prioridad
  finalizados = []  # Procesos terminados
  indice_procesos = 0
  n = len(procesos)

  # Inicializar CPUs con estado ocioso
  cpus = [None] * num_cpus  # Cada CPU ejecuta un proceso o está ociosa

  while len(finalizados) < n or any(cpus) or cola:
    # Agregar a la cola los procesos que llegan al tiempo actual
    while indice_procesos < n and procesos[indice_procesos].tiempo_llegada <= tiempo_actual:
      cola.append(procesos[indice_procesos])
      # Ordenar la cola por prioridad (mayor prioridad primero)
      cola.sort(key=lambda p: (-p.prioridad, p.tiempo_llegada))  # -p.prioridad: Mayor prioridad tiene menor valor
      indice_procesos += 1

      # Actualizar estado de las CPUs
    for i in range(num_cpus):
      if cpus[i]:
        cpus[i].tiempo_restante -= 1
        # Verificar si el proceso terminó
        if cpus[i].tiempo_restante == 0:
          cpus[i].tiempo_finalizacion = tiempo_actual
          cpus[i].tiempo_espera = cpus[i].tiempo_finalizacion - cpus[i].tiempo_llegada - cpus[i].tiempo_ejecucion
          finalizados.append(cpus[i])
          cpus[i] = None  # Liberar la CPU

    # Asignar procesos disponibles a CPUs ociosas
    for i in range(num_cpus):
      if cpus[i] is None and cola:
        proceso = cola.pop(0)  # Seleccionar el proceso con mayor prioridad
        cpus[i] = proceso

        # Registrar el tiempo de respuesta si no ha sido atendido
        if proceso.tiempo_respuesta == -1:
          proceso.tiempo_respuesta = tiempo_actual - proceso.tiempo_llegada

    # Avanzar el tiempo una unidad
    tiempo_actual += 1

    # Calcular resultados globales
  total_espera = sum(p.tiempo_espera for p in finalizados)
  total_respuesta = sum(p.tiempo_respuesta for p in finalizados)
  tiempo_espera_promedio = total_espera / n
  tiempo_respuesta_promedio = total_respuesta / n

  # Mostrar resultados
  finalizados.sort(key=lambda proceso: int(proceso.pid))
  print("\nResultados de la simulación:")
  print(f"{'Proceso':<10}{'Nombre':<40}{'Llegada':<10}{'Ejecución':<10}{'Prioridad':<10}{'Finalización':<15}{'Espera':<10}{'Respuesta':<10}")
  for p in finalizados:
    print(f"{p.pid:<10}{p.nombre:<40}{p.tiempo_llegada:<10}{p.tiempo_ejecucion:<10}{p.prioridad:<10}{p.tiempo_finalizacion:<15}{p.tiempo_espera:<10}{p.tiempo_respuesta:<10}")

  print(f"\nTiempo de espera promedio: {tiempo_espera_promedio:.2f}")
  print(f"Tiempo de respuesta promedio: {tiempo_respuesta_promedio:.2f}")

def graficar_gantt_progresivo_en_ventana(gantt_chart, num_cpus, fig, ax):
    """
    Función para generar el diagrama de Gantt de manera progresiva en una sola ventana.

    Args:
        gantt_chart (list): Lista de tuplas con formato (time, pid, cpu) que representa la ejecución de los procesos.
        num_cpus (int): Número de CPUs disponibles.
        fig (Figure): Figura de matplotlib que contiene el gráfico.
        ax (Axes): Ejes de matplotlib para el gráfico.
    """
    ax.clear()  # Limpia los ejes para actualizar la gráfica
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']

    for (time, pid, cpu) in gantt_chart:
        # Dibujar la barra correspondiente al proceso
        ax.broken_barh([(time, 1)], (cpu * 10, 9), facecolors=colors[int(pid) % len(colors)])
        # Agregar el número de PID como texto dentro de la barra
        ax.text(time + 0.5, cpu * 10 + 4.5, f"{pid}", color='white', ha='center', va='center', fontsize=8)

    # Configurar etiquetas y detalles del gráfico
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("CPU")
    ax.set_yticks([i * 10 + 4.5 for i in range(num_cpus)])
    ax.set_yticklabels([f"CPU {i}" for i in range(num_cpus)])
    ax.grid(True)
    plt.title("Diagrama de Gantt - Prioridad SMP")

    fig.canvas.draw()  # Actualiza el gráfico en la misma ventana
    plt.pause(0.1)  # Pausa para que la animación sea visible


def simulador_prioridad(procesos, num_cpus):
    tiempo_actual = 0
    cola = []  # Cola de procesos listos, ordenada por prioridad
    finalizados = []  # Procesos terminados
    indice_procesos = 0
    n = len(procesos)

    # Inicializar CPUs con estado ocioso
    cpus = [None] * num_cpus  # Cada CPU ejecuta un proceso o está ociosa

    # Para visualizar la ejecución
    gantt_chart = []

    # Crear la figura y los ejes de matplotlib para el gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    while len(finalizados) < n or any(cpus) or cola:
        # Agregar a la cola los procesos que llegan al tiempo actual
        while indice_procesos < n and procesos[indice_procesos].tiempo_llegada <= tiempo_actual:
            cola.append(procesos[indice_procesos])
            # Ordenar la cola por prioridad (mayor prioridad primero)
            cola.sort(key=lambda p: (-p.prioridad, p.tiempo_llegada))  # -p.prioridad: Mayor prioridad tiene menor valor
            indice_procesos += 1

        # Actualizar estado de las CPUs
        for i in range(num_cpus):
            if cpus[i]:
                cpus[i].tiempo_restante -= 1

                # Registrar en el diagrama de Gantt
                gantt_chart.append((tiempo_actual - 1, cpus[i].pid, i))

                # Verificar si el proceso terminó
                if cpus[i].tiempo_restante == 0:
                    cpus[i].tiempo_finalizacion = tiempo_actual
                    cpus[i].tiempo_espera = cpus[i].tiempo_finalizacion - cpus[i].tiempo_llegada - cpus[i].tiempo_ejecucion
                    finalizados.append(cpus[i])
                    cpus[i] = None  # Liberar la CPU

        # Asignar procesos disponibles a CPUs ociosas
        for i in range(num_cpus):
            if cpus[i] is None and cola:
                proceso = cola.pop(0)  # Seleccionar el proceso con mayor prioridad
                cpus[i] = proceso

                # Registrar el tiempo de respuesta si no ha sido atendido
                if proceso.tiempo_respuesta == -1:
                    proceso.tiempo_respuesta = tiempo_actual - proceso.tiempo_llegada

        # Dibujar el Gantt progresivamente al final de cada unidad de tiempo
        graficar_gantt_progresivo_en_ventana(gantt_chart, num_cpus, fig, ax)

        # Avanzar el tiempo una unidad
        tiempo_actual += 1

    # Calcular resultados globales
    total_espera = sum(p.tiempo_espera for p in finalizados)
    total_respuesta = sum(p.tiempo_respuesta for p in finalizados)
    tiempo_espera_promedio = total_espera / n
    tiempo_respuesta_promedio = total_respuesta / n

    # Mostrar resultados
    finalizados.sort(key=lambda proceso: int(proceso.pid))
    print("\nResultados de la simulación:")
    print(
        f"{'Proceso':<10}{'Nombre':<40}{'Llegada':<10}{'Ejecución':<10}{'Prioridad':<10}{'Finalización':<15}{'Espera':<10}{'Respuesta':<10}")
    for p in finalizados:
        print(
            f"{p.pid:<10}{p.nombre:<40}{p.tiempo_llegada:<10}{p.tiempo_ejecucion:<10}{p.prioridad:<10}{p.tiempo_finalizacion:<15}{p.tiempo_espera:<10}{p.tiempo_respuesta:<10}")

    print(f"\nTiempo de espera promedio: {tiempo_espera_promedio:.2f}")
    print(f"Tiempo de respuesta promedio: {tiempo_respuesta_promedio:.2f}")

    plt.show()  # Mantener la ventana abierta al final