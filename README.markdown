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

    `cd oauth-proxy`
    
    `twistd -n oauth_proxy --consumer-key testkey --consumer-secret testsecret --token $KEY --token-secret $SECRET`

1. try accessing the posts through the oauth-proxy, you should get

    `curl -x localhost:8001 "http://localhost:8000/api/posts.yaml"`

You can also set your browser's proxy settings, in order to use the twisted oauth-proxy, so that you can play without using curl, if you like.