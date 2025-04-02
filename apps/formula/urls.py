from django.urls import path
from .views import FormulaPage, FormulaDetail, CalculateAPI, FunksionalHolatPage, DownloadFileView, InformationView

app_name = "formula"
urlpatterns = [
    path('', FormulaPage.as_view(), name='formula'),
    path('funksional-holatni-aniqlash', FunksionalHolatPage.as_view(), name='funksional-holat'),
    path('<int:pk>/', FormulaDetail.as_view(), name='detail'),
    path('api/<int:id>/', CalculateAPI.as_view(), name='calculate-api'),
    path('download-funksional-excel', DownloadFileView.as_view(), name='download-excel'),
    path('information/', InformationView.as_view(), name='information'), 
]