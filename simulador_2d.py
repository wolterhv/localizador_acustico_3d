import numpy as np
import math
import random
import matplotlib.pyplot as plt

TAU = 2*math.pi

class Localizador2D:

    def __init__(self, pos_O, R):

        self.pos_O = pos_O
        self.pos_A = obtener_punto_de_coords_polares(self.pos_O, R, TAU/4)
        self.pos_B = obtener_punto_de_coords_polares(self.pos_O, R, TAU/4+TAU/3)
        self.pos_C = obtener_punto_de_coords_polares(self.pos_O, R, TAU/4+2*TAU/3)

        return

    def calc_retardos(self, pos_X):
        L = calc_dist(self.pos_O, pos_X)
        d_A = calc_dist(self.pos_A, pos_X) - L
        d_B = calc_dist(self.pos_B, pos_X) - L
        d_C = calc_dist(self.pos_C, pos_X) - L
        return (d_A, d_B, d_C)

    def calc_residuos(self, pos_F, pos_X):
        retardos = self.calc_retardos(pos_F)
        return calc_residuos(pos_X, 
                             self.pos_A, 
                             self.pos_B, 
                             self.pos_C, 
                             retardos[0], 
                             retardos[1], 
                             retardos[2])

def obtener_punto_de_coords_polares(pos_O, r, th):
    """Devuelve punto con coordenadas polares "r" y "th" centrado en el punto
    "pos_O"."""
    x = r*math.cos(th)
    y = r*math.sin(th)
    punto = np.array([x, y])
    punto += pos_O
    return punto

def calc_residuos(pos_X, pos_A, pos_B, pos_C, d_A, d_B, d_C):
    residuos = []
    residuos.append(abs(calc_dist(pos_X, pos_A) - calc_dist(pos_X, pos_B) - (d_A - d_B)))
    residuos.append(abs(calc_dist(pos_X, pos_A) - calc_dist(pos_X, pos_C) - (d_A - d_C)))
    residuos.append(abs(calc_dist(pos_X, pos_B) - calc_dist(pos_X, pos_C) - (d_B - d_C)))
    return residuos

def calc_dist(pos_A, pos_B):
    return np.linalg.norm(pos_A - pos_B)

def generar_punto_aleatorio(pos_O, max_dist):
    r = max_dist*random.random()
    th = TAU*random.random()
    punto = obtener_punto_de_coords_polares(pos_O, r, th)
    return punto

if __name__ == "__main__":

    origen = np.zeros(2)

    loc = Localizador2D(origen, 5)

    # Crear fuente 30 unidades alejada del centro del localizador
    # fuente = generar_punto_aleatorio(origen, 60)
    fuente = obtener_punto_de_coords_polares(origen, 60, TAU/9)

    # Crear matriz cuadrada con un lado de 80 unidades, centrada en el
    # localizador con una densidad arbitraria y uniforme de puntos
    lado = 80
    sep = 1
    X = np.arange(origen[0]-lado, origen[1]+lado, sep)
    Y = np.arange(origen[0]-lado, origen[1]+lado, sep)

    xx, yy = np.meshgrid(X, Y, sparse=True)

    def maya_calc_residuos(loc, F, x, y, i):
        return loc.calc_residuos(F, np.array([x, y]))[i]

    Z0 = maya_calc_residuos(loc, fuente, xx, yy, 0)
    Z1 = maya_calc_residuos(loc, fuente, xx, yy, 1)
    Z2 = maya_calc_residuos(loc, fuente, xx, yy, 2)

    # Normalize
    Z0 = Z0/np.max(Z0)
    Z1 = Z1/np.max(Z1)
    Z2 = Z2/np.max(Z2)

    # Invert
    Z0 = np.max(Z0) - Z0
    Z1 = np.max(Z1) - Z1
    Z2 = np.max(Z2) - Z2

    # Accentuate
    Z0 = np.power(Z0,1)
    Z1 = np.power(Z1,1)
    Z2 = np.power(Z2,1)

    ZX = Z0*Z1*Z2

    # Graficar la matriz con matplotlib
    h0 = plt.contourf(X, Y, ZX, 300)

    # Graficar puntos de interés
    scat_x = []
    scat_y = []
    for p in [fuente, loc.pos_A, loc.pos_B, loc.pos_C]:
        scat_x.append(p[0])
        scat_y.append(p[1])

    h1 = plt.scatter(scat_x, scat_y)

    plt.show()
