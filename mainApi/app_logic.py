from django.contrib.auth.models import User, Group
from django.db.models import Q
from mainApi.models import UserProfile, AllMedHistory
from mainApi.models import AllEvent, UserEvent, Like, Comment, UserCreatedEvent

def getAllMedHistoryList(historyType):
    '''
    Returns searchable list of Med issues by type
    '''
    return AllMedHistory.objects.filter(historyType=historyType)

#need to show only 30 at one time then load next 30
def getFeedEvents(pk, ifShared):
    '''
    Populates personal, friend or public feed based on pk of user and isShared(0, 1 or 2)
    '''
    
    if ifShared == 0:
#        feed = User.objects.filter(pk=pk, allUserEvents__CompletedOrSharedInfo__completed__exact=1)
        feed = UserEvent.objects.filter(user_id=pk, completed__exact=1).order_by('dateCompleted')
        return feed
    elif ifShared == 1:
        feed =  UserEvent.objects.filter(ifShared__lte=ifShared).order_by('dateShared') #need to figure out how to show only friends UserEvents. Will probobly need a many to many relationship with UserProfile and itself to designate who is a friend with whom
        return feed
    elif ifShared == 2:
        feed = UserEvent.objects.filter(ifShared__exact=2).order_by('dateShared')
        # possibly need to filter for completed as well
        return feed
    elif ifShared == 3:
        feed = UserEvent.objects.filter(user_id=pk, ifShared__gte=1).order_by('dateShared')
        return feed

#need to add usercreated events
def getUserEvents(age, gender):
    '''
    Logic that pulls events from AllEvents to UserEvents
    '''
    #convert dateof birth to integer AGE
    if gender == '1':
        timeline = AllEvent.objects.filter(minAge__lte=age, maxAge__gte=age, gender__lte=1)
    elif gender == '2':
        timeline = AllEvent.objects.filter((Q(minAge__lte=age) & Q(maxAge__gte=age)), Q(gender__exact=2) | Q(gender__exact=0))
    elif gender == '0':
        timeline = AllEvent.objects.filter(minAge__lte=age, maxAge__gte=age, gender__exact=0)
    return timeline

    #further filter using keyword tags in all events
    
    #eventually I want to populate UserEvents with all the correct AllEvents and then repopulate everytime a new user signs up or add a new AllMedHistory\
    
def getTimelineEvents(pk):
    '''
    Populates Timeline events
    '''
    return UserEvent.objects.filter(user_id=pk).order_by('allEvent_id__minAge') #will this work???
    # need to incorporate created events

def getFriendInfo(pk):
    '''
    gets viewable friend profile info
    '''
    return User.objects.filter(pk=pk, allUserEvents__CompletedOrSharedInfo__ifShared__gte=1).order_by('allUserEvents__CompletedOrSharedInfo__dateShared')
    



#users = User.objects.all().select_related('profile')




#    http -a shimon_aronhime:wellosity PUT http://127.0.0.1:8000/mainApi/ email=natanaronhime@gmail.com userProfile:='{"gender":'2'}'












