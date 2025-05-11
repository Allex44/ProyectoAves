import numpy as np

N = 200
r = 100  # radio de la nube

phi = np.random.uniform(0, 2*np.pi, N)
costheta = np.random.uniform(-1, 1, N)
u = np.random.uniform(0, 1, N)

theta = np.arccos(costheta)
radius = r * np.cbrt(u)

x0 = np.zeros((3, N))
x0[0] = radius * np.sin(theta) * np.cos(phi)
x0[1] = radius * np.sin(theta) * np.sin(phi)
x0[2] = radius * np.cos(theta)

v0 = np.random.normal(0, 1, (3, N))

s0 = np.random.choice([0, 1], size=N, p=[0.05, 0.95])

np.savez("iniciales.npz", x0=x0, v0=v0, s0=s0)

#IgnoreMe: Ajustes para el modelo 3D en modelo.txt: Crep=3.0 Cali=4.0 Catt=0.015 Nt=1500