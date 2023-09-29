from rest_framework import serializers

from scrapping.models import (
    Informations, 
    Pages
)


class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informations
        fields = ['name', 'release_date', 'author', 'resume', 'category']