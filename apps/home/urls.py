from django.urls import path
from .views import HomePageView, ContactPage, MyFavouriteView, AddOrRemoveFavourite, PremiumPage, SubscribeView,ChatBotView,BloodAIView

app_name = "home"
urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('contact/', ContactPage.as_view(), name='contact'),
    path('my-favourite/', MyFavouriteView.as_view(), name='my-favourite'),
    path('api/add-or-remove-favourite/', AddOrRemoveFavourite.as_view(), name='add-or-remove-favourite'),
    path('premium/', PremiumPage.as_view(), name='premium'),
    path('subs/', SubscribeView.as_view(), name='subscribe'),
    path("chatbot/", ChatBotView.as_view(), name="chatbot"),
    path("blood-ai/", BloodAIView.as_view(), name="blood_ai"),
    

]
