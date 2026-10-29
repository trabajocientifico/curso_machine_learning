# Ejercicios de aprendizaje automático con datos reales de Colombia

Notebooks de Python, ejecutados y comentados, listos para usar en clase. Hay dos tipos de notebook. Las **prácticas por técnica** se nombran por tema (`2-1-…`, `2-2-…`, `2-3-…`) y acompañan a la clase del mismo nombre; las del 2.1 y el 2.2 usan bases simuladas con fines didácticos y las del 2.3 (K-means, componentes principales y detección de anomalías) usan los municipios reales del ejercicio 02. Los **ejercicios integradores 01 a 03** son los del programa del módulo y usan datos reales.

| Notebook | Técnica | Datos |
|---|---|---|
| `2-1-ingenieria-caracteristicas.ipynb` | Las 8 situaciones del mazo de ingeniería de características (faltantes, categóricas, distribución, discretización, atípicos, escalamiento, selección, creación) y una tubería final contra la línea base | 600 hogares **simulados** con fines didácticos (`2-1-ingenieria-caracteristicas.xlsx`), al estilo de una encuesta de hogares |
| `2-2-regresion-lineal.ipynb` | Regresión lineal simple y múltiple (MCO con `statsmodels` y `scikit-learn`), supuestos, log del ingreso, variables ficticias, multicolinealidad (VIF), métricas MAE, RMSE, R² y R² ajustado contra una línea base, Ridge y Lasso | 800 personas ocupadas **simuladas** (`2-2-regresion-lineal.xlsx`), ecuación de Mincer |
| `2-2-regresion-logistica.ipynb` | Regresión logística simple y múltiple: por qué no una recta, curva S, máxima verosimilitud, odds ratio, umbral y matriz de confusión, exactitud, precisión, sensibilidad, F1 y AUC contra una línea base, curva ROC, regularización C y `class_weight` | 1.000 estudiantes de primer año **simulados** (`2-2-regresion-logistica.xlsx`), ecuación logística conocida |
| `2-2-arbol-decision.ipynb` | Árbol de decisión (CART): preguntas en cadena, impureza de Gini calculada a mano, reglas de cada hoja, profundidad y sobreajuste, `max_depth`/`min_samples_leaf`/`ccp_alpha` con validación cruzada, métricas contra la línea base y la logística, ROC, importancia | 1.200 hogares **simulados** (`2-2-hogares-subsidio.xlsx`), pobreza con umbrales e interacciones |
| `2-2-random-forest.ipynb` | Random forest con los mismos hogares: inestabilidad de un árbol, bootstrap, votación, error OOB, número de árboles, `max_features`/`min_samples_leaf`, comparación con logística y árbol, importancia por impureza y por permutación, dependencia parcial | `2-2-hogares-subsidio.xlsx` (la misma base del árbol) |
| `2-2-k-vecinos.ipynb` | k vecinos más cercanos (kNN) con los mismos hogares: por qué escalar, los vecinos de un hogar, mapas de decisión con k = 1, 9 y 75, k con validación cruzada, más variables frente a pocas (maldición de la dimensión), comparación con línea base, logística y árbol, ROC | `2-2-hogares-subsidio.xlsx` (la misma base) |
| `2-2-svm.ipynb` | Máquinas de soporte vectorial (SVM): margen duro y vectores de soporte, escalar, margen suave y C, kernel RBF y gamma, kernel/C/gamma con validación cruzada, del puntaje a la probabilidad, comparación con logística, árbol, random forest y kNN | `2-2-hogares-subsidio.xlsx` (la misma base) |
| `2-3-k-means.ipynb` | K-means con datos reales: por qué escalar, el algoritmo a mano, mínimos locales y varios inicios, codo y silueta, silueta de cada municipio, perfil de los grupos con el IPM como validación externa, mapa y regiones, estabilidad (ARI), línea base con terciles del IPM y agrupación con las 15 privaciones | `ej2_privaciones_ipm_2018.csv` (1.122 municipios **reales**; la misma base del ejercicio 02) |
| `2-3-pca.ipynb` | Componentes principales: correlaciones, PCA a mano con dos variables, por qué escalar, varianza explicada y criterios (codo, autovalor mayor que 1, 70 %), cargas, plano PC1 × PC2, índice compuesto frente al IPM y al promedio simple (línea base), mapas, estabilidad de las cargas y PCA + K-means | `ej2_privaciones_ipm_2018.csv` (1.122 municipios **reales**) |
| `2-3-anomalias.ipynb` | Detección de anomalías: z y la caja, distancia de Mahalanobis, Isolation Forest y LOF; comparación entre métodos (globales y locales), mapa, evaluación con 30 errores de digitación sembrados (precisión y sensibilidad según cuántos casos se revisan) y un puente con el error de reconstrucción de PCA | `ej2_privaciones_ipm_2018.csv` (1.122 municipios **reales**) |
| `01_random_forest_pobreza_municipal.ipynb` | Random Forest (regresión), validación espacial, importancia por permutación, dependencia parcial | IPM municipal DANE (CNPV 2018) + registros administrativos 2018 (salud, educación, servicios, recaudo) y luces nocturnas VIIRS, 1.121 municipios |
| `02_kmeans_pca_tipologias_municipales.ipynb` | PCA + K-Means, codo y silueta, perfilado, estabilidad (ARI) | 15 privaciones del IPM municipal DANE (CNPV 2018), 1.122 municipios |
| `03_arima_vs_gradient_boosting_trm.ipynb` | ARIMA (Box-Jenkins), Gradient Boosting con rezagos, evaluación con origen móvil, prueba de Diebold-Mariano | TRM diaria del Banco de la República, 1991–2026, agregada a promedio mensual |

## Cómo usarlos

**En Google Colab:** abra el notebook, cree una carpeta `datos` en el panel de archivos y suba ahí los archivos de la carpeta `datos/` de este paquete. Colab ya trae todas las librerías salvo `geopandas` en algunas versiones (`!pip install geopandas`).

**En su computador:** `pip install -r requirements.txt` y abra los notebooks desde esta carpeta.

Tiempo de ejecución aproximado en una máquina de 2 núcleos: 4 min (ej. 1), 1 min (ej. 2), 1 min (ej. 3), menos de 1 min (prácticas 2-1, 2-2 y 2-3).

## Carpeta `datos/`

| Archivo | Contenido |
|---|---|
| `2-1-ingenieria-caracteristicas.xlsx` | Hoja `hogares`: 600 hogares simulados (19 columnas, con faltantes, texto, cola larga y errores de digitación a propósito). Hoja `diccionario`: qué es cada variable y en qué situación del mazo se usa |
| `2-2-regresion-lineal.xlsx` | Hoja `trabajadores`: 800 personas ocupadas simuladas (edad, educación, experiencia, horas, formalidad, sexo, zona, sector, estrato, ingreso). Hoja `diccionario` |
| `2-2-regresion-logistica.xlsx` | Hoja `estudiantes`: 1.000 estudiantes de primer año simulados (sede, zona de origen, sexo, edad, Saber 11, distancia a la sede, estrato, trabajo, beca, primera generación, promedio del primer semestre y deserción). Hoja `diccionario` |
| `2-2-hogares-subsidio.xlsx` | Hoja `hogares`: 1.200 hogares simulados (tipo de municipio, zona, personas, menores de 5, adultos mayores, educación y sexo de quien encabeza el hogar, ocupados, ingreso por persona, cuartos, hacinamiento, acueducto, piso de tierra, internet, régimen de salud y pobre). Hoja `diccionario`. La usan las prácticas de árbol, random forest, k vecinos y SVM |
| `2-3-mipymes-boyaca.xlsx` | Base para pedirle a una IA las técnicas no supervisadas del tema 2.3. Hoja `empresas`: 1.000 MiPymes de Boyacá **simuladas** (municipio, provincia, zona, sector, distancia a Tunja; 13 variables numéricas: antigüedad, empleados, ventas, activos, empleo formal, educación del gerente, digitalización, ventas en línea, capacitación, exportación, innovación, deuda y margen; para validar, crecimiento de las ventas y supervivencia a 3 años). Tiene cuatro segmentos latentes, dos factores (tamaño y formalidad; digital frente a industrial), ~2 % de faltantes en dos variables y 30 anomalías sembradas. Hoja `diccionario`. Hoja `que_pedir`: para K-means, PCA, anomalías y PCA + K-means, la pregunta, las variables, dos prompts (uno corto para que la IA haga el análisis con el archivo adjunto y otro para que cree un .py y un .ipynb con la optimización de k, del número de componentes o de los parámetros de los detectores), qué revisar en la respuesta y qué debería encontrar (cifras calculadas con scikit-learn). Hoja `clave_docente`: el segmento simulado de cada empresa y las anomalías sembradas; **se borra antes de entregar el archivo** |
| `ej1_ipm_covariables_2018.csv` | IPM municipal 2018 y 17 covariables administrativas y satelitales |
| `ej2_privaciones_ipm_2018.csv` | Las 15 privaciones del IPM y el IPM por municipio, con región natural. La usan el ejercicio 02 y las prácticas 2-3 de K-means, componentes principales y detección de anomalías |
| `ej3_trm_diaria.csv` | TRM diaria, 27-nov-1991 a 28-ago-2026 |
| `ej3_trm_mensual.csv` | TRM promedio mensual |
| `municipios_colombia.geojson` | Límites municipales (MGN 2018, DANE), geometría simplificada para mapas |

## Fuentes

- IPM municipal por privación (DANE, CNPV 2018) y covariables administrativas: repositorio público [BrySB/TG_MCD_Grupo5_SAE_Pobreza_2026](https://github.com/BrySB/TG_MCD_Grupo5_SAE_Pobreza_2026) (Salgado, Caicedo y Trochez, Maestría en Ciencia de Datos, PUJ Cali), que compila datos del DANE, MinSalud (BDUA), MEN, UPME y VIIRS.
- TRM: serie del Banco de la República publicada en el repositorio [Juanhv24/Time-Series-Colombia](https://github.com/Juanhv24/Time-Series-Colombia) (Universidad de La Salle).
- Límites municipales: Marco Geoestadístico Nacional 2018 del DANE, vía [caticoa3/colombia_mapa](https://github.com/caticoa3/colombia_mapa).

Las regiones naturales (Andina, Caribe, Pacífica, Orinoquía, Amazonía) se asignaron por departamento; es una simplificación, porque varios departamentos tienen territorio en más de una región.
