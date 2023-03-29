from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def addFood(request):
    data = {}
    message = ""
    status = 0
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
    return JsonResponse({
        "Data": data,
        "Message": message,
        "Status": status
    })