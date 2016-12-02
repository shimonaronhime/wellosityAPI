from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from mainApi import views
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework import renderers
from rest_framework_nested import routers
from mainApi.views import UserViewSet

schema_view = get_schema_view(title='WellosityAPI')
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

#user_event_detail = views.UserEventDetail.as_view({
#    'get': 'retrieve',
#    'put': 'update',
#    'patch': 'partial_update',
##    'delete': 'destroy',
#})

urlpatterns = [
    url(r'^', include(router.urls)),
#    url(r'^api-token-auth/', views.obtain_auth_token),
    url('^schema/$', schema_view),
    
    url(r'^users/(?P<pk>[0-9]+)/med-history/$', views.AllMedHistoryList.as_view(), name='allmedhistory-list'),
    url(r'^med-history/(?P<pk>[0-9]+)/$', views.AllMedHistoryDetail.as_view(), name='allmedhistory-detail'),
    
    
    url(r'^users/(?P<pk>[0-9]+)/created-events/$', views.CreatedEventList.as_view(), name='created-event-list'),
    url(r'^created-event/(?P<pk>[0-9]+)/$', views.CreatedEventDetail.as_view(), name='created-event-detail'),
    
    
    url(r'^users/(?P<pk>[0-9]+)/private-feed/$', views.PrivateFeed.as_view(), name='user-private-feed'),
    url(r'^users/(?P<pk>[0-9]+)/friend-feed/$', views.FriendFeed.as_view(), name='user-friend-feed'),
    url(r'^users/(?P<pk>[0-9]+)/public-feed/$', views.PublicFeed.as_view(), name='user-public-feed'),
    url(r'^users/(?P<pk>[0-9]+)/friend-profile-feed/$', views.FriendProfileFeed.as_view(), name='user-friend-profile-feed'),
    url(r'^users/(?P<pk>[0-9]+)/timeline/$', views.TimelineEvents.as_view(), name='user-timeline'),
    
    url(r'^user-event/(?P<pk>[0-9]+)/$', views.UserEventDetail.as_view(), name='user-event-detail'),
#    url(r'^user-event/(?P<pk>[0-9]+)/$', user_event_detail, name='user-event-detail'),
    url(r'^allevent/(?P<pk>[0-9]+)/$', views.AllEventDetail.as_view(), name='allevent-detail'),
    url(r'^likes/(?P<pk>[0-9]+)/$', views.LikeList.as_view(), name='like-list'),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.CommentList.as_view(), name='comment-list'),
    
    url(r'^users/(?P<pk>[0-9]+)/friend-list/$', views.FriendList.as_view(), name ='user-friend-list'),
    url(r'^med-history-search/(?P<historyType>[0-9]+)/$', views.AllMedHistorySearchList.as_view()),
    
    
    
     
    
    
    #this is only for practice purposes
    url(r'^UserEvents/(?P<age>[0-9]+)/(?P<gender>[0-9]+)/$', views.UserEvents.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
#{'get':'retrieve','put':'update','delete':'destroy'}
#user_list = UserViewSet.as_view({
#    'get': 'list',
#    'post': 'create'
#})

#
#allmedhistory_list = UserAllMedHistoryViewSet.as_view({
#    'get': 'list',
#    'post': 'create',
#   
#})
