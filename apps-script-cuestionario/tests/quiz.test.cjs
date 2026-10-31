const { test, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
let api, rows, failWrite, failFlush, lockAvailable, released;
beforeEach(() => {
  rows = []; failWrite = false; failFlush = false; lockAvailable = true; released = false;
  const props = { SPREADSHEET_ID: 'test-sheet', TOKEN_SECRET: 'test-secret' };
  const sheet = {
    getLastRow: () => rows.length + 1, getMaxRows: () => 1000,
    getRange(row, col) { return {
      createTextFinder: id => ({ matchEntireCell: () => ({ findNext: () => { const i = rows.findIndex(r => r[0] === id); return i < 0 ? null : { getRow: () => i + 2 }; } }) }),
      getValue: () => rows[row - 2][col - 1],
      setValues: values => { if (failWrite) throw new Error('Fallo de escritura'); rows.push(...values); }
    }; }
  };
  const context = vm.createContext({
    console, Date, PropertiesService: { getScriptProperties: () => ({ getProperty: key => props[key] }) },
    Utilities: { getUuid: () => crypto.randomUUID(), computeHmacSha256Signature: (text, secret) => crypto.createHmac('sha256', secret).update(text).digest(), base64EncodeWebSafe: data => Buffer.from(data).toString('base64url') },
    LockService: { getScriptLock: () => ({ tryLock: () => lockAvailable, releaseLock: () => { released = true; } }) },
    Session: { getEffectiveUser: () => ({ getEmail: () => 'otra@example.com' }), getActiveUser: () => ({ getEmail: () => '' }) },
    SpreadsheetApp: { openById: () => ({ getSheetByName: () => sheet }), flush: () => { if (failFlush) throw new Error('Respuesta perdida'); } }
  });
  vm.runInContext(fs.readFileSync(path.join(__dirname, '..', 'Code.gs'), 'utf8') + '\nthis.api = { getQuiz, submitQuiz, grade_, validate_, sign_, configurar_, configurarProyecto, styleHeader_, QUESTIONS, CONFIG };', context);
  api = context.api;
});
function payload() { return { name: 'María Fernanda Pérez', token: api.getQuiz().token, answers: Array.from(api.QUESTIONS, q => q.correct) }; }
test('publica exactamente 10 preguntas con 4 opciones, sin claves ni explicaciones', () => {
  const quiz = api.getQuiz(); assert.equal(quiz.questions.length, 10);
  quiz.questions.forEach(q => { assert.equal(q.options.length, 4); assert.equal(q.correct, undefined); assert.equal(q.explanation, undefined); });
  assert.equal(new Set(quiz.questions.map(q => q.id)).size, 10);
});
test('10 aciertos: 50 puntos, nota 5 y una fila completa de 30 columnas', () => {
  const result = api.submitQuiz(payload()); assert.equal(result.total, 50); assert.equal(result.grade, 5); assert.equal(result.correctCount, 10);
  assert.equal(rows.length, 1); assert.equal(rows[0].length, 30); assert.equal(rows[0][25], 50); assert.equal(rows[0][27], 5); assert.equal(rows[0][28], 1); assert.ok(released);
});
test('0 aciertos: 0 puntos y nota 0', () => {
  const p = payload(); p.answers = p.answers.map(a => (a + 1) % 4); const r = api.submitQuiz(p); assert.equal(r.total, 0); assert.equal(r.grade, 0);
});
test('7 aciertos: 35 puntos y nota 3,5; cada puntuación se guarda en su columna', () => {
  const p = payload(); p.answers = p.answers.map((a, i) => i < 7 ? a : (a + 1) % 4); const r = api.submitQuiz(p); assert.equal(r.total, 35); assert.equal(r.grade, 3.5);
  r.review.forEach((q, i) => assert.equal(rows[0][6 + i * 2], q.points));
});
test('ignora una nota manipulada por el cliente', () => { const p = payload(); p.answers = p.answers.map(a => (a + 1) % 4); p.total = 50; p.grade = 5; assert.equal(api.submitQuiz(p).total, 0); });
test('reenvío idéntico devuelve el comprobante sin duplicar', () => { const p = payload(); const first = api.submitQuiz(p); const again = api.submitQuiz(p); assert.equal(again.id, first.id); assert.equal(again.submittedAt, first.submittedAt); assert.equal(rows.length, 1); });
test('el mismo ID con respuestas diferentes no altera el registro', () => { const p = payload(); api.submitQuiz(p); p.answers[0] = (p.answers[0] + 1) % 4; assert.throws(() => api.submitQuiz(p), /ya fue registrado/); assert.equal(rows.length, 1); });
test('rechaza preguntas faltantes, valores fuera de rango, cadenas y arrays dispersos', () => {
  for (const answers of [[], Array(10).fill(-1), Array(10).fill(4), Array(10).fill('1'), new Array(10)]) { const p = payload(); p.answers = answers; assert.throws(() => api.submitQuiz(p), /10 preguntas/); }
  assert.equal(rows.length, 0);
});
test('normaliza el nombre y exige nombre y apellido', () => {
  const p = payload(); p.name = '  María   Pérez  '; assert.equal(api.submitQuiz(p).name, 'María Pérez');
  for (const name of ['', 'Ana', 'X'.repeat(151), 'Ana\nPérez']) { const q = payload(); q.name = name; assert.throws(() => api.submitQuiz(q), /nombre/); }
});
test('neutraliza fórmulas en nombres sin alterar el comprobante', () => { const p = payload(); p.name = '=HYPERLINK("https://ejemplo.test") Apellido'; const r = api.submitQuiz(p); assert.ok(rows[0][2].startsWith("'=")); assert.ok(r.name.startsWith('=')); });
test('rechaza tokens alterados y expirados', () => {
  const p = payload(); p.token.issuedAt -= 1000; assert.throws(() => api.submitQuiz(p), /sesión no es válida/);
  const q = payload(); q.token.issuedAt -= 25 * 60 * 60 * 1000; q.token.signature = api.sign_(q.token); assert.throws(() => api.submitQuiz(q), /sesión venció/); assert.equal(rows.length, 0);
});
test('la contención del bloqueo no guarda una fila', () => { lockAvailable = false; assert.throws(() => api.submitQuiz(payload()), /varios envíos/); assert.equal(rows.length, 0); });
test('un fallo de escritura no devuelve éxito y libera el bloqueo', () => { failWrite = true; assert.throws(() => api.submitQuiz(payload()), /Fallo de escritura/); assert.equal(rows.length, 0); assert.ok(released); });
test('un fallo tras escribir permite recuperar el comprobante sin duplicar', () => { const p = payload(); failFlush = true; assert.throws(() => api.submitQuiz(p), /Respuesta perdida/); failFlush = false; assert.equal(api.submitQuiz(p).total, 50); assert.equal(rows.length, 1); });
test('la configuración rechaza una cuenta diferente a la propietaria', () => { assert.throws(() => api.configurar_(), /opvargas23@gmail.com/); });
test('un visitante anónimo no puede usar el inicializador público', () => { assert.throws(() => api.configurarProyecto(), /Solo la cuenta propietaria/); });
test('el formato respeta que setFrozenRows de Google no devuelve una hoja', () => {
  let frozen = false, height = false;
  const range = { setBackground() { return this; }, setFontColor() { return this; }, setFontWeight() { return this; }, setWrap() { return this; } };
  api.styleHeader_({ getRange: () => range, setFrozenRows: () => { frozen = true; }, setRowHeight: () => { height = true; } }, 30);
  assert.ok(frozen && height);
});
