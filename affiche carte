import matplotlib.pyplot as plt

execution_times = []
with open("execution_times.txt", "r") as file:
    for line in file:
        execution_times.append(float(line.strip()))

plt.plot(range(1, len(execution_times) + 1), execution_times, marker='+')
plt.xlabel('Exécution')
plt.ylabel('Temps d\'exécution (secondes)')
plt.title('Évolution des temps d\'exécution')
plt.grid(True)
plt.show()
