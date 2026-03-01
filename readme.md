01-03-2026 - Creo la aplicación accounts para centralizar en manejo de usuarios, registro por email, pero SIGUE SIN FUNCIONAR!

También está instalado Jazzmin. Están comentadas en settings.py las lineas por pruebas con el admin por defecto...

## NO ANDA ##

Pruebas de configuración en el backend
VER en How-to-do:
*** Tips para personalizar el backend ***
La opción usada acá fue solamente agregar código css.

Todavia confuso el tema de usuarios y salesperson

usr: romualdo
pas: asdf1234-

en el formulario, contra que se loguea?

El formulario (en home.html) está intentando hacer login, pero **no está verificando contra la base de datos de Users de Django**. Hay varios problemas:

## **Problemas en tu formulario:**

### **2. Falta la vista de autenticación**
El formulario envía a `{% url 'home' %}`, pero necesitas una vista que procese el login.

### **3. No usa el sistema de autenticación de Django**
Para que funcione contra la tabla `User`, necesitas usar Django's `authenticate()` y `login()`.

## **Solución Correcta:**

### **Paso 1: Crear la vista de login**
# en views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticar contra la base de datos de Django
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login exitoso
            login(request, user)
            messages.success(request, f'¡Bienvenido {username}!')
            return redirect('dashboard')  # Redirige a donde quieras
        else:
            # Login fallido
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('login')  # Vuelve al formulario
    
    # Si es GET, muestra el formulario
    return render(request, 'login.html')
```

### **Paso 2: Configurar la URL**
```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # ... otras URLs
]
```

### **Paso 3: Corregir el template HTML**
```html
<!-- login.html -->
<div class="col-md-8 offset-md-2">
    <br>
    <h2>Todo Comienza Aquí</h2>
    <br>
    
    <!-- Mostrar mensajes de error/éxito -->
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <!-- UN SOLO FORMULARIO -->
    <form method="POST" action="{% url 'login' %}">
        {% csrf_token %}
        <div class="mb-3">
            <input type="text" class="form-control" name="username" placeholder="Usuario" required>
        </div>
        <br>
        <div class="mb-3">
            <input type="password" class="form-control" name="password" placeholder="Password" required>
        </div>
        <br>
        <button type="submit" class="btn btn-secondary">Login</button>
    </form>
    
    <!-- Enlace para olvidó contraseña -->
    <br>
    <p><a href="{% url 'password_reset' %}">¿Olvidaste tu contraseña?</a></p>
</div>
```

### **Paso 4: Verificar el usuario "romualdo"**
Primero, verifica que el usuario exista y esté activo:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# Buscar el usuario
try:
    user = User.objects.get(username='romualdo')
    print(f"Usuario encontrado: {user.username}")
    print(f"Email: {user.email}")
    print(f"is_active: {user.is_active}")
    print(f"is_staff: {user.is_staff}")
    print(f"is_superuser: {user.is_superuser}")
    
    # Verificar contraseña (si la conoces)
    # password_correct = user.check_password('la_contraseña')
    # print(f"¿Contraseña correcta?: {password_correct}")
    
except User.DoesNotExist:
    print("El usuario 'romualdo' no existe")
```

### **Paso 5: Usar el sistema de autenticación de Django (RECOMENDADO)**
Django ya tiene vistas de login listas para usar:

```python
# urls.py
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Login con las vistas built-in de Django
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
```

```html
<!-- login.html más simple -->
{% extends 'base.html' %}

{% block content %}
<div class="col-md-8 offset-md-2">
    <h2>Iniciar Sesión</h2>
    
    {% if form.errors %}
        <div class="alert alert-danger">
            Usuario o contraseña incorrectos. Intenta de nuevo.
        </div>
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Login</button>
    </form>
</div>
{% endblock %}
```

### **Paso 6: Depuración - Ver qué está recibiendo la vista**
```python
# views.py - Versión con debug
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"DEBUG: Usuario recibido: '{username}'")
        print(f"DEBUG: Contraseña recibida: '{password}'")
        
        user = authenticate(request, username=username, password=password)
        print(f"DEBUG: Usuario autenticado: {user}")
        
        if user is not None:
            print(f"DEBUG: Login exitoso para {user.username}")
            login(request, user)
            return redirect('dashboard')
        else:
            print("DEBUG: Autenticación fallida")
            # Verificar si el usuario existe pero la contraseña está mal
            try:
                user_exists = User.objects.get(username=username)
                print(f"DEBUG: El usuario existe pero contraseña incorrecta")
            except User.DoesNotExist:
                print(f"DEBUG: El usuario no existe en la BD")
            
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'login.html')
```

### **Paso 7: Problemas comunes con el usuario "romualdo"**
1. **Mayúsculas/minúsculas:** Django es case-sensitive en usernames
2. **Espacios:** Verifica que no tenga espacios al inicio/final
3. **Usuario inactivo:** `is_active=False`
4. **Contraseña incorrecta:** ¿La creaste con `createsuperuser` o manualmente?

```python
# Verificar todo sobre "romualdo"
python manage.py shell
```

```python
from django.contrib.auth.models import User
import sys

# Buscar sin importar mayúsculas
username_to_find = 'romualdo'
users = User.objects.filter(username__iexact=username_to_find)

if users.exists():
    user = users.first()
    print(f"✅ Usuario encontrado: {user.username}")
    print(f"   ID: {user.id}")
    print(f"   Email: {user.email}")
    print(f"   Active: {user.is_active}")
    print(f"   Staff: {user.is_staff}")
    print(f"   Superuser: {user.is_superuser}")
    print(f"   Último login: {user.last_login}")
    
    # Verificar contraseña (pide ingresarla)
    import getpass
    password = getpass.getpass("Ingresa la contraseña para probar: ")
    if user.check_password(password):
        print("✅ Contraseña correcta")
    else:
        print("❌ Contraseña incorrecta")
else:
    print(f"❌ No existe usuario con username: {username_to_find}")
    
    # Listar todos los usuarios para ver cómo están escritos
    print("\nTodos los usuarios:")
    for u in User.objects.all():
        print(f"  - '{u.username}' (ID: {u.id})")
```

### **Paso 8: Resetear contraseña de "romualdo"**
```bash
# Desde la terminal
python manage.py shell
```

```python
from django.contrib.auth.models import User

user = User.objects.get(username='romualdo')
user.set_password('nueva_contraseña_segura')
user.save()
print(f"Contraseña cambiada para {user.username}")
```

## **Resumen:**
Tu formulario **NO está conectado** al sistema de autenticación de Django. Necesitas:

1. **Eliminar el form anidado** (tienes `<form>` dentro de `<form>`)
2. **Crear una vista** que use `authenticate()` y `login()`
3. **Verificar** que el usuario "romualdo" exista, esté activo y tenga la contraseña correcta

¿Quieres que te ayude a crear la vista completa de autenticación o prefieres usar las vistas built-in de Django que ya están listas?