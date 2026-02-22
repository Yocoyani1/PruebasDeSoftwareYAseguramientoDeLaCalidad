# A01796044_A6.2 - Sistema de Reservaciones

Actividad 6.2 - Ejercicio de programación 3: Sistema de Reservaciones

**Matrícula:** A01796044

## Descripción

Sistema de reservaciones implementado en Python con las siguientes abstracciones:

- **Hotel**: Gestión de hoteles (crear, eliminar, mostrar, modificar, reservar habitación, cancelar reserva)
- **Customer**: Gestión de clientes (crear, eliminar, mostrar, modificar)
- **Reservation**: Gestión de reservaciones (crear, cancelar)

Los datos se almacenan en archivos JSON en el directorio `data/`.

## Requisitos

- Python 3.8+
- coverage, flake8, pylint (ver requirements.txt)

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

### Programa principal (menú interactivo)

```bash
python main.py
# o
python -m src
```

### Ejecutar pruebas unitarias

```bash
python -m unittest discover -v -s tests
```

### Verificar cobertura (>=85%)

```bash
coverage run -m unittest discover -s tests
coverage report
```

### Verificar estilo PEP8 con Flake8

```bash
flake8 src tests main.py
```

### Verificar con Pylint

```bash
pylint src
```

## Estructura del proyecto

```
A01796044_A6.2/
├── src/                   # Código fuente
│   ├── __init__.py       # Exporta Hotel, Customer, Reservation, ReservationSystem, main
│   ├── __main__.py       # Permite: python -m src
│   ├── models/           # Modelos de dominio
│   │   ├── hotel.py      # Clase Hotel
│   │   ├── customer.py   # Clase Customer
│   │   └── reservation.py # Clase Reservation
│   └── services/         # Lógica de negocio
│       └── system.py     # ReservationSystem y menú interactivo
├── tests/                 # Pruebas unitarias (estructura refleja src/)
│   ├── models/            # Tests de modelos
│   │   ├── test_hotel.py
│   │   ├── test_customer.py
│   │   └── test_reservation.py
│   └── services/          # Tests de servicios
│       └── test_system.py
├── data/                  # Archivos de datos
│   ├── hotels.json
│   ├── customers.json
│   └── reservations.json
├── main.py               # Punto de entrada
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Estándares

- PEP-8 compliant
- Sin advertencias de Flake8 ni Pylint
- Cobertura de tests >= 85%
- Manejo de datos inválidos en archivos (errores en consola, ejecución continúa)
