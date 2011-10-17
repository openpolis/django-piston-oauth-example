from django.conf.urls.defaults import *
from piston.resource import Resource
# from piston.authentication import HttpBasicAuthentication, OAuthAuthentication
from api.authentication import TwoLeggedOAuthAuthentication
from api.handlers import BlogpostHandler

# auth = HttpBasicAuthentication(ealm='Example Blog API')
# auth = OAuthAuthentication(ealm='Example Blog API')
auth = TwoLeggedOAuthAuthentication(realm='Example Blog API')

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
