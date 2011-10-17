## About

This fork from [glogiotatidis's django-piston-oauth-example](https://github.com/glogiotatidis/django-piston-oauth-example)
is a refactoring that changes the folders structure, by simplifying it, in my opinion, and adds a blog application, in order to test the oauth on some real URLs.


I like the fact that glogiotatidis uses the [piston release from pbs education](https://github.com/pbs-education/django-piston), replacing /oauth.py/ and
/authentication.py/ with the ones from [snowy](http://git.gnome.org/browse/snowy/tree/).
It seems to me that there's more activity there than in the original [jespern](https://bitbucket.org/jespern/django-piston/wiki/Home)'s project.
So I want to try and use it for my project.

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

    `pythom manage.py syncdb`
    
1. start server

    `python manage.py runserver`
    
1. login to admin panel through http://localhost:8000/admin/
  * Create a new Consumer with Key: testkey and Secret: testsecret
  * Create a test blog post
1. Your app is now accepting oauth-requests

## Try
1. Make sure that server runs
1. Make sure that you have activated the environment
1. Run oauth_client.py and follow the instructions 
   * be sure to browse the authentication url!
   * insert some fake PIN when requested (3098)
1. You should end up with a oauth_token and a oauth_token_secret printed on screen
1. try accessing the posts, in yml format, you should get the denied message
    
    `curl http://localhost:8000/api/posts.yaml`
    
1. launch twisted oauth-proxy ($KEY and $SECRET must be substituted manually in the command line)

    cd oauth-proxy
    twistd -n oauth_proxy --consumer-key testkey --consumer-secret testsecret --token $KEY --token-secret $SECRET

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

In order to enable two-legged authentication for this example project:

1. go to gregbayer's [https://github.com/gregbayer/django-piston-two-legged-oauth](https://github.com/gregbayer/django-piston-two-legged-oauth)
1. copy `src/authentication.py` content into your `api/authentication.py` file
1. modify your api/urls.py file so that it looks like the one below (YMMV)
1. launch twisted oauth-proxy, using 'empty' access token key and secret

    cd oauth-proxy
    twistd -n oauth_proxy --consumer-key testkey --consumer-secret testsecret --token "" --token-secret ""

1. try accessing the posts through the oauth-proxy, done!

    `curl -x localhost:8001 "http://localhost:8000/api/posts.yaml"`

Now, your application is able to expose resources both through the three-legged and the two-legged authentication workflow.


\# urls.py

    from django.conf.urls.defaults import *
    from piston.resource import Resource
    from api.authentication import TwoLeggedOAuthAuthentication
    from api.handlers import BlogpostHandler

    #auth = HttpBasicAuthentication(realm='My sample API')
    # auth = OAuthAuthentication(realm="Test Realm")
    auth = TwoLeggedOAuthAuthentication(realm='API')

    class CsrfExemptResource( Resource ):
        def __init__( self, handler, authentication = None ):
            super( CsrfExemptResource, self ).__init__( handler, authentication )
            self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )

    def TwoLeggedOAuthProtectedResource(handler):
        return CsrfExemptResource(handler=handler, authentication=auth)

    blogposts = TwoLeggedOAuthProtectedResource(handler=BlogpostHandler)

    urlpatterns = patterns('',
        url(r'^posts\.(?P<emitter_format>.+)', blogposts, name='blogposts'),
        # automated documentation url(r'^$', documentation_view),
    )

    urlpatterns += patterns(
        'piston.authentication',
        url(r'^oauth/request_token/$','oauth_request_token'),
        url(r'^oauth/authorize/$','oauth_user_auth'),
        url(r'^oauth/access_token/$','oauth_access_token'),
    )



