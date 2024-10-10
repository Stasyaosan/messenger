from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from meow_messenger.models import *
import json
from django.contrib.auth.hashers import make_password, check_password
from meow_messenger.views import generate_Token


@csrf_exempt
def get_messages(request):
    if request.method == 'POST':
        id_chat = request.POST['id_chat']
        count = int(request.POST['count'])
        try:
            messages = Message.objects.filter(chat=Group_chat.objects.filter(id=id_chat).first())
        except:
            return HttpResponse('Error data')
        d = []
        for m in messages[:count + 1]:
            img = ''
            if m.file != '':
                img = f'/media/{str(m.file)}'
            d.append({
                'id': m.id,
                'text': m.text,
                'user': m.user.id,
                'chat': m.chat.id,
                'file': img,
                'datetime': str(m.datetime)
            })
        return HttpResponse(json.dumps(d))


@csrf_exempt
def get_chats(request):
    if request.method == 'POST':
        id_user = request.POST['id_user']
        token = request.POST['token']
        if get_object_or_404(User, id=id_user).token_api != token:
            return HttpResponse('403')
        else:
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
            login = request.POST['login']
            password = request.POST['password']
            if User.objects.filter(login=login).exists():
                user = get_object_or_404(User, login=login)
                if check_password(password, user.password):
                    return HttpResponse(json.dumps({'token': user.token_api}))
                else:
                    return HttpResponse('Неверный пароль!')
            else:
                return HttpResponse('Такого логина не существует')
        except:
            return HttpResponse('auth error')


@csrf_exempt
def reg(request):
    if request.method == 'POST':
        email = request.POST['email']
        login = request.POST['login']
        password = request.POST['password']
        token = generate_Token()
        if User.objects.filter(email=email).exists():
            return HttpResponse('1')

        user = User(login=login, email=email, password=make_password(password), token=token, token_api=generate_Token())
        user.save()

        return HttpResponse('2')


@csrf_exempt
def get_id_user(request):
    token = request.POST['token']
    user = User.objects.filter(token_api=token).first()
    return HttpResponse(json.dumps({'id_user': user.id}))


@csrf_exempt
def add_message(request):
    if request.method == 'POST':
        id_chat = request.POST['id_chat']
        text_message = request.POST['text_message']
        id_user = request.POST['id_user']
        token = request.POST['token']
        user = get_object_or_404(User, id=id_user)
        chat = get_object_or_404(Group_chat, id=id_chat)
        if user.token_api == token:
            message_add = Message(text=text_message, user=user, chat=chat)
            message_add.save()
            return HttpResponse(json.dumps({'status': 'ok', 'id_message': message_add.id}))
        else:
            return HttpResponse(json.dumps({'status': 'Error token'}))


@csrf_exempt
def DeleteMessage(request):
    id_message = request.POST['id_message']
    Message.objects.filter(id=id_message).delete()
    return HttpResponse(json.dumps({'status': 'ok'}))
