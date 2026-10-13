# Ejercicios de aprendizaje automático con datos reales de Colombia

Tres notebooks de Python, ejecutados y comentados, listos para usar en clase.

| Notebook | Técnica | Datos |
|---|---|---|
| `01_random_forest_pobreza_municipal.ipynb` | Random Forest (regresión), validación espacial, importancia por permutación, dependencia parcial | IPM municipal DANE (CNPV 2018) + registros administrativos 2018 (salud, educación, servicios, recaudo) y luces nocturnas VIIRS, 1.121 municipios |
| `02_kmeans_pca_tipologias_municipales.ipynb` | PCA + K-Means, codo y silueta, perfilado, estabilidad (ARI) | 15 privaciones del IPM municipal DANE (CNPV 2018), 1.122 municipios |
| `03_arima_vs_gradient_boosting_trm.ipynb` | ARIMA (Box-Jenkins), Gradient Boosting con rezagos, evaluación con origen móvil, prueba de Diebold-Mariano | TRM diaria del Banco de la República, 1991–2026, agregada a promedio mensual |

## Cómo usarlos

**En Google Colab:** abra el notebook, cree una carpeta `datos` en el panel de archivos y suba ahí los archivos de la carpeta `datos/` de este paquete. Colab ya trae todas las librerías salvo `geopandas` en algunas versiones (`!pip install geopandas`).

**En su computador:** `pip install -r requirements.txt` y abra los notebooks desde esta carpeta.

Tiempo de ejecución aproximado en una máquina de 2 núcleos: 4 min (ej. 1), 1 min (ej. 2), 1 min (ej. 3).

## Carpeta `datos/`

| Archivo | Contenido |
|---|---|
| `ej1_ipm_covariables_2018.csv` | IPM municipal 2018 y 17 covariables administrativas y satelitales |
| `ej2_privaciones_ipm_2018.csv` | Las 15 privaciones del IPM y el IPM por municipio, con región natural |
| `ej3_trm_diaria.csv` | TRM diaria, 27-nov-1991 a 28-ago-2026 |
| `ej3_trm_mensual.csv` | TRM promedio mensual |
| `municipios_colombia.geojson` | Límites municipales (MGN 2018, DANE), geometría simplificada para mapas |

## Fuentes

- IPM municipal por privación (DANE, CNPV 2018) y covariables administrativas: repositorio público [BrySB/TG_MCD_Grupo5_SAE_Pobreza_2026](https://github.com/BrySB/TG_MCD_Grupo5_SAE_Pobreza_2026) (Salgado, Caicedo y Trochez, Maestría en Ciencia de Datos, PUJ Cali), que compila datos del DANE, MinSalud (BDUA), MEN, UPME y VIIRS.
- TRM: serie del Banco de la República publicada en el repositorio [Juanhv24/Time-Series-Colombia](https://github.com/Juanhv24/Time-Series-Colombia) (Universidad de La Salle).
- Límites municipales: Marco Geoestadístico Nacional 2018 del DANE, vía [caticoa3/colombia_mapa](https://github.com/caticoa3/colombia_mapa).

Las regiones naturales (Andina, Caribe, Pacífica, Orinoquía, Amazonía) se asignaron por departamento; es una simplificación, porque varios departamentos tienen territorio en más de una región.
