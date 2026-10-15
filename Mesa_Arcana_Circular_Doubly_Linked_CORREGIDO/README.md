# Mesa Arcana — Mesa de cartas con turnos circulares

## Caso de estudio

Mesa Arcana simula una mesa de juego de cartas. Los jugadores se conectan en un círculo: el turno avanza a la derecha, se puede hacer reversa hacia la izquierda y saltar varias posiciones. Es un caso concreto y diferente de ejemplos comunes como relojes, bancos o editores de figuras.

## Estructura de datos

Una **lista circular doblemente enlazada** es una colección dinámica de elementos en la que cada elemento mantiene dos referencias: una al vecino de la derecha y otra al vecino de la izquierda. Es circular porque el último se conecta con el primero y viceversa.

En este proyecto, los nombres de clases, métodos, atributos, módulos y variables están en inglés. La interfaz y los mensajes que ve el usuario están en español.

Cada `Player` tiene `right_neighbor` y `left_neighbor`. Con un solo jugador, ambos enlaces apuntan al mismo objeto. Si se elimina al último jugador, la mesa queda vacía y `current_player` pasa a `None`; nunca quedan enlaces vacíos en una mesa que aún contenga jugadores.

## Funcionalidades

- Insertar al inicio, al final y en una posición intermedia (posiciones desde 1).
- Eliminar y buscar jugadores por nombre, sin distinguir mayúsculas.
- Recorrer la mesa hacia la derecha y hacia la izquierda.
- Avanzar turno, reversa y saltos positivos o negativos.
- Interfaz gráfica de escritorio en español con Tkinter.
- Menú alternativo por consola en español.
- Validación de nombres vacíos o duplicados y posiciones incorrectas.
- Comprobación de integridad de enlaces.
- Pruebas automáticas con `unittest`.

## Por qué aplica

En una mesa de cartas, los turnos se repiten circularmente. La estructura evita reiniciar manualmente el recorrido al llegar al último jugador. Como hay enlaces en ambos sentidos, la reversa se realiza siguiendo una única referencia. Los saltos se implementan recorriendo tantos enlaces como indique el usuario.

## Ventajas

- Recorrido en ambos sentidos.
- Avance de turno circular sin reiniciar desde el primer participante.
- Una vez localizado un jugador, reconectar enlaces al insertar o eliminar requiere O(1).
- Tamaño dinámico: admite agregar o quitar participantes.

## Desventajas

- Usa más memoria que una lista simplemente enlazada porque cada jugador mantiene dos referencias.
- Actualizar dos enlaces exige cuidado.
- Buscar por nombre requiere recorrer la estructura.
- Una referencia mal asignada puede romper el círculo; por eso se implementa `validate_integrity()`.

## Complejidad temporal

Sea **n** el número de jugadores.

| Operación | Complejidad | Explicación |
|---|---:|---|
| Insertar al inicio / final | O(n) total | Buscar nombres duplicados cuesta O(n); enlazar cuesta O(1) |
| Insertar en posición | O(n) | Recorre hasta la posición |
| Buscar | O(n) | Puede revisar todos los jugadores |
| Eliminar | O(n) | Buscar cuesta O(n), reconectar enlaces cuesta O(1) |
| Recorrer ambos sentidos | O(n) | Visita cada jugador una vez |
| Avanzar / reversa | O(1) | Sigue un enlace |
| Saltar k turnos | O(min(|k| mod n, n)) | Sigue los enlaces para completar el salto |
| Espacio | O(n) | Un objeto por jugador con dos referencias |

## Diagrama conceptual

```text
               right_neighbor →
       ┌────────────────────────────────┐
       ▼                                │
    [Ana] ⇄ [Beto] ⇄ [Cami] ⇄ [Dani]
       │                                ▲
       └────────────────────────────────┘
               ← left_neighbor

Last.right_neighbor = First
First.left_neighbor = Last
```

Con un único jugador, `right_neighbor` y `left_neighbor` apuntan al mismo jugador.

## Requisitos

- Python 3.10 o superior.
- Tkinter, normalmente incluido en Python para Windows.
- No requiere instalar paquetes externos.

## Ejecutar en Visual Studio Code (Windows)

1. Descarga y extrae el ZIP.
2. En Visual Studio Code, selecciona **Archivo → Abrir carpeta** y abre la carpeta `Mesa_Arcana_Circular_Doubly_Linked` que contiene `main.py`.
3. Abre **Terminal → Nueva terminal**. Comprueba que la terminal está en la carpeta que contiene `main.py`.
4. Ejecuta la interfaz gráfica:

   ```powershell
   py main.py
   ```

5. Para el menú de consola:

   ```powershell
   py console.py
   ```

No escribas `bash python main.py`: eso intenta ejecutar Bash mediante WSL. En PowerShell se utiliza directamente `py main.py`.

## Ejecutar las pruebas

Desde la carpeta raíz del proyecto:

```powershell
py -m unittest discover -s tests -v
```

El resultado esperado termina en `OK`.

## Organización

```text
Mesa_Arcana_Circular_Doubly_Linked/
├── main.py
├── console.py
├── README.md
├── .gitignore
├── card_table/
│   ├── __init__.py
│   ├── structure.py
│   └── ui.py
└── tests/
    └── test_structure.py
```

## Commits ordenados

Registra commits reales en cada etapa; no simules un historial previo. Ejemplo:

```bash
git init
git add README.md .gitignore
git commit -m "docs: document card table case study"
git add card_table/structure.py
git commit -m "feat: implement circular doubly linked table"
git add card_table/ui.py main.py console.py
git commit -m "feat: add Spanish desktop and console interfaces"
git add tests/
git commit -m "test: cover table operations and validation"
```
