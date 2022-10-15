"""Defines URL patterns for learning_logs."""
from unicodedata import name
from django.urls import path
from . import views
app_name = 'learninglog'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    #page that shows all topics.
    path('topic/', views.topics, name='topics'),

    #Detail page for a single topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    #page for adding a new topic by the user
     path('new_topic/', views.new_topic, name='new_topic'),

     #page for the new entry by the user
     path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),

     #page for editting an entry
      path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry',),

    

]