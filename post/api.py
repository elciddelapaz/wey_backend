from django.http import JsonResponse
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer
from .models import Post, Like, Comment, Trend
from account.models import User
from account.serializers import UserSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import PostForm


@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]
    for user in request.user.friends.all():
        user_ids.append(user.id)
    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    trend = request.GET.get('trend', '')
    if trend:
        posts = posts.filter(body__icontains='#' + trend)
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)
    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    return JsonResponse({
        'posts': post_serializer.data,
        'user': user_serializer.data
    }, safe=False)


@api_view(['GET'])
def post_detail(request, id):
    post = Post.objects.get(pk=id)
    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })


@api_view(['GET'])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def post_create(request):
    data = request.data
    form = PostForm(request.data)
    if (form.is_valid()):
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something'})


@api_view(['POST'])
def post_like(request, id):
    post = Post.objects.get(pk=id)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post = Post.objects.get(pk=id)
        post.likes_count += 1
        post.likes.add(like)
        post.save()
        return JsonResponse({'message': 'like created'})
    else:
        return JsonResponse({'message': 'post already liked'})


@api_view(['POST'])
def post_create_comment(request, id):
    comment = Comment.objects.create(
        body=request.data.get('body'), created_by=request.user)
    post = Post.objects.get(pk=id)
    post.comments.add(comment)
    post.comments_count += 1
    post.save()

    serializer = CommentSerializer(comment)
    return JsonResponse(serializer.data, safe=False)
