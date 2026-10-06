import numpy as np
import matplotlib.pyplot as plt
import rasterio
from scipy import ndimage
from pyproj import Transformer
#La función para convertir coordenadas (ver docstring)
def convert(x, y):
    """
    Convert coordinates from UTM Zone 18S (EPSG:32719) to UTM Zone 19S (EPSG:32718).

    This function uses pyproj's `Transformer` to reproject a pair of coordinates
    from one UTM zone to another, both defined in WGS84.

    Parameters
    ----------
    x : float
        Easting coordinate in meters (UTM Zone 18S, EPSG:32719).
    y : float
        Northing coordinate in meters (UTM Zone 18S, EPSG:32719).

    Returns
    -------
    x_new : float
        Transformed easting coordinate in meters (UTM Zone 19S, EPSG:32718).
    y_new : float
        Transformed northing coordinate in meters (UTM Zone 19S, EPSG:32718).

    Notes
    -----
    - This function is currently hardcoded to transform from EPSG:32719 to EPSG:32718.
    - Both source and destination CRS use WGS84 datum.
    - For batch conversion of many points, consider using `transformer.transform` with arrays.
    """
    # Huso actual y destino (ejemplo: de 18S a 19S)
    src_epsg = 32719  # WGS84 UTM Zone 18S
    dst_epsg = 32718  # WGS84 UTM Zone 19S

    # Crear transformador
    transformer = Transformer.from_crs(src_epsg, dst_epsg, always_xy=True)

    # Transformar
    x_new, y_new = transformer.transform(x, y)
    return x_new, y_new
#Lee la imagen referenciada
path = "./rectified_UTM18.tif"
with rasterio.open(path) as src:
    r = src.read(1).astype("float32")
    g = src.read(2).astype("float32")
    b = src.read(3).astype("float32")
    bounds = src.bounds
    extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
# Optional: normalize to [0,1] if needed
def norm(x):
    lo, hi = np.nanpercentile(x, (2, 98))
    return np.clip((x - lo) / (hi - lo), 0, 1)
rgb = np.dstack([norm(r), norm(g), norm(b)])
#Lee los dos datasets
data_desembocadura = np.loadtxt("batimetria desembocadura_1_agosto.xyz")
data_full = np.loadtxt("batimetria_ajustada_1_agosto.xyz")
#Los arreglos x19,y19 y los *_1 tienen los valores en utm huso 19S
x19, y19 = convert(data_full[:, 0], data_full[:, 1])
x19_desembocadura, y19_desembocadura = convert(data_desembocadura[:, 0], data_desembocadura[:, 1])
#El rectángulo objetivo
##desembocadura
xleft = 772300+950#771764#773223.4+50
ybot = 6.180551e6-200
xright = 773.798e3+300
ytop = 6.180928e6
padding = 100
#laguna


plt.imshow(rgb, extent=extent, origin="upper")
from matplotlib.patches import Rectangle
# Lower-left corner, width, height
rect = Rectangle(
    (xleft, ybot),
    width=xright - xleft,
    height=ytop - ybot,
    edgecolor="green",
    facecolor="none",
    linewidth=2,
)
plt.scatter(x19, y19, s=1, c="red", label="Puntos batimétricos")
plt.scatter(
    x19_desembocadura, y19_desembocadura, s=1, c="blue", label="Puntos desembocadura"
)
plt.xlim(xleft - padding, xright + padding)
plt.ylim(ybot - padding, ytop + padding)
plt.gca().add_patch(rect)
plt.gca().set_aspect("equal")
plt.show()
mesh_resolution = 0.25#0.25#0.2#4
x = np.arange(xleft, xright, mesh_resolution)
y = np.arange(ybot, ytop, mesh_resolution)
xmesh, ymesh = np.meshgrid(x, y)
xmesh.shape
xmask = (x19 >= xleft) & (x19 <= xright)
ymask = (y19 >= ybot) & (y19 <= ytop)
mask = xmask & ymask
#%Interpolar así nomás deja valores nan
from scipy.interpolate import griddata

Zi = griddata(
    np.vstack([x19[mask], y19[mask]]).T, data_full[mask, 2], (xmesh, ymesh), method="linear"
)
nan_mask = np.isnan(Zi)
np.any(nan_mask)
#%gpt sugiere esto instead:
import numpy as np
from scipy.interpolate import griddata

# Puntos y valores
pts = np.vstack([x19[mask], y19[mask]]).T  # (N, 2)
vals = data_full[mask, 2]  # (N,)

# Malla destino (X, Y) con misma forma
# xmesh, ymesh ya definidos

# 1) Interpolación lineal (NaN fuera del casco convexo)
Zi_lin = griddata(pts, vals, (xmesh, ymesh), method="linear")

# 2) Interpolación por vecino más cercano (no deja NaN)
Zi_near = griddata(pts, vals, (xmesh, ymesh), method="nearest")

# 3) Combinar: lineal donde exista, nearest donde era NaN
# Zi = np.where(np.isnan(Zi_lin), Zi_near, Zi_lin)
Zi = np.where(np.isnan(Zi_lin), Zi_near, Zi_lin)


# % Arreglar el hoyo usando rangos en coordenadas reales
from matplotlib.path import Path
from matplotlib.patches import Polygon

# % Arreglar batimetría en un polígono (ejemplo: pentágono)
# Coordenadas UTM de los vértices del polígono (en orden)
poly_coords = [
    (773218+20, 6.18055e6-200),#abajo izquierda
    (773500+500, 6.18055e6-200), # abajo derecha
    (773380, 6.18059e6),
    (773300, 6.18065e6),#putna arriba
    (773215, 6.18060e6),#arriba izuqierda
]

# Crear un Path (para testear qué puntos están dentro)
poly_path = Path(poly_coords)

# Generar máscara de puntos dentro del polígono
points = np.vstack((xmesh.ravel(), ymesh.ravel())).T  # (N, 2)
mask = poly_path.contains_points(points).reshape(xmesh.shape)

# Modificar Zi dentro del polígono
Zi[mask] = -3

# Visualización
plt.imshow(Zi, extent=[xleft, xright, ybot, ytop],
           origin="lower", vmin=-1, vmax=1, cmap=plt.cm.bwr_r)

# Dibujar el polígono en la figura
poly_patch = Polygon(poly_coords, closed=True,
                     edgecolor="black", facecolor="none", linewidth=2)
plt.gca().add_patch(poly_patch)

plt.gca().set_aspect("equal")
plt.show()

# %---------------------------------------------------------------------
# BLOQUE: Suavizado que SOBREESCRIBE la variable 'Zi'
#---------------------------------------------------------------------
from scipy import ndimage

# Define la intensidad del suavizado.
sigma_suavizado = 50.0

# Aplica el filtro y actualiza la misma variable 'Zi'.
Zi = ndimage.gaussian_filter(Zi, sigma=sigma_suavizado)

# --- Visualización del resultado final ---
# Muestra el contenido de 'Zi' después de haber sido suavizada.
plt.figure(figsize=(7, 6))
plt.imshow(Zi, extent=[xleft, xright, ybot, ytop],
           origin="lower", vmin=-4, vmax=1, cmap=plt.cm.terrain)
plt.title("Batimetría Suavizada ('Zi' ya fue sobrescrita)")
plt.gca().set_aspect("equal")
plt.colorbar(label="Elevación (m)")
plt.show()

#%
plt.subplot(121)
plt.imshow(Zi,extent=[xleft, xright, ybot, ytop], origin="lower", vmin=-1, vmax=1, cmap=plt.cm.bwr_r)
plt.subplot(122)
plt.imshow(rgb,extent=extent, origin="upper")
plt.xlim(xleft , xright )
plt.ylim(ybot , ytop )
plt.tight_layout()
#Reviso que no hayan NaNs
nan_mask = np.isnan(Zi)
np.any(nan_mask)
#Como está tan seco pongo un zref
zref = 1.0
plt.subplot(121)
plt.imshow(Zi+zref,extent=[xleft, xright, ybot, ytop], origin="lower", vmin=-1, vmax=1, cmap=plt.cm.bwr_r)
plt.subplot(122)
plt.imshow(rgb,extent=extent, origin="upper")
plt.xlim(xleft , xright )
plt.ylim(ybot , ytop )
plt.tight_layout()
import numpy as np
import plotly.graph_objects as go
from PIL import Image



#% Ahora uso un módulo que hice para configurar celeri2
import celeris
c = celeris.Constants()
celeris_Zi = -(Zi + zref)
np.savetxt("bathy.txt", celeris_Zi, fmt="%.6f")

c.NLSW_or_Bous = 1
c.dx = mesh_resolution
c.dy = mesh_resolution
c.isManning = 1
c.friction = 0.015
c.base_depth = -np.min(celeris_Zi.flatten())
c.seaLevel = 0
c.zmin = celeris_Zi.min()
c.zmax = celeris_Zi.max()

c.HEIGHT, c.WIDTH = celeris_Zi.shape


c.west_boundary_type = 2
c.east_boundary_type = 1
c.south_boundary_type = 0
c.north_boundary_type = 0

c.showBreaking = 1

import json

# Path to save the JSON file
file_path = "./config.json"

# Save the dictionary as a JSON file
with open(file_path, "w") as json_file:
    json.dump(
        celeris.asdict(c), json_file, indent=4
    )  # Use `indent` for pretty formatting

celeris.write_waves(
    "waves_mono.txt",
    [celeris.Wave(amplitude=3, period=13, direction=0, phase=5.61043)],
    #[celeris.Wave(amplitude=0.2*4, period=60, direction=0, phase=5.61043)],
)

plt.pcolormesh(celeris_Zi, vmin=-3, vmax=3, cmap=plt.cm.bwr_r)
plt.colorbar()

#Overlay

x_overlay = np.arange(extent[0], extent[1], (extent[1]-extent[0])/rgb.shape[1])
y_overlay = np.arange(extent[3], extent[2], -(extent[3]-extent[2])/rgb.shape[0])
x_overlay.shape,y_overlay.shape, rgb.shape

x_overlay_mask = (
    (x_overlay>=xleft) & (x_overlay<=xright)
)
y_overlay_mask = (
    (y_overlay>=ybot) & (y_overlay<=ytop)
)
y_overlay_mask.shape

plt.imshow(rgb[y_overlay_mask,:,:][:,x_overlay_mask,:],extent=[xleft, xright, ybot, ytop], origin="upper")
plt.axis("off")
plt.savefig("overlay.png")


#% ver batimetria
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(111, projection="3d")
surf = ax.plot_surface(
    xmesh, ymesh, -Zi + zref,   # Usa la batimetría interpolada
    cmap="terrain",            # Colormap tipo terreno
    edgecolor="k",             # Bordes negros para ver la malla
    linewidth=0.3,             # Grosor de la malla
    antialiased=True,
    alpha=1
)
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=12, label="Profundidad (m)")
ax.view_init(elev=60, azim=45)
ax.set_xlim(xleft, xright)
ax.set_ylim(ybot, ytop)
ax.set_zlim(np.min(-Zi+zref), np.max(-Zi+zref))
plt.tight_layout()
plt.savefig("angle.png")
plt.show()

#%% wave
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)  # reproducibilidad

# Parámetros del mar
Hs = 3          # altura significativa [m]
Tp = 13.0         # periodo de pico [s]
gamma = 3.3       # factor de agudización JONSWAP
g = 9.81
N = 200           # número de ondas

# Frecuencia de pico y discretización
fp = 1.0 / Tp
f = np.linspace(0.5*fp, 3*fp, N)
df = f[1] - f[0]

# Espectro JONSWAP "crudo"
alpha = 0.076 * (Hs**2 * fp**4 / g**2)**0.22
sigma = np.where(f <= fp, 0.07, 0.09)
r = np.exp(- (f - fp)**2 / (2 * (sigma * fp)**2))
S_raw = alpha * g**2 * f**(-5) * np.exp(-1.25 * (fp/f)**4) * gamma**r

# Normalización: forzar que la integral del espectro corresponda a Hs
m0_raw = np.sum(S_raw * df)          # varianza original
m0_target = Hs**2 / 16               # varianza deseada
scale = m0_target / m0_raw
S = S_raw * scale                    # espectro ajustado

# Amplitudes de cada componente
a = np.sqrt(2.0 * S * df)

# Periodos, fases y direcciones
periods = 1.0 / f
phases = 2 * np.pi * np.random.rand(N)
directions = np.zeros(N)

# Escribir archivo directamente (SOBREESCRIBE waves_mono.txt)
with open("waves.txt", 'w') as fh:
    fh.write(f"[NumberOfWaves] {N}\n")
    fh.write("=================================\n")
    for ai, Ti, di, ph in zip(a, periods, directions, phases):
        fh.write(f"{ai:.6f}\t{Ti:.6f}\t{di:.6f}\t{ph:.6f}\n")

# Señal sintética (superposición de todas las ondas)
t = np.linspace(0, 200, 2000)
eta = np.zeros_like(t)
for ai, Ti, ph in zip(a, periods, phases):
    eta += ai * np.cos(2 * np.pi * t / Ti + ph)

# Graficar
plt.figure()
plt.plot(f, S)
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Energía [m²/Hz]")
plt.title(f"Espectro JONSWAP (γ={gamma})")
plt.grid()
plt.savefig("espectro_jonswap.png")
plt.show()

plt.figure()
plt.plot(t, eta)
plt.xlabel("Tiempo [s]")
plt.ylabel("Elevación [m]")
plt.title("Señal superficial sintética")
plt.grid()
plt.savefig("jonswap.png")
plt.show()
