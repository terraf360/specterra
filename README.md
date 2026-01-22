# specterra 🛰️

**Procesamiento de imágenes satelitales multiespectrales para exploración mineral**

Librería Python para cargar, procesar y analizar imágenes de satélite (Landsat, Sentinel-2) con enfoque en exploración geológica y minera.

## ✨ Características

- 🎯 **Multi-sensor**: Soporta Landsat 8/9 Collection 2 y Sentinel-2 L2A
- 🗺️ **Bandas abstractas**: Usa nombres consistentes (`red`, `nir`, `swir1`) independientes del sensor
- 📊 **Índices espectrales**: Biblioteca completa para detección de minerales
- 🎨 **Visualización**: Composiciones RGB y mapas de índices

## 🚀 Instalación

```bash
# Crear ambiente conda
conda env create -f environment.yml
conda activate specterra

# O instalar con pip
pip install specterra
```

## 📖 Uso básico

```python
import specterra

# Cargar imagen Landsat 9
img = specterra.load("path/to/landsat9/", sensor='landsat9c2')

# Visualizar RGB natural
img.plot_rgb()

# O Sentinel-2
sentinel = specterra.load("path/to/sentinel/", sensor='sentinel2')
sentinel.plot_rgb()
```

## 🎓 Sensores soportados

| Sensor | Código | Bandas |
|--------|--------|--------|
| Landsat 9 C2 | `landsat9c2` | coastal, blue, green, red, nir, swir1, swir2 |
| Landsat 8 C2 | `landsat8c2` | coastal, blue, green, red, nir, swir1, swir2 |
| Sentinel-2 L2A | `sentinel2` | coastal, blue, green, red, rededge1-3, nir, nir_narrow, swir1, swir2 |

## 📁 Estructura del proyecto

```
specterra/
├── src/specterra/
│   ├── __init__.py
│   └── core.py          # Clase principal SatelliteImage
├── ejemplos/
│   └── ejemplo_basico.py
├── environment.yml
├── pyproject.toml
└── README.md
```

## 🤝 Contribuir

Este es el primer repositorio de la suite **terraf360**:
- **specterra** - Imágenes satelitales (este repo)
- **magneterra** - Magnetometría
- **graviterra** - Gravimetría
- **lidarmine** - Topografía/LiDAR
- **geolearn** - Machine Learning geológico

## 📄 Licencia

MIT License
