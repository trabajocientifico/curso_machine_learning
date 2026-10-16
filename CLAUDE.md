# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es este repositorio

Material docente del **Módulo 2: Machine Learning para la Investigación** (30 horas, 100 % virtual) del **Diplomado en Inteligencia Artificial para la Investigación** del CENES, Facultad de Ciencias Económicas, Administrativas y Contables de la UPTC. El programa propuesto está en `Modulo_2_Machine_Learning_para_la_Investigacion.pdf` (temas 2.1 a 2.5, resultados de aprendizaje y tres ejercicios prácticos). No es una aplicación: son mazos de clase en HTML y notebooks de ejercicios. El énfasis del material es conceptual y aplicado a datos reales de Colombia (pobreza municipal, territorio, TRM).

Todo el contenido está en español (Colombia), con trato de «usted» en los textos dirigidos al estudiante y coma decimal en la prosa.

## Comandos

No hay build, linter ni pruebas.

- **Mazos HTML:** se abren directamente en el navegador; la entrada es `start index.html`. Solo necesitan internet para Google Fonts.
- **Notebooks** (ejecutar siempre desde `ejercicios_ml_colombia/`, porque leen `Path('datos')` relativo):
  - `pip install -r requirements.txt`
  - `jupyter notebook`
  - Reejecutar uno conservando las salidas: `jupyter nbconvert --to notebook --execute --inplace 01_random_forest_pobreza_municipal.ipynb`
  - Duración aproximada: 4 min (ej. 1), 1 min (ej. 2), 1 min (ej. 3).

## Estructura

### `index.html` (raíz)

Portada del módulo y punto de entrada, con cinco láminas: portada, perfil del docente, objetivo, «La ruta» (una tarjeta por tema 2.1–2.5 más los ejercicios) y «Conocer el curso» (formulario de entrada con `QR-formulario.png` y enlaces a un Apps Script). Usa la paleta y las fuentes de `index/FUNDAMENTOS.html` (blanco, azul `--st`, naranja `--ml`, Schibsted Grotesk y JetBrains Mono).

- A diferencia de los mazos de `index/`, aquí las láminas **sí** están en el HTML: cada una es un `<section class="slide">` con `data-block`, `data-title` y `data-sub`, de donde el motor arma el menú «Índice».
- Al añadir un mazo a `index/`, enlazarlo en la tarjeta de su tema con un `<a class="mod-tema" href="index/…">` y quitarle a la tarjeta la clase `soon` y el «Próximamente».
- La lámina del docente (`.pf`) y `oscar-vargas.png` son los datos personales del profesor: no cambiarlos sin que lo pida. Su contenido vigente salió de `diapositiva 2 y 3.html`, que el usuario usa como fuente.
- La portada entrena en vivo una regresión logística con rasgos polinomiales (Adam, 260 épocas) sobre tres conjuntos que se turnan (`CONJUNTOS`), y solo corre mientras la portada está activa.
- La comparación de la lámina del objetivo es un SVG generado en JS; su animación la hace el CSS con `.slide.active`, así que se repite cada vez que se entra.

### Mazos HTML (`index/`)

Cada archivo es autocontenido (CSS y JS en línea) y **tiene su propio motor de presentación; no comparten código**. Un cambio de comportamiento hay que hacerlo archivo por archivo.

| Archivo | Contenido | Motor |
|---|---|---|
| `FUNDAMENTOS.html` | 41 láminas en cuatro bloques: investigación y datos, con tipos de variables y variable dependiente/independiente (2–9); conceptos básicos: modelo (manzana y cuenca), algoritmo, IA y ML, qué es aprender, supervisado y no supervisado (10–19); ML frente a estadística (20–26) y flujo de trabajo en ML (27–41). Los dos primeros bloques abren con una lámina de ruta (`entrada()`) y cierran con un reto interactivo | GSAP embebido; arreglo `SLIDES` llenado con `slide({build(c){…}})`; escenario 1600×900 escalado con `fit()` |
| `FUNDAMENTOS-TECNICAS-GENERALIDADES.html` | 15 láminas: mapa de técnicas, una por lámina | JS puro; arreglo `D` de objetos con `steps`, `build`, `enter`; escenario 1280×720; admite `#n` en la URL para abrir en la lámina *n* |
| `animacion-ejemplo-regresion-lineal-simple.html` | Mínimos cuadrados en 9 pasos, con deslizadores de β₀ y β₁ (experiencia laboral e ingreso) | JS puro; arreglo `STEPS` declarativo (`t`, `s`, `show`); datos fijos en `DATA`; único con tema oscuro |
| `animacion-ejemplo-arbol-decision.html` | CART con Gini: deserción según aprobación y distancia a la sede | GSAP embebido; `build(s, T)` reconstruye el paso `s`; SVG 1600×900 |
| `animacion-ejemplo-random-forest-animado.html` | Bootstrap, árboles y votación, 7 láminas (fincas aptas para café según altitud y pendiente) | JS puro; `STEPS` de pares `[lámina, función]`; SVG 1280×720 |

Los `FUNDAMENTOS*` son las clases del tema 2.1; los `animacion-ejemplo-*` son demostraciones de una sola técnica (tema 2.2). Los temas 2.3, 2.4 y 2.5 aún no tienen mazo.

Convenciones:

- El contenido de las láminas se genera desde JS (el `<body>` casi no tiene marcado, salvo en la regresión lineal). Para cambiar un texto hay que buscarlo en el `<script>`.
- En los dos archivos con GSAP, el **primer** `<script>` es la librería minificada (~72 KB): no leerlo ni editarlo. El código propio está en el segundo.
- Navegación común: flecha derecha / abajo / espacio / PageDown avanzan, flecha izquierda / arriba / PageUp retroceden, `Home` vuelve al inicio y el clic avanza. `End` no existe en la regresión lineal, y `F` (pantalla completa) solo está en `FUNDAMENTOS.html`, el árbol y el random forest. `FUNDAMENTOS.html` tiene además un índice (botón «☰ Índice» o tecla `I`) que se arma solo a partir de `kicker` y `title` de cada lámina, con un enlace de vuelta a `index.html`. En el random forest el clic derecho retrocede.
- Los elementos con los que el público interactúa (clase `.interactive` en el mazo de técnicas, `#panel` en la regresión) no deben disparar el avance de lámina. En los retos de `FUNDAMENTOS.html` (láminas 9 y 19) el clic no avanza: se detiene en `c.root`; las flechas sí avanzan, y el primer → muestra la solución. Los ayudantes de juego (`arrastrable`, `svgPt`, `boton`, `marca`) están con los componentes.
- Los algoritmos se calculan de verdad en el navegador (CART, bootstrap, mínimos cuadrados) con un generador pseudoaleatorio de semilla fija: las cifras en pantalla salen del cálculo, no están escritas a mano.
- Todos respetan `prefers-reduced-motion`.
- Colores y tipografías son variables CSS en `:root`; cada mazo tiene su propia paleta.
- En `FUNDAMENTOS.html` las clases de texto (`.mono`, `.sm`, `.h3`…) fijan el color por CSS, así que un `fill` pasado como atributo no tiene efecto: el color propio va en `style`. Los comentarios `/* ---------- N · … */` numeran las láminas en orden; al insertar una hay que renumerarlos. Los ejemplos se comparten entre láminas desde «Datos compartidos»: `MUNI` (60 municipios: distancia a la capital del departamento e IPM), `STUD` (40 estudiantes) y `RIO` (lluvia y caudal de 60 días, con `sim`, `stor` y `rmse`); la deserción estudiantil es el ejemplo hilo de las láminas 2–7 y del bloque de flujo de trabajo. Los ejemplos se eligen del objetivo del módulo (pobreza, municipios, hogares, empresas, deserción); la única excepción deliberada es el modelo hidrológico de las láminas 12–14 (la calibración de k reaparece en la 13 como ejemplo de algoritmo), que muestra un modelo basado en teoría. La lámina «Objetivo» de `index.html` repite el generador de `MUNI`.

### `ejercicios_ml_colombia/`

Tres notebooks **ya ejecutados y comentados**, para usar en clase o en Google Colab. Las fuentes de los datos y el contenido de cada CSV están en `ejercicios_ml_colombia/README.md`.

| Notebook | Técnica | Datos |
|---|---|---|
| `01_random_forest_pobreza_municipal.ipynb` | Random Forest de regresión, validación agrupada por departamento, importancia por permutación, dependencia parcial | `ej1_ipm_covariables_2018.csv` |
| `02_kmeans_pca_tipologias_municipales.ipynb` | PCA + K-Means, codo y silueta, estabilidad (ARI) | `ej2_privaciones_ipm_2018.csv` |
| `03_arima_vs_gradient_boosting_trm.ipynb` | ARIMA frente a Gradient Boosting, origen móvil, Diebold-Mariano | `ej3_trm_diaria.csv` |

Convenciones:

- Las dos primeras celdas de código son iguales en los tres: imports + `DATOS = Path('datos')` + `SEMILLA = 42`, y el bloque «Estilo gráfico común» (constantes `AZUL`, `NARANJA`, `AQUA`, `ROJO`, `GRIS`, `TINTA`, `TINTA2`, mapas de color `SEQ` y `DIV`, y `mpl.rcParams`). Un notebook nuevo debe copiar ese bloque y usar esas constantes en vez de colores sueltos.
- Secciones numeradas (`## 1.`, `## 2.`…). Después de cada celda de código hay una celda de texto que **interpreta el resultado citando las cifras obtenidas**: si cambia el código o los datos, hay que reejecutar y actualizar esas cifras en la prosa.
- Cada notebook cierra con «Conclusiones» y una lista de retos para los estudiantes.
- Siempre hay una línea base contra la cual comparar (regresión lineal, paseo aleatorio) y una validación exigente (por departamento, origen móvil); el mensaje pedagógico depende de esa comparación.
- Los mapas unen `municipios_colombia.geojson` por `cod_mpio` y usan `encuadre(ax)` para recortar a Colombia continental.
- Los notebooks se guardan con salidas (entre 0,6 y 1 MB cada uno): no limpiarlas.

## Cosas a tener en cuenta

- `ejercicios_ml_colombia/ejercicios_ml_colombia/01_random_forest_pobreza_municipal.ipynb` es una copia del notebook 1 que solo difiere en la versión del kernel guardada en los metadatos. La versión de trabajo es la del nivel superior.
- La carpeta `CURSO - MACHINE LEARNING/` contiene 89 SVG numerados (unos 72 MB en total): no leerlos ni añadirlos a git sin que lo pidan.
