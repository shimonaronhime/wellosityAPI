from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from mainApi.models import User, UserProfile, AllMedHistory, AllEvent, UserCreatedEvent, UserEvent, Comment, Like
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ('user',)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

#admin.site.register(UserProfile)
admin.site.register(AllMedHistory)
admin.site.register(AllEvent)
admin.site.register(UserEvent)
admin.site.register(UserCreatedEvent)
admin.site.register(Comment)
admin.site.register(Like)

 
