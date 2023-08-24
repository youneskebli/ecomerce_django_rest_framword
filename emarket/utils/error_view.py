from django.http import JsonResponse

def handler404(request,exception):
    message = ("this path does not exist")
    response = JsonResponse(data={'error':message})
    response.status_code=404
    return response

def handler500(request):
    message = ("internel server erooooor")
    response = JsonResponse(data={'error':message})
    response.status_code=500
    return response