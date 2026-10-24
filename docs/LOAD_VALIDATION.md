# Validación de carga regulada — 24 de octubre de 2026

Equipo disponible: **Intel Core i7-8700 @ 3.20 GHz**, seis núcleos físicos / doce procesadores lógicos, **Intel UHD Graphics 630**, Windows x64, kernel **10.0.26300**. No había batería instalada. No se realizaron ensayos físicos de autonomía, conexión del cargador o brillo.

## Resultados físicos

Muestreo por segundo; uso global promediado sobre tres muestras. Cada ensayo duró cinco minutos. Se excluyen los primeros 15 segundos de adaptación; quedan aproximadamente 285 segundos evaluados. CPU admite ±5 puntos y GPU ±10; el criterio exige al menos 90 % de cumplimiento simultáneo.

| Ensayo CPU/GPU | CPU media (mín.–máx.) | GPU media (mín.–máx.) | Cumplimiento | Resultado |
|---|---|---|---|---|
| 0/50 | Sin objetivo CPU | 49.98 % (45.84–54.94) | 100 % | Perfil válido |
| 50/0, calibración con actividad externa variable | 50.12 % (40.27–64.23) | Sin objetivo GPU | 79.39 % | Perfil no válido |
| **100/50, motor entregado** | **99.99 % (99.75–100)** | **49.93 % (42.81–55.92)** | **100 %** | **Perfil válido** |

En el ensayo de calibración CPU 50 %, la actividad externa estimada variaba ampliamente y llegó a superar por sí sola el objetivo. Una media cercana al objetivo no certifica estabilidad: se conservan las desviaciones y el resultado no válido. Ese ensayo incluyó la corrección anticipada de la media móvil; posteriormente se añadió el corte inmediato de carga propia cuando la estimación externa supera el objetivo. CPU 20/30/50 % en condiciones de reposo y GPU 20/30/100 % todavía requieren ensayos de laboratorio.

En la prueba conjunta se solicitaron inicialmente un núcleo físico y CPU 100 %; el motor amplió a los seis núcleos físicos. Durante su ejecución pasaron las pruebas de respuesta de interfaz ante consultas lentas y una sesión real de interfaz/auxiliar sin carga adicional, con registro y cierre asíncrono. La sesión de interfaz usó registros en `build/load-ui-records` para mantener la comprobación dentro del proyecto.

Los datos por segundo están en `build/load-gpu50.json`, `build/load-cpu50-final.json` y `build/load-combined-final.json`. Los archivos de compilación/ensayo no se versionan; esta tabla conserva los resultados relevantes. SHA-256 de `PatiaLoadHost.dll` utilizado en el ensayo conjunto:

```text
d46544c853c69af7956cfaa9414f6b8da14cfc159fdef78f1ab785f75af6c8e7
```

## Comprobaciones automatizadas y distribución

- **41 pruebas Python aprobadas**, incluidas tres pruebas opcionales con el auxiliar nativo real: actualización/parada/cierre en un único proceso, watchdog de comunicación y terminación mediante Job Object. Se ejecutaron habilitando `PIXELTEST_NATIVE_TESTS=1`.
- **30 comprobaciones nativas de carga aprobadas**: realimentación, actividad externa, objetivos 0/20/30/50/100, límites, topología híbrida/SMT/grupos y contadores GPU por LUID.
- **14 comprobaciones del recolector de hardware aprobadas**.
- Prueba real de ventana principal y sesión interfaz/auxiliar, con muestras JSONL, resumen, cancelación única y cierre completo de hilos.
- Portable generado en `dist/carga-regulada/PixelTest/PixelTest.exe`. Se verificaron módulos Python incorporados, hashes del auxiliar y runtime, licencias y ausencia de PowerMax y los ejecutables de inventario sustituidos.

## Validación pendiente

No se certifica aún la matriz completa Intel/AMD, SMT e híbridos físicos, GPU AMD/NVIDIA y equipos con múltiples adaptadores. Falta la comparación visual con los contadores de Windows en esos equipos, las pruebas físicas de batería y restauración de brillo, ensayos prolongados de autonomía y ejecución en instalaciones limpias Windows 10/11 sin Python/.NET. El portable incluye los runtimes; su inclusión no sustituye esa comprobación en equipos limpios.
