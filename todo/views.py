from datetime import datetime
from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required
from LIVR import Validator
import json
from django.http import HttpResponse
from todo.models import Link, Game, LastActivity


ADD_LINK_VALIDATOR = Validator.Validator({
    'url': ['required', 'url'],
    'limit': ['required', 'integer']
})

ADD_GAME_VALIDATOR = Validator.Validator({
    'name': 'required',
    'limit': ['required', 'integer']
})


VISITED_SITE_VALIDATOR = Validator.Validator({
    'url': ['required']
})


OPENED_PROGRAM_VALIDATOR = Validator.Validator({
    'name': 'required'
})


@login_required
def add_game_handler(request):
    parsed_data = json.loads(request.body.decode('utf-8'))
    valid_data = ADD_GAME_VALIDATOR.validate(parsed_data)
    if valid_data:
        game = Game(
            name=valid_data['name'],
            limit=valid_data['limit'],
            user=request.user
        )
        game.save()
        return HttpResponse(json.dumps({
            'state': 'success',
            'Program name': valid_data['name']
        }))
    else:
        return HttpResponse(
            json.dumps({
                'error': 'Parameters is not valid: {0!s}'.format(ADD_GAME_VALIDATOR.get_errors())
            }),
            status=422,
            content_type="application/json")


@login_required
def add_link_handler(request):
    parsed_data = json.loads(request.body.decode('utf-8'))
    valid_data = ADD_LINK_VALIDATOR.validate(parsed_data)
    if valid_data:
        host = urlparse(valid_data['url']).hostname
        link = Link(
            url=host,
            limit=valid_data['limit'],
            user=request.user
        )
        link.save()
        return HttpResponse(json.dumps({
            'state': 'success',
            'url': valid_data['url']
        }))
    else:
        return HttpResponse(
            json.dumps({
                'error': 'Parameters is not valid: {0!s}'.format(ADD_LINK_VALIDATOR.get_errors())
            }),
            status=422,
            content_type="application/json")


@login_required
def get_activities_handler(request):
    links = Link.objects.filter(user=request.user)
    games = Game.objects.filter(user=request.user)
    response_data = [{
        'id': i.id,
        'url': i.url,
        'limit': i.limit,
        'gone_time': i.gone_time,
        'type': 'link'
    } for i in links]
    response_data.extend([{
        'id': i.id,
        'url': i.name,
        'limit': i.limit,
        'gone_time': i.gone_time,
        'type': 'game'
    } for i in games])
    return HttpResponse(json.dumps(response_data))


@login_required
def site_visited_handler(request):
    parsed_data = json.loads(request.body.decode('utf-8'))
    valid_data = VISITED_SITE_VALIDATOR.validate(parsed_data)
    if valid_data:
        host = urlparse(valid_data['url']).hostname
        try:
            last_activity = LastActivity.objects.get(user=request.user)
        except LastActivity.DoesNotExist:
            last_activity = LastActivity()

        delta_time = datetime.now() - last_activity.time.replace(tzinfo=None)
        if last_activity.activity is not None:
            last_activity.activity.gone_time += delta_time.seconds // 60
            last_activity.activity.save()

        if Link.objects.filter(url=host).exists():
            last_activity.activity = Link.objects.get(url=host)
        else:
            last_activity.activity = None
        last_activity.time = datetime.now()
        last_activity.save()
        return HttpResponse(json.dumps({"status": "success"}))
    else:
        return HttpResponse(
            json.dumps({
                'error': 'Parameters is not valid: {0!s}'.format(VISITED_SITE_VALIDATOR.get_errors())
            }),
            status=422,
            content_type="application/json")


@login_required
def program_opened_handler(request):
    parsed_data = json.loads(request.body.decode('utf-8'))
    valid_data = OPENED_PROGRAM_VALIDATOR.validate(parsed_data)
    if valid_data:
        program_name = valid_data['name']
        try:
            last_activity = LastActivity.objects.get(user=request.user)
        except LastActivity.DoesNotExist:
            last_activity = LastActivity()

        delta_time = datetime.now() - last_activity.time.replace(tzinfo=None)
        if last_activity.activity is not None:
            last_activity.activity.gone_time += delta_time.seconds // 60
            last_activity.activity.save()

        if Game.objects.filter(name=program_name).exists():
            last_activity.activity = Game.objects.get(name=program_name)
        else:
            last_activity.activity = None
        last_activity.time = datetime.now()
        last_activity.save()
        return HttpResponse(json.dumps({"status": "success"}))
    else:
        return HttpResponse(
            json.dumps({
                'error': 'Parameters is not valid: {0!s}'.format(OPENED_PROGRAM_VALIDATOR.get_errors())
            }),
            status=422,
            content_type="application/json")
