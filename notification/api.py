from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from .serializers import NotificationSerializer
from .models import Notification


@api_view(['GET'])
def notifications(request):
    notification = request.user.received_notification.filter(is_read=False)
    serializer = NotificationSerializer(notification, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def read_notification(request, id):
    notification = Notification.objects.filter(
        created_for=request.user).get(id=id)
    notification.is_read = True
    notification.save()

    return JsonResponse({'message': 'notification read'})
