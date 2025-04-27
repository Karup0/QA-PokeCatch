from django.db import models

class PokemonCapture(models.Model):
    pokemon_name = models.CharField(max_length=100)
    pokedex_number = models.IntegerField()
    date_captured = models.DateField(auto_now_add=True)
    is_shiny = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.pokemon_name} (#{self.pokedex_number})"

class TradeOffer(models.Model):
    """
    Modelo para registrar ofertas de intercambio de Pokémon.
    """
    username = models.CharField(max_length=100)  # Nombre del usuario que ofrece
    pokemon_name = models.CharField(max_length=100)  # Nombre del Pokémon ofrecido
    pokedex_number = models.IntegerField()  # Número de Pokédex
    is_shiny = models.BooleanField(default=False)  # ¿Es shiny?
    date_posted = models.DateTimeField(auto_now_add=True)  # Fecha en que se ofreció

    def __str__(self):
        return f"{self.pokemon_name} ofrecido por {self.username}"