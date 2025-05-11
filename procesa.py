# procesa.py

import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import shutil
from mpl_toolkits.mplot3d import Axes3D


def main():
    # Cargar datos de simulación
    datos = np.load("resultados.npz")
    xn = datos["xn"]  # (3, N, Nt)
    vn = datos["vn"]
    sn = datos["sn"]

    N = xn.shape[1]
    Nt = xn.shape[2]

    # 1. Calcular baricentro
    baricentro = xn.mean(axis=1)  # shape: (3, Nt)
    plt.figure()
    plt.plot(baricentro[0], label="X")
    plt.plot(baricentro[1], label="Y")
    plt.plot(baricentro[2], label="Z")
    plt.title("Evolución del baricentro")
    plt.xlabel("Paso de tiempo")
    plt.ylabel("Posición media")
    plt.legend()
    plt.grid()
    plt.savefig("baricentro.png")
    plt.close()
    print("✔ Gráfico baricentro.png guardado")

    # 2. Elongaciones
    ex = xn[0].max(axis=0) - xn[0].min(axis=0)
    ey = xn[1].max(axis=0) - xn[1].min(axis=0)
    ez = xn[2].max(axis=0) - xn[2].min(axis=0)

    plt.figure()
    plt.plot(ex, label="X")
    plt.plot(ey, label="Y")
    plt.plot(ez, label="Z")
    plt.title("Elongación por eje")
    plt.xlabel("Paso de tiempo")
    plt.ylabel("Distancia")
    plt.legend()
    plt.grid()
    plt.savefig("elongacion.png")
    plt.close()
    print("✔ Gráfico elongacion.png guardado")

    # 3. Velocidad media y desviación típica
    normas_v = np.linalg.norm(vn, axis=0)  # (N, Nt)
    v_prom = normas_v.mean(axis=0)
    v_std = normas_v.std(axis=0)

    plt.figure()
    plt.plot(v_prom, label="Media")
    plt.fill_between(range(Nt), v_prom - v_std, v_prom + v_std, alpha=0.3, label="± Desv. Típica")
    plt.title("Velocidad media con desviación típica")
    plt.xlabel("Paso de tiempo")
    plt.ylabel("Velocidad")
    plt.legend()
    plt.grid()
    plt.savefig("velocidad.png")
    plt.close()
    print("✔ Gráfico velocidad.png guardado")

    # 4. Animación
    print("⏳ Generando animación...")
    os.makedirs("frames", exist_ok=True)
    imagenes = []

    for n in range(0, Nt, 10):  # cada 10 pasos
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        colores = ['red' if s == 0 else 'blue' for s in sn[:, n]]
        ax.scatter(xn[0, :, n], xn[1, :, n], xn[2, :, n], c=colores, s=10)
        ax.set_xlim(xn[0].min(), xn[0].max())
        ax.set_ylim(xn[1].min(), xn[1].max())
        ax.set_zlim(xn[2].min(), xn[2].max())
        ax.set_title(f"Paso {n}")
        nombre = f"frames/frame_{n:04d}.png"
        plt.savefig(nombre)
        plt.close()
        imagenes.append(imageio.imread(nombre))

    imageio.mimsave("animacion.gif", imagenes, fps=10)
    print("✔ Animación guardada como animacion.gif")

    # 5. Limpieza
    shutil.rmtree("frames")
    print("🧹 Carpeta frames eliminada")

    print("\n✅ Análisis finalizado. Archivos generados:")
    print("  - baricentro.png")
    print("  - elongacion.png")
    print("  - velocidad.png")
    print("  - animacion.gif")


if __name__ == "__main__":
    main()