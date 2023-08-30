import django
import os
import sys
from collections import Counter
from datetime import timedelta
from django.utils import timezone

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wey_backend.settings")
django.setup()

from post.models import User

users = User.objects.all()

for user in users:
    user.people_you_may_know.clear()
    for friend in user.friends.all():
        for friends_friend in friend.friends.all():
            if friends_friend not in user.friends.all() and friends_friend != user:
                user.people_you_may_know.add(friends_friend)
