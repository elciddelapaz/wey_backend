from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer


@api_view(['GET'])
def me(request):
    return JsonResponse({'id': request.user.id, 'name': request.user.name, 'email': request.user.email})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'
    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })
    # form.save()
    if form.is_valid():
        form.save()
    else:
        message = 'error'

    return JsonResponse({'message': message})


@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []

    if user == request.user:
        requests = FriendRequest.objects.filter(
            created_for=request.user, status=FriendRequest.SENT)
    friends = user.friends.all()
    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'request': FriendRequestSerializer(requests, many=True).data
    }, safe=False)


@api_view(['POST'])
def send_friend_request(request, pk):
    user = User.objects.get(pk=pk)
    check1 = FriendRequest.objects.filter(
        created_for=request.user).filter(created_by=user)
    check2 = FriendRequest.objects.filter(
        created_for=user).filter(created_by=request.user)
    if not check1 or not check2:
        FriendRequest.objects.create(created_for=user, created_by=request.user)
        return (JsonResponse({'message': 'friend request sent'}))
    else:
        return (JsonResponse({'message': 'request already sent'}))


@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friend_request = FriendRequest.objects.filter(
        created_for=request.user).get(created_by=user)
    friend_request.status = status
    friend_request.save()

    user.friends.add(request.user)
    user.friends_count += 1
    user.save()

    request_user = request.user
    request_user.friends_count += 1
    request_user.save()

    return (JsonResponse({'message': 'friend request updated'}))
