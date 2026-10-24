from pathlib import Path  # Importa Path para construir rutas a carpetas y archivos.
import numpy as np  # Importa NumPy para operaciones numéricas.
import pandas as pd  # Importa pandas para leer y limpiar la base.
from sklearn.compose import ColumnTransformer  # Importa el transformador que trata columnas numéricas y categóricas por separado.
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor, RandomForestClassifier, RandomForestRegressor  # Importa los modelos de ensamble.
from sklearn.impute import SimpleImputer  # Importa el imputador de valores faltantes.
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge  # Importa los modelos lineales.
from sklearn.metrics import f1_score, mean_absolute_error, mean_squared_error, precision_score, r2_score, recall_score, roc_auc_score  # Importa las métricas de evaluación.
from sklearn.model_selection import train_test_split  # Importa la división entrenamiento/validación.
from sklearn.naive_bayes import GaussianNB  # Importa Naive Bayes.
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor  # Importa los modelos de vecinos cercanos.
from sklearn.pipeline import make_pipeline  # Importa la función que encadena preprocesamiento y modelo.
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # Importa la codificación y el escalamiento.
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor  # Importa los árboles de decisión.

ARCHIVO_DATOS = Path(__file__).resolve().parent / "datos" / "desercion_escolar.xlsx"  # Define la ruta de la base generada.
SEMILLA = 42  # Fija la semilla de la división y los modelos.
CUPOS = 1500  # Define el cupo del programa de alerta temprana.
NUMERICAS = ["grado", "edad", "extraedad", "estrato", "ingreso_hogar_smmlv", "nivel_madre", "numero_hermanos", "horas_trabajo_semana", "distancia_colegio_km", "estudiantes_por_docente", "inasistencia_dias"]  # Lista las predictoras numéricas.
CATEGORICAS = ["region", "zona", "sexo", "etnia", "acceso_internet", "beneficiario_pae", "transferencia_condicionada", "victima_conflicto"]  # Lista las predictoras categóricas.


def limpiar(datos):  # Corrige los problemas introducidos deliberadamente en la base.
    for columna in CATEGORICAS:  # Recorre las columnas de texto.
        datos[columna] = datos[columna].astype("string").str.strip().str.casefold()  # Elimina espacios y unifica mayúsculas.
    datos["region"] = datos["region"].replace({"pacifica": "pacífica", "orinoquia": "orinoquía", "amazonia": "amazonía"})  # Unifica las tildes de región.
    datos["sexo"] = datos["sexo"].replace({"h": "hombre", "m": "mujer"})  # Expande las abreviaturas de sexo.
    for columna in ["acceso_internet", "beneficiario_pae", "transferencia_condicionada", "victima_conflicto"]:  # Recorre las variables Sí/No.
        datos[columna] = datos[columna].replace({"si": "sí"})  # Unifica la escritura de Sí.
    datos.loc[datos["horas_trabajo_semana"] == 99, "horas_trabajo_semana"] = np.nan  # Convierte el código 99 en faltante.
    datos.loc[~datos["edad"].between(9, 22), "edad"] = np.nan  # Marca como faltantes las edades imposibles.
    datos.loc[datos["ingreso_hogar_smmlv"] > 30, "ingreso_hogar_smmlv"] /= 100  # Corrige los ingresos digitados con ceros de más.
    datos["extraedad"] = datos["edad"] - datos["grado"] - 5  # Crea la extraedad como indicador de rezago.
    datos["nivel_madre"] = datos["educacion_madre"].map({"Ninguna": 0, "Primaria": 1, "Secundaria": 2, "Técnica": 3, "Universitaria": 4})  # Codifica la educación de la madre de forma ordinal.
    datos[CATEGORICAS] = datos[CATEGORICAS].astype(object).where(datos[CATEGORICAS].notna(), np.nan)  # Usa NaN en lugar de pd.NA para que scikit-learn pueda imputar.
    return datos  # Devuelve la base limpia.


def preprocesador(escalar):  # Construye el preprocesamiento común a todos los modelos.
    pasos_numericos = [SimpleImputer(strategy="median")] + ([StandardScaler()] if escalar else [])  # Imputa con la mediana y escala si el modelo lo requiere.
    return ColumnTransformer([("num", make_pipeline(*pasos_numericos), NUMERICAS), ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore", drop="if_binary", sparse_output=False)), CATEGORICAS)])  # Une el tratamiento numérico y categórico.


def main():  # Revisa la base y entrena modelos de referencia.
    datos = limpiar(pd.read_excel(ARCHIVO_DATOS, sheet_name="estudiantes"))  # Lee y limpia la base.
    print(f"Filas: {len(datos):,} | Tasa de deserción: {datos['deserto'].mean():.1%} | Puntaje medio: {datos['puntaje_prueba_diagnostica'].mean():.0f} (DE {datos['puntaje_prueba_diagnostica'].std():.0f})")  # Resume los objetivos.
    print("\nCorrelaciones con los objetivos:")  # Anuncia la tabla de correlaciones.
    print(datos[NUMERICAS + ["puntaje_prueba_diagnostica", "deserto"]].corr()[["puntaje_prueba_diagnostica", "deserto"]].round(2).to_string())  # Muestra la correlación de cada numérica con ambos objetivos.

    X = datos[NUMERICAS + CATEGORICAS]  # Selecciona las predictoras (sin 'deserto' para evitar fuga en la regresión).
    X_ent, X_val, y_ent, y_val, d_ent, d_val = train_test_split(X, datos["puntaje_prueba_diagnostica"], datos["deserto"], test_size=0.2, random_state=SEMILLA, stratify=datos["deserto"])  # Divide 80/20 manteniendo la tasa de deserción.

    regresores = {"Regresión lineal": (LinearRegression(), True), "Ridge": (Ridge(alpha=10), True), "Árbol (prof. 8)": (DecisionTreeRegressor(max_depth=8, random_state=SEMILLA), False), "KNN (k=25)": (KNeighborsRegressor(25), True), "Random Forest": (RandomForestRegressor(300, min_samples_leaf=5, n_jobs=-1, random_state=SEMILLA), False), "Gradient Boosting": (HistGradientBoostingRegressor(random_state=SEMILLA), False)}  # Define los modelos de regresión.
    filas = []  # Prepara la tabla de resultados de regresión.
    for nombre, (modelo, escalar) in regresores.items():  # Recorre cada regresor.
        estimado = make_pipeline(preprocesador(escalar), modelo).fit(X_ent, y_ent).predict(X_val)  # Entrena y predice en validación.
        filas.append({"Modelo": nombre, "MAE": mean_absolute_error(y_val, estimado), "RMSE": mean_squared_error(y_val, estimado) ** 0.5, "R2": r2_score(y_val, estimado)})  # Guarda las métricas.
    print("\nPREGUNTA 1 — Regresión (validación):")  # Anuncia la tabla de regresión.
    print(pd.DataFrame(filas).round(3).to_string(index=False))  # Muestra la tabla.

    X_ent_c = X_ent.assign(puntaje_prueba_diagnostica=y_ent)  # Añade el puntaje como predictor de deserción (ocurre antes).
    X_val_c = X_val.assign(puntaje_prueba_diagnostica=y_val)  # Hace lo mismo en validación.
    NUMERICAS.append("puntaje_prueba_diagnostica")  # Incluye el puntaje en el preprocesamiento numérico.
    clasificadores = {"Regresión logística": (LogisticRegression(max_iter=2000), True), "Árbol (prof. 6)": (DecisionTreeClassifier(max_depth=6, random_state=SEMILLA), False), "KNN (k=50)": (KNeighborsClassifier(50), True), "Naive Bayes": (GaussianNB(), True), "Random Forest": (RandomForestClassifier(400, min_samples_leaf=10, n_jobs=-1, random_state=SEMILLA), False), "Gradient Boosting": (HistGradientBoostingClassifier(random_state=SEMILLA), False)}  # Define los clasificadores.
    cupos_val = round(CUPOS * len(X_val) / len(datos))  # Escala el cupo del programa al tamaño de validación.
    filas = []  # Prepara la tabla de resultados de clasificación.
    for nombre, (modelo, escalar) in clasificadores.items():  # Recorre cada clasificador.
        prob = make_pipeline(preprocesador(escalar), modelo).fit(X_ent_c, d_ent).predict_proba(X_val_c)[:, 1]  # Entrena y obtiene probabilidades.
        pred = (prob >= 0.5).astype(int)  # Clasifica con el umbral por defecto.
        top = np.argsort(-prob)[:cupos_val]  # Elige a los de mayor riesgo según el cupo.
        filas.append({"Modelo": nombre, "AUC": roc_auc_score(d_val, prob), "Precisión@0.5": precision_score(d_val, pred, zero_division=0), "Recall@0.5": recall_score(d_val, pred), "F1@0.5": f1_score(d_val, pred), f"Desertores captados en top {cupos_val}": f"{d_val.to_numpy()[top].sum()} de {d_val.sum()}"})  # Guarda las métricas.
    print("\nPREGUNTA 2 — Clasificación (validación):")  # Anuncia la tabla de clasificación.
    print(pd.DataFrame(filas).round(3).to_string(index=False))  # Muestra la tabla.


if __name__ == "__main__":  # Ejecuta el programa solo cuando se llama directamente.
    main()  # Llama a la función principal.
