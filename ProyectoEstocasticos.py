import pygame
import sys
import math
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

# Número de trayectorias a generar
num_trayectorias = 5

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

pygame.font.init()

#-------------------------------------- Variables Iniciales ------------------------------------
K= 5.4      #Constante de elasticidad resorte
m= 10       #masa del objeto
g= 9.81     #Gravedad Constante
X0= 350     #Posicion Inicial objeto
V0= 1       #Velocidad Inicial
#----------------------------------------------------------------------------------------------
anchoP,anchoD,anchog= 700, 200,450 #valores pantalla de animacion
altoP,altog=200,300
#Valores vibracion
P0=0
vi=2

#------------------- Pantalla -----------------
screen = pygame.display.set_mode((anchoP+anchoD,altoP+altog))
clock = pygame.time.Clock()


#------------------- Secciones -----------------
animacion= pygame.Surface((anchoP,altoP))
datos= pygame.Surface((anchoD,altoP))
g_vel= pygame.Surface((anchog,altog))
g_pos= pygame.Surface((anchog,altog))
fuente= pygame.font.Font(None,20)

#--------- Configuracion de las graficas ------------

#----------------------------------------------------
while True:
    clock.tick(60)  # Framerate
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
            
    animacion.fill((255,255,255)) #colorea la pantalla de blanco
    datos.fill((255,255,255))
    g_pos.fill((255,200,255))
    g_vel.fill((255,255,200))
    
    #Coordenadas punto de anclaje
    x=0 
    x1=2
    y=25
    ancho,alto=25,150
    radio=25
    #tiempo de ejecucion
    Tiempo=pygame.time.get_ticks()/1000
    
    #Vibracion punto de anclaje
    P0+=vi
    if P0 >0 or P0<15:
        vi=-vi
#   
    X0 +=V0
    if X0> (anchoP-radio) or X0<(P0+ancho+radio):
        V0=-V0


    #-------------------- Dibujar punto de anclaje --------------
    pygame.draw.rect(animacion,(0,0,0), (P0,y,ancho,alto), width=2) 
    pygame.draw.rect(animacion,(0,0,0), (0,0,anchoP,altoP), width=2)
    #-------------------- Dibujar resorte -----------------------
    pygame.draw.line(animacion,(255,0,0),(P0+ancho,altoP/2),(X0,altoP/2),5)       
    #-------------------- Dibujar objeto masa --------------------      
    pygame.draw.circle(animacion, (0,0,0), (X0,altoP/2),radio,width=2)
    pygame.draw.circle(animacion, (255,255,255),(X0,altoP/2),(radio-2)) #Relleno del circulo
    # -------------------------------------------------
    texto_velocidad=fuente.render("Velocidad: {} m/s".format(V0),True,(0,0,0))
    texto_Posicion=fuente.render("Posicion: {} m".format(X0),True,(0,0,0))
    texto_tiempo=fuente.render("Tiempo: {:.2f} s".format(Tiempo),True,(0,0,0))
    
    datos.blit(texto_velocidad,(10,10))
    datos.blit(texto_Posicion,(10,30))
    datos.blit(texto_tiempo,(10,50))
    
    screen.blit(g_pos,(0,altoP),(0,0,anchog,altog))
    screen.blit(g_vel,(anchog,altoP),(0,0,anchog,altog))
    screen.blit(datos, (anchoP, 0), (0, 0, anchoD, altoP))
    screen.blit(animacion,(0,0))
    pygame.display.update()