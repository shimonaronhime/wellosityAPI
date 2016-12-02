from django.shortcuts import render
#from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, filters, authentication, permissions
from mainApi.serializers import UserSerializer, UserProfileSerializer, AllMedHistorySerializer
from mainApi.serializers import FriendListSerializer, UserCreatedEventSerializer, LikeSerializer
from mainApi.serializers import UserEventSerializer, AllEventSerializer, CommentSerializer, buildOutUserEventSerializer
from mainApi.models import UserProfile, AllMedHistory
from mainApi.models import AllEvent, UserEvent, Like, Comment, UserCreatedEvent
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from mainApi.permissions import IsOwner, IsAdminOrSelf
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view
from django.http import Http404
from mainApi.app_logic import getAllMedHistoryList, getFeedEvents, getTimelineEvents, getUserEvents, getFriendInfo
from rest_framework.decorators import detail_route, list_route


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions. 
    
    permissions: list(aut), retrieve(admin or self), post(auth), put/patch(admin or self)
    """
    queryset = User.objects.order_by('id')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrSelf,) #IsAdminOrSelf doesnt currently work   
#   people shouldnt be able to update other users

class AllMedHistorySearchList(APIView):
    '''
    Return a list of AllMedHistories for search purposes. Current issues, medications, family history or allergies. 
    
    permissions: auth or admin
    '''
    def get(self, request, historyType, format=None):
        querySet = getAllMedHistoryList(historyType)
        serializer = AllMedHistorySerializer(querySet, many=True)
        return Response(serializer.data)


class AllMedHistoryList(generics.ListCreateAPIView):
    '''
    List user's medical history 
    
    permissions: admin or self
    '''
    serializer_class = AllMedHistorySerializer
    permission_classes = (IsAdminUser,)
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        q = User.objects.get(id=pk)
        return q.allMedHistories.all() 

class AllMedHistoryDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Details for each medical history 
    
    permissions: admin or self
    '''
#do not need update here
    
    serializer_class = AllMedHistorySerializer
    permission_classes = (IsAdminUser,)
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        q = User.objects.get(allMedHistories__id__exact=pk)
        return q.allMedHistories.get(id=pk)
        
    def retrieve(self, request, pk=None):
        q = User.objects.get(allMedHistories__id__exact=pk)
        queryset = q.allMedHistories.get(id=pk)
        serializer = AllMedHistorySerializer(queryset, context={'request': request})
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        q = User.objects.get(allMedHistories__id__exact=pk)
        queryset = q.allMedHistories.get(id=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class CreatedEventList(generics.ListCreateAPIView):
    #post doesnt work (cant create with nested serializer)
    '''
    List user's created event..
    create DOESNT WORK
    
    permissions: admin or self
    '''
    serializer_class = UserCreatedEventSerializer
    permission_classes = (IsAdminUser,)
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        q = User.objects.get(id=pk)
        return q.userCreatedEvents.all() 

class CreatedEventDetail(generics.RetrieveUpdateDestroyAPIView):
    #updating not working
    '''
    Details for each created event
    UPDATE DOESNT WORK
    
    permissions: admin or self
    '''

    serializer_class = UserCreatedEventSerializer
    permission_classes = (IsAdminUser,)
    
#    def get_queryset(self):
#        pk = self.kwargs['pk']
#        q = User.objects.get(userCreatedEvents__id__exact=pk)
#        return q.userCreatedEvents.get(id=pk)
        
    def retrieve(self, request, pk=None):
        q = User.objects.get(userCreatedEvents__id__exact=pk)
        queryset = q.userCreatedEvents.get(id=pk)
        serializer = UserCreatedEventSerializer(queryset, context={'request': request})
        return Response(serializer.data)
    
    def partial_update(self, request, pk=None):
        q = User.objects.get(userCreatedEvents__id__exact=pk)
        queryset = q.userCreatedEvents.get(id=pk)
        serializer = UserCreatedEventSerializer(data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        q = User.objects.get(userCreatedEvents__id__exact=pk)
        queryset = q.userCreatedEvents.get(id=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PrivateFeed(APIView):
    '''
    permissions: admin or self
    '''
    def get(self, request, pk, format=None):
        querySet = getFeedEvents(pk, 0)
        serializer = UserEventSerializer(querySet, many=True, context={'request': request})
        return Response(serializer.data)
    
class FriendFeed(APIView):
    '''
    permissions: admin, self
    '''
    def get(self, request, pk, format=None):
        querySet = getFeedEvents(pk, 1)
        serializer = UserEventSerializer(querySet, many=True, context={'request': request})
        return Response(serializer.data)
    
class PublicFeed(APIView):
    '''
    permissions: auth
    '''
    def get(self, request, pk, format=None):
        querySet = getFeedEvents(pk, 2)
        serializer = UserEventSerializer(querySet, many=True, context={'request': request})
        return Response(serializer.data)
    
class FriendProfileFeed(APIView):
    '''
    permissions: admin, self or FRIEND
    '''
    #need to make sure you can only access the view if you are friends with the person
    def get(self, request, pk, format=None):
        querySet = getFeedEvents(pk, 3)
        serializer = UserEventSerializer(querySet, many=True, context={'request': request})
        return Response(serializer.data)
    
class TimelineEvents(APIView):
    '''
    Return a list of timeline events for each user
    
    permissions: admin or self
    '''
    def get(self, request, pk, format=None):
        querySet = getTimelineEvents(pk)
        serializer = UserEventSerializer(querySet, many=True, context={'request': request})
        return Response(serializer.data)


class UserEventDetail(generics.RetrieveUpdateDestroyAPIView):
#class UserEventDetail(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,                      viewsets.GenericViewSet):
#class UserEventDetail(viewsets.ViewSet):
    '''
    Updates UserEvent
    
    permissions: admin or self
    '''
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        q = User.objects.get(eventsOfUser__id__exact=pk)
        return q.eventsOfUser.get(id=pk)
    
    serializer_class = UserEventSerializer
    permission_classes = (IsAdminUser,) 
    
    
    

    def retrieve(self, request, pk=None):
        q = User.objects.get(eventsOfUser__id__exact=pk)
        queryset = q.eventsOfUser.get(id=pk)
        serializer = UserEventSerializer(queryset, context={'request': request})
        return Response(serializer.data)
        
    def update(self, request, pk=None):
        q = User.objects.get(eventsOfUser__id__exact=pk)
        queryset = q.eventsOfUser.get(id=pk)
        serializer = UserEventSerializer(data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#    
#    def partial_update(self, request, pk=None):
#        q = User.objects.get(eventsOfUser__id__exact=pk)
#        queryset = q.eventsOfUser.get(id=pk)
#        serializer = UserEventSerializer(data=request.data, context={'request': request}, partial=True)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        
class AllEventDetail(APIView):
    '''
    Return a list of timeline events for each user
    
    permissions: admin or self
    '''
    def get(self, request, pk, format=None):
        q = UserEvent.objects.get(id=pk)
        querySet = q.allEvent
        serializer = AllEventSerializer(querySet, context={'request': request})
        return Response(serializer.data)

class LikeList(generics.ListCreateAPIView):
    '''
    Lists likes for each user event. may need delete functionality
    
    permission
    '''
    serializer_class = LikeSerializer
    permission_classes = (IsAdminUser,)
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Like.objects.filter(userEvent_id__exact=pk)

class CommentList(generics.ListCreateAPIView):
    '''
    lists comments for each user event. may need delete functionality.
    '''
    serializer_class = CommentSerializer
    permission_classes = (IsAdminUser,)
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comment.objects.filter(userEvents_id__exact=pk)

class FriendList(APIView):
    '''
    Returns list of friends
    
    permissions: admin or self
    '''
    def get(self, request, pk, format=None):
        querySet = UserProfile.objects.get(user_id=pk)
        serializer = FriendListSerializer(querySet, context={'request': request})
        return Response(serializer.data)
    

    
    
    
    
    
    

    
#practice   
class UserEvents(APIView):
    '''
    Used to generate timeline events from user inputted data
    '''
    def get(self, request, age, gender, format=None):
        querySet = getUserEvents(age, gender)
        serializer = buildOutUserEventSerializer(querySet, many=True)
        return Response(serializer.data) 
    
    
    
    
    
    