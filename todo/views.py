from django.contrib.auth.decorators import login_required
from LIVR import Validator
import json
from django.http import HttpResponse
from todo.models import Link, Game


ADD_LINK_VALIDATOR = Validator.Validator({
    'url': ['required', 'url'],
    'limit': ['required', 'integer']
})

ADD_GAME_VALIDATOR = Validator.Validator({
    'name': 'required',
    'limit': ['required', 'integer']
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
            'url': valid_data['url']
        }))
    else:
        HttpResponse(
            json.dumps({
                'error': 'Parameters is not valid: {0!s}'.format(ADD_LINK_VALIDATOR.get_errors())
            }),
            status=422,
            content_type="application/json")


@login_required
def add_link_handler(request):
    parsed_data = json.loads(request.body.decode('utf-8'))
    valid_data = ADD_LINK_VALIDATOR.validate(parsed_data)
    if valid_data:
        link = Link(
            url=valid_data['url'],
            limit=valid_data['limit'],
            user=request.user
        )
        link.save()
        return HttpResponse(json.dumps({
            'state': 'success',
            'url': valid_data['url']
        }))
    else:
        HttpResponse(
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
        'url': i.url,
        'limit': i.limit,
        'gone_time': i.gone_time,
        'type': 'game'
    } for i in games])
    return HttpResponse(json.dumps(response_data))
