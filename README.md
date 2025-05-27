# 🧢 PokeCatch

Aplicación web para gestionar y transferir colecciones de Pokémon entre usuarios, incluyendo captura, visualización de faltantes, y un sistema de transferencia tipo "paquete". Inspirada en el universo Pokémon y construida con herramientas modernas de desarrollo web.

---

## 📘 Introducción

**PokeCatch** es una aplicación web desarrollada como proyecto académico con el propósito de poner en práctica conceptos clave de programación web, bases de datos, diseño de interfaces y comunicación entre usuarios. Simula un sistema de colección personal de Pokémon con una interfaz intuitiva y funcional.

---

## 🎯 Objetivo

Desarrollar una aplicación web responsiva y funcional que permita a los usuarios:
- Capturar y guardar Pokémon en su cuenta.
- Visualizar su colección y los Pokémon faltantes.
- Realizar transferencias de Pokémon entre cuentas (tipo "paquete").
- Aprender conceptos de desarrollo web como manejo de sesiones, bases de datos relacionales, formularios, y vistas dinámicas.

---

## 🎯 Propósito

El propósito de este proyecto es aplicar los conocimientos adquiridos en el desarrollo de aplicaciones web usando Django, PostgreSQL y Bootstrap, demostrando la capacidad de implementar lógica de negocio, manejo de usuarios, autenticación, relaciones entre tablas, y navegación segura.

---

## 🛠️ Características

- 🔐 Autenticación de usuarios (registro, login, logout).
- 🧾 Captura de Pokémon con detalles como sprite, número de Pokédex y tipo.
- 📋 Visualización de Pokémon capturados y faltantes.
- 📦 Sistema de transferencia de Pokémon entre usuarios (sin restricciones por duplicados).
- 💾 Base de datos relacional con historial persistente de capturas.
- 🎨 Interfaz amigable con Bootstrap 5.

---

## ⚙️ Instalación

### 1. Clona el repositorio:

    ```bash
    git clone https://github.com/Karup0/QA-PokeCatch.git
    cd QA-PokeCatch/backend

### 2. Crear un entorno virtual:

    python -m venv venv
    venv\Scripts\activate   # En Windows

### 3. Instala las dependencias:

    pip install -r requirements.txt

### 4. Crea el archivo .env y agrega tu configuración:

    SECRET_KEY=tu_clave_django
    DEBUG=True

### 5. Configura tu base de datos PostgreSQL en settings.py:

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'PokemonsDB',
        'USER': 'postgres',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
              }
      }

### 6. Realiza las migraciones:

    python manage.py makemigrations
    python manage.py migrate

### 7. Inicia el servidor:

    python manage.py runserver


## 📖 Manual de Usuario

  # Iniciar Sesión / Registro
  - Accede desde la página de inicio y regístrate con un nombre de usuario y contraseña.
  - Luego inicia sesión para acceder al resto de las funciones.
    
  # Capturar Pokémon
  - Dirígete a "Capturar Pokémon".
  - Introduce el nombre del Pokémon y se añadirá a tu colección con datos automáticos desde PokéAPI.
  
  #  Ver Capturados
  - Accede a tu lista de Pokémon capturados.
    
  # Ver Faltantes
  - Se muestra la lista de Pokémon que aún no tienes, basada en la PokéDex nacional.

  #Transferir Pokémon
  - Desde "Transferir Pokémon", selecciona uno de tus Pokémon y un usuario receptor.
  - El receptor recibirá una copia del Pokémon (aunque ya lo tenga repetido).


## 🧰 Herramientas Empleadas

  - Django – Framework principal para el backend.
  - PostgreSQL – Base de datos relacional.
  - Bootstrap 5 – Diseño responsivo y estilizado.
  - Python Decouple – Manejo seguro de variables de entorno.
  - PokéAPI – API externa para obtener datos de los Pokémon.

## 💡 Conceptos de Programación Web Aplicados

- 🔄 CRUD básico (crear, leer, actualizar, eliminar).
- 🔐 Autenticación de usuarios con sesiones.
- 📦 Relaciones entre modelos (User y PokemonCapture).
- 🌐 Templates con Jinja2 usando herencia y bloques (base.html).
- 📨 Transferencia simulada mediante lógica de duplicación controlada.
- ⚙️ Uso de formularios, validación y manejo de POST.
- 🌍 Diseño MVC: vistas -> templates -> modelos.
- 🔐 Protección contra CSRF y uso de decoradores @login_required.

## 📚 Referencias
Django Documentation
Bootstrap 5
PostgreSQL
PokéAPI
Python Decouple

## 🧩 Conclusión
PokeCatch es un proyecto que consolida habilidades de desarrollo web fullstack, enfocándose en funcionalidades reales de gestión de datos, navegación segura y diseño web. Permite entender cómo integrar múltiples tecnologías y recursos para construir una app funcional y escalable.

##🤝 Contribuciones
¿Te gustaría mejorar esta app? Puedes contribuir:

- Haz un fork del repositorio.
- Crea una nueva rama con tus mejoras (git checkout -b mejora-feature).
- Realiza tus cambios y súbelos con un commit claro.
- Envía un pull request para revisión.

### Capturas de pantalla de la app en uso

este es el login cuando abres la app y la ejecutas en ek servidor

![image](https://github.com/user-attachments/assets/e1bc8947-e229-47fe-953d-3ccb9d449d3a)

Esta es la primera pantalla que ves cuando ya inicias sesion 

![image](https://github.com/user-attachments/assets/bf425f09-d6b6-496b-8436-5548440965a5)

Esta es la seccion de los pokemones que ya capturaste 

![image](https://github.com/user-attachments/assets/3cd6a246-903a-4b21-bec7-000213e8d1ec)

![image](https://github.com/user-attachments/assets/dd96e83e-5d28-4757-a75d-b918154311ca)


![image](https://github.com/user-attachments/assets/3a480b12-c314-4c9c-891a-b19e0948d980)

Aqui ves todos los pokemones de todas las generaciones y los que te faltan por capturar

![image](https://github.com/user-attachments/assets/081c25a9-55c4-4e00-91e5-9e0cc69ec818)

Aqui estan los pokemones faltantes y los puedes buscar por filtros o busqueda por nombre o numero

![image](https://github.com/user-attachments/assets/fdfabd61-47c6-4553-9c09-548a80730f89)

![image](https://github.com/user-attachments/assets/914c738e-626d-4242-946f-be74a848a25b)

![image](https://github.com/user-attachments/assets/418b96ab-abb4-4adc-ab26-12e81cef392e)

![image](https://github.com/user-attachments/assets/4e121760-d5ce-46ab-a629-f64eec3b4db2)

Transferencia de pokemones

![image](https://github.com/user-attachments/assets/1cede9aa-0ce9-43f1-90f3-93ec60875d42)

![image](https://github.com/user-attachments/assets/6f4317d0-d76a-4fa7-977c-544fb7b963c3)

![image](https://github.com/user-attachments/assets/2d926c98-583a-4022-80c1-fdb9da53897c)


