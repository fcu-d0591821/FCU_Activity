from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index),
    path('signup', views.UserCreate.as_view(), name='signup'),
    path('activity', views.activity_list),
    path('activity/create', views.activity_create),
    path('activity/<aid>', views.activity_detail),
    path('activity/<aid>/delete', views.activity_delete),
    path('activity/<aid>/modify', views.activity_edit),
    path('getActivity', views.get_activity),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
