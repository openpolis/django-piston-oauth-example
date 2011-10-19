from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, require_mime, require_extended
from blog.models import Blogpost

from django.contrib.auth.decorators import login_required


class BlogpostHandler(BaseHandler):
    """
    Authenticated entrypoint for blogposts.
    """
    model = Blogpost
    
    def read(self, request, id=None):
        base = Blogpost.objects
        if id is None:
            # return PostSummaryView([x for x in base.all()])
            return [{'title': x.title, 'author': x.author.username} for x in base.all()]
        else:
            try:
                post = base.get(id=id)
            except Blogpost.DoesNotExist:
                raise Exception('Error retrieving post with ID %s: not found' % id)
            # return PostDetailedView(post)
            return post
    
    def create(self, request):
        """ Creates a new blogpost.  """
        attrs = self.flatten_dict(request.POST)
        print "CREATE ", attrs, request.user
        if self.exists(**attrs):
            return rc.DUPLICATE_ENTRY
        else:
            post = Blogpost(title=attrs['title'], content=attrs['content'], author=request.user)
            post.save()
        return post
 
