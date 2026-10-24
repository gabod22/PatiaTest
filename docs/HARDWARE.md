# Módulos de hardware de PatiaTest

La aplicación consulta las baterías, discos, CPU, RAM, placa/BIOS y GPU sin ejecutar BatteryInfoView, CrystalDiskInfo, CPU-Z, GPU-Z ni HWiNFO. Python conserva la interfaz PySide6 y las métricas de `psutil`; `PatiaHardwareHost`, un componente propio en C#, consulta Windows y las bibliotecas integradas.

## Compilar y ejecutar

Se requiere Windows x64, Python 3.10 o posterior y el SDK .NET **10.0.400** para compilar. El runtime .NET queda incluido en el componente portable; no se necesita instalarlo en los equipos de diagnóstico.

Desde la raíz del proyecto:

```powershell
python -m pip install -r requirements.txt
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-hardware.ps1
python PixelTest.py
```

Ejecutar como administrador para permitir el acceso al hardware que lo requiere. Para crear la distribución completa:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-portable.ps1
```

El resultado es **`dist/PixelTest/PixelTest.exe`**. Copiar la carpeta completa, incluido `_internal`. El archivo de PyInstaller incluye el componente, su runtime, las licencias y el preparador de sensores. Excluye los ejecutables sustituidos y sus exportaciones. Los otros programas de pruebas se conservan.

Si esa copia está abierta, Windows impide reemplazarla. Se puede generar otra distribución con `python -m PyInstaller --noconfirm --workpath build/portable --distpath dist/actualizado PixelTest.spec`; su ejecutable queda en `dist/actualizado/PixelTest/PixelTest.exe`.

`runtime/`, los paquetes restaurados y los resultados de compilación no se versionan. `packages.lock.json`, `global.json`, el proyecto C# y el manifiesto del instalador fijan la configuración de compilación. `scripts/build-hardware.ps1 -SkipAssets` permite recompilar sin descargar nuevamente los recursos ya preparados.

## Uso

La pestaña **Hardware** contiene Baterías, Discos, CPU/RAM/placa, GPU y Sensores. También se puede acceder a cada vista desde Herramientas. El resumen existente muestra todos los discos y baterías, sin el límite anterior de cinco columnas.

Las vistas muestran solo los datos de revisión: batería (salud y capacidades, ciclos, carga y alimentación); discos (modelo, serie, capacidad, interfaz/volúmenes, salud, desgaste disponible, temperatura, lecturas/escrituras y horas/encendidos); CPU (modelo, núcleos, hilos y frecuencia nominal); RAM (ranura, capacidad, tipo, velocidad y fabricante); placa/BIOS (fabricante/modelo, versión y fecha); GPU (modelo, fabricante, memoria y controlador). La fuente y el motivo de un dato ausente se consultan pasando el cursor. Los registros SMART crudos, identificadores internos, instrucciones CPUID, temporizaciones y metadatos duplicados no se muestran.

Sensores prioriza temperatura y uso global de CPU/GPU/RAM, frecuencia media de los núcleos, potencia, memoria en uso, ventiladores y actividad de cada disco. Se omiten las cargas por hilo y los límites o perfiles estáticos de los sensores. El nombre original, fuente e instante de lectura quedan en la ayuda emergente.

- **Actualizar dispositivos** vuelve a enumerar el hardware y reabre el proveedor de sensores.
- **Preparar sensores (PawnIO)** inicia el instalador oficial **2.2.0** incluido en el paquete. Verifica SHA-256 y firma digital antes de ejecutarlo. La instalación requiere UAC y la elección de la edición oficial firmada; el monitor no instala el controlador automáticamente.
- **Reiniciar mínimos/máximos** elimina los extremos acumulados durante la sesión.
- Las lecturas de sensores se solicitan cada segundo. SMART se consulta cada 30 segundos; la detección de discos mediante WMI, cada 10 segundos. Una consulta lenta puede ampliar el intervalo, sin bloquear la interfaz.
- Una lectura caducada muestra un guion, conserva su instante original y no se incorpora a los extremos como una medición nueva. El límite es de 5 segundos para sensores y 65 para SMART.

Si se instala PawnIO durante la sesión, el preparador reinicia únicamente el componente de hardware para volver a detectar el controlador. Si la instalación pide reiniciar Windows, realizar ese reinicio antes de evaluar los sensores.

## Fuentes y cálculos

| Área | Fuente | Tratamiento |
|---|---|---|
| Baterías físicas | SetupAPI y `IOCTL_BATTERY_QUERY_*` | Nombre, fabricante, serie, fecha, química, capacidades, ciclos, voltaje, carga/descarga, temperatura y autonomía cuando el controlador los entrega. |
| Salud de batería | Capacidad completa / capacidad de diseño × 100 | No se calcula con capacidades desconocidas, cero o relativas. Un valor superior a 100 % se conserva. |
| Inventario de almacenamiento | WMI y DiskInfoToolkit 1.1.2 | Incluye unidades sin letra, USB y dispositivos visibles para Windows aunque no permitan consultar SMART. |
| Salud y desgaste de discos | SMART y reglas de fabricante de la biblioteca | Estado y vida restante son campos diferentes. Los HDD no reciben un porcentaje de vida genérico. |
| NVMe | Registro SMART normalizado | Los contadores de datos se multiplican por 512 000 bytes. Los 128 bits se conservan como texto decimal en el protocolo y como enteros exactos en Python. |
| Desgaste NVMe | `percentage_used` | Se conserva el desgaste original, incluso por encima de 100. La vida restante estimada es `max(0, 100 - percentage_used)`. Cero advertencias críticas no garantiza ausencia de cualquier fallo. |
| Lectura/escritura actual | `psutil` / contadores de Windows | Velocidad en B/s por disco, separada de los contadores acumulados SMART. |
| CPU, RAM y placa/BIOS | WMI/SMBIOS; `py-cpuinfo` para el resumen inicial | Frecuencias nominales/configuradas separadas de sensores actuales. El monitor no repite la consulta CPUID ni muestra SPD o temporizaciones. |
| GPU | DXGI, WMI, NVML y AMD ADL cuando están instalados | Memoria dedicada separada de la memoria compartida máxima. Los DLL de los proveedores se cargan desde Windows; no se redistribuyen. |
| Sensores | LibreHardwareMonitorLib 0.9.6 | CPU/GPU/RAM/placa, temperaturas, carga, frecuencias, potencia, voltajes y ventiladores disponibles. No se exponen funciones de control. |

El componente puede entregar los atributos SMART originales en el protocolo, pero la interfaz conserva únicamente el resumen útil de salud y uso. Las conversiones SATA específicas de fabricante proceden de DiskInfoToolkit; los campos sin una interpretación disponible permanecen desconocidos. Los contadores SATA convertidos se presentan en GiB según las conversiones binarias de esa versión de la biblioteca.

**No disponible** es diferente de cero o de un estado de salud bueno. El motivo y la fuente acompañan al dato. Un puente USB o una controladora RAID puede ocultar SMART; una RAM puede no tener sensor térmico o bloquear SPD. No se completan especificaciones mediante una base de modelos ni se deducen por el nombre comercial.

## Protocolo y recuperación

Python crea un único proceso hijo oculto, por ruta absoluta y sin shell. La comunicación usa JSON UTF-8 por líneas sobre stdin/stdout. No hay servidor de red ni archivos CSV/TXT/XML intermedios. La salida de diagnóstico del componente se separa del protocolo.

Solicitud:

```json
{"version":1,"id":"identificador-de-solicitud","operation":"inventory"}
```

Operaciones: `inventory`, `sample`, `refresh_devices`, `shutdown`. Cada respuesta incluye `version`, `id`, `operation`, `timestamp`, `devices`, `readings` y `errors`. Los dispositivos tienen `id`, `kind`, `name` y `fields`; cada campo contiene valor, unidad, fuente, disponibilidad y motivo. Cada lectura identifica dispositivo y sensor, e incluye valor, unidad, fuente e instante UTC.

Los proveedores trabajan en paralelo y disponen de 1,5 segundos para entregar resultados. Un proveedor pendiente no se ejecuta otra vez simultáneamente. Se devuelven resultados parciales y los campos anteriores se marcan caducados cuando falla la consulta. El cliente limita a 5 segundos la espera de cada respuesta, valida su identidad/versión y puede reiniciar su propio proceso. Diez respuestas consecutivas con un proveedor bloqueado provocan su recuperación mediante reinicio del componente. Nunca se termina un proceso por nombre global.

Un `QThread` dedicado ejecuta las consultas, filtrado, formato y cálculo de mínimos/máximos. Publica una única muestra reemplazable; la interfaz toma la más reciente cada 250 ms y no acumula señales con lecturas atrasadas. Los modelos de las tablas viven en el hilo gráfico y actualizan solo los valores cambiados, sin reconstruir celdas ni recalcular anchos en cada muestra. Solo se actualiza la vista de detalle visible. Las lecturas caducan aunque deje de llegar información. El cierre de la ventana solicita la parada y espera su señal de finalización sin bloquear el bucle gráfico. [Reglas de hilos y modelos de Qt](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QAbstractTableModel.html#thread-safety).

El monitor de `psutil` sigue siendo independiente. La ausencia o retirada de batería termina las pruebas de descarga existentes con un mensaje, sin acceder a un objeto inexistente.

## Verificación y cobertura

```powershell
python -m unittest discover -s tests -v
runtime/hardware/PatiaHardwareHost.exe --self-test
python scripts/smoke-hardware.py
python scripts/smoke-ui.py
```

Las pruebas automatizadas cubren resultados parciales, identidad y versión del protocolo, respuestas inválidas, cierre inesperado, recuperación, tiempo de espera, eliminación del hijo propio, marcas de tiempo .NET/Python 3.10, valores desconocidos/caducados, extremos de sensores, siete dispositivos por tabla y retirada de batería. Las comprobaciones nativas cubren salud de batería, capacidades relativas/desconocidas, contadores NVMe de 128 bits, unidades, desgaste, advertencias críticas y aislamiento/recuperación de proveedores.

Validación realizada el **23 de octubre de 2026**:

- Compilación y publicación Windows x64 con runtime incluido: correctas, sin advertencias del compilador.
- 16 pruebas Python/Qt correctas; las 14 comprobaciones nativas de la implementación anterior se conservan.
- Prueba de respuesta de la interfaz con consultas de 350 ms y 2.000 lecturas: consultas fuera del hilo gráfico, actualizaciones del modelo en el hilo gráfico, temporizador de interfaz activo, valores actualizados sin reiniciar el modelo y parada sin espera síncrona.
- Ventana principal: renderizada con el módulo real, unas 10 filas de sensores/estados principales y cierre limpio. El script de prueba omite cambios de Wi-Fi, energía y cámara; genera `build/hardware-ui.png`.
- Equipo anfitrión Windows, compilación 26300: Intel Core i7-8700, Intel UHD Graphics 630, placa modelo 312A, dos módulos RAM y discos Patriot M.2 P300 1024GB / WDC WD10EZEX-08WN4A0. Se comprobaron respuestas parciales durante el arranque y recuperación de los datos de inventario en la siguiente consulta.
- Entorno restringido: WMI denegado, mientras DXGI y parte de los sensores siguieron respondiendo. Fuera del aislamiento, WMI entregó el inventario. Sin PawnIO instalado se obtuvieron 62 lecturas declaradas, de las que 40–41 tenían valores disponibles durante el muestreo.
- Instalador PawnIO 2.2.0: SHA-256 y firma Authenticode válidos. **No se instaló el controlador en el equipo anfitrión.**

Pendiente de validación física: Windows 10 limpio y Windows 11 sin runtimes de desarrollo, portátiles con una y varias baterías, AMD/NVIDIA y GPU híbrida, discos SATA/NVMe con acceso SMART elevado, diferentes puentes USB/RAID, GPU con más de 4 GiB, SPD accesible, sensores después de instalar PawnIO y suspensión/reanudación. Las pruebas simuladas no sustituyen esa matriz ni una comparación simultánea con las herramientas originales.

## Dependencias y referencias

El paquete incluye los textos de licencia, metadatos y referencias de fuentes en `_internal/runtime/licenses/DEPENDENCIES.txt`. Las bibliotecas se distribuyen sin modificar. El instalador del controlador permanece como un recurso separado y se ejecuta solo desde la preparación explícita.

- [LibreHardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor), [DiskInfoToolkit](https://github.com/Blacktempel/DiskInfoToolkit).
- [Baterías en Windows](https://learn.microsoft.com/en-us/windows/win32/power/enumerating-battery-devices), [NVMe en Windows](https://learn.microsoft.com/en-us/windows/win32/fileio/working-with-nvme-devices), [DXGI](https://learn.microsoft.com/en-us/windows/win32/api/dxgi/ns-dxgi-dxgi_adapter_desc).
- [PawnIO oficial](https://pawnio.eu/), [instalador 2.2.0](https://github.com/namazso/PawnIO.Setup/releases/tag/2.2.0).
- [NVML](https://docs.nvidia.com/deploy/nvml-api/), [AMD ADL](https://github.com/GPUOpen-LibrariesAndSDKs/display-library).
