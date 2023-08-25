from .models import Notification
from post.models import Post
from account.models import FriendRequest


def create_notification(request, type_of_notification, post_id=None, friend_request_id=None):
    created_for = None
    if type_of_notification == 'postlike':
        body = f'{request.user.name} liked one of your post!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'postcomment':
        body = f'{request.user.name} commented on one of your post!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'newfriendrequest':
        friend_request = FriendRequest.objects.get(pk=friend_request_id)
        created_for = friend_request.created_for
        body = f'{request.user.name} sent you a friend request!'
    elif type_of_notification == 'acceptedfriendrequest':
        friend_request = FriendRequest.objects.get(pk=friend_request_id)
        created_for = friend_request.created_for
        body = f'{request.user.name} accepted your a friend request!'
    elif type_of_notification == 'rejectedfriendrequest':
        friend_request = FriendRequest.objects.get(pk=friend_request_id)
        created_for = friend_request.created_for
        body = f'{request.user.name} rejected your a friend request!'

    notification = Notification.objects.create(
        created_by=request.user,
        type_of_notification=type_of_notification,
        body=body,
        post_id=post_id,
        created_for=created_for,
    )
    return notification
