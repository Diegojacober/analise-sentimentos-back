from rest_framework import serializers
from core.models import Comentario

# dados serializados de comentarios
class CommentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['id', 'nome', 'comentario', 'classificacao']
        read_only_fields = ['id', 'classificacao']
