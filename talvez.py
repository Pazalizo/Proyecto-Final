import pygame
import sys
import matplotlib.pyplot as plt
import numpy as np

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
c = 0.2  # Coeficiente de amortiguamiento
k = 1.0  # Constante del resorte
sigma = 2  # Desviación estándar del ruido blanco

# Condiciones iniciales
x0 = 0.0  # Posición inicial
v0 = 1.0  # Velocidad inicial

# Parámetros de integración
dt = 0.01  # Paso de tiempo
tf = 30.0  # Tiempo final

# Generar las trayectorias
num_trayectorias = 5  # Número de trayectorias a generar
trayectorias = [metodo_euler(x0, v0, f, dt, tf) for _ in range(num_trayectorias)]

# Generación de gráficas
plt.figure(figsize=(10, 5))

# Trayectorias de posición
plt.subplot(2, 1, 1)
for i, (xTiempo, xValue, vValue) in enumerate(trayectorias):
    plt.plot(xTiempo, xValue, label=f'Trayectoria {i+1}')
plt.xlabel('Tiempo')
plt.ylabel('Posición')
plt.title('Trayectorias de Posición')
plt.legend()

# Trayectorias de velocidad
plt.subplot(2, 1, 2)
for i, (xTiempo, xValue, vValue) in enumerate(trayectorias):
    plt.plot(xTiempo, vValue, label=f'Trayectoria {i+1}')
plt.xlabel('Tiempo')
plt.ylabel('Velocidad')
plt.title('Trayectorias de Velocidad')
plt.legend()

plt.tight_layout()
plt.show()

pygame.font.init()

#-------------------------------------- Variables Iniciales ------------------------------------
anchoP, anchoD, anchog = 700, 200, 450
altoP, altog = 200, 300

P0 = 0
vi = 2
escala = 50  # Factor de escala para ajustar los valores de posición y velocidad a la pantalla de Pygame

#------------------- Pantalla -----------------
screen = pygame.display.set_mode((anchoP + anchoD, altoP + altog))
clock = pygame.time.Clock()

#------------------- Secciones -----------------
animacion = pygame.Surface((anchoP, altoP))
datos = pygame.Surface((anchoD, altoP))
fuente = pygame.font.Font(None, 20)

# Para la animación, usamos solo la primera trayectoria
xTiempo, xValue, vValue = trayectorias[0]

#----------------------------------------------------
while True:
    clock.tick(60)  # Framerate
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    animacion.fill((255, 255, 255))  # colorea la pantalla de blanco
    datos.fill((255, 255, 255))
    
    # Coordenadas punto de anclaje
    x = 0
    x1 = 2
    y = 25
    ancho, alto = 25, 150
    radio = 25
    
    # tiempo de ejecución
    Tiempo = pygame.time.get_ticks() / 1000
    idx = min(int(Tiempo / dt), len(xValue) - 1)
    X0 = xValue[idx] * escala  # valor escalado para la animación
    V0 = vValue[idx] * escala  # valor escalado para la animación

    # Vibración punto de anclaje
    P0 += vi
    if P0 > 0 or P0 < 15:
        vi = -vi

    #-------------------- Dibujar punto de anclaje --------------
    pygame.draw.rect(animacion, (0, 0, 0), (P0, y, ancho, alto), width=2) 
    pygame.draw.rect(animacion, (0, 0, 0), (0, 0, anchoP, altoP), width=2)
    
    #-------------------- Dibujar resorte -----------------------
    pygame.draw.line(animacion, (255, 0, 0), (P0 + ancho, altoP / 2), (int(X0), altoP / 2), 5)       
    
    #-------------------- Dibujar objeto masa --------------------
    pygame.draw.circle(animacion, (0, 0, 0), (int(X0), altoP // 2), radio, width=2)
    pygame.draw.circle(animacion, (255, 255, 255), (int(X0), altoP // 2), radio - 2)  # Relleno del círculo
    
    # -------------------------------------------------
    texto_velocidad = fuente.render("Velocidad: {:.2f} m/s".format(vValue[idx]), True, (0, 0, 0))  # usamos el valor original
    texto_Posicion = fuente.render("Posicion: {:.2f} m".format(xValue[idx]), True, (0, 0, 0))  # usamos el valor original
    texto_tiempo = fuente.render("Tiempo: {:.2f} s".format(Tiempo), True, (0, 0, 0))

    
    datos.blit(texto_velocidad, (10, 10))
    datos.blit(texto_Posicion, (10, 30))
    datos.blit(texto_tiempo, (10, 50))
    
    screen.blit(datos, (anchoP, 0), (0, 0, anchoD, altoP))
    screen.blit(animacion, (0, 0))
    pygame.display.update()
