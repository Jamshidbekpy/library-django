from apps.resources.models import Category, Resource, ResourceType
from apps.formula.models import Formula
def categories(request):
    # print(request.META.get('HTTP_HOST'))
    # print(request.META.get('HTTP_USER_AGENT'))
    # print(request.META.get('HTTP_REFERER'))
    # print(request.META.get('HTTP_ACCEPT_LANGUAGE'))
    # print(request.META.get('HTTP_ACCEPT_ENCODING'))
    # print(request.META.get('HTTP_ACCEPT'))
    # print(request.META.get('HTTP_CONNECTION'))
    # print(request.META.get('HTTP_COOKIE'))
    # print(request.META.get('HTTP_UPGRADE_INSECURE_REQUESTS'))
    # print(request.META.get('HTTP_CACHE_CONTROL'))
    # print(request.META.get('HTTP_SEC_FETCH_DEST'))
    # print(request.META.get('HTTP_SEC_FETCH_SITE'))
    # print(request.META.get('HTTP_SEC_FETCH_MODE'))
    # print(request.META.get('HTTP_SEC_FETCH_USER'))
    # print(request.META.get('HTTP_SEC_CH_UA'))
    # print(request.META.get('HTTP_SEC_CH_UA_MOBILE'))
    
    # # get the user's IP address
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]
    # else:
    #     ip = request.META.get('REMOTE_ADDR')
    # print(ip)
    
    # # get current base url
    # print(request.build_absolute_uri())
    
    # print("-------------------")
    context = {
        'categories': Category.objects.all(),
       
    }
    return context


