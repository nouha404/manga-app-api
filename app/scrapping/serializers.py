from rest_framework import serializers
from scrapping.models import (
    Informations,
    Pages
)


class InformationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informations
        fields = ['release_date', 'author', 'resume', 'category', 'manga_title']
        read_only_fields = ['release_date', 'author', 'resume', 'category']


class PagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pages
        fields = '__all__'
        read_only_fields = ['name', 'chapters']
