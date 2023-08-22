import django
import os
import sys
from collections import Counter
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wey_backend.settings")
django.setup()

from post.models import Post, Trend

def extract_hashtag(text, trends):
    for word in text.split():
        if word[0] == '#':
            trends.append(word[1:])
    return trends


for trend in Trend.objects.all():
    trend.delete()

trends = []
for post in Post.objects.all(): 
    extract_hashtag(post.body, trends)
    
for trend in Counter(trends).most_common(10):
    Trend.objects.create(hashtag=trend[0], occurences=trend[1])