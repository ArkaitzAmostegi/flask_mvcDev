````md
# Flask MVC – Gestión de Libros, Socios y Préstamos

Aplicación web en **Python + Flask** con arquitectura **MVC** para gestionar una pequeña biblioteca:
- Libros (listado, disponibles, búsqueda, alta/edición)
- Socios (listado, alta/edición)
- Préstamos y devoluciones
- Autenticación con **Flask-Login** (usuario admin)

---

## Funcionalidades

### Libros
- Listar todos los libros (indicando si están disponibles o prestados).
- Listar únicamente los libros disponibles.
- Buscar libros por título (coincide por parte del texto e ignora mayúsculas/minúsculas).
- Crear y editar libros *(requiere login admin)*.

### Préstamos
- Prestar un libro a un socio mediante formulario web *(requiere login admin)*.
- Control de errores:
  - libro no existe
  - socio no existe
  - libro ya prestado
  - socio ya tiene un libro
- Devolver un libro a partir del socio que lo tiene prestado *(requiere login admin)*.
- Mostrar socios con préstamo activo e indicar qué libro tiene cada uno.

### Formularios (Flask-WTF)
- Formulario de búsqueda de libros
- Formulario de creación/edición de libros
- Formulario de préstamo
- Formulario de devolución
- Formulario de socios (alta/edición)

Los formularios:
- Validan datos
- Muestran errores claros
- Evitan uso directo de `request.form` sin validación

---

## Requisitos

- Python 3.10+ (recomendado)
- Windows / Linux / macOS
- Dependencias en `requirements.txt`

> Nota: si usas Python 3.14+ y tienes problemas con wheels, prueba Python 3.12.

---

## Instalación y ejecución (Windows PowerShell)

### 1) Clonar
```bash
git clone https://github.com/ArkaitzAmostegi/flask_mvcDev
cd flask_mvcDev
````

### 2) Crear entorno virtual

```powershell
python -m venv venv
```

### 3) Activar entorno virtual

```powershell
.\venv\Scripts\Activate.ps1
```

### 4) Instalar dependencias

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5) Ejecutar la app

```powershell
python run.py
```

Abrir en el navegador:

* [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Credenciales de administrador

Usuario inicial:

* **user:** `admin`
* **pass:** `1234`

---

## Estructura del proyecto

```text
flask_mvcDev/
│  run.py
│  requirements.txt
│  README.md
│
├─ app/
│  ├─ __init__.py              # create_app(), registro de blueprints
│  ├─ extensions.py            # db, login_manager
│  │
│  ├─ controllers/             # Blueprints (rutas)
│  │   ├─ navigation_controller.py
│  │   ├─ libros_controller.py
│  │   ├─ socios_controller.py
│  │   ├─ auth_controller.py
│  │   └─ api_controller.py
│  │
│  ├─ models/                  # Modelos SQLAlchemy
│  │   ├─ libro.py
│  │   ├─ socio.py
│  │   └─ user.py
│  │
│  ├─ services/                # Lógica de negocio
│  │   ├─ libros_service.py
│  │   └─ socios_service.py
│  │
│  ├─ forms/                   # Formularios Flask-WTF
│  │   ├─ libro_form.py
│  │   ├─ socio_form.py
│  │   ├─ login_form.py
│  │   ├─ buscar_form.py
│  │   ├─ prestamo_form.py
│  │   └─ devolucion_form.py
│  │
│  ├─ decorators/              # Decoradores (auth/roles/validaciones)
│  │   └─ auth.py              # role_required('admin')
│  │
│  ├─ templates/
│  │   ├─ base.html
│  │   ├─ paginas/
│  │   │   ├─ inicio.html
│  │   │   ├─ auth/login.html
│  │   │   ├─ libros/...
│  │   │   └─ socios/...
│  │
│  └─ static/
│      └─ css/estilos.css
│
└─ venv/                       # entorno virtual (NO se sube a git)
```

---

## Endpoints (resumen)

### Web

* `/` Inicio
* `/auth/login` Login
* `/auth/logout` Logout
* `/libros/` Listado
* `/libros/disponibles` Disponibles
* `/libros/buscar` Buscar
* `/libros/crear` Crear libro *(admin)*
* `/libros/<id>/editar` Editar libro *(admin)*
* `/libros/<id>` Detalle (según implementación)
* `/libros/<id>/prestar` Prestar *(admin)*
* `/libros/devolver` Devolver *(admin)*
* `/libros/socios/prestamos` Socios con préstamo
* `/socios/` Listado socios
* `/socios/crear` Crear socio *(admin)*
* `/socios/<id>/editar` Editar socio *(admin)*

### API (ejemplo)

* `/api/listar` Libros en JSON

---