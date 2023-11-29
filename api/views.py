from rest_framework import (
    viewsets,
    mixins,
    status,
)
from core.models import Comentario
from api import serializers
from rest_framework.response import Response
from rest_framework import status
from LeIA import SentimentIntensityAnalyzer 
from rest_framework.decorators import api_view
import pandas as pd
import json
from django.core import serializers as seria

class ComentarioViewSet(viewsets.ModelViewSet):
    

    serializer_class = serializers.CommentarioSerializer
    queryset = Comentario.objects.all()
    
    
    # função de post
    def create(self, request):
        # cria a funçaõ para analisar
        s = SentimentIntensityAnalyzer()
        # valid os dados recebidos
        serializer = serializers.CommentarioSerializer(data=request.data)
        if (serializer.is_valid()): 
            sentimento = s.polarity_scores(serializer.validated_data.get("comentario"))
            # faz verificações para definir o sentimento
            nota = ""
            if (sentimento["compound"] >= 0.05):
                nota = "positivo"
            if (sentimento["compound"] <= 0.0499):
                nota = "negativo"
            if ((sentimento["compound"] > -0.05) and (sentimento["compound"] < 0.05)):
                nota = "neutro"
            
            # cria um novo comentario ja validado
            comment = Comentario.objects.create(
                nome=serializer.validated_data.get("nome"),
                comentario=serializer.validated_data.get("comentario"),
                classificacao=nota
            )
            
            # retorna o comentario criado
            return Response(serializers.CommentarioSerializer(comment).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST   )
        
        
    # função de put
    def update(self, request):
        print("ATUALIZAR")
        
    # função de patch
    def partial_update(self, request):
        print("patch")
        
    #rota para gerar o excel
    @api_view(http_method_names=['GET'])
    def gerar_excel(request):
        all_comments = Comentario.objects.all()
        data = seria.serialize("json", all_comments)
        struct = json.loads(data)
        df = pd.read_json(data, orient='id')
        df.to_excel("coments.xlsx")
        return Response({"message": "excel_gerado"}, status=status.HTTP_201_CREATED)
