import matplotlib.pyplot as plt
import numpy as np

def E_Xt (x0, v0, m, c, k, t):
    coef1 = x0 * np.exp(-0.5 * t * c / m)
    coef2 = (m * v0 + c * x0) / (m * x0) - c / (2 * m)
    coef3 = np.sqrt(abs((np.power(c, 2)) / (4 * (np.power(m, 2))) - k / m))

    first_term = np.cosh(t * coef3)
    second_term = coef2 / coef3 * np.sinh(t * coef3)

    return coef1 * (first_term + second_term)

def E_Vt(x0, v0, m, c, k, t):
    coef1 = x0 * np.exp(-0.5 * t * c / m)
    coef2 = (c / (2 * m)) + (k * x0) / (m * v0)
    coef3 = np.sqrt(abs((np.power(c, 2)) / (4 * (np.power(m, 2))) - k / m))
    
    first_term = np.cosh(t) * coef3
    second_term = coef2 / coef3 * np.sinh(t)
    
    return coef1 * (first_term - second_term)

# Parámetros del sistema
m = 1.0  # Masa del oscilador
c = 0.1  # Coeficiente de amortiguamiento
k = 1.0  # Constante del resorte
sigma = 1  # Desviación estándar del ruido blanco

# Condiciones iniciales
x0 = 1.0  # Posición inicial
v0 = 1.0  # Velocidad inicial

# Parámetros de integración
dt = 0.01  # Paso de tiempo
tf = 30.0  # Tiempo final

# Crear arreglo de tiempo
t_values = np.arange(0, tf, dt)

# Calcular posición en cada instante de tiempo usando la solución analítica
x_values = E_Xt(x0, v0, m, c, k, t_values)
v_values = E_Vt(x0, v0, m, c, k, t_values)

# Graficar
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(t_values, x_values, label="Posición en función del tiempo")
plt.ylabel('Posición')
plt.subplot(2, 1, 2)
plt.plot(t_values, v_values, label="Velocidad en función del tiempo")
plt.ylabel('Velocidad')
plt.title('Gráfica de la posición del oscilador en función del tiempo')
plt.legend()
plt.show()

