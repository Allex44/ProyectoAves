import numpy as np

N = 200
L = 200

x0 = np.zeros((3, N))
x0[0] = np.random.uniform(0, L, N)  # X
x0[2] = np.random.uniform(0, L, N)  # Z

v0 = np.zeros((3, N))
v0[0] = np.random.normal(0, 1, N)  # VX
v0[2] = np.random.normal(0, 1, N)  # VZ

s0 = np.ones(N, dtype=int)
s0[:10] = 0  # primeros 10 líderes

np.savez("iniciales.npz", x0=x0, v0=v0, s0=s0)

# IgnoreMe Datos 2d: Crep= 2.5 Cali=3 Catt= 0.01 Nt= 1000