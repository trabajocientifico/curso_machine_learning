from pathlib import Path  # Importa Path para construir rutas a carpetas y archivos.
import numpy as np  # Importa NumPy para simular las variables con distribuciones realistas.
import pandas as pd  # Importa pandas para armar la tabla y guardarla en Excel.
from openpyxl.styles import Alignment, Font, PatternFill  # Importa estilos para dar formato a las hojas de Excel.

CARPETA_PROYECTO = Path(__file__).resolve().parent  # Obtiene la ubicación de este script.
CARPETA_DATOS = CARPETA_PROYECTO / "datos"  # Define la carpeta donde se guardará la base de datos.
ARCHIVO_DATOS = CARPETA_DATOS / "desercion_escolar.xlsx"  # Define la ruta del archivo Excel de salida.
SEMILLA = 2026  # Fija la semilla para que la base sea siempre la misma.
N = 20000  # Define el número de estudiantes de la base.
CUPOS_PROGRAMA = 1500  # Define los cupos del programa de alerta temprana usados en la pregunta 2.
rng = np.random.default_rng(SEMILLA)  # Crea el generador de números aleatorios reproducible.


def sigmoide(x):  # Define la función logística que convierte un puntaje latente en probabilidad.
    return 1 / (1 + np.exp(-x))  # Devuelve una probabilidad entre 0 y 1.


def generar_estudiantes():  # Genera las 20 variables siguiendo relaciones causales plausibles.
    # --- Territorio y características personales ---
    regiones = np.array(["Andina", "Caribe", "Pacífica", "Orinoquía", "Amazonía"])  # Lista las regiones naturales de Colombia.
    region = rng.choice(regiones, N, p=[0.52, 0.24, 0.11, 0.07, 0.06])  # Asigna la región con pesos cercanos a la matrícula oficial.
    prob_rural = pd.Series(region).map({"Andina": 0.22, "Caribe": 0.30, "Pacífica": 0.45, "Orinoquía": 0.38, "Amazonía": 0.50}).to_numpy()  # Define la probabilidad de ruralidad según la región.
    rural = rng.random(N) < prob_rural  # Determina si el estudiante vive en zona rural.
    hombre = rng.random(N) < 0.51  # Asigna el sexo con una leve mayoría de hombres en secundaria oficial.
    grado = rng.choice(np.arange(6, 12), N, p=[0.19, 0.18, 0.17, 0.16, 0.155, 0.145])  # Asigna el grado con menos estudiantes en grados altos por la deserción acumulada.

    prob_afro = pd.Series(region).map({"Andina": 0.04, "Caribe": 0.15, "Pacífica": 0.55, "Orinoquía": 0.03, "Amazonía": 0.03}).to_numpy()  # Define la proporción afrocolombiana por región.
    prob_indigena = pd.Series(region).map({"Andina": 0.04, "Caribe": 0.08, "Pacífica": 0.10, "Orinoquía": 0.12, "Amazonía": 0.35}).to_numpy() * np.where(rural, 1.6, 0.6)  # Define la proporción indígena, mayor en zona rural.
    u = rng.random(N)  # Genera un número uniforme para elegir la etnia.
    etnia = np.where(u < prob_afro, "Afrocolombiana", np.where(u < prob_afro + prob_indigena, "Indígena", np.where(u < prob_afro + prob_indigena + 0.01, "Otra", "Ninguna")))  # Asigna la etnia según las proporciones anteriores.

    # --- Nivel socioeconómico del hogar (variable latente que no se publica) ---
    efecto_region = pd.Series(region).map({"Andina": 0.0, "Caribe": -0.25, "Pacífica": -0.6, "Orinoquía": -0.15, "Amazonía": -0.4}).to_numpy()  # Define la brecha socioeconómica regional.
    nse = rng.normal(0, 1, N) - 0.7 * rural + efecto_region - 0.3 * (etnia != "Ninguna")  # Construye el nivel socioeconómico latente del hogar.

    estrato_latente = nse + rng.normal(0, 0.5, N)  # Añade ruido porque el estrato no refleja perfectamente el bienestar del hogar.
    cortes_estrato = np.quantile(estrato_latente, [0.40, 0.75, 0.93, 0.98, 0.995])  # Fija cortes para obtener la distribución típica de colegios oficiales.
    estrato = np.digitize(estrato_latente, cortes_estrato) + 1  # Convierte el puntaje latente en estratos de 1 a 6.
    estrato = np.where(rural, np.minimum(estrato, 3), estrato)  # Limita el estrato rural a 3 como ocurre en la estratificación real.

    ingreso = np.exp(np.log(1.2) + 0.30 * (estrato - 1) + 0.30 * nse + rng.normal(0, 0.40, N))  # Simula el ingreso del hogar en salarios mínimos con distribución log-normal.
    ingreso = np.round(np.clip(ingreso, 0.15, None), 2)  # Evita ingresos casi nulos y redondea a dos decimales.

    niveles_madre = np.array(["Ninguna", "Primaria", "Secundaria", "Técnica", "Universitaria"])  # Lista los niveles educativos de la madre en orden.
    madre_latente = 0.8 * nse + rng.normal(0, 0.6, N)  # Relaciona la educación de la madre con el nivel socioeconómico.
    nivel_madre = np.digitize(madre_latente, np.quantile(madre_latente, [0.05, 0.35, 0.75, 0.90]))  # Convierte el puntaje en cinco niveles ordenados (0 a 4).
    educacion_madre = niveles_madre[nivel_madre]  # Asigna la etiqueta del nivel educativo.

    hermanos = np.clip(rng.poisson(np.exp(0.75 + 0.25 * rural - 0.18 * nivel_madre)), 0, 9)  # Simula más hermanos en hogares rurales y con menor educación materna.

    # --- Trayectoria escolar ---
    repitencias = np.clip(rng.poisson(np.exp(-1.5 - 0.40 * nse + 0.25 * hombre + 0.20 * rural)), 0, 3)  # Simula los años repetidos (no se publica, se infiere de la extraedad).
    ingreso_tardio = (rng.random(N) < 0.08 + 0.07 * rural).astype(int)  # Simula el ingreso tardío al sistema escolar, más común en zona rural.
    extraedad = repitencias + ingreso_tardio  # Calcula los años de rezago respecto a la edad esperada.
    edad = grado + 5 + extraedad + (rng.random(N) < 0.5)  # Calcula la edad sumando el rezago y el mes de nacimiento.

    distancia = np.where(rural, rng.gamma(2.0, 3.5, N), rng.gamma(2.0, 0.8, N))  # Simula distancias mayores al colegio en zona rural.
    distancia = np.round(np.clip(distancia, 0.1, 45), 1)  # Limita la distancia a valores plausibles y redondea.

    internet = rng.random(N) < sigmoide(1.0 + 1.2 * nse - 1.8 * rural)  # Simula el acceso a internet según bienestar y zona.
    pae = rng.random(N) < sigmoide(2.2 - 0.9 * (estrato - 1) + 0.8 * rural)  # Simula la cobertura del PAE, focalizada en estratos bajos con errores.
    transferencia = rng.random(N) < sigmoide(-1.2 + 2.0 * (ingreso < 1.0) + 0.5 * rural - 0.6 * (estrato >= 3) + 0.15 * hermanos)  # Simula las transferencias condicionadas con errores de inclusión y exclusión.
    riesgo_conflicto = pd.Series(region).map({"Andina": 0.0, "Caribe": 0.4, "Pacífica": 1.2, "Orinoquía": 0.9, "Amazonía": 0.6}).to_numpy()  # Define la exposición al conflicto armado por región.
    victima = rng.random(N) < sigmoide(-2.6 + riesgo_conflicto + 0.8 * rural)  # Simula la condición de víctima del conflicto.

    trabaja = rng.random(N) < sigmoide(-4.0 + 0.5 * (edad - 12) - 0.8 * nse + 0.6 * rural + 0.5 * hombre + 0.4 * victima - 0.5 * transferencia)  # Simula el trabajo infantil y juvenil.
    horas = np.where(trabaja, np.clip(np.round(6 + rng.gamma(2.0, 5.0 + 2.5 * rural + 1.5 * (nse < -1), N)), 4, 60), 0).astype(int)  # Simula horas semanales trabajadas, más altas en hogares pobres y rurales.

    estudiantes_docente = np.where(rural, rng.normal(18, 6, N), rng.normal(32, 5, N)) + 3 * (region == "Caribe")  # Simula la razón estudiantes por docente del colegio.
    estudiantes_docente = np.round(np.clip(estudiantes_docente, 6, 45)).astype(int)  # Limita la razón a valores plausibles.

    gamma_heterogeneidad = rng.gamma(3.0, 1 / 3.0, N)  # Introduce heterogeneidad individual (binomial negativa) en la inasistencia.
    lambda_inasistencia = np.exp(1.6 + 0.05 * np.minimum(distancia, 25) + 0.025 * horas + 0.35 * victima - 0.25 * pae + 0.05 * hermanos - 0.15 * nse + 0.25 * extraedad)  # Define la inasistencia esperada según barreras de acceso.
    inasistencia = np.clip(rng.poisson(lambda_inasistencia * gamma_heterogeneidad), 0, 120)  # Simula los días de inasistencia del año anterior.

    # --- Objetivo 1: puntaje en la prueba diagnóstica (inicio de año) ---
    señal_puntaje = (22 * np.log(ingreso) + 6 * nivel_madre + 14 * internet * (nivel_madre >= 2)  # Suma el capital del hogar; internet solo rinde si la madre puede acompañar.
                     - 0.3 * inasistencia - 28 * (inasistencia > 20) - 3 * hermanos  # Penaliza la inasistencia con un salto al superar 20 días.
                     - 4 * extraedad - 14 * (extraedad >= 2) - 8 * victima + 12 * pae * (estrato <= 2)  # Penaliza el rezago fuerte; el PAE ayuda solo a los más pobres.
                     - 30 * (horas > 20) - 15 * ((horas > 20) & (extraedad >= 1))  # Penaliza el trabajo intenso, peor si ya hay rezago (interacción).
                     - 15 * (rural & ~internet) - 9 * np.log1p(distancia)  # Añade la interacción rural sin internet y un efecto decreciente de la distancia.
                     - 1.5 * np.maximum(estudiantes_docente - 30, 0) - 1.5 * np.maximum(15 - estudiantes_docente, 0)  # Efecto en U: aulas saturadas o escuelas multigrado muy pequeñas.
                     - 8 * (etnia == "Indígena"))  # Penaliza la barrera lingüística de una prueba en castellano.
    ruido_puntaje = rng.normal(0, np.sqrt(np.var(señal_puntaje) * 0.32 / 0.68), N)  # Ajusta el ruido para que el R² máximo alcanzable sea cercano a 0,68.
    puntaje = np.round(np.clip(260 + señal_puntaje - señal_puntaje.mean() + ruido_puntaje, 0, 500)).astype(int)  # Centra la prueba en 260 puntos y la limita a la escala 0–500.

    # --- Objetivo 2: deserción al final del año ---
    logit_desercion = (0.8 * (extraedad >= 2) + 0.9 * (horas > 20) + 2.0 * ((extraedad >= 2) & (horas > 20))  # Suma rezago y trabajo; juntos multiplican el riesgo.
                       + 1.1 * (inasistencia > 20) + 0.6 * ((inasistencia > 20) & (puntaje < 200)) + 0.9 * (puntaje < 200) + 0.02 * inasistencia - 0.006 * (puntaje - 260)  # Añade los umbrales de inasistencia y bajo desempeño.
                       + 0.8 * ((distancia > 8) & ~pae) + 0.6 * victima + 0.15 * hombre + 0.7 * (edad >= 16)  # Añade la distancia sin alimentación escolar, victimización y edad.
                       - 0.3 * pae - 0.9 * transferencia * (ingreso < 1.0) + 0.4 * np.isin(grado, [9, 10])  # La transferencia protege solo a los hogares pobres; riesgo en grados de transición.
                       + rng.normal(0, 0.6, N))  # Añade factores no observados (familia, salud, migración) que ningún modelo puede ver.
    intercepto = -3.0  # Inicia la búsqueda del intercepto que produce la tasa deseada.
    for _ in range(60):  # Ajusta el intercepto por bisección simple para lograr una tasa de deserción cercana a 12 %.
        tasa = sigmoide(intercepto + logit_desercion).mean()  # Calcula la tasa esperada con el intercepto actual.
        intercepto += (0.12 - tasa) * 4  # Corrige el intercepto en la dirección de la tasa objetivo.
    deserto = (rng.random(N) < sigmoide(intercepto + logit_desercion)).astype(int)  # Simula la deserción observada.

    si_no = lambda x: np.where(x, "Sí", "No")  # Define una función que convierte booleanos en Sí/No.
    return pd.DataFrame({  # Arma la tabla final con el orden de las 20 variables.
        "id_estudiante": [f"EST-{i:05d}" for i in range(1, N + 1)],  # Crea un identificador único que no es variable del modelo.
        "region": region, "zona": np.where(rural, "Rural", "Urbana"), "sexo": np.where(hombre, "Hombre", "Mujer"),  # Variables territoriales y de sexo.
        "grado": grado, "edad": edad, "etnia": etnia, "estrato": estrato,  # Variables escolares, demográficas y de estrato.
        "ingreso_hogar_smmlv": ingreso, "educacion_madre": educacion_madre, "numero_hermanos": hermanos,  # Variables del hogar.
        "horas_trabajo_semana": horas, "distancia_colegio_km": distancia, "acceso_internet": si_no(internet),  # Variables de trabajo y acceso.
        "beneficiario_pae": si_no(pae), "transferencia_condicionada": si_no(transferencia), "victima_conflicto": si_no(victima),  # Variables de programas sociales y vulnerabilidad.
        "estudiantes_por_docente": estudiantes_docente, "inasistencia_dias": inasistencia,  # Variables del colegio y de asistencia.
        "puntaje_prueba_diagnostica": puntaje, "deserto": deserto,  # Variables objetivo de regresión y clasificación.
    })


def ensuciar(datos):  # Introduce imperfecciones reales solo en las variables predictoras.
    datos = datos.copy()  # Evita modificar la tabla limpia original.
    datos["edad"] = datos["edad"].astype("Int64")  # Permite enteros con valores faltantes.
    rural = datos["zona"].eq("Rural").to_numpy()  # Identifica a los estudiantes rurales para generar nulos no aleatorios.
    nulos_ingreso = rng.random(N) < np.where(rural, 0.09, 0.035)  # Hace que el ingreso falte más en zona rural (faltantes MAR).
    datos.loc[nulos_ingreso, "ingreso_hogar_smmlv"] = np.nan  # Borra los ingresos seleccionados.
    for columna, proporcion in [("educacion_madre", 0.04), ("distancia_colegio_km", 0.03), ("inasistencia_dias", 0.03), ("acceso_internet", 0.015)]:  # Recorre las demás columnas con faltantes.
        datos.loc[rng.random(N) < proporcion, columna] = np.nan  # Borra al azar la proporción indicada.
    datos["inasistencia_dias"] = datos["inasistencia_dias"].astype("Int64")  # Mantiene la inasistencia como entero con faltantes.

    filas = rng.choice(N, 40, replace=False)  # Elige 40 hogares con ingresos digitados con ceros de más.
    datos.loc[filas, "ingreso_hogar_smmlv"] = datos.loc[filas, "ingreso_hogar_smmlv"] * 100  # Multiplica el ingreso por 100 como error de digitación.
    datos.loc[rng.random(N) < 0.01, "horas_trabajo_semana"] = 99  # Inserta el código 99 de "no responde" en las horas de trabajo.
    filas = rng.choice(N, 15, replace=False)  # Elige 15 registros con edades imposibles.
    datos.loc[filas, "edad"] = rng.choice([3, 4, 5, 45, 52, 99], 15)  # Inserta edades fuera del rango escolar.

    variantes = {"zona": {"Urbana": ["urbana", "URBANA", "Urbana "], "Rural": ["rural", "RURAL", " Rural"]},  # Define escrituras inconsistentes de zona.
                 "region": {"Pacífica": ["Pacifica", "pacífica"], "Orinoquía": ["Orinoquia"], "Amazonía": ["Amazonia"], "Andina": ["andina"]},  # Define errores de tildes y mayúsculas en región.
                 "sexo": {"Hombre": ["hombre", "H"], "Mujer": ["mujer", "M"]}}  # Define abreviaturas y minúsculas en sexo.
    for columna in ["acceso_internet", "beneficiario_pae", "transferencia_condicionada", "victima_conflicto"]:  # Recorre las variables Sí/No.
        variantes[columna] = {"Sí": ["Si", "si", "SI"], "No": ["no", "NO"]}  # Define escrituras sin tilde y en mayúsculas.
    for columna, reemplazos in variantes.items():  # Recorre cada columna con variantes.
        for valor, opciones in reemplazos.items():  # Recorre cada valor correcto y sus variantes.
            filas = datos.index[datos[columna].eq(valor) & (rng.random(N) < 0.05)]  # Elige 5 % de las filas con ese valor.
            datos.loc[filas, columna] = rng.choice(opciones, len(filas))  # Reemplaza por una escritura inconsistente.
    return datos  # Devuelve la tabla con imperfecciones.


DICCIONARIO = [  # Describe cada variable para la hoja de diccionario.
    ("id_estudiante", "Identificador", "Texto", "Código único del estudiante. No es una variable predictora."),
    ("region", "Categórica nominal", "Andina, Caribe, Pacífica, Orinoquía, Amazonía", "Región natural donde está el colegio."),
    ("zona", "Categórica binaria", "Urbana, Rural", "Zona de residencia del estudiante."),
    ("sexo", "Categórica binaria", "Hombre, Mujer", "Sexo registrado en la matrícula (SIMAT)."),
    ("grado", "Numérica discreta", "6 a 11", "Grado que cursa el estudiante en el año de análisis."),
    ("edad", "Numérica discreta", "Años", "Edad cumplida al inicio del año. La extraedad (edad − grado − 5) indica rezago escolar."),
    ("etnia", "Categórica nominal", "Ninguna, Afrocolombiana, Indígena, Otra", "Autorreconocimiento étnico."),
    ("estrato", "Categórica ordinal", "1 a 6", "Estrato socioeconómico de la vivienda."),
    ("ingreso_hogar_smmlv", "Numérica continua", "Salarios mínimos mensuales", "Ingreso total mensual del hogar."),
    ("educacion_madre", "Categórica ordinal", "Ninguna < Primaria < Secundaria < Técnica < Universitaria", "Máximo nivel educativo alcanzado por la madre o cuidadora."),
    ("numero_hermanos", "Numérica discreta", "Personas", "Número de hermanos que viven en el hogar."),
    ("horas_trabajo_semana", "Numérica discreta", "Horas por semana (0 = no trabaja)", "Horas dedicadas a trabajo remunerado o en finca familiar."),
    ("distancia_colegio_km", "Numérica continua", "Kilómetros", "Distancia entre la vivienda y el colegio."),
    ("acceso_internet", "Categórica binaria", "Sí, No", "El hogar tiene conexión a internet."),
    ("beneficiario_pae", "Categórica binaria", "Sí, No", "Recibe el Programa de Alimentación Escolar."),
    ("transferencia_condicionada", "Categórica binaria", "Sí, No", "El hogar recibe una transferencia monetaria condicionada a la asistencia escolar."),
    ("victima_conflicto", "Categórica binaria", "Sí, No", "El estudiante está inscrito en el Registro Único de Víctimas."),
    ("estudiantes_por_docente", "Numérica discreta", "Estudiantes", "Razón de estudiantes por docente en el colegio."),
    ("inasistencia_dias", "Numérica discreta", "Días", "Días de inasistencia registrados el año anterior."),
    ("puntaje_prueba_diagnostica", "Numérica discreta (OBJETIVO REGRESIÓN)", "0 a 500 puntos", "Puntaje en la prueba diagnóstica de inicio de año (todos la presentan)."),
    ("deserto", "Binaria (OBJETIVO CLASIFICACIÓN)", "1 = desertó, 0 = continúa", "El estudiante abandonó el sistema escolar antes de terminar el año."),
]

PREGUNTAS = [  # Redacta las dos preguntas que guían el trabajo de los estudiantes.
    ("PREGUNTA 1 — REGRESIÓN", ""),
    ("Contexto", "La Secretaría de Educación quiere asignar tutorías de refuerzo antes de que los estudiantes lleguen al Saber 11. Para hacerlo necesita anticipar el desempeño académico de cada estudiante."),
    ("Pregunta", "¿Qué puntaje en la prueba diagnóstica (puntaje_prueba_diagnostica) se espera de cada estudiante según sus condiciones socioeconómicas, familiares y escolares, y qué modelo de machine learning lo predice con menor error?"),
    ("Modelos mínimos", "Entrene y compare al menos cuatro: regresión lineal, Ridge o Lasso, árbol de decisión, KNN, Random Forest, Gradient Boosting."),
    ("Métricas", "MAE, RMSE y R² en validación (división 80/20 y validación cruzada de 5 particiones)."),
    ("Regla", "No use 'deserto' como predictora: ocurre al final del año, después de la prueba (fuga de información)."),
    ("Decisión de política", "¿Qué variables explican más el puntaje? ¿Qué pesa más: las condiciones del hogar o las del colegio?"),
    ("", ""),
    ("PREGUNTA 2 — CLASIFICACIÓN BINARIA", ""),
    ("Contexto", f"Un programa de alerta temprana contra la deserción tiene cupo para {CUPOS_PROGRAMA:,} estudiantes (7,5 % de la base). Debe elegir a quién atender."),
    ("Pregunta", "¿Qué estudiantes tienen mayor riesgo de desertar este año (deserto = 1) y qué modelo de machine learning los identifica mejor?"),
    ("Modelos mínimos", "Entrene y compare al menos cuatro: regresión logística, árbol de decisión, KNN, Naive Bayes, Random Forest, Gradient Boosting."),
    ("Métricas", "Matriz de confusión, precisión, sensibilidad (recall), F1 y AUC-ROC. Explique por qué la exactitud (accuracy) engaña cuando solo ~12 % deserta."),
    ("Umbral", f"Elija el umbral de probabilidad de modo que el programa atienda {CUPOS_PROGRAMA:,} estudiantes. ¿Cuántos desertores reales captura el mejor modelo?"),
    ("Decisión de política", "¿Qué variables pesan más en el riesgo? ¿Qué sugieren los resultados sobre el PAE y las transferencias condicionadas?"),
    ("", ""),
    ("ANTES DE MODELAR", "La base tiene problemas reales: valores faltantes, códigos de no respuesta, atípicos y categorías escritas de varias formas. Límpiela y documente cada decisión."),
]


def dar_formato(libro):  # Aplica formato legible a las tres hojas.
    encabezado = PatternFill("solid", fgColor="1F4E79")  # Define el relleno azul de los encabezados.
    for hoja in libro.worksheets:  # Recorre cada hoja del libro.
        for celda in hoja[1]:  # Recorre la fila de encabezados.
            celda.font = Font(bold=True, color="FFFFFF")  # Pone el texto del encabezado en blanco y negrita.
            celda.fill = encabezado  # Aplica el relleno azul.
        hoja.freeze_panes = "A2"  # Fija la fila de encabezados al desplazarse.
    for columna in libro["estudiantes"].columns:  # Recorre las columnas de la hoja de datos.
        libro["estudiantes"].column_dimensions[columna[0].column_letter].width = max(12, len(str(columna[0].value)) + 2)  # Ajusta el ancho al nombre de la variable.
    for hoja, anchos in [("diccionario", [28, 36, 48, 80]), ("preguntas", [36, 120])]:  # Define anchos para las hojas de texto.
        for i, ancho in enumerate(anchos):  # Recorre cada columna de la hoja.
            libro[hoja].column_dimensions[chr(65 + i)].width = ancho  # Asigna el ancho de la columna.
        for fila in libro[hoja].iter_rows(min_row=2):  # Recorre las filas de contenido.
            for celda in fila:  # Recorre cada celda de la fila.
                celda.alignment = Alignment(wrap_text=True, vertical="top")  # Ajusta el texto largo dentro de la celda.
    for fila in libro["preguntas"].iter_rows(min_row=2):  # Recorre la hoja de preguntas.
        if fila[0].value and fila[0].value.isupper():  # Detecta los títulos de cada pregunta.
            fila[0].font = Font(bold=True, color="C55A11", size=12)  # Resalta el título en naranja.


def main():  # Define la función principal que genera y guarda la base.
    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)  # Crea la carpeta de datos si no existe.
    datos = ensuciar(generar_estudiantes())  # Genera la base y le añade imperfecciones.
    with pd.ExcelWriter(ARCHIVO_DATOS, engine="openpyxl") as escritor:  # Abre el archivo Excel de salida.
        datos.to_excel(escritor, sheet_name="estudiantes", index=False)  # Guarda los 20.000 estudiantes.
        pd.DataFrame(DICCIONARIO, columns=["variable", "tipo", "valores / unidades", "descripción"]).to_excel(escritor, sheet_name="diccionario", index=False)  # Guarda el diccionario de variables.
        pd.DataFrame(PREGUNTAS, columns=["apartado", "contenido"]).to_excel(escritor, sheet_name="preguntas", index=False)  # Guarda las dos preguntas.
        dar_formato(escritor.book)  # Da formato a las hojas antes de cerrar el archivo.
    print(f"Base guardada en {ARCHIVO_DATOS} ({len(datos):,} filas, {datos.shape[1] - 1} variables).")  # Informa dónde quedó el archivo.
    print(f"Tasa de deserción: {datos['deserto'].mean():.1%}")  # Muestra la tasa de deserción obtenida.


if __name__ == "__main__":  # Ejecuta el programa solo cuando se llama directamente.
    main()  # Llama a la función principal.
