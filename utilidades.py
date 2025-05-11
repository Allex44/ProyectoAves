# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 19:06:59 2025

@author: Yin
"""

import numpy as np
import random

def calcular_vecinos(posiciones, M):
    '''
    Calcula los M vecinos más cercanos para cada ave en la bandada.

    Parámetros:
        posiciones : Array 3xN con las posiciones de todas las aves.
        M : Número de vecinos cercanos a considerar.
    Devoluciones:
        Lista de listas con los índices de los M vecinos más cercanos para cada ave.
    '''
    N = posiciones.shape[1] # Número total de aves
    vecinos = []
    
    for i in range(N):
        # Calcular distancias a todas las otras aves
        distancias = np.linalg.norm(posiciones - posiciones[:, i:i+1], axis=0)
        
        # Ordenar índices por distancia (excluyendo al propio ave)
        indices_ordenados = np.argsort(distancias)[1:M+1] # Excluye a si mismo
        vecinos.append(indices_ordenados.tolist())
        
    return vecinos

def calcular_acciones(k, posiciones, velocidades, estados, vecinos, Crep, Cali, Catt):
    '''
    Calcula la acción total Ak sobre el ave k.

    Parámetros:
        k : Índice del ave.
        posiciones : Array 3xN de posiciones actuales.
        velocidades : Array 3xN de velocidades actuales.
        estados : Array N de caracteres (0 líder, 1 seguidor).
        vecinos : Lista de listas de vecinos.
        Crep, Cali, Catt : Constantes del modelo.
    Devoluciones:
        Vector de acción Ak (3 componentes).
    '''
    epsilon = 1e-6
    M = len(vecinos[k]) # Número de vecinos del ave k
    
    # Iniciar acciones
    Aatt = np.zeros(3)
    Arep = np.zeros(3)
    Aali = np.zeros(3)
    
    for j in vecinos[k]:
        # Atracción: hacia los vecinos
        Aatt += posiciones[:, j] - posiciones[:, k]
        
        # Repulsión: alejándose de los vecinos
        diff = posiciones[:, k] - posiciones[:, j]
        Arep += diff / (np.linalg.norm(diff)**2 + epsilon)
        
        # Alineamiento: igualar velocidad con vecinos
        Aali += velocidades[:, j] - velocidades[:, k]
        
    # Aplicar constantes
    Aatt *= Catt
    Arep *= Crep
    Aali *= (Cali / M) if M > 0 else  0  # Evitar división por cero si no hay vecinos
    
    # Determinar acción total
    if estados[k] == 0: # Líder
        Ak = Arep
    else: # Seguidor
        Ak = Arep + Aatt + Aali
        
    return Ak

def euler_simplectico(posiciones, velocidades, acciones, dt):
    '''
    Actualiza posiciones y velocidades usandoel método  de Euler simpléctico.

    Parámetros:
        posiciones : Posiciones actuales (3xN).
        velocidades : Velocidades actuales (3xN).
        acciones : Acciones calculadas (3xN).
        dt : Paso de tiempo.
    Devoluciones:
        nuevas_posiciones
        nuevas_velocidades
    '''
    nuevas_velocidades = velocidades + dt * acciones  # Actualizar velocidades
    nuevas_posiciones = posiciones + dt * nuevas_velocidades # Actualizar posiciones
    
    return nuevas_posiciones, nuevas_velocidades

def actualizar_estados(estados_actuales, posiciones, Nper, D, p, historial_lideres):
    '''
    Actualiza los estados de líder/seguidor por cada ave.

    Parámetros:
        estados_actuales : Estados actuales (0 o 1).
        posiciones : Array 3xN con posiciones actuales.
        Nper : Pasos consecutivos máximos como líder.
        D : Distancia mínima para mantener liderazgo.
        p : Probabilidad de que un seguidor se convierta en líder.
        historial_lideres : Lista con historial de estados de cada ave.
    Devoluciones:
        nuevos_estados
        historial_líderes

    '''
    
    N = len(estados_actuales)
    nuevos_estados = estados_actuales.copy()
    
    for i in range(N):
        estado = estados_actuales[i]
        
        if estado == 1: # Si es seguidor
            # Probabilidad p de convertirse en líder
            if random.random() < p:
                nuevos_estados[i] = 0
                nuevo_estado = 0
            else:
                nuevo_estado = 1
                
        else: # Si es líder
            lider_suf = len(historial_lideres[i]) >= Nper and all(s==0 for s in historial_lideres[i][-Nper:])
            distancias = np.linalg.norm(posiciones- posiciones[:, i:i+1], axis=0)
            distancias[i] = np.inf
            alejado = np.min(distancias) > D
            
            if lider_suf or alejado:
                nuevos_estados[i] = 1
                nuevo_estado = 1
            else:
                nuevo_estado = 0
                
        historial_lideres[i].append(nuevo_estado)
                    
    return nuevos_estados, historial_lideres

