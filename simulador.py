#!/usr/bin/env python3
"""
Este script utiliza unidades del SI, excepto donde se especifica lo contrario.
"""

import math
import random
from vectormath import *

TAU = 2*math.pi

def generar_punto_aleatorio(origen, max_dist):
    punto = Vector3()
    R = random.random()*max_dist
    th_azi = random.random()*TAU/2
    th_pol = random.random()*TAU
    vector3_init_sph(punto, R, th_azi, th_pol)
    return punto

def calc_residuos(pos_X, pos_A, pos_B, d_A, d_B):
    return abs(pos_X-pos_A)-abs(pos_X-pos_B) - (d_A-d_B)

def generar_bola_discreta(pos_O, R, min_R, sep_ang, sep_casc):
    """Devuelve un conjunto de puntos que conforman una bola de radio "R"
    centrada en "pos_O".  La bola se genera a partir de una serie de
    cascarones, como una cebolla.  Cada cascarón es un conjunto de puntos en
    una espiral que envuelve a una esfera imaginaria.  A lo largo de la
    espiral, los puntos adyacentes se encuentran separados de sí mismos una
    separación angular respecto al centro de la esfera de "sep_ang".  El paso
    angular de la espiral es también "sep_ang".  La separación entre cascarones
    adyacentes es "sep_casc".  En el centro de la bola, hay una bola vacía de
    radio "min_R"."""
    bola = []
    seg_rad = floor(R/sep_rad)
    seg_circ = TAU/sep_ang
    # Generar la bola por cascarones
    irad = min_R-sep_casc
    th_azi = 0
    th_pol = 0
    # for icasc in range(1,seg_rad):
    #     for ipunto in range(100): # Sustituir 100 por algo razonable
    #     irad += sep_casc
    #     sep_puntos
    #     punto = Vector3()
    #     vector3_init_sph(punto, irad, th_azi, th_pol)
    #     bola.append(punto)

    return bola


class LocalizadorTetrahedrico:

    def __init__(self, pos_O, R):
        # Construir tetrahedro centrado en posO, inscrito en esfera de radio R,
        # con extremos A, B, C y D.
        # Extremo A alineado con eje Z (vertical)
        tmp_vec = Vector3()
        tmp_vec.z = R
        self.pos_A = pos_O + tmp_vec
        # Extremo B en el plano XZ
        tmp_vec = Vector3()
        tmp_vec.y = TAU/3
        self.pos_B = self.pos_A.rotate_about(pos_O, tmp_vec)
        # Extremo C una copia del extremo B girada TAU/3 alrededor de Z
        tmp_vec = Vector3()
        tmp_vec.z = TAU/3
        self.pos_C = self.pos_B.rotate_about(pos_O, tmp_vec)
        # Extremo D una copia del extremo D girada TAU/3 alrededor de Z
        self.pos_D = self.pos_C.rotate_about(pos_O, tmp_vec)
        return       

    def calc_residuos(self, pos_X, d_A, d_B, d_C, d_D):
        sum = 0
        sum += calc_residuos(pos_X, self.pos_A, self.pos_B, d_A, d_B)
        sum += calc_residuos(pos_X, self.pos_A, self.pos_C, d_A, d_C)
        sum += calc_residuos(pos_X, self.pos_A, self.pos_D, d_A, d_D)
        sum += calc_residuos(pos_X, self.pos_B, self.pos_C, d_B, d_C)
        sum += calc_residuos(pos_X, self.pos_B, self.pos_D, d_B, d_D)
        sum += calc_residuos(pos_X, self.pos_C, self.pos_D, d_C, d_D)
        return sum


# Generador de posiciones aleatorias

if __name__ == "__main__":

    punto = generar_punto_aleatorio(Vector3(), 10)
    print(punto)
    

