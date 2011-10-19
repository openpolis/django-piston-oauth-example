from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication, OAuthAuthentication
from api.authentication import TwoLeggedOAuthAuthentication
from api.handlers import BlogpostHandler


# two-legged
auth = TwoLeggedOAuthAuthentication(realm='ExampleAPI')

# three-legged
# auth = OAuthAuthentication(realm='ExampleAPI')


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
