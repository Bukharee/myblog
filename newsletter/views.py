from django.shortcuts import render
from .models import Subscribe
from .utils import SendSubscribeMail
from django.http import HttpResponse, JsonResponse


def subscribe(request):
    if request.method == 'POST':
        email = request.POS['email_id']
        email_qs = Subscribe.objects.filter(email_id=email)
        if email_qs.exists():
            data = {
                'status': '404'
            }
            return JsonResponse(data)
        else:
            Subscribe.objects.create(email_id= email)
            SendSubscribeMail(email)
            return HttpResponse('/')