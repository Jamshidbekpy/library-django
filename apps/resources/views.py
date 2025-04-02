from django.shortcuts import render
from apps.resources.models import Category, Resource, ResourceType
from django.views.generic import ListView, DetailView
from django.db.models import Q 
from django.views import View
from django.core.paginator import Paginator
# Create your views here.

class ResourceTypeResourcesView(View):
    pass
    # paginate_by = 16
    # PAGINATION_URL = ''
    # def get(self, request, id):
    #     r_type = ResourceType.objects.filter(is_active = True, id=id).first()
        
    #     resources = Resource.objects.filter(is_active = True, resource_type = r_type)
    #     context={
    #         'r_type':r_type,
    #         'resources':resources,
            
    #     }
    #     return render(request, 'resources.html', context)
    
    # def get_queryset(self):
       
    #     queryset = Resource.objects.filter(is_active=True).order_by('-id')  # Base queryset

    #     # Get search query from request.GET (modify as needed)
    #     search_query = self.request.GET.get('search', '')
    #     if search_query:
    #         self.PAGINATION_URL = f'&search={search_query}'  
    #         queryset = queryset.filter(Q(title__icontains=search_query) | 
    #                                    Q(description__icontains=search_query) | 
    #                                    Q(author__icontains=search_query) | 
    #                                    Q(keywords__icontains=search_query))

    #     # Add additional filters based on request.GET parameters (modify as needed)
    #     filter_by_category = self.request.GET.get('category', '')
    #     if filter_by_category:
    #         self.PAGINATION_URL += f'&category={filter_by_category}'  
    #         queryset = queryset.filter(category__slug=filter_by_category)
            
            
    #     filter_by_type = self.request.GET.get('resourceType', '')
    #     if filter_by_type:
    #         self.PAGINATION_URL += f'&resourceType={filter_by_type}'
    #         queryset = queryset.filter(resource_type=filter_by_type)
            
            
    #     filter_by_auditoriya = self.request.GET.get('auditoria', '')
    #     if filter_by_auditoriya:
    #         self.PAGINATION_URL += f'&auditoria={filter_by_auditoriya}'
    #         queryset = queryset.filter(auditoria=filter_by_auditoriya)
        
    #     return queryset
    
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
    
from django.db.models import F

class ResourceDetailView(DetailView):
    model = Resource
    template_name = 'resource_detail.html'
    context_object_name = 'resource'
    lookup_field = 'slug'
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated:
            viewed_resources = set(request.session.get('viewed_resources', []))
            if str(self.object.id) not in viewed_resources:
                Resource.objects.filter(id=self.object.id).update(views=F('views') + 1)
                viewed_resources.add(str(self.object.id))
                request.session['viewed_resources'] = list(viewed_resources)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mostResources'] = Resource.objects.filter(category=self.object.category).exclude(id=self.object.id).order_by('?')[:4]
        context['tg_link'] = f"https://t.me/share/url?url={self.request.build_absolute_uri()}&text={self.object.title}"
        context['copy_link'] = f"{self.request.build_absolute_uri()}"
        if self.request.user.is_authenticated:
            # favorites = {f"{resource.id}": resource.is_favourited(resource, self.request.user) for resource in resources}
            favorites = list(self.request.user.favourites.all().values_list('resource_id', flat=True))
            print(favorites)
        else:
            favorites = []
        context['favorites'] = favorites
        return context
    
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import Resource

class WatermarkedFileView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'message':"Yuklab olish uchun tizimga kirishingiz kerak! "},status=status.HTTP_403_FORBIDDEN)
        try:
            resource = Resource.objects.get(pk=pk)
            response = HttpResponse(resource.watermarked_file, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{resource.watermarked_file.name}"'
            return response
        except Resource.DoesNotExist:
            return Response({'message': "Hech qanday ma'lumot topilmadi."}, status=status.HTTP_404_NOT_FOUND)


class DownloadFileView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'message':"Yuklab olish uchun tizimga kirishingiz kerak! "}, status=status.HTTP_403_FORBIDDEN)
        
        if  request.user.status == 'free':
            print(request.user.status)
            return Response({'message':"Sizning yuklab olishga huquqingiz yo'q!"}, status=status.HTTP_403_FORBIDDEN)
        try:
            resource = Resource.objects.get(pk=pk)
            response = HttpResponse(resource.original_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{resource.original_file.name}"'
            return response
        except Resource.DoesNotExist:
            return Response({'message': "Hech qanday ma'lumot topilmadi."}, status=status.HTTP_404_NOT_FOUND)
    
class HomePageView(View):
    def get(self, request):
        famous_ten_categories = Category.objects.all()[:10]

        context={
            'famous_ten_categories':famous_ten_categories,
        }

        return render(request, 'home.html', context)


class CategoryRecoursesView(View):
    pass
#     def get(self, request, id):
#         ctg = Category.objects.get(id=id)
#         category_resources = Resource.objects.all().filter(is_active=True, category=ctg)
        
#         context = {
#             'ctg':ctg,
#             'resources':category_resources,
           
#         }
#         return render(request, 'resources.html', context)



def custom_404_view(request, exception):
    return render(request, '404.html', status=404)