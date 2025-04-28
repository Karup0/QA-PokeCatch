# models.py

from django.db import models
from django.contrib.auth.models import User

class PokemonCapture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon_name = models.CharField(max_length=100)
    pokedex_number = models.IntegerField()
    date_captured = models.DateTimeField(auto_now_add=True)
    is_shiny = models.BooleanField(default=False)
    types = models.JSONField(default=list, blank=True)
    sprite_url = models.URLField(null=True, blank=True, default='')

    def __str__(self):
        return f"{self.pokemon_name} (#{self.pokedex_number})"


