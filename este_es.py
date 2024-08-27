import pygame
import sys
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Define las variables a nivel global para que sean accesibles en todas las funciones
m_value = c_value = k_value = sigma_value = x0_value = v0_value = dt_value = tf_value = None

def retrieve_input():
    global m_value, c_value, k_value, sigma_value, x0_value, v0_value, dt_value, tf_value, tr_value
    try:
        m_value = float(entry_m.get())
    except ValueError:
        m_value = 1.0

    try:
        c_value = float(entry_c.get())
    except ValueError:
        c_value = 0.2

    try:
        k_value = float(entry_k.get())
    except ValueError:
        k_value = 1.0

    try:
        sigma_value = float(entry_sigma.get())
    except ValueError:
        sigma_value = 2.0

    try:
        x0_value = float(entry_x0.get())
    except ValueError:
        x0_value = 0.0

    try:
        v0_value = float(entry_v0.get())
    except ValueError:
        v0_value = 1.0

    try:
        dt_value = float(entry_dt.get())
    except ValueError:
        dt_value = 0.01

    try:
        tf_value = float(entry_tf.get())
    except ValueError:
        tf_value = 30.0
        
    try:
        tr_value = int(entry_tr.get())
    except ValueError:
        tr_value = 5
    
    hacer_graficas()
        
def hacer_graficas():
      
    def f(x, v):
        return -k_value * x / m_value - c_value * v / m_value

    def metodo_euler(x0, v0, f, dt, tf):
        xTiempo = np.arange(0, tf + dt, dt)
        xValue = np.zeros(len(xTiempo))
        xValue[0] = x0
        vValue = np.zeros(len(xTiempo))
        vValue[0] = v0
        for i in range(1, len(xTiempo)):
            xValue[i] = xValue[i - 1] + vValue[i - 1] * dt
            vValue[i] = vValue[i - 1] + f(xValue[i - 1], vValue[i - 1]) * dt + (sigma_value / m_value) * np.sqrt(dt) * np.random.normal(0, 1)
        return xTiempo, xValue, vValue
    
    # Generar las trayectorias
    trayectorias = [metodo_euler(x0_value, v0_value, f, dt_value, tf_value) for _ in range(tr_value)]

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
    desplazamiento = anchoP / 2  # Desplazamiento para mantener la masa dentro de la pantalla en caso de valores negativos

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
        idx = min(int(Tiempo / dt_value), len(xValue) - 1)
        X0 = xValue[idx] * escala + desplazamiento  # valor escalado para la animación
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

window = tk.Tk()

label_m = tk.Label(window, text = "Masa (m):")
label_m.pack()
entry_m = tk.Entry(window)
entry_m.pack()

label_c = tk.Label(window, text = "Constante de amortiguamiento (c):")
label_c.pack()
entry_c = tk.Entry(window)
entry_c.pack()

label_k = tk.Label(window, text = "Constante del resorte (k):")
label_k.pack()
entry_k = tk.Entry(window)
entry_k.pack()

label_sigma = tk.Label(window, text = "(sigma):")
label_sigma.pack()
entry_sigma = tk.Entry(window)
entry_sigma.pack()

label_x0 = tk.Label(window, text = "Posicion Inicial (x0):")
label_x0.pack()
entry_x0 = tk.Entry(window)
entry_x0.pack()

label_v0 = tk.Label(window, text = "Velocidad Inicial (v0):")
label_v0.pack()
entry_v0 = tk.Entry(window)
entry_v0.pack()

label_dt = tk.Label(window, text = "Paso (dt):")
label_dt.pack()
entry_dt = tk.Entry(window)
entry_dt.pack()

label_tr = tk.Label(window, text = "Numero de Trayectorias:")
label_tr.pack()
entry_tr = tk.Entry(window)
entry_tr.pack()

label_tf = tk.Label(window, text = "Tiempo final (tf):")
label_tf.pack()
entry_tf = tk.Entry(window)
entry_tf.pack()

button = tk.Button(window, text = "Calculate", command = retrieve_input)
button.pack()

window.mainloop()