from rest_framework import serializers
from .models import Client, Project

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    # Para recibir el ID del cliente al crear un proyecto
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), source='client'
    )

    class Meta:
        model = Project
        fields = '__all__'