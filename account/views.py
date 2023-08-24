from django.shortcuts import render
from .models import User
from django.http import HttpResponse


def activateemail(request):
    email = request.GET.get('email', '')
    id = request.GET.get('id', '')

    if email and id:
        user = User.objects.get(id=id, email=email)
        user.is_active = True
        user.save()
        return HttpResponse('The user is now activated. You can now login')
    else:
        return HttpResponse('The parameters are not valid')
