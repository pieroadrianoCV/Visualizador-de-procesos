from collections import deque
import matplotlib.pyplot as plt

# Función para simular Round Robin con avance unitario
def simulador_round_robin_smp_unitario(procesos, quantum, num_cpus):
    tiempo_actual = 0
    cola = deque()  # Cola de procesos listos
    finalizados = []  # Procesos terminados
    indice_procesos = 0
    #n = len(procesos)
    n = 4
    # Inicializar CPUs con estado ocioso
    cpus = [None] * num_cpus  # Cada CPU ejecuta un proceso o está ociosa
    tiempo_restante_cpu = [0] * num_cpus  # Tiempo restante de ejecución en cada CPU

    while len(finalizados) < n or any(cpus) or cola:
        # Agregar a la cola los procesos que llegan al tiempo actual
        while indice_procesos < n and procesos[indice_procesos].tiempo_llegada <= tiempo_actual:
            cola.append(procesos[indice_procesos])
            indice_procesos += 1

        # Actualizar estado de las CPUs
        for i in range(num_cpus):
            if cpus[i]:
                # Reducir el tiempo restante del proceso en la CPU
                tiempo_restante_cpu[i] -= 1
                cpus[i].tiempo_restante -= 1

                # Verificar si el proceso terminó
                if cpus[i].tiempo_restante == 0:
                    cpus[i].tiempo_finalizacion = tiempo_actual
                    cpus[i].tiempo_espera = cpus[i].tiempo_finalizacion - cpus[i].tiempo_llegada - cpus[i].tiempo_ejecucion
                    finalizados.append(cpus[i])
                    cpus[i] = None  # Liberar la CPU
                elif tiempo_restante_cpu[i] == 0:
                    # Si el quantum se agotó, devolver el proceso a la cola
                    cola.append(cpus[i])
                    cpus[i] = None

        # Asignar procesos disponibles a CPUs ociosas
        for i in range(num_cpus):
            if cpus[i] is None and cola:
                proceso = cola.popleft()
                cpus[i] = proceso
                tiempo_restante_cpu[i] = min(quantum, proceso.tiempo_restante)

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
    print(f"{'Proceso':<10}{'Nombre':<40}{'Llegada':<10}{'Ejecución':<10}{'Finalización':<15}{'Espera':<10}{'Respuesta':<10}")
    for p in finalizados:
        print(f"{p.pid:<10}{p.nombre:<40}{p.tiempo_llegada:<10}{p.tiempo_ejecucion:<10}{p.tiempo_finalizacion:<15}{p.tiempo_espera:<10}{p.tiempo_respuesta:<10}")

    print(f"\nTiempo de espera promedio: {tiempo_espera_promedio:.2f}")
    print(f"Tiempo de respuesta promedio: {tiempo_respuesta_promedio:.2f}")

def simulador(procesos, quantum, num_cpus):
    tiempo_actual = 0
    cola = deque()  # Cola de procesos listos
    finalizados = []  # Procesos terminados
    indice_procesos = 0
    #n = len(procesos)
    n = 4
    # Inicializar CPUs con estado ocioso
    cpus = [None] * num_cpus  # Cada CPU ejecuta un proceso o está ociosa
    tiempo_restante_cpu = [0] * num_cpus  # Tiempo restante de ejecución en cada CPU

    # Para visualizar la ejecución
    gantt_chart = []

    while len(finalizados) < n or any(cpus) or cola:
        # Agregar a la cola los procesos que llegan al tiempo actual
        while indice_procesos < n and procesos[indice_procesos].tiempo_llegada <= tiempo_actual:
            cola.append(procesos[indice_procesos])
            indice_procesos += 1

        # Actualizar estado de las CPUs
        for i in range(num_cpus):
            if cpus[i]:
                # Reducir el tiempo restante del proceso en la CPU
                tiempo_restante_cpu[i] -= 1
                cpus[i].tiempo_restante -= 1

                # Registrar en el diagrama de Gantt
                gantt_chart.append((tiempo_actual, cpus[i].pid, i))

                # Verificar si el proceso terminó
                if cpus[i].tiempo_restante == 0:
                    cpus[i].tiempo_finalizacion = tiempo_actual
                    cpus[i].tiempo_espera = cpus[i].tiempo_finalizacion - cpus[i].tiempo_llegada - cpus[
                        i].tiempo_ejecucion
                    finalizados.append(cpus[i])
                    cpus[i] = None  # Liberar la CPU
                elif tiempo_restante_cpu[i] == 0:
                    # Si el quantum se agotó, devolver el proceso a la cola
                    cola.append(cpus[i])
                    cpus[i] = None

        # Asignar procesos disponibles a CPUs ociosas
        for i in range(num_cpus):
            if cpus[i] is None and cola:
                proceso = cola.popleft()
                cpus[i] = proceso
                tiempo_restante_cpu[i] = min(quantum, proceso.tiempo_restante)

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
    print(
        f"{'Proceso':<10}{'Nombre':<40}{'Llegada':<10}{'Ejecución':<10}{'Finalización':<15}{'Espera':<10}{'Respuesta':<10}")
    for p in finalizados:
        print(
            f"{p.pid:<10}{p.nombre:<40}{p.tiempo_llegada:<10}{p.tiempo_ejecucion:<10}{p.tiempo_finalizacion:<15}{p.tiempo_espera:<10}{p.tiempo_respuesta:<10}")

    print(f"\nTiempo de espera promedio: {tiempo_espera_promedio:.2f}")
    print(f"Tiempo de respuesta promedio: {tiempo_respuesta_promedio:.2f}")

    # Dibujar el diagrama de Gantt
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']

    for (time, pid, cpu) in gantt_chart:
        ax.broken_barh([(time, 1)], (cpu * 10, 9), facecolors=colors[int(pid) % len(colors)])

    ax.set_xlabel("Tiempo")
    ax.set_ylabel("CPU")
    ax.set_yticks([i * 10 + 4.5 for i in range(num_cpus)])
    ax.set_yticklabels([f"CPU {i}" for i in range(num_cpus)])
    ax.grid(True)
    plt.title("Diagrama de Gantt - Round Robin SMP")
    plt.show()
