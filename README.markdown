## About

This fork from [glogiotatidis's django-piston-oauth-example](https://github.com/glogiotatidis/django-piston-oauth-example)
is a refactoring that changes the folders structure, by simplifying it, in my opinion, and adds a blog application, in order to test the oauth on some real URLs.


I like the fact that glogiotatidis uses the [piston release from pbs education](https://github.com/pbs-education/django-piston), replacing /oauth.py/ and
/authentication.py/ with the ones from [snowy](http://git.gnome.org/browse/snowy/tree/).
It seems to me that there's more activity there than in the original [jespern](https://bitbucket.org/jespern/django-piston/wiki/Home)'s project.
So I want to try and use it for my project.

### Update
I cannot use piston release from pbs, since, it generates an error while inserting  data through POST. 
So I have to revert to the original jensen's piston code, and leave the advanced, customised features behind.
I will try to integrate it, somehow, once I got a better understanding of the code itself.

I added [twisted](http://twistedmatrix.com/trac/)'s [oauth-proxy](https://github.com/mojodna/oauth-proxy) plugin, so now twisted is part of the required packages to install. It is useful to quickly test oauth-request, by wrapping the oauth-part in a proxy. More on this below...

## Install

1. create a virtualenv, using [virtualenvwrapper](http://www.doughellmann.com/docs/virtualenvwrapper/command_ref.html) or whatever you like, create a working dir in django-piston-oauth-example
1. clone the repository

    `git clone git://github.com/openpolis/django-piston-oauth-example.git`

1. activate your virtualenv 

    `workon django-piston-oauth-example`, if using virtualenvwrapper
    
1. cd to django-piston-oauth-example
1. download and install django, twisted and dependencies

    `bash scripts/build_environment.sh`
    
1. create dbs, create superuser

    `django-admin.py syncdb`
    
1. start server

    `django-admin.py runserver`
    
1. login to admin panel through http://localhost:8000/admin/
  * Create a new Consumer with Key: `testkey` and Secret: `testsecret`
  * Create a test blog post
1. Your app is now accepting oauth-requests

## Try
1. Make sure that server runs
1. Make sure that you have activated the environment
1. Run `oauth_client.py` and follow the instructions 
   * be sure to browse the authentication url!
   * insert some fake PIN when requested (3098)
1. You should end up with a oauth_token and a oauth_token_secret printed on screen
1. try accessing the posts, in yml format, you should get the denied message
    
    `curl http://localhost:8000/api/posts.yaml`
    
1. launch twisted oauth-proxy ($KEY and $SECRET must be substituted manually in the command line)

    `cd oauth-proxy`
    
    `twistd -n oauth_proxy --consumer-key testkey --consumer-secret testsecret --token $KEY --token-secret $SECRET`

1. try accessing the posts through the oauth-proxy, you will get the yaml stream

    `curl -x localhost:8001 "http://localhost:8000/api/posts.yaml"`

You can also set your browser's proxy settings, in order to use the twisted oauth-proxy, so that you can play without using curl, if you like.


## Two-legged oauth workflow
According to this [cakebaker's post](http://cakebaker.42dh.com/2011/01/10/2-legged-vs-3-legged-oauth/)

> 2-legged OAuth, describes a typical client-server scenario, without any user involvement. 
> An example for such a scenario could be a local Twitter client application accessing your Twitter account.
> On a conceptual level 2-legged OAuth simply consists of the first and last steps of 3-legged OAuth:

> * Client has signed up to the server and got his client credentials (also known as “consumer key and secret”)
> * Client uses his client credentials (and empty token credentials) to access the protected resources on the server

This example already allows the two-legged authentication workflow, through the api/authentication.py file, grabbed from https://github.com/gregbayer/django-piston-two-legged-oauth. 
To test it:

1. launch twisted oauth-proxy, using 'empty' access token key and secret

    cd oauth-proxy
    twistd -n oauth_proxy --consumer-key testkey --consumer-secret testsecret --token "" --token-secret ""

1. try accessing the posts through the oauth-proxy, done!

    `curl -x localhost:8001 "http://localhost:8000/api/posts.yaml"`

## Advanced piston features
[PBS education's piston](https://github.com/pbs-education/django-piston) introduces many customisations.

### PistonView class
It is possible to define the exposed objects' views directly in the views file, using extensions of
the PistonView class.

\# api/views.py

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


\# api/handlers.py

    from piston.handler import BaseHandler, AnonymousBaseHandler
    from piston.utils import rc, require_mime, require_extended

    from blog.models import Blogpost
    from api.views import PostSummaryView

    class BlogpostHandler(BaseHandler):
        """
        Authenticated entrypoint for blogposts.
        """
        model = Blogpost
    
        def read(self, request, id=None):
            base = Blogpost.objects
            if id is None:
                return base.all()
            return PostSummaryView(base.get(pk=id))

\# api/urls.py

    from django.conf.urls.defaults import *
    from piston.resource import Resource
    from piston.authentication import OAuthAuthentication
    from api.handlers import BlogpostHandler

    auth = OAuthAuthentication(realm='Example Blog API')

    class CsrfExemptResource( Resource ):
        def __init__( self, handler, authentication = None ):
            super( CsrfExemptResource, self ).__init__( handler, authentication )
            self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )

    blogposts = CsrfExemptResource(handler=BlogpostHandler, authentication=auth)

    urlpatterns = patterns('',
        url(r'^posts\.(?P<emitter_format>.+)$', blogposts, name='blogposts'),
        url(r'^posts/(?P<id>[^/]+)\.(?P<emitter_format>.+)$', blogposts, name='blogpost'), 
        # automated documentation url(r'^$', documentation_view),
    )


