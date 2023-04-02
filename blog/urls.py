from django.urls import path
from . import views

app_name = "blog"


urlpatterns = [
    path('', views.post_lists, name='post_list'),
    path('tag/<slug:tag_slug>/',views.post_lists,name='post_list_by_tag'),
    #path('',views.PostListView.as_view(), name='post_list'),
    path('<int:month>/<int:day>/<int:year>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share,name='post_share'),
    path('<int:post_id>/comment',views.post_comment,name='post_comment'),
    path('postSearcher/',views.post_search),    
    
]