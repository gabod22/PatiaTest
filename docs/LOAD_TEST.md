# Carga CPU/GPU y pruebas de batería

La herramienta está en **Herramientas → Carga CPU/GPU** y en su propia pestaña. También se reutiliza en los tres modos de batería. PowerMax y `cpu_load_generator` ya no se utilizan ni distribuyen.

## Uso y resultados

Los objetivos editables de 0 a 100 % corresponden al **uso total**, incluidas otras aplicaciones. Cero desactiva el generador del recurso. Se seleccionan núcleos físicos iniciales y GPU; el motor puede ampliar los núcleos y muestra la cantidad efectiva. Perfiles CPU/GPU: Básico 20/0, Intermedio 50/30, Exigente 100/100 y Personalizado.

Solo hay una sesión compartida. La carga independiente permite aplicar cambios durante la ejecución; cada cambio reinicia la adaptación y evaluación del perfil y queda registrado. En batería, los parámetros están bloqueados. Sin adaptador o contadores GPU compatibles se deshabilita el objetivo gráfico y se explica el motivo; al iniciar se comprueban también Direct3D 11 y una lectura válida. No se usa WARP ni CPU como sustitución gráfica.

| Modo | Finalización |
|---|---|
| Por tiempo | Duración configurada, remanente mínimo y perfil válido si se activó carga. Exactamente 20 % satisface un mínimo de 20 %. |
| Exhaustiva | Autonomía hasta el corte; carga opcional inicialmente desactivada. No implica aprobación de batería. |
| Intensiva | Autonomía hasta el corte; carga inicialmente activada y al menos un objetivo positivo. No implica aprobación de batería. |

Valores iniciales: 120 minutos, remanente 20 %, corte 10 %, brillo 100 %. Las preferencias anteriores de duración y remanente se conservan. Corte y brillo se guardan en Configuración; el corte también puede elegirse antes de cada prueba. El brillo se captura y restaura cuando Windows ofrece control WMI; cualquier problema queda como advertencia en el registro. La inhibición de suspensión es temporal, sin cambiar el plan de energía.

No se inicia con cargador, batería ausente, porcentaje inválido o carga inicial que ya alcance el umbral. Conectar el cargador, retirar/cambiar baterías detectadas, suspender, superar un límite térmico o perder mediciones interrumpe la prueba. Se distinguen cancelación, interrupción, fallo del criterio de batería, error y perfil no válido. Se libera la carga antes del único resultado.

Los límites térmicos configurables iniciales son CPU 95 °C y GPU principal 90 °C durante tres segundos con lecturas recientes. Se excluyen hotspot/memoria y sensores de otras GPU. La ausencia de temperatura muestra supervisión parcial; no se inventan datos ni instala un controlador automáticamente.

## Implementación

`PatiaLoadHost` es un auxiliar C#/.NET 10 separado de `PatiaHardwareHost`. La coordinación y consulta de capacidades se ejecutan en `QThread`; la interfaz consume la última muestra sin consultas bloqueantes.

CPU: afinidad de grupo/procesador, topología física/SMT y clase de eficiencia de Windows, prioridad inferior a la normal y ventanas de trabajo/descanso de unos 100 ms. El uso global se mide por PDH `Processor Information(_Total) / % Processor Time`. La cantidad de núcleos se amplía según la capacidad disponible y la realimentación.

GPU: shader FP32 propio Direct3D 11 mediante Vortice 3.8.3. Solo hay un paquete pendiente; timestamps GPU adaptan paquetes de aproximadamente 3–10 ms. Un paquete sin respuesta durante un segundo provoca error. El adaptador se identifica por LUID DXGI; se suman contadores `GPU Engine / Utilization Percentage` de todos los procesos por motor y se toma el motor más ocupado de esa GPU, según el [criterio de Microsoft](https://devblogs.microsoft.com/directx/gpus-in-the-task-manager/).

Se muestrea cada segundo usando una media móvil de tres muestras. Si la actividad externa supera el objetivo, se reduce la carga propia; no se puede reducir el trabajo de otras aplicaciones. CPU busca ±5 puntos y GPU ±10. Los primeros 15 segundos consumen batería, pero se excluyen de estabilidad. Se exige cumplimiento conjunto durante al menos el 90 % del tiempo posterior. Las muestras ausentes, desviaciones e intervalos sin observación no certifican cumplimiento. Una sesión demasiado corta no obtiene perfil válido.

Protocolo JSON UTF-8 por líneas, sin shell, red ni archivos intermedios. Ejemplo: `{"version":1,"id":"x","operation":"start","config":{"cpu_target":20,"gpu_target":0,"initial_cores":0,"gpu_id":null}}`. Operaciones: `capabilities`, `start`, `update`, `status`, `stop`, `shutdown`. La respuesta conserva versión/id/operación y contiene `ok` más `data` o `error`. El estado distingue mediciones globales, objetivos, fracciones de trabajo del generador y núcleos efectivos. `cpu_generated` estima el tiempo CPU del auxiliar sobre la capacidad lógica total.

Un Job Object `KILL_ON_JOB_CLOSE` protege al auxiliar y un watchdog termina sesiones activas tras cinco segundos sin comunicación. EOF, cierre de PixelTest, errores y tiempos de espera liberan los procesos propios. El cierre de la interfaz espera asíncronamente al trabajador.

## Registros y compilación

Cada sesión escribe `%LOCALAPPDATA%/PixelTest/tests/<fecha-id>/samples.jsonl` y `summary.json`. Incluyen configuración, cambios, muestras por segundo, batería/alimentación, temperaturas disponibles, duración monotónica, cumplimiento, resultado del criterio de batería y causa de finalización. **Abrir registros** abre la última sesión o la carpeta general. Sustituye `c:/battery_test.txt`.

Igualar porcentajes no reproduce necesariamente el consumo eléctrico de una aplicación. Se registra el kernel `scalar-xorshift/d3d11-fp32-v1`; no es un benchmark ni un modelo universal de autonomía.

Compilar en Windows x64 con Python 3.10+ y SDK .NET 10.0.400:

```powershell
./scripts/build-hardware.ps1
./scripts/build-load.ps1
python -m unittest discover -s tests -v
./runtime/load/PatiaLoadHost.exe --self-test
$env:PIXELTEST_NATIVE_TESTS = '1'
python -m unittest discover -s tests -p test_load_native.py -v
Remove-Item Env:PIXELTEST_NATIVE_TESTS
python scripts/smoke-ui.py
./scripts/build-portable.ps1
```

El portable incluye ambos auxiliares, sus runtimes y licencias, sin necesitar Python o .NET instalados en destino. Copiar toda la carpeta de PyInstaller. [Vortice.Direct3D11/D3DCompiler 3.8.3](https://www.nuget.org/packages/Vortice.Direct3D11/3.8.3) y las dependencias transitivas quedan fijados mediante `packages.lock.json`; la recopilación de licencias incluye ambos proyectos.

Ensayo explícito y acotado: `python scripts/validate-load.py --cpu 50 --gpu 0 --seconds 300 --output build/load-cpu50.json`. Este script solo valida el motor, sin modificar brillo ni iniciar batería; no incorpora la supervisión térmica de la aplicación. Siempre cierra su auxiliar.

## Cobertura

Las pruebas automatizadas cubren límites, minutos/segundos, remanente exacto, batería ausente, cargador, cambio de baterías, suspensión, cancelación, pérdida de medición, cumplimiento conjunto, adaptación inicial, sensores caducados y limpieza antes del resultado. Incluyen consultas lentas fuera del hilo gráfico, configuración bloqueada, sesión única, protocolo y errores. Las comprobaciones nativas simulan actividad externa y topología híbrida/SMT/grupos y verifican agregación por LUID.

La matriz física completa Intel/AMD, SMT, GPU Intel/AMD/NVIDIA, batería prolongada y Windows 10/11 limpios sin runtimes instalados queda pendiente de laboratorio. No se presenta como realizada. Los resultados medidos localmente se detallan en [LOAD_VALIDATION.md](LOAD_VALIDATION.md).
