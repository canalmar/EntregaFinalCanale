# Tienda de Historias 📚

Tienda de Historias es un portal literario desarrollado con Django 5.2 para la entrega final del curso Python / Django de Coderhouse.

Los visitantes pueden explorar un catálogo de libros, buscar por título, autor o categoría y sumarse a la comunidad lectora a través del blog, que requiere login para publicar.

El staff (usuarios con is_staff=True) gestiona productos, clientes y blog desde la interfaz interna.

Por simplicidad académica no se incluyen carrito de compras ni pagos en línea; el foco está en la administración de contenidos y usuarios. 

---
## 🎬 Video demo
Subido a YouTube 👉 `[pendiente de agregar](#)` (máx. 10 minutos).

---
## 🚀 Demo rápida

```bash
# 1️⃣ Crear y activar entorno virtual
python -m venv .venv && .venv\Scripts\activate  # Windows
# o: source .venv/bin/activate  # Linux/Mac

# 2️⃣ Instalar dependencias
pip install -r requirements.txt

# 3️⃣ Aplicar migraciones
python manage.py migrate

# 4️⃣ Crear superusuario (elige usuario y contraseña)
python manage.py createsuperuser

# 5️⃣ (Opcional) Cargar datos de ejemplo
python manage.py loaddata demo  # categorías, productos, posts, clientes

# 6️⃣ Levantar el servidor
python manage.py runserver  # abre http://127.0.0.1:8000/
```

---
## 🗂️ Apps y estructura
| App | Propósito | Modelos principales |
|-----|-----------|--------------------|
| **core** | Home, About, autenticación, perfiles | `Profile` |
| **client** | Gestión de clientes (staff) | `Client` |
| **product** | Catálogo y CRUD de productos | `Category`, `Product` |
| **blog** | Publicación de posts | `Category`, `Post` |

---
## 🔑 Funcionalidades
- **Registro extendido** con e-mail, teléfono y dirección.
- **Login / Logout** usando formularios Bootstrap.
- **CRUD completo para staff** (productos, clientes, posts).
- **Catálogo público** con buscador y vista de detalle.
- **Blog** con categorías y búsqueda.
- **Perfil de usuario** editable (datos personales y contacto).
- **Internacionalización** (es-AR).
- **Subida de imágenes** (productos y posts).

---
## 🛠️ Instalación detallada
1. **Clonar** el repo:
   ```bash
   git clone https://github.com/usuario/TiendaHistorias.git && cd TiendaHistorias
   ```
2. **Crear entorno** virtual y activar.
3. **Instalar** dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. **Crear base de datos** y aplicar migraciones:
   ```bash
   python manage.py migrate
   ```
5. **Cargar datos de prueba**:
   ```bash
   python manage.py loaddata demo        # usa TiendaHistorias/fixtures/demo.json
   ```
6. **Levantar** el servidor:
   ```bash
   python manage.py runserver
   ```

### Variables opcionales (.env)
| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Clave secreta en producción | `changeme` |
| `DEBUG` | 0 / 1 | `0` |

---
## 📂 Demo data (`fixtures/demo.json`)
Incluye:
- 3 categorías
- 3 productos
- 2 posts de blog
- 2 usuarios cliente (alicia, pedro)

Cargar:
```bash
python manage.py loaddata demo
```

> El fixture demo.json debe estar en la carpeta `fixtures` al nivel de `manage.py` (ya está así por defecto). No es necesario usar rutas especiales ni cambiar settings.

> El fixture es seguro y no rompe nada: solo agrega datos de ejemplo para pruebas y demo.

---
## 🖼️ Capturas de pantalla
<details>
  <summary>Home + Catálogo</summary>

  ![Home](docs/img/home.png)
  ![Catálogo](docs/img/catalogo.png)
</details>

<details>
  <summary>Panel Staff</summary>

  ![Productos](docs/img/staff_productos.png)
  ![Clientes](docs/img/staff_clientes.png)
</details>

---
## 🏗️ Stack técnico
- **Python 3.12**
- **Django 5.2.x**
- SQLite (dev) / PostgreSQL (sugerido en prod)
- Bootstrap 5
- Docker (opcional)

---
## 📜 Comandos útiles
| Acción | Comando |
|--------|---------|
| Migrar | `python manage.py makemigrations && python manage.py migrate` |
| Crear superusuario | `python manage.py createsuperuser` |
| Tests | `python manage.py test` |
| Colectar estáticos | `python manage.py collectstatic` |

---
## 🏗️ Despliegue (resumen)
1. Preparar variables de entorno y DB PostgreSQL.
2. `python manage.py collectstatic --noinput`
3. Servir con Gunicorn + Nginx o plataforma preferida.

---
## 👩‍💻 Autor
**Marisa Canale**


