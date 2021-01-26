#!/usr/bin/env python3
"""
Este script utiliza unidades del SI, excepto donde se especifica lo contrario.
"""

import math
import random
import tabulate
from operator import itemgetter 
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
    # Los residuos no son proporcionales a la distancia entre "pos_X" y
    # "pos_A", lo que es problemático a la hora de discriminar puntos muy
    # lejanos de la fuente como posibles fuentes.
    return vector3_norm(pos_X-pos_A)-vector3_norm(pos_X-pos_B) - (d_A-d_B)

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
    # https://devforum.roblox.com/t/generating-equidistant-points-on-a-sphere/874144
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
        self.pos_O = pos_O
        # con extremos A, B, C y D.
        # Extremo A alineado con eje Z (vertical)
        tmp_vec = Vector3()
        tmp_vec.z = R
        self.pos_A = pos_O + tmp_vec
        # Extremo B en el plano XZ
        tmp_vec = Vector3()
        tmp_vec.y = 1
        self.pos_B = self.pos_A.rotate_about(pos_O, tmp_vec, TAU/3)
        # Extremo C una copia del extremo B girada TAU/3 alrededor de Z
        tmp_vec = Vector3()
        tmp_vec.z = 1
        self.pos_C = self.pos_B.rotate_about(pos_O, tmp_vec, TAU/3)
        # Extremo D una copia del extremo D girada TAU/3 alrededor de Z
        self.pos_D = self.pos_C.rotate_about(pos_O, tmp_vec, TAU/3)
        return       

    def calc_retardos(self, pos_X):
        # F: Fuente, O: referencia, U: monitor U
        # FO = L
        # FU = L + d_U => d_U = FU - L
        L   = vector3_norm(self.pos_O - pos_X)
        d_A = vector3_norm(self.pos_A - pos_X) - L
        d_B = vector3_norm(self.pos_B - pos_X) - L
        d_C = vector3_norm(self.pos_C - pos_X) - L
        d_D = vector3_norm(self.pos_D - pos_X) - L
        return (d_A, d_B, d_C, d_D)

    def calc_residuos(self, pos_X, d_A, d_B, d_C, d_D):
        sum = 0
        sum += abs(calc_residuos(pos_X, self.pos_A, self.pos_B, d_A, d_B))
        sum += abs(calc_residuos(pos_X, self.pos_A, self.pos_C, d_A, d_C))
        sum += abs(calc_residuos(pos_X, self.pos_A, self.pos_D, d_A, d_D))
        sum += abs(calc_residuos(pos_X, self.pos_B, self.pos_C, d_B, d_C))
        sum += abs(calc_residuos(pos_X, self.pos_B, self.pos_D, d_B, d_D))
        sum += abs(calc_residuos(pos_X, self.pos_C, self.pos_D, d_C, d_D))
        return sum


if __name__ == "__main__":

    origen = Vector3(0,0,0)

    lt = LocalizadorTetrahedrico(origen, 0.05)

    fuente = generar_punto_aleatorio(origen, 10)
    print(f"Fuente: {vector3_fstr(fuente)}")

    mft = Vector3(1000,0,0)

    puntos_prueba = []
    for i in range(20):
        puntos_prueba.append(generar_punto_aleatorio(origen, 40))

    puntos_prueba.append(mft)
    puntos_prueba.append(fuente)

    retardos = lt.calc_retardos(fuente)
    print(f"Retardos: {retardos}")

    residuos = {}
    for pp in puntos_prueba:
        residuos[pp] = lt.calc_residuos(pp, *retardos)

    table = []
    for p, r in residuos.items():
        table.append([vector3_fstr(p), r, str(vector3_norm(fuente - p))])

    # sorted_table = sorted(table, key=lambda x: x[1])
    sorted_table = sorted(table, key=itemgetter(1))
    table_hh = ("Vector", "Residuos", "Dist. de fuente")

    print(tabulate.tabulate(sorted_table, headers=table_hh))
    

