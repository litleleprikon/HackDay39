# Create your views here.
import json
import random
import smtplib

from django.contrib.auth.models import User
from LIVR import Validator
from django.contrib.auth import login, authenticate, logout
from django.http import *

from HackDay39.settings import SENDER_EMAIL, SENDER_PASSWORD

CREATE_USER_VALIDATOR = Validator.Validator({
    'email': ['required', 'email'],
})

LOGIN_VALIDATOR = Validator.Validator({
    'username': 'required',
    'password': 'required'
})

PASSWORD_LENGTH = 8


def pass_gen():
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join([alphabet[random.randrange(len(alphabet))] for _ in range(PASSWORD_LENGTH)])


def send_pass(target, password):
    message_text = """
    Hello dear user, this is your password for ToDo app {0:s}
    """.format(password)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, target, message_text)
    server.close()


def create_user(email, username):
    password = pass_gen()
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    user.save()
    send_pass(target=email, password=password)
    return HttpResponse(json.dumps({
        'status': 'User created',
        'username': username
    }))


def delete_user_handler(request):
    pass


def new_user_handler(request):
    data = json.loads(request.body.decode('utf-8'))
    valid_data = CREATE_USER_VALIDATOR.validate(data)

    if valid_data:
        email = valid_data['email']
        username = email.split('@', maxsplit=1)[0]
        users_count = User.objects.filter(username=username).count()

        if users_count > 0:
            return HttpResponse(json.dumps({'error': 'User already exist'}), status=409, content_type="application/json")

        return create_user(email, username)

    else:
        HttpResponse(
            json.dumps({
                'error': 'Parameters is not valid: {0!s}'.format(CREATE_USER_VALIDATOR.get_errors())
            }),
            status=422,
            content_type="application/json")


def authenticate_handler(request):
    data = json.loads(request.body.decode('utf-8'))
    valid_data = LOGIN_VALIDATOR.validate(data)
    if valid_data:
        user = authenticate(username=valid_data['username'], password=valid_data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(json.dumps({
                    'status': 'Login successful'
                }))
            return HttpResponse(json.dumps(
                {'error': 'Account disabled'}),
                status=403)
        return HttpResponse(json.dumps(
            {'error': 'Incorrect username or password'}),
            status=403)
    HttpResponse(
        json.dumps({
            'error': 'Parameters is not valid: {0!s}'.format(LOGIN_VALIDATOR.get_errors())
        }),
        status=422,
        content_type="application/json")


def logout_handler(request):
    logout(request)
    return HttpResponse(json.dumps({
        'status': 'Logout'
    }))


def logged_user(func):
    def wrapper(request):
        user = re