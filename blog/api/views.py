from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import BlogPostSerializer, CommentSerializer
from blog.models import BlogPost, Comment


@api_view(['GET'],)
@authentication_classes([])
@permission_classes([])
def all_blog_posts(request):
    blog = BlogPost.objects.all()
    serializer = BlogPostSerializer(blog, many=True)
    context = {
        'post': serializer.data
    }
    return Response(context)


@api_view(['GET'],)
@authentication_classes([])
@permission_classes([])
def view_blog(request, uuid):
    blog = BlogPost.objects.get(uuid=uuid)
    serializer = BlogPostSerializer(blog)
    comments = blog.comment_set.all()
    comment_serializer = CommentSerializer(comments, many=True)
    context = {
        'post': serializer.data,
        'comments': comment_serializer.data
    }
    return Response(context)