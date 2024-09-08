from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from meow_messenger.models import *
import json
from django.contrib.auth.hashers import make_password, check_password


@csrf_exempt
def get_messages(request, id_chat, count):
    if request.method == 'POST':
        try:
            messages = Message.objects.filter(chat=Group_chat.objects.filter(id=id_chat).first())
        except:
            return HttpResponse('Error data')
        d = []
        for m in messages[:count + 1]:
            if m.file != '':
                d.append({'file': f'/media/{str(m.file)}'})
            d.append({
                'id': m.id,
                'text': m.text,
                'user': m.user.id,
                'chat': m.chat.id,
                'file': '',
                'datetime': str(m.datetime)
            })
        return HttpResponse(json.dumps(d))


@csrf_exempt
def get_chats(request):
    if request.method == 'POST':
        id_user = request.POST['id_user']
        user = get_object_or_404(User, id=id_user)
        chats = Group_chat.objects.filter(users__in=[user])
        chats_new = []
        for chat in chats:
            members = []
            for member in chat.users.all():
                members.append({
                    'id': member.id,
                    'login': member.login,
                    'avatar': f'/media/{str(member.avatar)}'
                })
            chats_new.append({
                'id': chat.id,
                'title': chat.title,
                'description': chat.description,
                'avatar': f'{str(chat.avatar)}',
                'users': members
            })
        return HttpResponse(json.dumps(chats_new))
    else:
        return HttpResponse('Данные охраняются саблизубыми котиками^^')


@csrf_exempt
def add_chat(request):
    if request.method == 'POST':
        id_creator = int(request.POST['id_creator'])
        title = request.POST['title']
        description = request.POST['description']
        creator = get_object_or_404(User, id=id_creator)

        chat = Group_chat(title=title, description=description, creator=creator)
        chat.save()
        chat.users.add(creator)
        return HttpResponse('Ok')
    else:
        return HttpResponse('Данные охраняются саблизубыми котиками^^')


@csrf_exempt
def del_chat(request):
    if request.method == 'POST':
        try:
            id_chat = (int(request.POST['id_chat']))
            Group_chat.objects.filter(id=id_chat).delete()
        except:
            return HttpResponse('del error')
        return HttpResponse('Ok')
    else:
        return HttpResponse('del error')


@csrf_exempt
def auth(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            password = request.POST['password']
            if User.objects.filter(email=email).exists():
                user = get_object_or_404(User, email=email)
                if check_password(password, user.password):
                    return HttpResponse(json.dumps({'token': user.token_api}))
                else:
                    return HttpResponse('Неверный пароль!')
            else:
                return HttpResponse('Такого логина не существует')
        except:
            return HttpResponse('auth error')
