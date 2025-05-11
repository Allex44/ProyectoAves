# ProyectoAves
"The following program aims to study the behavior of birds in flocks through a series of functionalities developed in Python, which create 2D and 3D simulations and graphs that analyze, for example, their speed, elongation, and barycenter.

Simulación de Bandada de Aves

Este proyecto simula el comportamiento colectivo de una bandada de aves usando un modelo basado en interacción entre individuos (alineamiento, repulsión y atracción).

📁 Estructura del proyecto

- `utilidades.py`: funciones auxiliares para la simulación.
- `simula.py`: ejecuta la simulación y genera `resultados.npz`.
- `procesa.py`: analiza los resultados y genera gráficos y animación.
- `modelo.txt`: parámetros del modelo físico y de simulación.
- `iniciales.npz`: condiciones iniciales (posiciones, velocidades, estados).
- `resultados.npz`: archivo generado con datos simulados.
- `informe_aves.pdf`: informe con análisis y figuras.

▶️ Cómo usar

1. Asegúrate de tener Python 3.8+ instalado.
2. Instala las dependencias:

```bash
pip install numpy matplotlib imageio

Crea las condiciones iniciales ejecutando uno de estos scripts:

python crear_iniciales_2d.py  # para simulación en plano
python crear_iniciales_3d.py  # para simulación tridimensional

Ejecuta la simulación:
python simula.py

Analiza los resultados y genera gráficos:
python procesa.py

📝 Salidas generadas
resultados.npz: datos simulados

baricentro.png, elongacion.png, velocidad.png: gráficos de análisis

animacion.gif: evolución visual de la bandada


