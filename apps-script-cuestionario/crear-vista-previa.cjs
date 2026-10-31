// Genera una demostración autónoma; NO se carga este archivo ni su salida en Apps Script.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const context = vm.createContext({});
vm.runInContext(fs.readFileSync(path.join(__dirname, 'Code.gs'), 'utf8') + '\nthis.bank = QUESTIONS; this.config = CONFIG;', context);
const data = JSON.stringify({ questions: context.bank, title: context.config.title, version: context.config.version }).replace(/</g, '\\u003c');
const bridge = `<script>\nconst previewData = ${data};
window.QUIZ_PREVIEW = async function(method, payload) {
  if (method === 'getQuiz') return { title: previewData.title, version: previewData.version, points: 5, token: { id: 'DEMO-LOCAL', issuedAt: Date.now() }, questions: previewData.questions.map(({id,topic,text,options}) => ({id,topic,text,options})) };
  const review = previewData.questions.map((q,i) => ({...q, selected: payload.answers[i], points: payload.answers[i] === q.correct ? 5 : 0}));
  const total = review.reduce((s,q) => s + q.points, 0);
  return { id: 'DEMO-LOCAL-SIN-GUARDADO', name: payload.name, submittedAt: new Date().toISOString(), total, max: 50, grade: total / 10, correctCount: total / 5, review };
};\n</script>`;
const html = fs.readFileSync(path.join(__dirname, 'Index.html'), 'utf8').replace('  <script>', bridge + '\n  <script>');
fs.writeFileSync(path.join(__dirname, 'vista-previa.html'), html);
console.log('Vista previa generada: apps-script-cuestionario/vista-previa.html');
