from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
from piston.handler import PistonView, Field


class PostSummaryView(PistonView):
    fields = [
            'id',
            'title',
            Field('author.username', destination='author'),
            Field('', lambda x: x.created_on.strftime("%m/%d/%y"), destination='date_created'),
    ]


class PostDetailedView(PistonView):
    fields = [
            'title',
            'content',
            Field('author.username', destination='author'),
            Field('', lambda x: x.created_on.strftime("%m/%d/%y at %H:%M"), destination='time_created'),
    ]


def request_token_ready(request, token):
    error = request.GET.get('error', '')
    ctx = RequestContext(request, {
        'error' : error,
        'token' : token
    })
    return render_to_response(
        'piston/request_token_ready.html',
        context_instance = ctx
    )
