from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

        
class AllMedHistory(models.Model):
    '''
    This model lists out every searchable medical history item including current medical issues(type 1), medications (type 2), family history (type 3), allergies (type 4). Smoking history, pregnancy and possibly sexual activity are current issues.
    '''
    user = models.ManyToManyField(User, related_name= 'allMedHistories', blank=True)
    
    historyType = models.IntegerField(default=0) #types
    description = models.CharField(max_length = 230)
    
    def __str__(self):
        return '%d: %s' % (self.historyType, self.description)
    
    class Meta:
        ordering = ['historyType']

class AllEvent(models.Model):
    '''
    This table includes all possibe events that could be pushed to the user. It includes an event type (appt, labs, imaging, survey). The foreign keys indicate which, if any, medical histories are associated with the item.
    '''
    user = models.ManyToManyField(User, related_name = 'allUserEvents', through='UserEvent', blank=True)
    
    name = models.TextField(max_length = 100)
    eventType = models.IntegerField() #appt=1, labs=2, imaging=3, survey/counseling=4
    minAge = models.DecimalField(max_digits = 5, decimal_places = 2)
    maxAge = models.DecimalField(max_digits = 5, decimal_places = 2)
    gender = models.IntegerField(default=0) #0=both, 1=men, 2=women
    timelineDescription = models.TextField()
    publicFeedDescription = models.TextField(null = True, blank=True)
    personalFeedDescription = models.TextField(null = True, blank=True)
    counselingText = models.TextField(null = True, blank=True)
    
    
    allMedHistory1 = models.ForeignKey(AllMedHistory, on_delete=models.CASCADE, null=True, blank=True, related_name = 'AllEvents_allMedHistory1')
    allMedHistory2 = models.ForeignKey(AllMedHistory, on_delete=models.CASCADE, null=True, blank=True, related_name = 'AllEvents_allMedHistory2')
    allMedHistory3 = models.ForeignKey(AllMedHistory, on_delete=models.CASCADE, null=True, blank=True, related_name = 'AllEvents_allMedHistory3')
    allMedHistory4 = models.ForeignKey(AllMedHistory, on_delete=models.CASCADE, null=True, blank=True, related_name = 'AllEvents_allMedHistory4')
    allMedHistory5 = models.ForeignKey(AllMedHistory, on_delete=models.CASCADE, null=True, blank=True, related_name = 'AllEvents_allMedHistory5')
    allMedHistory6 = models.ForeignKey(AllMedHistory, on_delete=models.CASCADE, null=True, blank=True, related_name = 'AllEvents_allMedHistory6')
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    '''
    Links UserProfile to a User model instance. User includes username, password, email, first_name, last_name
    '''
    user = models.OneToOneField(User, primary_key = True, related_name='userProfile')

    birthDate = models.DateField(blank=True, null=True)
    gender = models.IntegerField(default=0, blank=True, null=True) # 1 is male, 2 is female
    completionPercentage = models.IntegerField(default=0, null=True, blank=True)
    profilePicture = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, blank=True, null=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    
    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

class UserCreatedEvent(models.Model):
    '''
    Events that are created by the user and added to the timeline
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'userCreatedEvents', null=True, blank=True)
    
    
    eventType = eventType = models.IntegerField() 
    withWhom = models.CharField(max_length = 100, null=True, blank=True)
    eventDate = models.DateField()
    description = models.TextField(max_length = 300, null=True, blank=True)
    
class UserEvent(models.Model):
    '''
    These are specific AllEvents that apply to specific users
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='eventsOfUser')
    allEvent = models.ForeignKey(AllEvent, on_delete=models.CASCADE, null=True, blank=True, related_name='eventInfo')
    
    createdEvent = models.OneToOneField(UserCreatedEvent, related_name='userEventForCreatedEvent', null=True, blank=True)
    
    completed = models.IntegerField(default=0, null=True, blank=True)
    dateCompleted = models.DateField(null=True, blank=True)
    dateShared = models.DateField(null=True, blank=True)
    ifShared = models.IntegerField(default=0, null=True, blank=True) #0=not shared, 1=friends, 2=public
    
    def __str__(self):
        return '%s : %d' % (self.user, self.completed) #need to add DateTimeField
    
    class Meta:
        ordering = ['dateCompleted']

class Like(models.Model):
    '''
    Every like by every user for any UserEvent
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    userEvent = models.ForeignKey(UserEvent, on_delete=models.CASCADE, null=True, blank=True, related_name = 'eventLikes')
    
    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
    
class Comment(models.Model):
    '''
    Every comment by every user for any UserEvent
    '''
    text = models.TextField(max_length = 400, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'commenter')
    userEvents = models.ForeignKey(UserEvent, on_delete=models.CASCADE, null=True, blank=True, related_name = 'eventComments')
    commentTime = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['commentTime']
    
    def __str__(self):
        return '%s: %s' % (self.text, self.commentTime)



