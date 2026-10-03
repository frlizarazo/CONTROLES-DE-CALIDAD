# ControlCalidadBase

## Descripción

`ControlCalidadBase` es una **clase abstracta base** diseñada para establecer una estructura común para los diferentes procesos de **control de calidad de datos hidrometeorológicos**.

La clase utiliza el módulo `abc` de Python para definir una interfaz que debe ser implementada por todas las clases de control de calidad que hereden de ella.

Su objetivo principal es estandarizar el flujo de trabajo de los controles, definiendo tres operaciones fundamentales:

1. **Procesar** los datos y aplicar las reglas de validación.
2. **Graficar** los resultados para realizar análisis descriptivos o de diagnóstico.
3. **Escribir archivos** con los resultados obtenidos.

Al ser una clase abstracta, `ControlCalidadBase` no está diseñada para ser utilizada directamente, sino como base para implementar controles específicos.

---

## Dependencias

La clase utiliza las siguientes librerías:

```python
from abc import ABC, abstractmethod
import pandas as pd
from typing import Tuple, List, Any, Dict
```

### `abc`

Se utiliza para definir la clase como abstracta y establecer métodos que obligatoriamente deben ser implementados por las clases hijas.

### `pandas`

Se utiliza para trabajar con los datos almacenados en estructuras `DataFrame`.

### `typing`

Se utiliza para definir los tipos esperados de los atributos, parámetros y valores de retorno.

---

## Estructura de la clase

```text
ControlCalidadBase
│
├── df_original
├── kwargs
├── df_procesado
├── eliminados
├── observaciones
│
├── procesar()
├── graficar()
└── escribir_archivos()
```

---

## Inicialización

La clase recibe un `DataFrame` y parámetros adicionales opcionales:

```python
def __init__(self, df: pd.DataFrame, **kwargs: Any):
```

### Parámetros

| Parámetro  | Tipo           | Descripción                                                                                       |
| ---------- | -------------- | ------------------------------------------------------------------------------------------------- |
| `df`       | `pd.DataFrame` | DataFrame que contiene los datos sobre los cuales se aplicará el control de calidad.              |
| `**kwargs` | `Any`          | Parámetros adicionales que pueden ser utilizados por las clases hijas para configurar el control. |

El DataFrame recibido se copia mediante:

```python
self.df_original = df.copy()
```

Esto permite conservar una versión original de los datos y evitar modificar directamente el DataFrame suministrado por el usuario.

---

# Atributos

## `df_original`

```python
self.df_original: pd.DataFrame
```

Contiene una copia de los datos originales recibidos por el control de calidad.

Su propósito es conservar el estado inicial de los datos antes de aplicar cualquier transformación, validación o eliminación.

---

## `kwargs`

```python
self.kwargs: Dict[str, Any]
```

Almacena parámetros adicionales proporcionados durante la creación de la instancia.

Esto permite que diferentes controles puedan recibir configuraciones particulares sin modificar la estructura de la clase base.

Por ejemplo:

```python
control = MiControl(
    df,
    limite_superior=100,
    limite_inferior=0
)
```

---

## `df_procesado`

```python
self.df_procesado: pd.DataFrame
```

Inicialmente se crea como un `DataFrame` vacío.

Después de ejecutar el método `procesar()`, debe contener los datos que cumplen las reglas establecidas por el control de calidad.

---

## `eliminados`

```python
self.eliminados: pd.DataFrame
```

Inicialmente es un `DataFrame` vacío.

Debe almacenar los registros que fueron identificados como inválidos o que no cumplen las reglas del control de calidad.

---

## `observaciones`

```python
self.observaciones: List[str]
```

Lista destinada a almacenar mensajes descriptivos relacionados con el proceso.

Puede utilizarse para registrar información como:

* Reglas aplicadas.
* Cantidad de registros evaluados.
* Cantidad de registros eliminados.
* Advertencias.
* Situaciones particulares encontradas durante el procesamiento.

---

# Métodos abstractos

La clase define tres métodos abstractos mediante `@abstractmethod`.

Esto significa que **toda clase que herede de `ControlCalidadBase` debe implementar estos métodos**.

---

## `procesar()`

```python
@abstractmethod
def procesar(self) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
    pass
```

### Objetivo

Ejecuta las reglas específicas del control de calidad sobre el DataFrame original.

El método debe realizar las validaciones correspondientes y actualizar los resultados del proceso.

### Retorno

Debe retornar una tupla con tres elementos:

```python
(
    df_procesado,
    eliminados,
    observaciones
)
```

Donde:

| Elemento        | Tipo           | Descripción                                          |
| --------------- | -------------- | ---------------------------------------------------- |
| `df_procesado`  | `pd.DataFrame` | Datos que permanecen después de aplicar el control.  |
| `eliminados`    | `pd.DataFrame` | Registros identificados como inválidos o eliminados. |
| `observaciones` | `List[str]`    | Información y mensajes generados durante el proceso. |

### Ejemplo

```python
def procesar(self):
    # Aplicar reglas de validación
    ...

    self.df_procesado = ...
    self.eliminados = ...
    self.observaciones = ...

    return (
        self.df_procesado,
        self.eliminados,
        self.observaciones
    )
```

---

# `graficar()`

```python
@abstractmethod
def graficar(self) -> None:
    pass
```

### Objetivo

Genera gráficos descriptivos o de diagnóstico relacionados con el control de calidad.

Dependiendo del control
