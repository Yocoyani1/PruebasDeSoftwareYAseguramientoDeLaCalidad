# A01796044_A4.2

Actividad 4.2 – Ejercicios de programación (Pruebas de Software y Aseguramiento de la Calidad).

## Requisitos

- Python 3.7+
- pylint: `pip install -r requirements.txt`

## Uso (desde cada programa)

```bash
# P1 – Estadísticas (media, moda, mediana, varianza poblacional, desv. estándar poblacional)
cd P1/source
python computeStatistics.py ../../data/numbers.txt ../results

# P2 – Conversión a binario y hexadecimal
cd P2/source
python convertNumbers.py ../../data/numbers.txt ../results

# P3 – Conteo de palabras
cd P3/source
python wordCount.py ../../data/words.txt ../results
```

El segundo argumento (`../results`) es opcional: si se omite, el archivo de resultados se escribe en el directorio actual.

## Pruebas

Desde cada carpeta de tests:

```bash
cd P1/tests && python -m unittest test_computeStatistics -v
cd P2/tests && python -m unittest test_convertNumbers -v
cd P3/tests && python -m unittest test_wordCount -v
```

## PyLint

```bash
pip install pylint
pylint P1/source/computeStatistics.py P2/source/convertNumbers.py P3/source/wordCount.py
```

Se puede usar el archivo `.pylintrc` en la raíz para configurar reglas. Corregir todos los mensajes C, R, W, E y F que se deseen cumplir; después de cada cambio, ejecutar de nuevo las pruebas.

## Entrega

- **Repositorio:** Nombre tipo `Matrícula_Actividad` (ej. `A01796044_A4.2`). Subir la liga en Canvas.
- **Archivos fuente:** Subir los archivos fuente a Canvas según indique la tarea.
- **Evidencia:** En las carpetas `results` de cada programa (y opcionalmente P1 Results.xlsx y capturas de pantalla en lugar de PDF).

Más detalles en **DOCUMENTACION_RESULTADOS.md**.
