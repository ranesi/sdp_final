from django.conf.urls import url
from . import views, views_users, views_documents

urlpatterns = [

    url(
        r'^$',
        views.homepage,
        name='homepage'
    ),

    # Document URLs

    url(
        r'^document/all$',
        views_documents.show_documents,
        name='show_entries'
    ),

    url(
        r'^document/(?P<pk>\d+)$',
        views_documents.document_detail,
        name='entry_detail'
    ),

    url(
        r'^document/add/$',
        views_documents.add_document,
        name='add_document'
    ),

    # User URLs

    url(
        r'^register/$',
        views_users.register,
        name='register'
    ),

    url(
        r'^logout_message/$',
        views_users.logout_message,
        name='logout_message'
    ),

    url(
        r'&about/$',
        views.about,
        name='about'
    ),

]
