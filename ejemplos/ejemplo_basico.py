"""
Ejemplo básico: Cargar y visualizar imágenes Landsat 9 y Sentinel-2
"""

import specterra

# ========== LANDSAT 9 ==========
print("=" * 60)
print("EJEMPLO 1: Landsat 9 Collection 2")
print("=" * 60)

landsat = specterra.load(
    path=r"../datos/casos_estudio/oaxaca/landsat9/LC09_L2SP_024048_20260110_20260111_02_T1",
    sensor='landsat9c2'
)

print(f"\n{landsat}\n")
print(f"Bandas disponibles: {list(landsat.bands.keys())}")

# RGB natural (Red, Green, Blue)
landsat.plot_rgb(r='red', g='green', b='blue')


# ========== SENTINEL-2 (cuando tengas datos) ==========
"""
print("=" * 60)
print("EJEMPLO 2: Sentinel-2 L2A")
print("=" * 60)

sentinel = specterra.load(
    path=r"path/to/sentinel2/",
    sensor='sentinel2'
)

print(f"\n{sentinel}\n")
print(f"Bandas disponibles: {list(sentinel.bands.keys())}")

# RGB natural
sentinel.plot_rgb(r='red', g='green', b='blue')

# Sentinel-2 tiene Red Edge - puedes hacer composiciones especiales
sentinel.plot_rgb(r='nir', g='red', b='green')  # False color
"""
