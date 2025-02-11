from .models import Announcement

def global_announcements(request):
    announcements = Announcement.objects.filter(is_active=True)
    return {'announcements': announcements}