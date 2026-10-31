# Sistema de Registro de Incidencias 777

Aplicación de escritorio para el registro, seguimiento y administración de incidencias, desarrollada con Python y SQLite.

## Descripción

Sistema de Registro de Incidencias 777 es una aplicación diseñada para facilitar el control y seguimiento de problemas relacionados con usuarios y equipos. Permite registrar incidencias, asignar prioridades, actualizar estados y consultar su historial, manteniendo organizada la información en una base de datos local.

## Funcionalidades

- Registro de incidencias con nombre, equipo y descripción del problema.
- Asignación de prioridades (alta, media y baja).
- Administración de estados (pendiente, en proceso y resuelto).
- Consulta y visualización de incidencias registradas.
- Búsqueda de incidencias por ID, nombre o equipo.
- Panel de estadísticas con el total de incidencias y su distribución por estado.
- Actualización del estado de las incidencias.
- Registro del técnico responsable y fecha de resolución.
- Visualización del detalle de cada incidencia.
- Eliminación de incidencias con confirmación.
- Interfaz gráfica con indicadores visuales de prioridad y estado.

## Tecnologías utilizadas

- Python
- Tkinter
- SQLite
- ttk (Themed Tkinter)
- datetime

## Estructura del proyecto

```text
SistemaIncidencias/
├── main.py
├── incidencias.db
├── .gitignore
└── .gitattributes
```

## Instalación local

1. Instala Python 3.

2. Clona este repositorio:

```bash
git clone https://github.com/7Marilu7/SistemaIncidencias.git
```

3. Accede a la carpeta del proyecto:

```bash
cd SistemaIncidencias
```

4. Ejecuta la aplicación:

```bash
python main.py
```

La aplicación abrirá su interfaz gráfica y permitirá comenzar a registrar y administrar incidencias.

## Base de datos

El sistema utiliza SQLite para almacenar la información de las incidencias, incluyendo:

- Datos del usuario y equipo.
- Descripción del problema.
- Prioridad y estado.
- Fecha de registro.
- Técnico responsable de la resolución.
- Fecha de resolución.

La base de datos `incidencias.db` se inicializa automáticamente cuando se ejecuta la aplicación.

## Estado del proyecto

Proyecto desarrollado como parte de un portafolio personal.

## Autoría

Desarrollado por **María Guadalupe Cruz Paz**.

[GitHub](https://github.com/7Marilu7)
