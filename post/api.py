from django.http import JsonResponse
from django.db.models import Q
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer
from .models import Post, Like, Comment, Trend
from account.models import User, FriendRequest
from account.serializers import UserSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import PostForm, AttachmentForm
from notification.utils import create_notification


@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]
    for user in request.user.friends.all():
        user_ids.append(user.id)
    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    trend = request.GET.get('trend', '')
    if trend:
        posts = posts.filter(body__icontains='#' +
                             trend).filter(is_private=False)
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    if not request.user in user.friends.all():
        posts = posts.filter(is_private=False)

    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friend_request = True

    if (request.user in user.friends.all()):
        can_send_friend_request = False

    check1 = FriendRequest.objects.filter(
        created_for=request.user).filter(created_by=user)
    check2 = FriendRequest.objects.filter(
        created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_friend_request = False
    return JsonResponse({
        'posts': post_serializer.data,
        'user': user_serializer.data,
        'can_send_friend_request': can_send_friend_request
    }, safe=False)


@api_view(['GET'])
def post_detail(request, id):
    user_ids = [request.user.id]
    for user in request.user.friends.all():
        user_ids.append(user.id)
    post = Post.objects.filter(
        Q(created_by_id__in=list(user_ids)) | Q(is_private=False)).get(pk=id)
    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })


@api_view(['GET'])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if (form.is_valid()):
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachment.add(attachment)

        user = request.user
        user.posts_count += 1
        user.save()
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
        create_notification(request, 'postlike', post_id=post.id)
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
    create_notification(request, 'postcomment', post_id=post.id)
    serializer = CommentSerializer(comment)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def post_report(request, id):
    post = Post.objects.get(id=id)
    post.reported_by.add(request.user)
    post.save()
    return JsonResponse({'message': 'post reported'})


@api_view(['DELETE'])
def post_delete(request, id):
    post = Post.objects.filter(created_by=request.user).get(id=id)
    post.delete()
    return JsonResponse({'message': 'deleted'})
