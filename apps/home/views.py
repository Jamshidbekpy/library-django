from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView
from apps.home.forms import ContactForm
from django.contrib import messages
from apps.resources.models import Resource, ResourceType
from apps.home.models import Favourite, Subscribe   
# Create your views here.
from django.db.models import Q 
from django.core.paginator import Paginator


class ResourceListView(ListView):
    model = Resource
    template_name = 'resources.html'
    context_object_name = 'resources'
    paginate_by = 16
    PAGINATION_URL = ''

    def get_queryset(self):
        queryset = Resource.objects.filter(is_active=True).order_by('-id')  # Base queryset

        # Get search query from request.GET (modify as needed)
        search_query = self.request.GET.get('search', '')
        if search_query:
            self.PAGINATION_URL = f'&search={search_query}'  
            queryset = queryset.filter(Q(title__icontains=search_query) | 
                                       Q(description__icontains=search_query) | 
                                       Q(author__icontains=search_query) | 
                                       Q(keywords__icontains=search_query))

        # Add additional filters based on request.GET parameters (modify as needed)
        filter_by_category = self.request.GET.get('category', '')
        if filter_by_category:
            self.PAGINATION_URL += f'&category={filter_by_category}'  
            queryset = queryset.filter(category__slug=filter_by_category)
            
            
        filter_by_type = self.request.GET.get('resourceType', '')
        if filter_by_type:
            self.PAGINATION_URL += f'&resourceType={filter_by_type}'
            queryset = queryset.filter(resource_type=filter_by_type)
            
            
        filter_by_auditoriya = self.request.GET.get('auditoria', '')
        if filter_by_auditoriya:
            self.PAGINATION_URL += f'&auditoria={filter_by_auditoriya}'
            queryset = queryset.filter(auditoria=filter_by_auditoriya)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resourceTypes'] = ResourceType.objects.all()
        context['search_query'] = self.request.GET.get('search', '')  # Pass search query to template
        context['filter_by_category'] = self.request.GET.get('category', '')  # Pass filter value to template
        context['filter_by_type'] = self.request.GET.get('resourceType', '')  
        context['filter_by_auditoriya'] = self.request.GET.get('auditoria', '') 
        context['pagination_url'] = self.PAGINATION_URL
        
        # Get paginated queryset
        resources = self.object_list
        paginator = Paginator(resources, self.paginate_by)
        page_number = self.request.GET.get('page', 1)  # Get current page from GET
        page_obj = paginator.get_page(page_number)
        
        if self.request.user.is_authenticated:
            # favorites = {f"{resource.id}": resource.is_favourited(resource, self.request.user) for resource in resources}
            favorites = list(self.request.user.favourites.all().values_list('resource_id', flat=True))
        else:
            favorites = []
        context['favorites'] = favorites

        # Update context with pagination information
        context['page_obj'] = page_obj
        context['is_paginated'] = paginator.num_pages > 1

        return context
    
    
class ContactPage(View):
    def get(self, request):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'contact.html', context)
    
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent successfully')
            return redirect('home:index')
        
        context = {
            'form': form
        }
        messages.error(request, f'Message not sent: {form.errors}')
        return render(request, 'contact.html', context)

class SubscribeView(View):
    def post(self, request):
        LAST_URL = request.META.get('HTTP_REFERER')        
        data = request.POST
        obuna = Subscribe()
        print(obuna)
        obuna.email = data.get('emailmanzil')
        
        obuna.save()
        messages.success(self.request, 'Siz muvaffaqiyatli obuna bo\'ldingiz')
        return redirect(LAST_URL)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import Resource

class AddOrRemoveFavourite(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to add to favourites'}, status=status.HTTP_401_UNAUTHORIZED)
        
        resource_id = request.data.get('resource_id')
        print(resource_id)
        if not resource_id:
            return Response({'error': 'Resource ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        resource = get_object_or_404(Resource, id=resource_id)
        print(resource)
        if not resource:
            return Response({'error': 'Resource not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user.favourites.filter(resource=resource).exists():
            request.user.favourites.filter(resource=resource).delete()
            print('deleted')
            return Response({'message': 'Resource removed from favourites', 'isFavourite': False}, status=status.HTTP_200_OK)
        
        request.user.favourites.create(resource=resource)
        print('created')
        return Response({'message': 'Resource added to favourites', 'isFavourite': True}, status=status.HTTP_200_OK)
    
    
class MyFavouriteView(ListView):
    model = Favourite
    template_name = 'my_favourite.html'
    context_object_name = 'favourites'
    paginate_by = 8
    PAGINATION_URL = ''
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return redirect('accounts:login')
        queryset = self.request.user.favourites.filter(is_active=True)
        

        # Get search query from request.GET (modify as needed)
        search_query = self.request.GET.get('search', '')
        if search_query:
            self.PAGINATION_URL = f'&search={search_query}'  
            queryset = queryset.filter(Q(resource__title__icontains=search_query) | 
                                       Q(resource__description__icontains=search_query) | 
                                       Q(resource__author__icontains=search_query) | 
                                       Q(resource__keywords__icontains=search_query))

        # Add additional filters based on request.GET parameters (modify as needed)
        filter_by_category = self.request.GET.get('category', '')
        if filter_by_category:
            self.PAGINATION_URL += f'&category={filter_by_category}'  
            queryset = queryset.filter(resource__category__slug=filter_by_category)
            
            
        filter_by_type = self.request.GET.get('resourceType', '')
        if filter_by_type:
            self.PAGINATION_URL += f'&resourceType={filter_by_type}'
            queryset = queryset.filter(resource__resource_type=filter_by_type)
            
            
        filter_by_auditoriya = self.request.GET.get('auditoria', '')
        if filter_by_auditoriya:
            self.PAGINATION_URL += f'&auditoria={filter_by_auditoriya}'
            queryset = queryset.filter(aresource__uditoria=filter_by_auditoriya)
            
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resourceTypes'] = ResourceType.objects.all()
        context['search_query'] = self.request.GET.get('search', '')  # Pass search query to template
        context['filter_by_category'] = self.request.GET.get('category', '')  # Pass filter value to template
        context['filter_by_type'] = self.request.GET.get('resourceType', '')  
        context['filter_by_auditoriya'] = self.request.GET.get('auditoria', '') 
        context['pagination_url'] = self.PAGINATION_URL
        
        # Get paginated queryset
        favourites = self.object_list
        paginator = Paginator(favourites, self.paginate_by)
        page_number = self.request.GET.get('page', 1)  # Get current page from GET
        page_obj = paginator.get_page(page_number)

        # Update context with pagination information
        context['page_obj'] = page_obj
        context['is_paginated'] = paginator.num_pages > 1

        favorites = list(self.request.user.favourites.all().values_list('resource_id', flat=True))
        print(favorites)
        context['favorites'] = favorites
        
        return context
    

class PremiumPage(View):

    def get(self, request):
        context = {
        }
        return render(request, 'premium.html', context)
    
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import openai

class DefonicAssistant:
    def __init__(self, api_key: str, base_url: str = "https://api.groq.com/openai/v1"):
        self.client = openai.OpenAI(
            base_url=base_url, 
            api_key=api_key
        )

    def get_response(self, user_input: str, model: str = "llama-3.3-70b-versatile") -> str:
        chat_completion = self.client.chat.completions.create(
    messages=[
        {"role": "system", "content": (
            "Siz Kitobiy — 'Kutubxona Yordamchisi' sun’iy intellektsiyasiz. Siz ICT JOBS jamoasi tomonidan ishlab chiqilgansiz."
            "Siz faqatgina kitoblar, mualliflar, janrlar va kutubxona bilan bog‘liq savollarga javob bera olasiz."
            "Siz doim O'zbek tilida (lotin yozuvida) javob berishingiz kerak."
            "Agar foydalanuvchi kitoblar yoki kutubxona bilan bog‘liq bo‘lmagan savol bersa, muloyimlik bilan faqat kutubxona mavzularida yordam bera olishingizni tushuntiring."
        )},
        {"role": "user", "content": user_input},
    ],
    model=model,
)
        return chat_completion.choices[0].message.content


class ChatBotView(View):
    template_name = "chatbot.html"
    assistant = DefonicAssistant(api_key=os.environ.get("GROQ_API_KEY", "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"))

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user_message = request.POST.get("message", "")

        if not user_message:
            return JsonResponse({"error": "Xabar bo'sh bo'lishi mumkin emas"}, status=400)

        try:
            bot_reply = self.assistant.get_response(user_message)
        except Exception as e:
            bot_reply = "Kechirasiz, serverda xatolik yuz berdi."

        return JsonResponse({"response": bot_reply})
    






