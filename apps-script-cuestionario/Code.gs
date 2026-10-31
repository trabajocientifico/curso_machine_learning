/** Evaluación conceptual · Módulo 2. Las claves permanecen en el servidor. */
const CONFIG = Object.freeze({
  title: 'Machine Learning · Evaluación conceptual',
  version: '2026-10-v1',
  owner: 'opvargas23@gmail.com',
  points: 5,
  ttlMs: 24 * 60 * 60 * 1000
});

const QUESTIONS = [
  { id: 'P01', topic: 'Tipos de aprendizaje',
    text: '¿Cuáles son los dos tipos de aprendizaje que se trabajaron principalmente en el módulo?',
    options: ['Lineal y digital.', 'Supervisado y no supervisado.', 'Rápido y lento.', 'Manual y automático.'], correct: 1,
    explanation: 'En el módulo se estudian el aprendizaje supervisado, con respuestas conocidas, y el no supervisado, que busca estructura sin esas respuestas.', source: 'index/2-1-clase-fundamentos.html' },
  { id: 'P02', topic: 'Reglas y aprendizaje',
    text: '¿Cuál es la principal diferencia entre un sistema basado en reglas y uno de machine learning?',
    options: ['El sistema de reglas siempre necesita más datos.', 'Machine learning funciona sin datos.', 'Los dos requieren escribir a mano todas las reglas de decisión.', 'En el primero se escriben las reglas; en machine learning el modelo aprende patrones a partir de datos.'], correct: 3,
    explanation: 'En un sistema basado en reglas una persona define cómo decidir. En machine learning se ajusta un modelo a partir de ejemplos.', source: 'index/2-1-clase-fundamentos.html' },
  { id: 'P03', topic: 'Aprendizaje supervisado',
    text: '¿Qué caracteriza a los datos usados para entrenar un modelo de aprendizaje supervisado?',
    options: ['Incluyen ejemplos con la respuesta que se quiere aprender a predecir.', 'No pueden contener números.', 'Siempre están organizados en grupos sin etiquetas.', 'Solo pueden ser imágenes.'], correct: 0,
    explanation: 'Los ejemplos de entrenamiento incluyen una respuesta conocida: por ejemplo, el precio de una vivienda o si un estudiante continuó sus estudios.', source: 'index/2-1-clase-fundamentos.html' },
  { id: 'P04', topic: 'Reconocer técnicas',
    text: '¿Cuál de estas técnicas NO corresponde al aprendizaje supervisado, tal como se presentó en clase?',
    options: ['Regresión lineal.', 'Regresión logística.', 'K-means para formar grupos.', 'Árbol de decisión para predecir una categoría.'], correct: 2,
    explanation: 'K-means forma grupos por semejanza sin necesitar una respuesta o etiqueta previamente asignada a cada caso.', source: 'index/2-1-clase-mapa-tecnicas.html' },
  { id: 'P05', topic: 'Aprendizaje no supervisado',
    text: '¿Cuál de estas situaciones es un ejemplo de aprendizaje no supervisado?',
    options: ['Predecir el precio de una vivienda usando ejemplos con precios conocidos.', 'Agrupar municipios por sus características, sin asignarles grupos de antemano.', 'Reconocer correos no deseados a partir de correos ya etiquetados.', 'Predecir si un estudiante desertará usando casos con resultados conocidos.'], correct: 1,
    explanation: 'Buscar grupos de municipios parecidos sin etiquetas previas es una tarea de agrupamiento no supervisado.', source: 'index/2-3-clase-no-supervisado.html' },
  { id: 'P06', topic: 'Clasificación',
    text: 'Si se quiere predecir si un correo es «no deseado» o «normal», ¿qué tarea se está realizando?',
    options: ['Clasificación, porque se predice una categoría.', 'Regresión, porque se predice un valor numérico continuo.', 'Agrupamiento, porque no existen categorías conocidas.', 'Reducción de dimensiones, porque se eliminan correos.'], correct: 0,
    explanation: 'La clasificación predice categorías. En este ejemplo las categorías son «no deseado» y «normal».', source: 'index/2-1-clase-mapa-tecnicas.html' },
  { id: 'P07', topic: 'Regresión',
    text: 'Si se quiere estimar el precio de una vivienda a partir de sus características, ¿qué tarea corresponde?',
    options: ['Clasificación de imágenes.', 'Agrupamiento sin etiquetas.', 'Detección de correos no deseados.', 'Regresión, porque se quiere predecir un valor numérico.'], correct: 3,
    explanation: 'La regresión se utiliza para predecir cantidades, como un precio, un ingreso o una temperatura.', source: 'index/2-2-clase-regresion-lineal.html' },
  { id: 'P08', topic: 'Entrenamiento y evaluación',
    text: '¿Para qué se reservan datos de prueba que el modelo no utilizó durante el entrenamiento?',
    options: ['Para que el modelo memorice también esos datos antes de evaluarlo.', 'Para evitar revisar la calidad de los datos.', 'Para evaluar cómo funciona el modelo en casos que no ha visto.', 'Para garantizar que nunca cometerá errores.'], correct: 2,
    explanation: 'Los datos de prueba permiten evaluar si lo aprendido resulta útil en casos nuevos. Un buen resultado no garantiza que el modelo nunca se equivoque.', source: 'index/2-1-clase-fundamentos.html' },
  { id: 'P09', topic: 'Sobreajuste',
    text: 'Un modelo funciona muy bien con los datos de entrenamiento, pero falla en casos nuevos. ¿Qué podría estar ocurriendo?',
    options: ['Sobreajuste: se adaptó demasiado a los ejemplos de entrenamiento.', 'El modelo ya aprendió todo y no necesita evaluación.', 'Los datos nuevos siempre están equivocados.', 'El modelo dejó de ser machine learning.'], correct: 0,
    explanation: 'El sobreajuste ocurre cuando el modelo se adapta demasiado a particularidades del entrenamiento y generaliza mal a nuevos casos.', source: 'index/2-2-clase-arbol-decision.html' },
  { id: 'P10', topic: 'Interpretación de resultados',
    text: 'Después de obtener los resultados de un modelo, ¿qué es lo más adecuado en una investigación?',
    options: ['Aceptar todas las predicciones como verdades definitivas.', 'Comunicar solo los resultados que parecen favorables.', 'Suponer que una predicción demuestra automáticamente una causa.', 'Interpretarlos en el contexto del problema y comunicar sus alcances y limitaciones.'], correct: 3,
    explanation: 'Los resultados requieren interpretación y evaluación en contexto. Una predicción por sí sola no demuestra causalidad ni elimina la incertidumbre.', source: 'index/2-1-clase-fundamentos.html' }
];

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle(CONFIG.title)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/** Punto de entrada del editor. La identidad ACTIVA impide su uso por visitantes. */
function configurarProyecto() {
  if (Session.getActiveUser().getEmail() !== CONFIG.owner) throw new Error('Solo la cuenta propietaria puede configurar este proyecto.');
  return configurar_();
}

/** Ejecutar UNA VEZ desde el editor, con la cuenta propietaria. No es un RPC público. */
function configurar_() {
  const account = Session.getEffectiveUser().getEmail();
  if (account !== CONFIG.owner) throw new Error('Abra el proyecto con ' + CONFIG.owner + '.');
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    const props = PropertiesService.getScriptProperties();
    if (props.getProperty('SPREADSHEET_ID')) {
      console.log('Hoja existente: ' + spreadsheet_().getUrl());
      return spreadsheet_().getUrl();
    }
    const pendingId = props.getProperty('PENDING_SPREADSHEET_ID');
    const ss = pendingId ? SpreadsheetApp.openById(pendingId) : SpreadsheetApp.create(CONFIG.title + ' · Resultados');
    props.setProperty('PENDING_SPREADSHEET_ID', ss.getId());
    ss.setSpreadsheetTimeZone('America/Bogota');
    // Fórmulas en sintaxis inglesa estable; la interfaz del cuestionario usa es-CO.
    ss.setSpreadsheetLocale('en_US');
    const responses = ss.getSheetByName('Respuestas') || ss.getSheets()[0].setName('Respuestas');
    const headers = ['ID del intento', 'Fecha y hora (Bogotá)', 'Nombre completo', 'Versión', 'Duración (segundos)'];
    QUESTIONS.forEach(q => headers.push(q.id + ' · Respuesta', q.id + ' · Puntos (0–5)'));
    headers.push('Total (0–50)', 'Máximo', 'Nota (0–5)', 'Porcentaje', 'Comprobante interno');
    ensureColumns_(responses, headers.length);
    responses.getRange(1, 1, 1, headers.length).setValues([headers]);
    styleHeader_(responses, headers.length);
    responses.setFrozenColumns(3);
    responses.setColumnWidth(1, 270).setColumnWidth(2, 170).setColumnWidth(3, 240);
    responses.getRange('B2:B').setNumberFormat('dd/mm/yyyy hh:mm:ss');
    responses.getRange('C2:C').setNumberFormat('@');
    responses.getRange('AB2:AB').setNumberFormat('0.0');
    responses.getRange('AC2:AC').setNumberFormat('0%');
    responses.hideColumns(30);
    if (!responses.getFilter()) responses.getRange(1, 1, responses.getMaxRows(), headers.length).createFilter();
    const bank = ss.getSheetByName('Preguntas') || ss.insertSheet('Preguntas');
    const bankHeaders = ['ID', 'Tema', 'Pregunta', 'Opción A', 'Opción B', 'Opción C', 'Opción D', 'Correcta', 'Puntos', 'Explicación', 'Fuente HTML'];
    bank.getRange(1, 1, 1, bankHeaders.length).setValues([bankHeaders]);
    bank.getRange(2, 1, QUESTIONS.length, bankHeaders.length).setValues(QUESTIONS.map(q =>
      [q.id, q.topic, q.text, ...q.options, 'ABCD'[q.correct], CONFIG.points, q.explanation, q.source]));
    styleHeader_(bank, bankHeaders.length);
    bank.setColumnWidth(3, 420).setColumnWidth(10, 420);
    bank.getDataRange().setWrap(true).setVerticalAlignment('top');
    const dashboard = ss.getSheetByName('Dashboard') || ss.insertSheet('Dashboard', 0);
    dashboard.getCharts().forEach(chart => dashboard.removeChart(chart));
    buildDashboard_(dashboard);
    const guide = ss.getSheetByName('Guía') || ss.insertSheet('Guía');
    guide.getRange(1, 1, 8, 2).setValues([
      ['EVALUACIÓN CONCEPTUAL', 'Instrucciones para el docente'],
      ['Cuenta propietaria', CONFIG.owner],
      ['Calificación', '10 preguntas × 5 puntos. Correcta: 5; incorrecta: 0. Total / 50; nota = total / 10.'],
      ['Dashboard', 'Los indicadores se actualizan con cada registro. Se cuentan intentos, no personas únicas.'],
      ['Exportar a Excel', 'Archivo → Descargar → Microsoft Excel (.xlsx). Incluye las cuatro pestañas.'],
      ['Privacidad', 'Mantenga este archivo restringido. Comparta únicamente la URL /exec del formulario.'],
      ['Banco de preguntas', 'La pestaña Preguntas documenta el banco. Editarla no cambia el cuestionario; el banco está en Code.gs.'],
      ['Reintentos', 'Un reenvío técnico conserva el mismo ID y no crea otra fila. Un nuevo cuestionario sí crea otro intento.']
    ]);
    styleHeader_(guide, 2);
    guide.setColumnWidth(1, 200).setColumnWidth(2, 800).getDataRange().setWrap(true);
    SpreadsheetApp.flush();
    props.setProperties({ SPREADSHEET_ID: ss.getId(), TOKEN_SECRET: Utilities.getUuid() + Utilities.getUuid() });
    props.deleteProperty('PENDING_SPREADSHEET_ID');
    console.log('RESULTADOS Y DASHBOARD: ' + ss.getUrl());
    return ss.getUrl();
  } finally { lock.releaseLock(); }
}

function getQuiz() {
  const props = PropertiesService.getScriptProperties();
  if (!props.getProperty('SPREADSHEET_ID') || !props.getProperty('TOKEN_SECRET')) {
    throw new Error('El formulario todavía no está habilitado. Contacte al docente.');
  }
  const token = { id: Utilities.getUuid(), issuedAt: Date.now(), version: CONFIG.version };
  token.signature = sign_(token);
  return {
    title: CONFIG.title, version: CONFIG.version, points: CONFIG.points, token: token,
    questions: QUESTIONS.map(q => ({ id: q.id, topic: q.topic, text: q.text, options: q.options.slice() }))
  };
}

function submitQuiz(payload) {
  const clean = validate_(payload);
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) throw new Error('Hay varios envíos en curso. Espere unos segundos y vuelva a enviar.');
  try {
    const sheet = spreadsheet_().getSheetByName('Respuestas');
    const lastRow = sheet.getLastRow();
    const existing = lastRow > 1 ? sheet.getRange(2, 1, lastRow - 1, 1)
      .createTextFinder(clean.token.id).matchEntireCell(true).findNext() : null;
    if (existing) {
      const receipt = JSON.parse(sheet.getRange(existing.getRow(), 30).getValue());
      if (receipt.name !== clean.name || receipt.review.some((q, i) => q.selected !== clean.answers[i])) {
        throw new Error('Este intento ya fue registrado con otras respuestas. Abra de nuevo el formulario para comenzar otro.');
      }
      return receipt;
    }
    if (Date.now() - clean.token.issuedAt > CONFIG.ttlMs) throw new Error('La sesión venció. Recargue la página para iniciar otro cuestionario.');
    const result = grade_(clean);
    const row = [result.id, new Date(result.submittedAt), safeCell_(result.name), CONFIG.version, result.durationSeconds];
    result.review.forEach(q => row.push(q.options[q.selected], q.points));
    row.push(result.total, result.max, result.grade, result.total / result.max, JSON.stringify(result));
    const nextRow = sheet.getLastRow() + 1;
    if (nextRow > sheet.getMaxRows()) sheet.insertRowsAfter(sheet.getMaxRows(), 500);
    sheet.getRange(nextRow, 1, 1, row.length).setValues([row]);
    SpreadsheetApp.flush();
    return result; // Solo se confirma después de guardar la fila.
  } finally { lock.releaseLock(); }
}

function validate_(payload) {
  if (!payload || typeof payload !== 'object') throw new Error('Envío inválido.');
  const token = payload.token;
  if (!token || !/^[\da-f-]{36}$/i.test(token.id || '') || !Number.isSafeInteger(token.issuedAt) ||
      token.version !== CONFIG.version || typeof token.signature !== 'string' || token.signature !== sign_(token) ||
      token.issuedAt > Date.now() + 60000) throw new Error('La sesión no es válida. Recargue el formulario.');
  if (typeof payload.name !== 'string' || /[\x00-\x1f\x7f]/.test(payload.name)) throw new Error('Escriba un nombre válido.');
  const name = payload.name.normalize('NFC').trim().replace(/\s+/g, ' ');
  if (name.length < 5 || name.length > 150 || name.split(' ').length < 2 || !/[A-Za-zÀ-ÿ]/.test(name)) {
    throw new Error('Escriba su nombre completo, con nombre y apellido (máximo 150 caracteres).');
  }
  if (!Array.isArray(payload.answers) || payload.answers.length !== QUESTIONS.length ||
      !QUESTIONS.every((q, i) => Number.isInteger(payload.answers[i]) && payload.answers[i] >= 0 && payload.answers[i] < q.options.length)) {
    throw new Error('Responda las 10 preguntas antes de enviar.');
  }
  return { name: name, answers: payload.answers.slice(), token: token };
}

function grade_(clean) {
  const review = QUESTIONS.map((q, i) => ({ id: q.id, text: q.text, options: q.options.slice(),
    selected: clean.answers[i], correct: q.correct, points: clean.answers[i] === q.correct ? CONFIG.points : 0,
    explanation: q.explanation }));
  const total = review.reduce((sum, q) => sum + q.points, 0);
  return { id: clean.token.id, name: clean.name, version: CONFIG.version, submittedAt: new Date().toISOString(),
    durationSeconds: Math.max(0, Math.round((Date.now() - clean.token.issuedAt) / 1000)),
    total: total, max: QUESTIONS.length * CONFIG.points, grade: total / QUESTIONS.length,
    correctCount: review.filter(q => q.points > 0).length, review: review };
}

function sign_(token) {
  const secret = PropertiesService.getScriptProperties().getProperty('TOKEN_SECRET');
  if (!secret) throw new Error('El formulario todavía no está habilitado.');
  return Utilities.base64EncodeWebSafe(Utilities.computeHmacSha256Signature(token.id + '|' + token.issuedAt + '|' + token.version, secret));
}
function spreadsheet_() {
  const id = PropertiesService.getScriptProperties().getProperty('SPREADSHEET_ID');
  if (!id) throw new Error('Ejecute configurar_ desde el editor antes de publicar.');
  return SpreadsheetApp.openById(id);
}
function safeCell_(value) { return /^[=+\-@]/.test(value) ? "'" + value : value; }
function ensureColumns_(sheet, count) {
  if (sheet.getMaxColumns() < count) sheet.insertColumnsAfter(sheet.getMaxColumns(), count - sheet.getMaxColumns());
}
function styleHeader_(sheet, count) {
  sheet.getRange(1, 1, 1, count).setBackground('#18324f').setFontColor('#ffffff').setFontWeight('bold').setWrap(true);
  sheet.setFrozenRows(1);
  sheet.setRowHeight(1, 42);
}
function buildDashboard_(sheet) {
  sheet.getRange('A1:F1').merge().setValue('MACHINE LEARNING · RESULTADOS DEL GRUPO');
  styleHeader_(sheet, 6);
  sheet.getRange('A3:B6').setValues([
    ['Intentos registrados', '=COUNTA(Respuestas!A2:A)'],
    ['Promedio del total / 50', '=IFERROR(AVERAGE(Respuestas!Z2:Z),0)'],
    ['Promedio de la nota / 5', '=IFERROR(AVERAGE(Respuestas!AB2:AB),0)'],
    ['Promedio de aciertos', '=IFERROR(AVERAGE(Respuestas!AC2:AC),0)']
  ]);
  sheet.getRange('B4:B5').setNumberFormat('0.0');
  sheet.getRange('B6').setNumberFormat('0%');
  sheet.getRange('A8:F8').setValues([['Pregunta', 'Tema', 'Correctas', 'Incorrectas', '% de acierto', 'Promedio / 5']]);
  sheet.getRange('A8:F8').setBackground('#e6edf4').setFontWeight('bold');
  QUESTIONS.forEach((q, i) => {
    const col = String.fromCharCode(71 + 2 * i), r = i + 9;
    sheet.getRange(r, 1, 1, 6).setValues([[q.id, q.topic,
      '=COUNTIF(Respuestas!' + col + '2:' + col + ',5)', '=MAX(0,$B$3-C' + r + ')',
      '=IFERROR(C' + r + '/(C' + r + '+D' + r + '),0)', '=IFERROR(AVERAGE(Respuestas!' + col + '2:' + col + '),0)']]);
  });
  sheet.getRange('E9:E18').setNumberFormat('0%');
  sheet.getRange('F9:F18').setNumberFormat('0.0');
  sheet.getRange('A20:F21').merge().setValue('Cada fila de Respuestas corresponde a un intento. Para exportar: Archivo → Descargar → Microsoft Excel (.xlsx). La hoja es privada; comparta solo el formulario.').setWrap(true);
  sheet.setColumnWidth(1, 230).setColumnWidth(2, 250).setColumnWidths(3, 4, 125);
  sheet.insertChart(sheet.newChart().setChartType(Charts.ChartType.COLUMN)
    .addRange(sheet.getRange('A8:A18')).addRange(sheet.getRange('E8:E18'))
    .setNumHeaders(1).setPosition(23, 1, 0, 0).setOption('title', 'Porcentaje de acierto por pregunta')
    .setOption('legend', { position: 'none' }).setOption('colors', ['#3469ba'])
    .setOption('vAxis', { minValue: 0, maxValue: 1, format: 'percent' }).setOption('width', 880).setOption('height', 360).build());
}
