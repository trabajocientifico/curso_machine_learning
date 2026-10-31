# Evaluación conceptual de Machine Learning

Formulario para el Módulo 2: Machine Learning para la Investigación. Cuenta propietaria confirmada: **opvargas23@gmail.com**. Preparado el 31 de octubre de 2026.

Proyecto creado en Google Apps Script:
https://script.google.com/home/projects/1aDq8oFDdiH0DfMW6_KWX1yuGw-gKu3OdFO02znsshEQ1rHBNKJmKSY_U/edit

**Publicado y verificado.**

- [Formulario para los participantes](https://script.google.com/macros/s/AKfycbwyTWAx8apfLUpsCbQ2J6i-gBwXiDjazVcvdHMApXHL6WWZ_yvKenM2nKYCcAGSQN53/exec).
- [Resultados y dashboard privados](https://docs.google.com/spreadsheets/d/1aSErPd_QxY3ZX0N37AKeWguRQUYa8qexWVGnXxlz9bc/edit).
- [Copia inicial en Excel](Resultados-machine-learning.xlsx). Para obtener respuestas futuras, exporte nuevamente desde la hoja.

La prueba real de guardado y actualización del dashboard fue satisfactoria; se retiró el registro técnico. El libro está listo para recibir participantes. Véase `ESTADO-DESPLIEGUE.md`.

## Qué incluye

- Nombre completo obligatorio y 10 preguntas de selección única, con cuatro opciones cada una.
- Navegación por preguntas, progreso y revisión de todas las respuestas antes del envío.
- Calificación en el servidor: **5 puntos por acierto y 0 por error**; total sobre 50; nota sobre 5 = total / 10. No hay puntuaciones parciales porque cada pregunta tiene una sola respuesta correcta.
- Resultado inmediato después de confirmar el guardado, explicaciones y comprobante personal descargable en texto.
- Google Sheets privado con cuatro pestañas: `Dashboard`, `Respuestas`, `Preguntas` y `Guía`.
- Registro de cada respuesta y su puntaje, nombre, fecha/hora de Bogotá, duración, total, nota y porcentaje.
- Dashboard con número de intentos, promedios y aciertos por pregunta; gráfico de barras.
- Exportación de todo el libro a Excel desde **Archivo → Descargar → Microsoft Excel (.xlsx)**.

## Archivos

| Archivo | Uso |
|---|---|
| `Code.gs` | Banco, calificación, validación, almacenamiento y creación de la hoja. En el editor remoto se llama `Código.gs`. |
| `Index.html` | Formulario adaptable a pantallas pequeñas. |
| `appsscript.json` | Zona horaria, entorno V8 y permisos del proyecto. |
| `vista-previa.html` | Demostración autónoma: abrir en el navegador. **No guarda datos en Google.** Contiene claves solo para simular la corrección; no publicarla como evaluación. |
| `PREGUNTAS.md` | Las 10 preguntas, opciones, claves y justificaciones para revisión docente. |
| `REGISTRO-PROYECTO.md` | Inventario de los HTML del curso y decisiones pedagógicas. |
| `tests/quiz.test.cjs` | Pruebas de lógica y persistencia con servicios simulados. |

## Puesta en marcha

Los tres archivos de producción se cargaron en el proyecto enlazado. Si necesita reinstalarlo:

1. Abra Google Apps Script con la cuenta propietaria y cree un proyecto.
2. Pegue `Code.gs` en el archivo de código y cree un archivo HTML llamado exactamente `Index` con el contenido de `Index.html`.
3. En Configuración del proyecto, active «Mostrar el archivo de manifiesto appsscript.json en el editor» y copie el manifiesto incluido.
4. Seleccione **configurarProyecto** en la lista de funciones y pulse **Ejecutar**. Complete personalmente la autorización solicitada por Google. Si la primera ejecución se detiene por permisos, vuelva a ejecutarla.
5. En el registro de ejecución aparecerá `RESULTADOS Y DASHBOARD` seguido del enlace de la nueva hoja. La función conserva el mismo libro si se ejecuta de nuevo después de terminar correctamente.
6. Seleccione **Implementar → Nueva implementación → Aplicación web**. Configure «Ejecutar como: Yo (opvargas23@gmail.com)» y «Quién tiene acceso: Cualquier usuario» para participantes sin cuenta. Publique y conserve la URL que termina en `/exec`.
7. Abra esa URL, complete un intento identificado como prueba y compruebe su fila y el dashboard en la hoja. No se considera listo para estudiantes hasta verificar este guardado real.
8. Comparta únicamente la URL `/exec`; mantenga restringidos el proyecto y la hoja.

La aplicación usa el [servicio HTML y sus llamadas asíncronas](https://developers.google.com/apps-script/guides/html/communication) y la [implementación como aplicación web](https://developers.google.com/apps-script/guides/web) de Google. Solo solicita acceso a hojas de cálculo e identidad de correo; no requiere Gmail, contactos ni archivos generales de Drive. El permiso de hojas que ofrece Apps Script es amplio, aunque este código solo crea y usa el libro de resultados.

## Uso y mantenimiento

El dashboard cuenta **intentos**, no personas únicas. El nombre completo no autentica a la persona: alguien puede abrir de nuevo el formulario y presentar otro intento. No se recoge correo, documento de identidad ni contraseña. No se han definido umbrales de aprobación que el docente no haya solicitado.

Un reenvío técnico utiliza el mismo identificador y devuelve el comprobante guardado sin otra fila. Si una conexión falla, use **Reintentar envío** sin recargar. Durante ese reintento las respuestas se mantienen fijas para no alterar un envío que pudo haberse guardado. Si recarga antes del envío, se perderán las respuestas; no se almacena el nombre en el almacenamiento persistente del navegador. La sesión admite hasta 24 horas.

La pestaña `Preguntas` es documental; **editarla no modifica el formulario**. Para cambiar el contenido se edita `QUESTIONS` en `Code.gs`. Para otra evaluación con distinto banco, cree una copia del proyecto y un libro nuevo para no mezclar indicadores de preguntas distintas. Las propiedades del script guardan `SPREADSHEET_ID` y el secreto de firma; no las publique.

Si la creación inicial se interrumpe, `PENDING_SPREADSHEET_ID` conserva el libro parcial para completar la instalación al volver a ejecutar `configurarProyecto`. No se elimina ningún libro automáticamente.

## Verificación local

Desde la raíz del repositorio:

```powershell
node --test apps-script-cuestionario/tests/quiz.test.cjs
node apps-script-cuestionario/crear-vista-previa.cjs
```

Las pruebas cubren notas extremas y mixtas, las 30 columnas de cada registro, ausencia de claves en `getQuiz`, puntajes manipulados, preguntas faltantes, nombres, fórmulas maliciosas en celdas, tokens inválidos, reenvíos, bloqueo y fallos de escritura. Los servicios de Google se simulan: estas pruebas no sustituyen la verificación del despliegue real.
