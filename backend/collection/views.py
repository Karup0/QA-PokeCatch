import requests  # 🆕 Para conectarnos a PokéAPI
from django.shortcuts import render, redirect
from .models import PokemonCapture, TradeOffer  # 🆕 Importamos los modelos necesarios

def capture_pokemon(request):
    error_message = None  # 🆕 Para capturar errores si existen

    if request.method == 'POST':
        pokemon_name = request.POST.get('pokemon_name').lower()  # PokéAPI usa minúsculas
        pokedex_number = request.POST.get('pokedex_number')
        is_shiny = request.POST.get('is_shiny') == 'on'

        # Validamos contra PokéAPI
        pokeapi_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

        try:
            response = requests.get(pokeapi_url)
            if response.status_code == 200:
                # El Pokémon existe, entonces lo guardamos
                PokemonCapture.objects.create(
                    pokemon_name=pokemon_name.capitalize(),  # Guardamos bonito
                    pokedex_number=pokedex_number,
                    is_shiny=is_shiny
                )
                return redirect('capture')  # Redirigimos si todo salió bien
            else:
                error_message = "El Pokémon que intentas capturar no existe. Revisa el nombre."
        except Exception as e:
            error_message = "Error al conectar con PokéAPI. Inténtalo más tarde."

    # Si GET o si hubo error, renderizamos normalmente
    return render(request, 'collection/capture.html', {'error_message': error_message})

def missing_pokemon(request):
    # Paso 1: Traer todos los Pokémon capturados
    captured_pokemons = PokemonCapture.objects.values_list('pokemon_name', flat=True)
    captured_pokemons = [name.lower() for name in captured_pokemons]  # normalizamos a minúsculas

    # Paso 2: Consultar a PokéAPI todos los Pokémon
    all_pokemons = []
    try:
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=151')  # Primera generación
        if response.status_code == 200:
            data = response.json()
            for pokemon in data['results']:
                all_pokemons.append(pokemon['name'])
    except Exception as e:
        all_pokemons = []

    # Paso 3: Comparar y obtener los faltantes
    missing_pokemons = [poke for poke in all_pokemons if poke not in captured_pokemons]

    return render(request, 'collection/missing.html', {'missing_pokemons': missing_pokemons})

def captured_pokemon(request):
    """
    Vista para mostrar todos los Pokémon que han sido capturados.
    Se listan en orden descendente por fecha de captura.
    """
    pokemons = PokemonCapture.objects.all().order_by('-date_captured')
    
    return render(request, 'collection/captured.html', {'pokemons': pokemons})

def trade_pokemon(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        pokemon_name = request.POST.get('pokemon_name').lower()
        pokedex_number = request.POST.get('pokedex_number')
        is_shiny = request.POST.get('is_shiny') == 'on'

        # Validar que el Pokémon existe en PokéAPI
        pokeapi_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

        try:
            response = requests.get(pokeapi_url)
            if response.status_code == 200:
                # Pokémon válido, crear la oferta
                TradeOffer.objects.create(
                    username=username,
                    pokemon_name=pokemon_name.capitalize(),
                    pokedex_number=pokedex_number,
                    is_shiny=is_shiny
                )
                return redirect('trade')
            else:
                error_message = "El Pokémon ingresado no existe. Verifica el nombre."
        except Exception as e:
            error_message = "Error al validar Pokémon. Intenta más tarde."

    # Traer todas las ofertas activas
    offers = TradeOffer.objects.all().order_by('-date_posted')

    return render(request, 'collection/trade.html', {'offers': offers, 'error_message': error_message})