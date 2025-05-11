# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 19:05:34 2025

@author: Yin
"""

import numpy as np
from utilidades import(calcular_vecinos, calcular_acciones, actualizar_estados, euler_simplectico)


def simula():
    '''
    Función que realiza la simulación de la bandada de aves.
    
    Parámetros:
        modelo.npz : ruta al archivo con los parámetros del modelo.
        iniciales.npz: ruta al archivo con las condiciones iniciales.
    Devoluciones:
        resultados.npz : ruta donde guardar los resultados de la simulación.
    '''
    
    # Leer parámetros del modelo.txt
    with open('modelo.txt', 'r') as f:
        parametros = {}
        for line in f:
            if '=' in line:
                clave, valor = line.strip().split('=')
                parametros[clave.strip()] = float(valor.strip())
           
            
    # Extraer parámetros        
    Crep = parametros['Crep']
    Cali = parametros['Cali']
    Catt = parametros['Catt']
    M = int(parametros['M'])
    N = int(parametros['N'])
    Nper = int(parametros['Nper'])
    D = parametros['D']
    p = parametros['p']
    t0 = parametros['t0']
    dt = parametros['dt']
    Nt = int(parametros['Nt'])
    
    # Cargar condiciones iniciales
    datos_iniciales = np.load('iniciales.npz')
    x0 = datos_iniciales['x0']
    v0 = datos_iniciales['v0']
    s0 = datos_iniciales['s0']

    # Asegurar que x0 y v0 tengan 3 coordenadas (añadir z = 0 si faltan)
    if x0.shape[1] == 2:
        x0 = np.hstack((x0, np.zeros((x0.shape[0], 1))))
    if v0.shape[1] == 2:
        v0 = np.hstack((v0, np.zeros((v0.shape[0], 1))))
    
    # Preparar arrays para almacenar resultados
    xn = np.zeros((3, N, Nt))
    vn = np.zeros((3, N, Nt))
    sn = np.zeros((N, Nt), dtype=int)
    
    # Establecer condiciones iniciales
    xn[:, :, 0] = x0.T
    vn[:, :, 0] = v0.T
    sn[:, 0] = s0
    
    # Historial de estados para verificar Nper
    historial_lideres = [[s0[i]] for i in range(N)]
        
    # Bucle principal de la simulación
    for n in range (1, Nt):
        # Obtener estados actuales
        posicion_actual = xn[:, :, n-1]
        velocidad_actual = vn[:, :, n-1]
        estado_actual = sn[:, n-1]
        
        # Calcular vecinos cercanos para cada ave
        vecinos = calcular_vecinos(posicion_actual, M)
        
        # Iniciar arrays para acciones
        acciones = np.zeros((3, N))
        
        for k in range(N):
            # Calcular la acción Ak para cada individuo
            acciones[:, k] = calcular_acciones(k, posicion_actual, velocidad_actual, estado_actual, vecinos, Crep, Cali, Catt)
            
        # Actualizar posiciones y velocidades usando Euler simpléctico
        nuevas_posiciones, nuevas_velocidades = euler_simplectico(posicion_actual, velocidad_actual, acciones, dt)
        
        # Actualizar estados (líder/seguidor)
        nuevos_estados, historial_lideres = actualizar_estados(estado_actual, posicion_actual, Nper, D, p, historial_lideres)
        
        # Almacenar resultados del paso actual
        xn[:, :, n] = nuevas_posiciones
        vn[:, :, n] = nuevas_velocidades
        sn[:, n] = nuevos_estados
    
    # Guardar resultados en resultados.npz
    np.savez('resultados.npz', xn=xn, vn=vn, sn=sn)
    print("Resultados guardados en resultados.npz.")
    
if __name__ == "__main__":
    simula() # Ejecutar la simulación al correr el script
        
        