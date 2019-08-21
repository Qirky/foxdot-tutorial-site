from django.urls import path

from . import views

# Add app_name for namespacing multuple apps urlpatterns

app_name = 'tutorials' # {% url 'detail' %} becomes {% url 'tutorials:detail' %}

urlpatterns = [
    # i.e. /tutorials/
    path('', views.IndexView.as_view(), name='index'), # Map the root the index http-response
    
    # Can be called in the {% url <name> %} template tag! Use for changing details to specifics etc but keeps the mapping

    path('<int:pk>/', views.DetailView.as_view(), name='detail'), # specify the primary key argument
    path('<int:tutorial_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/thanks/', views.ThanksView.as_view(), name='thanks'),
    path('<int:pk>/comments/', views.CommentsView.as_view(), name='comments')
]