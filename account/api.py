from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm, ProfileForm, PasswordChangeForm
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from django.core.mail import send_mail
from notification.utils import create_notification


@api_view(['GET'])
def me(request):
    return JsonResponse(
        {
            'id': request.user.id,
            'name': request.user.name,
            'email': request.user.email,
            'avatar': request.user.get_avatar()
        }
    )


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
    if form.is_valid():
        user = form.save()
        user.is_active = False
        user.save()
        url = f'http://127.0.0.1:8000/activateemail/?email={user.email}&id={user.id}'
        send_mail(
            "Please verify your email",
            f"The url for activating your account is: {url}",
            "noreply@wey.com",
            [user.email],
        )
    else:
        message = form.errors.as_json()
    return JsonResponse({'message': message}, safe=False)


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


@api_view(['GET'])
def my_friend_suggestions(request):
    serializer = UserSerializer(
        request.user.people_you_may_know.all(), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def send_friend_request(request, pk):
    user = User.objects.get(pk=pk)
    check1 = FriendRequest.objects.filter(
        created_for=request.user).filter(created_by=user)
    check2 = FriendRequest.objects.filter(
        created_for=user).filter(created_by=request.user)
    if not check1 or not check2:
        friend_request = FriendRequest.objects.create(
            created_for=user, created_by=request.user)
        create_notification(request, 'newfriendrequest',
                            friend_request_id=friend_request.id)
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

    create_notification(request, 'acceptedfriendrequest',
                        friend_request_id=friend_request.id)

    return (JsonResponse({'message': 'friend request updated'}))


@api_view(['POST'])
def edit_profile(request):
    user = request.user
    email = request.data.get('email')
    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'Email already exists!'})
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

        serializer = UserSerializer(user)
        return JsonResponse({'message': 'success', 'user': serializer.data})


@api_view(['POST'])
def edit_password(request):
    user = request.user
    form = PasswordChangeForm(data=request.POST, user=user)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)
