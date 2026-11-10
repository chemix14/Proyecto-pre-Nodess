# 🌐 Plataforma Web Pre-NODESS Teziutlán 🚀

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Bootstrap 5](https://img.shields.io/badge/Bootstrap_5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-green.svg?style=for-the-badge)](LICENSE)

> **Ciencia, tecnología e investigación comunitaria al servicio del desarrollo regional y la economía social y solidaria.**

---

## 📖 Descripción del Proyecto

**Pre-NODESS** (Nodo de Impulso a la Economía Social y Solidaria) es una plataforma web integral diseñada para visibilizar, articular y gestionar proyectos de investigación comunitaria, vinculación académica y desarrollo regional en el estado de Puebla y zonas de influencia.

La plataforma conecta activamente a **instituciones de educación superior** (TecNM Campus Teziutlán, Puebla, Minatitlán, CICATA-IPN, Universidad de la Sabana), **gobiernos locales** y **Organismos del Sector Social de la Economía (OSSE)** como cooperativas y colectivos comunitarios.

---

## ✨ Características Principales

- 🏛️ **Portal Institucional Dinámico:** Muestra la historia, áreas de enfoque, hitos, semblanzas de investigadores y municipios de impacto.
- 🤝 **Directorio de Alianzas y Redes:** Clasificación de aliados estratégicos (Academia, Sector Público y OSSE).
- 📁 **Gestión de Proyectos:** Catálogo público de proyectos de investigación aplicada con fichas detalladas por municipio.
- 🔒 **Panel de Administración Privado (`/admin`):**
  - Autenticación con sesiones cifradas y contraseñas seguras con hash (`bcrypt`).
  - CRUD completo para registrar, visualizar y eliminar proyectos, instituciones aliadas y municipios.
  - Actualización dinámica de información de contacto institucional.
- 🎨 **Interfaz Moderna y Responsiva:** Desarrollada con **Bootstrap 5**, animaciones fluidas con **AOS (Animate On Scroll)** y tipografías estilizadas (*Inter* y *Merriweather*).
- ⚡ **Semillero de Datos Rápido (`/init-db`):** Endpoint de inicialización automática con datos precargados para demostraciones y pruebas inmediatas.

---

## 🛠️ Tecnologías Utilizadas

| Capa | Tecnologías |
| :--- | :--- |
| **Backend** | [Python](https://www.python.org/) &bull; [FastAPI](https://fastapi.tiangolo.com/) &bull; [Uvicorn](https://www.uvicorn.org/) &bull; [Starlette Sessions](https://www.starlette.io/) |
| **Base de Datos & ORM** | [SQLAlchemy](https://www.sqlalchemy.org/) &bull; [SQLite](https://www.sqlite.org/) |
| **Seguridad** | [Passlib](https://passlib.readthedocs.io/) con algoritmo `bcrypt` |
| **Frontend** | [Jinja2 Templates](https://jinja.palletsprojects.com/) &bull; [HTML5](https://developer.mozilla.org/es/docs/Web/HTML) / [CSS3](https://developer.mozilla.org/es/docs/Web/CSS) &bull; [Bootstrap 5](https://getbootstrap.com/) |
| **Diseño e Iconografía** | [FontAwesome 6](https://fontawesome.com/) &bull; [Google Fonts](https://fonts.google.com/) &bull; [AOS Library](https://michalsnik.github.io/aos/) |

---

## 📂 Estructura del Repositorio

```text
Proyecto-pre-Nodess/
├── database.py              # Modelos SQLAlchemy y conexión a SQLite
├── main.py                  # Servidor FastAPI, rutas públicas, admin y auth
├── nodess_prenodes.db       # Base de datos SQLite
├── requirements.txt         # Dependencias del proyecto
├── templates/               # Vistas HTML con Jinja2
│   ├── base.html            # Layout maestro con navbar, footer y estilos
│   ├── index.html           # Página principal interactiva y estadísticas
│   ├── acerca.html          # Historia, hitos y zonas de impacto
│   ├── proyectos.html       # Catálogo de proyectos comunitarios
│   ├── investigadores.html  # Semblanzas de académicos
│   ├── alianzas.html        # Directorio de instituciones aliadas
│   ├── vinculacion.html     # Red de investigación y divulgación
│   ├── contacto.html        # Canales de comunicación
│   ├── login.html           # Inicio de sesión para administradores
│   └── admin.html           # Panel de administración y gestión
└── README.md                # Documentación del proyecto
```

---

## 🚀 Instalación y Puesta en Marcha

### 1️⃣ Clonar el Repositorio
```bash
git clone https://github.com/TU-USUARIO/Proyecto-pre-Nodess.git
cd Proyecto-pre-Nodess
```

### 2️⃣ Crear y Activar un Entorno Virtual (Recomendado)
```bash
# En Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# En Windows:
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Iniciar el Servidor de Desarrollo
```bash
python main.py
```
O directamente con `uvicorn`:
```bash
uvicorn main:app --reload --port 8000
```

Accede desde tu navegador a: **`http://127.0.0.1:8000`** 🌐

---

## 🔑 Carga Inicial y Panel de Control

1. **Inicializar datos de prueba:**  
   Visita en tu navegador:  
   👉 `http://127.0.0.1:8000/init-db`  
   *(Creará el usuario administrador y precargará instituciones, municipios y datos iniciales)*.

2. **Acceder como Administrador:**  
   Dirígete a: `http://127.0.0.1:8000/login`
   - **Usuario:** `admin`
   - **Contraseña:** `admin123`

---

## 🤝 Red de Alianzas

- 🎓 **TecNM Campus Teziutlán**
- 🎓 **TecNM Campus Puebla**
- 🎓 **TecNM Campus Minatitlán**
- 🎓 **CICATA-IPN (Unidad Legaria)**
- 🎓 **Universidad de la Sabana (Colombia)**
- 🏛️ **H. Ayuntamiento Municipal de Tenampulco**
- 🌾 **Sociedad Cooperativa Sabores de Calpan S.C.**

---

<p align="center">
  Desarrollado con ❤️ para el impulso de la <b>Economía Social y Solidaria</b>
</p>
