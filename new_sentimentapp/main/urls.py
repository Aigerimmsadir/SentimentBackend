from django.urls import path
from main.views import *
urlpatterns = [
    path('comments/', CommentList.as_view()),

]