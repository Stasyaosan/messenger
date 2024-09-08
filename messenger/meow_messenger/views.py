from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
import random
from django.db.models import Q
from datetime import datetime


def index(request):
    if 'user' in request.session:
        return redirect('/profile')

    return render(request, 'index.html')


def generate_Token():
    s = 'asdfklewjtwogkassdkGGUYGUYGUYTFlgfnmsdklgnhythbGUYHJERIGVKGIfdfsdf564643wjklegnweklfgfgerygfyegydfgYYYGY656565rfyrgye'
    return ''.join([s[random.randint(0, len(s) - 1)] for i in range(32)])


def ajaxReg(request):
    print(request.POST)
    email = request.POST['email']
    login = request.POST['login']
    password = request.POST['password']
    token = generate_Token()
    if User.objects.filter(email=email).exists():
        return HttpResponse('1')

    user = User(login=login, email=email, password=make_password(password), token=token, token_api=generate_Token())
    user.save()

    url = 'http://127.0.0.1:8000/suc/' + token + ''
    send_mail(subject='Активация учётной записи', message=url, from_email=settings.EMAIL_HOST_USER,
              recipient_list=[email])
    return HttpResponse('2')


def suc_user(request, token):
    if User.objects.filter(token=token).exists():
        User.objects.filter(token=token).update(suc=1, token='')
        return HttpResponse('Вы успешно активировали свою учетную запись! <a href="/">Перейти на сайт</a>')
    else:
        return HttpResponse('Token не верный!')


def ajaxAuth(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            if User.objects.filter(suc=1, email=email).exists():
                user = User.objects.filter(email=email).first()
                if check_password(password, user.password) and email == user.email:
                    request.session['user'] = user.email
                    return HttpResponse('3')
                else:
                    return HttpResponse('2')
            else:
                return HttpResponse('1')
        else:
            return HttpResponse('4')
    else:
        return HttpResponse('5')


def get_chat(request, id):
    from django.utils import timezone
    current_chat = get_object_or_404(Group_chat, id=id)
    messages = Message.objects.filter(chat=current_chat).order_by('datetime')
    all_users = User.objects.all()

    current_user = User.objects.filter(email=request.session['user']).first()
    current_user.update_date = timezone.localtime()
    current_user.save()
    print(current_user.update_date)

    current_date = datetime.now().date().strftime('%Y-%m-%d')
    current_time = datetime.now().time().strftime('%H:%M')

    return render(request, 'chat/chat.html',
                  {'all_users': all_users, 'current_chat': current_chat, 'login': current_user.login,
                   'current_user': current_user, 'messages': messages,
                   'chats': get_user_chat(current_user), 'current_date': current_date, 'current_time': current_time})


def create_chat(request):
    if 'user' in request.session:
        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            creator = get_object_or_404(User, email=request.session['user'])
            new_chat = Group_chat(title=title, description=description,
                                  creator=creator)
            new_chat.save()
            new_chat.users.add(creator)

    return redirect('/profile')


def profile(request):
    if 'user' in request.session:
        if request.method == 'POST':
            path = ''
            login = request.POST['login']
            if 'avatar' in request.FILES:
                if request.FILES['avatar']:
                    file = request.FILES['avatar']
                    fs = FileSystemStorage()
                    fs.save('avatars/' + file.name, file)
                    path = 'avatars/' + file.name

            user = get_object_or_404(User, email=request.session['user'])
            user.login = login

            if path != '':
                user.avatar = path
            user.save()
        current_user = User.objects.filter(email=request.session['user']).first()
    return render(request, 'chat/profile.html', {'user': current_user, 'chats': get_user_chat(current_user)})


def logout(request):
    if 'user' in request.session:
        del request.session['user']

    return redirect('/')


def get_user_chat(user):
    return Group_chat.objects.filter(users__in=[user])


def add_user(request, id_chat, id_user):
    chat = get_object_or_404(Group_chat, id=id_chat)
    user = get_object_or_404(User, id=id_user)
    current_user = get_object_or_404(User, email=request.session['user'])
    if chat.creator.id == current_user.id:
        chat.users.add(user)

    return redirect('/chat/' + str(id_chat))


def settings_chat(request):
    if request.method == 'POST' and 'user' in request.session:
        path = ''
        id_chat = request.POST['id_chat']
        title = request.POST['title']
        description = request.POST['description']
        if 'avatar_chat' in request.FILES:
            if request.FILES['avatar_chat']:
                file = request.FILES['avatar_chat']
                fs = FileSystemStorage()
                fs.save('avatars_chat/' + file.name, file)
                path = 'avatars_chat/' + file.name

        chat = get_object_or_404(Group_chat, id=id_chat)
        chat.title = title
        chat.description = description
        if path != '':
            chat.avatar = path
        chat.save()

        return redirect('/chat/' + id_chat)


def del_chat(request, id_chat):
    Group_chat.objects.filter(id=id_chat).delete()

    return redirect('/')


def delete_message(request, id_message, id_chat):
    message = Message.objects.filter(id=id_message).first()
    current_user = User.objects.filter(email=request.session['user']).first()
    if current_user == message.user:
        Message.objects.filter(id=id_message).delete()
    return redirect('/chat/' + str(id_chat))


def update_date_user(id_user):
    User.objects.filter(id=id_user).update(update_date=datetime.now())
