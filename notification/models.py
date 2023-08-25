import uuid
from django.db import models
from account.models import User
from post.models import Post


class Notification(models.Model):
    NEWFRIENDREQUEST = 'newfriendrequest'
    ACCPETEDFRIENDREQUEST = 'acceptedfriendrequest'
    REJECTEDFRIENDREQUEST = 'rejectedfriendrequest'
    POST_LIKE = 'postlike'
    POST_COMMENT = 'postcomment'

    CHOICES_TYPE_OF_NOTIFICATION = (
        (NEWFRIENDREQUEST, 'New friend request'),
        (ACCPETEDFRIENDREQUEST, 'Accepted friend request'),
        (REJECTEDFRIENDREQUEST, 'Rejected friend request'),
        (POST_LIKE, 'Post like'),
        (POST_COMMENT, 'Post comment'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(
        max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name="created_notification", on_delete=models.CASCADE)
    created_for = models.ForeignKey(
        User, related_name="received_notification", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
