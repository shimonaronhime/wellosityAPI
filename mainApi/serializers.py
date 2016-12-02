from django.contrib.auth.models import User, Group
from rest_framework import serializers
from mainApi.models import UserProfile, AllMedHistory
from mainApi.models import AllEvent, UserEvent, Like, Comment, UserCreatedEvent
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework.serializers import HyperlinkedModelSerializer


class CommentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = Comment
        fields = ('user_id','first_name','last_name','text', 'commentTime')

class LikeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = Like
        fields = ('user_id','first_name','last_name')

class AllEventSerializer(serializers.ModelSerializer):  
    class Meta:
        model = AllEvent
        fields = ('eventType', 'timelineDescription', 'publicFeedDescription', 'personalFeedDescription')

class UserEventSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-event-detail')
#    allEvent = AllEventSerializer(read_only=True, required=False)
    allEvent = serializers.HyperlinkedIdentityField(view_name='allevent-detail')
    eventComments = serializers.HyperlinkedIdentityField(view_name='comment-list')  
    eventLikes = serializers.HyperlinkedIdentityField(view_name='like-list')
    class Meta:
        model = UserEvent
        fields = ('url', 'id', 'allEvent', 'completed','dateCompleted','dateShared', 'ifShared','eventComments', 'eventLikes')

class AllMedHistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AllMedHistory
        fields = ('url', 'id', 'historyType','description')       
   

class UserCreatedEventSerializer(serializers.HyperlinkedModelSerializer):
    #i may want to nest this serializer into UserEvent but then AllEvent will not have to be required
    userEventForCreatedEvent = UserEventSerializer()
    url = serializers.HyperlinkedIdentityField(view_name='created-event-detail')
    class Meta:
        model = UserCreatedEvent
        fields = ('url', 'id', 'eventType', 'withWhom', 'eventDate', 'description', 'userEventForCreatedEvent')
    
    def create(self, validated_data):
        userEventForCreatedEvent_data = validated_data.pop('userEventForCreatedEvent')
        createdEvent = UserCreatedEvent.objects.create(**validated_data)
        UserEvent.objects.create(createdEvent=createdEvent, **userEventForCreatedEvent_data)
        return createdEvent
    
    def update(self, validated_data):
        pass
    

class UserProfileSerializer(serializers.ModelSerializer):  
    friends = serializers.HyperlinkedIdentityField(view_name='user-friend-list') 
    class Meta:
        model = UserProfile
        fields = ('birthDate', 'gender', 'completionPercentage', 'profilePicture', 'friends')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Used when creating or updating a new User/Profile
    '''
    userProfile = UserProfileSerializer()
    allMedHistories = serializers.HyperlinkedIdentityField(view_name='allmedhistory-list')     
    userCreatedEvents = serializers.HyperlinkedIdentityField(view_name='created-event-list')
    timeline = serializers.HyperlinkedIdentityField(view_name='user-timeline')
    privateFeed = serializers.HyperlinkedIdentityField(view_name='user-private-feed')
    friendFeed = serializers.HyperlinkedIdentityField(view_name='user-friend-feed')
    publicFeed = serializers.HyperlinkedIdentityField(view_name='user-public-feed')
    friendProfileFeed = serializers.HyperlinkedIdentityField(view_name='user-friend-profile-feed')
    class Meta:
        model = User
        fields = ('url','id','username', 'first_name', 'last_name', 'email', 'password', 'userProfile', 'allMedHistories', 'userCreatedEvents', 'timeline', 'privateFeed', 'friendFeed', 'publicFeed', 'friendProfileFeed')
        
    def create(self, validated_data):
        userProfile_data = validated_data.pop('userProfile')
        user = User.objects.create(**validated_data)
        UserProfile.objects.create(user=user, **userProfile_data)
        return user
    
    def update(self, instance, validated_data):
        userProfile_data = validated_data.pop('userProfile')
        userProfile = instance.userProfile

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        #need to add profilePicture
        userProfile.birthDate = userProfile_data.get('birthDate', userProfile.birthDate)
        userProfile.gender = userProfile_data.get('gender', userProfile.gender)
        userProfile.save()

        return instance


class FriendListSerializer(serializers.ModelSerializer):
    friends = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='user-detail')
    class Meta:
        model = UserProfile
        fields = ('friends',)
    

    
    
        
class buildOutUserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllEvent
        fields = ('id', 'name', 'eventType', 'gender','timelineDescription', 'publicFeedDescription', 'personalFeedDescription')



#class PrivateField(serializers.Field):
#    def get_attribute(self, obj):
#        # We pass the object instance onto `to_representation`,
#        # not just the field attribute.
#        return obj
#
#    def to_representation(self, obj):
#        # for read functionality
#        if obj.created_by != self.context['request'].user:
#            return ""
#        else:
#            return obj.private_field1
#
#    def to_internal_value(self, data):
#        pass
        # for write functionality
        # check if data is valid and if not raise ValidationError
    
        

        
        
        
        

