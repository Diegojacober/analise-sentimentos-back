from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
#adicionar view de comentarios as rotas
router.register('comments', views.ComentarioViewSet)

app_name = 'api'

urlpatterns = [
    #inclui todas as rotas de comments
    path('', include(router.urls)),
    #url especifica apenas para pegar a função de excel
    path('excel', views.ComentarioViewSet.gerar_excel, name='gerar_excel'),
]