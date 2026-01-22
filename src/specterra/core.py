"""
Módulo core de specterra - Clase principal para imágenes satelitales
"""

import numpy as np
from pathlib import Path
from typing import Dict, Optional, Union
import warnings


# ========== CONFIGURACIÓN DE BANDAS POR SENSOR ==========

SENSOR_CONFIG = {
    'landsat9c2': {
        'name': 'Landsat 9 Collection 2',
        'file_pattern': {
            'coastal': '*_SR_B1.TIF',
            'blue': '*_SR_B2.TIF',
            'green': '*_SR_B3.TIF',
            'red': '*_SR_B4.TIF',
            'nir': '*_SR_B5.TIF',
            'swir1': '*_SR_B6.TIF',
            'swir2': '*_SR_B7.TIF',
        },
        'scale_factor': 0.0000275,
        'offset': -0.2,
    },
    
    'landsat8c2': {
        'name': 'Landsat 8 Collection 2',
        'file_pattern': {
            'coastal': '*_SR_B1.TIF',
            'blue': '*_SR_B2.TIF',
            'green': '*_SR_B3.TIF',
            'red': '*_SR_B4.TIF',
            'nir': '*_SR_B5.TIF',
            'swir1': '*_SR_B6.TIF',
            'swir2': '*_SR_B7.TIF',
        },
        'scale_factor': 0.0000275,
        'offset': -0.2,
    },
    
    'sentinel2': {
        'name': 'Sentinel-2 L2A',
        'file_pattern': {
            'coastal': '*_B01_*.jp2',      # 60m
            'blue': '*_B02_*.jp2',         # 10m
            'green': '*_B03_*.jp2',        # 10m
            'red': '*_B04_*.jp2',          # 10m
            'rededge1': '*_B05_*.jp2',     # 20m
            'rededge2': '*_B06_*.jp2',     # 20m
            'rededge3': '*_B07_*.jp2',     # 20m
            'nir': '*_B08_*.jp2',          # 10m
            'nir_narrow': '*_B8A_*.jp2',   # 20m
            'swir1': '*_B11_*.jp2',        # 20m
            'swir2': '*_B12_*.jp2',        # 20m
        },
        'scale_factor': 0.0001,  # Sentinel-2 L2A viene en valores enteros (0-10000)
        'offset': 0.0,
    },
}


# ========== CLASE PRINCIPAL ==========

class SatelliteImage:
    """
    Clase para cargar y procesar imágenes satelitales multiespectrales.
    
    Soporta:
    - Landsat 8/9 Collection 2
    - Sentinel-2 L2A
    
    Attributes:
    -----------
    path : Path
        Ruta al directorio con las bandas
    sensor : str
        Tipo de sensor
    bands : dict
        Diccionario con bandas cargadas (nombres abstractos: 'red', 'nir', etc.)
    metadata : dict
        Metadatos geoespaciales
    """
    
    def __init__(self, path: Union[str, Path], sensor: str = 'landsat9c2'):
        """
        Inicializa la imagen satelital.
        
        Parameters:
        -----------
        path : str or Path
            Ruta al directorio que contiene las bandas
        sensor : str
            Tipo de sensor: 'landsat9c2', 'landsat8c2', 'sentinel2'
        """
        self.path = Path(path)
        self.sensor = sensor
        self.bands = {}
        self.metadata = None
        
        if sensor not in SENSOR_CONFIG:
            raise ValueError(f"Sensor '{sensor}' no soportado. Opciones: {list(SENSOR_CONFIG.keys())}")
        
        self.config = SENSOR_CONFIG[sensor]
        self._load_bands()
    
    def _load_bands(self):
        """Carga las bandas desde archivos usando rasterio."""
        import rasterio
        import glob
        import os
        
        file_patterns = self.config['file_pattern']
        scale = self.config['scale_factor']
        offset = self.config['offset']
        
        print(f"🛰️  Cargando {self.config['name']}...")
        
        for band_name, pattern in file_patterns.items():
            # Buscar archivo de banda
            files = glob.glob(os.path.join(str(self.path), pattern))
            
            if not files:
                warnings.warn(f"⚠️  No se encontró banda '{band_name}' con patrón {pattern}")
                continue
            
            # Leer la banda
            with rasterio.open(files[0]) as src:
                data = src.read(1).astype(np.float32)
                
                # Aplicar escala y offset
                self.bands[band_name] = data * scale + offset
                
                # Guardar metadatos de la primera banda
                if self.metadata is None:
                    self.metadata = {
                        'crs': src.crs,
                        'transform': src.transform,
                        'width': src.width,
                        'height': src.height,
                        'bounds': src.bounds,
                        'sensor': self.config['name']
                    }
        
        print(f"✓ Cargadas {len(self.bands)} bandas: {list(self.bands.keys())}")
    
    def get_band(self, name: str) -> np.ndarray:
        """
        Obtiene una banda por su nombre abstracto.
        
        Parameters:
        -----------
        name : str
            Nombre de la banda ('red', 'nir', 'swir1', etc.)
        
        Returns:
        --------
        np.ndarray
            Array con los valores de la banda
        """
        if name not in self.bands:
            available = list(self.bands.keys())
            raise KeyError(f"Banda '{name}' no disponible. Bandas cargadas: {available}")
        return self.bands[name]
    
    def plot_rgb(self, r='red', g='green', b='blue', stretch=2, figsize=(12, 10)):
        """
        Visualiza composición RGB.
        
        Parameters:
        -----------
        r, g, b : str
            Nombres de bandas para canales RGB (default: 'red', 'green', 'blue')
        stretch : float
            Percentil para stretch de contraste (default=2)
        figsize : tuple
            Tamaño de la figura
        """
        import matplotlib.pyplot as plt
        
        # Verificar bandas
        for band_name in [r, g, b]:
            if band_name not in self.bands:
                raise ValueError(f"Banda '{band_name}' no disponible. Opciones: {list(self.bands.keys())}")
        
        # Obtener bandas
        red_band = self.get_band(r)
        green_band = self.get_band(g)
        blue_band = self.get_band(b)
        
        # Normalizar
        def normalize(band, stretch_pct=2):
            band_clip = np.clip(band, 0, 1)
            valid = band_clip[band_clip > 0]
            if len(valid) == 0:
                return band_clip
            p_low = np.percentile(valid, stretch_pct)
            p_high = np.percentile(valid, 100 - stretch_pct)
            return np.clip((band_clip - p_low) / (p_high - p_low + 1e-10), 0, 1)
        
        # Crear RGB
        rgb = np.dstack([
            normalize(red_band, stretch),
            normalize(green_band, stretch),
            normalize(blue_band, stretch)
        ])
        
        # Plotear
        fig, ax = plt.subplots(figsize=figsize)
        ax.imshow(rgb)
        ax.set_title(f"RGB ({r.upper()}, {g.upper()}, {b.upper()}) - {self.config['name']}", 
                    fontsize=14, fontweight='bold')
        ax.axis('off')
        plt.tight_layout()
        plt.show()
        
        return fig
    
    def __repr__(self):
        return f"SatelliteImage(sensor='{self.sensor}', bands={len(self.bands)}, size={self.metadata['width']}x{self.metadata['height']})"


# ========== FUNCIÓN DE CARGA ==========

def load(path: Union[str, Path], sensor: str = 'landsat9c2') -> SatelliteImage:
    """
    Carga una imagen satelital.
    
    Parameters:
    -----------
    path : str or Path
        Ruta al directorio con las bandas
    sensor : str
        Tipo de sensor: 'landsat9c2', 'landsat8c2', 'sentinel2'
    
    Returns:
    --------
    SatelliteImage
        Imagen satelital cargada
    
    Examples:
    ---------
    >>> import specterra
    >>> img = specterra.load("path/to/landsat/", sensor='landsat9c2')
    >>> img.plot_rgb()
    """
    import os
    if not os.path.exists(path):
        raise FileNotFoundError(f"No existe la ruta: {path}")
    
    return SatelliteImage(path, sensor=sensor)
