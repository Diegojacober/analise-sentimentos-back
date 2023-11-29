from django.db import models

# tabela de comentários do banco de dados 
class Comentario(models.Model):
    nome = models.CharField(max_length=255)
    comentario = models.CharField(max_length=255)
    classificacao = models.CharField(max_length=255)
