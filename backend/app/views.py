from django.http import JsonResponse


def api_health(request):
    return JsonResponse({})
