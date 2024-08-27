import numpy as np
import matplotlib.pyplot as plt

def f(x, v):
    return -k * x / m - c * v / m

def metodo_euler(x0, v0, f, dt, tf):
    xTiempo = np.arange(0, tf + dt, dt)
    xValue = np.zeros(len(xTiempo))
    xValue[0] = x0
    vValue = np.zeros(len(xTiempo))
    vValue[0] = v0
    for i in range(1, len(xTiempo)):
        xValue[i] = xValue[i - 1] + vValue[i - 1] * dt
        vValue[i] = vValue[i - 1] + f(xValue[i - 1], vValue[i - 1]) * dt + (sigma / m) * np.sqrt(dt) * np.random.normal(0, 1)
    return xTiempo, xValue, vValue

# Parámetros del sistema
m = 1.0  # Masa del oscilador
c = 0.5  # Coeficiente de amortiguamiento
k = 1.0  # Constante del resorte
sigma = 2  # Desviación estándar del ruido blanco

# Condiciones iniciales
x0 = 0.0  # Posición inicial
v0 = 1.0  # Velocidad inicial

# Parámetros de integración
dt = 0.01  # Paso de tiempo
tf = 60.0  # Tiempo final

# Número de trayectorias a generar
num_trayectorias = 4

# Generar y graficar las trayectorias
plt.figure()

# Trayectorias de posición
plt.subplot(2, 1, 1)
for i in range(num_trayectorias):
    xTiempo, xValue, vValue = metodo_euler(x0, v0, f, dt, tf)
    plt.plot(xTiempo, xValue, label=f'Trayectoria {i+1}')
plt.xlabel('Tiempo')
plt.ylabel('Posición')
plt.title('Trayectorias de Posición')
plt.legend()

# Trayectorias de velocidad
plt.subplot(2, 1, 2)
for i in range(num_trayectorias):
    xTiempo, xValue, vValue = metodo_euler(x0, v0, f, dt, tf)
    plt.plot(xTiempo, vValue, label=f'Trayectoria {i+1}')
plt.xlabel('Tiempo')
plt.ylabel('Velocidad')
plt.title('Trayectorias de Velocidad')
plt.legend()

plt.tight_layout()
plt.show()