from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import (SignupView, UserProfileUpdateView, DrawNamesView,
                    UserProfileDetailView, ActivateView,
                    RequestActivationEmailView, MassEmailView)

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login',
        kwargs={'template_name': 'user_manager/login.html'}),
    url(r'^logout/$', auth_views.logout, name='logout',
        kwargs={'next_page': '/'}),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^account/$', UserProfileUpdateView.as_view(), name='account'),
    url(r'^activate/(?P<username>[0-9A-Za-z_]+)-(?P<code>[0-9A-Za-z_:-]+)/$',
        ActivateView.as_view(), name='activate-user'),
    url(r'^activate/request/$', RequestActivationEmailView.as_view(),
        name='activate-user'),
    url(r'^draw-names/$', DrawNamesView.as_view(), name='draw-names'),
    url(r'^mass-email/$', MassEmailView.as_view(), name='mass-email'),
    url(r'^@(?P<username>[a-zA-Z0-9_]+)/$', UserProfileDetailView.as_view(),
        name='user-detail'),
]
