# A01796044_A5.2 - Compute Sales

Actividad 5.2 – Ejercicio de programación (Pruebas de Software y Aseguramiento de la Calidad).

## Requisitos

- Python 3.7+
- pylint y flake8: `pip install -r requirements.txt`

## Uso

```bash
cd source
python computeSales.py ../data/priceCatalogue.json ../data/salesRecord.json
```

El programa escribe `SalesResults.txt` en el directorio actual (directorio desde donde se invoca).

## Estructura de archivos JSON

**priceCatalogue.json** – Catálogo de precios:
```json
[
  {"title": "Product A", "price": 10.50},
  {"title": "Product B", "price": 25.00}
]
```

**salesRecord.json** – Registro de ventas:
```json
[
  {
    "Sale": "Sale 001",
    "Products": [
      {"title": "Product A", "quantity": 2},
      {"title": "Product B", "quantity": 1}
    ]
  }
]
```

También se aceptan las claves alternativas: `name`, `product` (producto); `products`, `items` (lista de productos); `quantity`, `qty`, `amount` (cantidad).

## Pruebas

```bash
python -m pytest tests/test_computeSales.py -v
```

O con unittest:
```bash
cd tests && python -m unittest test_computeSales -v
```

## Verificación de calidad

**Flake8:**
```bash
flake8 source/computeSales.py tests/test_computeSales.py
```

**Pylint:**
```bash
pylint source/computeSales.py tests/test_computeSales.py --jobs=1
```

## Estructura del proyecto

```
A01796044_A5.2/
├── source/
│   └── computeSales.py
├── data/
│   ├── priceCatalogue.json
│   └── salesRecord.json
├── tests/
│   └── test_computeSales.py
├── results/
│   ├── SalesResults.txt
│   ├── TestResults.txt
│   ├── Flake8Results.txt
│   └── PylintResults.txt
├── requirements.txt
├── .flake8
├── .pylintrc
├── README.md
└── DOCUMENTACION_RESULTADOS.md
```
