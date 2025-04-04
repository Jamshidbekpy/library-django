from apps.resources.models import Category, Resource, ResourceType
def categories(request):

    context = {
        'categories': Category.objects.all(),
       
    }
    return context


