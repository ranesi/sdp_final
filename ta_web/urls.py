from django.conf.urls import url
from . import views, user_views, document_views

urlpatterns = [

    url(
        r'^$',
        views.homepage,
        name='homepage'
    ),

    # Document URLs

    url(
        r'^document/all$',
        document_views.show_documents,
        name='show_entries'
    ),

    url(
        r'^document/(?P<pk>\d+)$',
        document_views.document_detail,
        name='entry_detail'
    ),

    url(
        r'^document/add/$',
        document_views.add_document,
        name='add_document'
    ),

    # User URLs

    url(
        r'^register/$',
        user_views.register,
        name='register'
    ),

    url(
        r'^logout_message/$',
        user_views.logout_message,
        name='logout_message'
    ),

    url(
        r'&about/$',
        views.about,
        name='about'
    ),

]
