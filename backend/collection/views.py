import requests  # 🆕 Para conectarnos a PokéAPI
import time # 🆕 Para manejar tiempos de espera
from django.core.cache import cache  # 🆕 Para manejar caché
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PokemonCapture  # 🆕 Importamos los modelos necesarios

@login_required(login_url='login')
def capture_pokemon(request):
    error_message = None

    if request.method == 'POST':
        pokemon_name = request.POST.get('pokemon_name', '').strip().lower()
        pokedex_number = request.POST.get('pokedex_number')
        is_shiny = request.POST.get('is_shiny') == 'on'

        # Validación básica
        if not pokemon_name or not pokedex_number:
            error_message = "Por favor completa todos los campos"
        else:
            try:
                # Verificar existencia en PokéAPI
                response = requests.get(
                    f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}",
                    timeout=5  # Timeout para evitar esperas largas
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validar que el número de Pokédex coincida
                    if int(pokedex_number) != data['id']:
                        error_message = f"El número de Pokédex no coincide. {pokemon_name.capitalize()} es #{data['id']}"
                    else:
                        # Crear captura
                        PokemonCapture.objects.create(
                            user=request.user,
                            pokemon_name=data['name'].capitalize(),
                            pokedex_number=data['id'],
                            is_shiny=is_shiny,
                            types=[t['type']['name'] for t in data['types']],
                            sprite_url=data['sprites']['front_default']
                        )
                        
                        # Limpiar caché de Pokémon faltantes
                        generation_id = get_generation_by_pokedex(data['id'])
                        if generation_id:
                            cache_key = f"missing_pokemon_user_{request.user.id}_gen_{generation_id}"
                            cache.delete(cache_key)
                            
                        return redirect('captured')  # Redirigir a la lista de capturados
                
                else:
                    error_message = "Pokémon no encontrado. Verifica el nombre o número"
            
            except requests.exceptions.Timeout:
                error_message = "Tiempo de espera agotado. Intenta nuevamente"
            except requests.exceptions.RequestException:
                error_message = "Error al conectar con PokéAPI. Intenta más tarde"
            except Exception as e:
                error_message = f"Error inesperado: {str(e)}"

    return render(request, 'collection/capture.html', {
        'error_message': error_message,
        'form_data': {
            'pokemon_name': request.POST.get('pokemon_name', ''),
            'pokedex_number': request.POST.get('pokedex_number', ''),
            'is_shiny': request.POST.get('is_shiny', '')
        }
    })

def get_generation_by_pokedex(pokedex_number):
    """Determina la generación basada en el número de Pokédex"""
    pokedex_number = int(pokedex_number)
    for gen_id, gen_data in GENERATIONS.items():
        if gen_data['start'] <= pokedex_number <= gen_data['end']:
            return gen_id
    return None

# Datos de generaciones (rango de números según Pokédex Nacional)
GENERATIONS = {
    1: {"name": "Generación I (Kanto)", "start": 1, "end": 151},
    2: {"name": "Generación II (Johto)", "start": 152, "end": 251},
    3: {"name": "Generación III (Hoenn)", "start": 252, "end": 386},
    4: {"name": "Generación IV (Sinnoh)", "start": 387, "end": 493},
    5: {"name": "Generación V (Teselia)", "start": 494, "end": 649},
    6: {"name": "Generación VI (Kalos)", "start": 650, "end": 721},
    7: {"name": "Generación VII (Alola)", "start": 722, "end": 809},
    8: {"name": "Generación VIII (Galar)", "start": 810, "end": 898},
    9: {"name": "Generación IX (Paldea)", "start": 899, "end": 1025},
}

@login_required(login_url='login')
def missing_pokemon(request):
    generation = request.GET.get('generation')
    
    if generation:
        generation = int(generation)
        gen_data = GENERATIONS[generation]
        
        cache_key = f"missing_pokemon_user_{request.user.id}_gen_{generation}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            missing_pokemons = cached_data['pokemons']
            unique_types = cached_data['types']
        else:
            missing_data = get_missing_for_generation(request.user, gen_data)
            missing_pokemons = missing_data['pokemons']
            unique_types = missing_data['types']
            
            cache.set(
                cache_key,
                {'pokemons': missing_pokemons, 'types': unique_types},
                timeout=settings.POKEAPI_CACHE_TIMEOUT
            )
        
        # Convertir tipos a minúsculas para consistencia
        for pokemon in missing_pokemons:
            pokemon['types'] = [t.lower() for t in pokemon['types']]
        
        return render(request, 'collection/missing.html', {
            'show_grid': True,
            'missing_pokemons': missing_pokemons,
            'pokemon_types': sorted(unique_types),  # <-- Esta es la línea clave que faltaba
            'current_gen': f"Generación {generation}"
        })
    return render(request, 'collection/missing.html', {
        'show_grid': False
    })

def get_missing_for_generation(user, gen_data):
    """Obtiene Pokémon faltantes para una generación específica"""
    captured = set(PokemonCapture.objects.filter(
        user=user,
        pokedex_number__range=(gen_data['start'], gen_data['end'])
    ).values_list('pokedex_number', flat=True))
    
    missing_pokemons = []
    unique_types = set()
    
    for pokedex_num in range(gen_data['start'], gen_data['end'] + 1):
        if pokedex_num not in captured:
            pokemon_data = get_pokemon_details(pokedex_num)
            if pokemon_data:
                # Convertir tipos a minúsculas aquí para consistencia
                pokemon_data['types'] = [t.lower() for t in pokemon_data['types']]
                missing_pokemons.append(pokemon_data)
                unique_types.update(pokemon_data['types'])
    
    return {
        'pokemons': missing_pokemons,
        'types': sorted(unique_types)  # Ordenamos los tipos alfabéticamente
    }

def get_pokemon_list_from_api(start, end):
    """Obtiene lista básica de Pokémon de la API (optimizado)"""
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={end-start+1}&offset={start-1}")
    return response.json().get('results', [])

def get_pokemon_details(pokedex_num):
    """Obtiene detalles específicos de un Pokémon con manejo de errores"""
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokedex_num}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'name': data['name'].capitalize(),
                'pokedex_number': data['id'],
                'types': [t['type']['name'].capitalize() for t in data['types']],
                'sprite': data['sprites']['front_default'],
                'official_artwork': data['sprites']['other']['official-artwork']['front_default']
            }
    except requests.exceptions.RequestException:
        return None
    return None

@login_required(login_url='login')
def captured_pokemon(request):
    """Vista para mostrar todos los Pokémon capturados con opciones de gestión"""
    captured_pokemons = PokemonCapture.objects.filter(user=request.user).order_by('-date_captured')
    
    # Preparar los datos en el mismo formato que los faltantes para reutilizar el template
    pokemons = []
    unique_types = set()
    
    for capture in captured_pokemons:
        pokemon_data = {
            'id': capture.id,  # ID para operaciones de eliminación
            'name': capture.pokemon_name,
            'pokedex_number': capture.pokedex_number,
            'types': [t.lower() for t in capture.types],
            'sprite': capture.sprite_url,
            'is_shiny': capture.is_shiny,
            'date_captured': capture.date_captured
        }
        pokemons.append(pokemon_data)
        unique_types.update(pokemon_data['types'])
    
    return render(request, 'collection/captured.html', {
        'pokemons': pokemons,
        'pokemon_types': sorted(unique_types),
        'show_grid': True
    })
    
@login_required(login_url='login')
def delete_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(PokemonCapture, id=pokemon_id, user=request.user)
    
    if request.method == 'POST':
        # Limpiar caché de Pokémon faltantes
        generation_id = get_generation_by_pokedex(pokemon.pokedex_number)
        if generation_id:
            cache_key = f"missing_pokemon_user_{request.user.id}_gen_{generation_id}"
            cache.delete(cache_key)
        
        pokemon.delete()
        messages.success(request, f'Has liberado a {pokemon.pokemon_name}')
    
    return redirect('captured')

# REGISTRO
def register(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            error_message = "Este usuario ya existe."
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)  # Loguearlo automáticamente después de registrar
            return redirect('capture')  # Redirigir al inicio

    return render(request, 'collection/register.html', {'error_message': error_message})

# LOGIN
def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('capture')  # Redirigir al inicio
        else:
            error_message = "Usuario o contraseña incorrectos."

    return render(request, 'collection/login.html', {'error_message': error_message})

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')

from django.views.decorators.http import require_GET

@require_GET
def pokemon_api_proxy(request, pokedex_num):
    """Proxy para evitar CORS y manejar errores"""
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokedex_num}", timeout=3)
        return JsonResponse(response.json(), safe=False)
    except requests.exceptions.RequestException:
        return JsonResponse({'error': 'Pokémon no disponible'}, status=404)