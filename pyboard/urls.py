"""py_board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from board import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('login_form/', views.login_form),
    path('login/',views.login),
    path('signup_form/',views.signup_form),
    path('signup/',views.signup),
    path('logout/',views.logout),
    
    path('',views.home),
    path('movie_save/',views.movie_save),
    path('chart/',views.chart),
    path('wordcloud/',views.wordcloud),
    path('cctv_map/', views.cctv_map),
    
    path('list/',views.list),
    path('write/', views.write),
    path('insert/', views.insert),
    path('download/', views.download),
    path('detail/',views.detail),
    path('update/',views.update),
    path('delete/', views.delete),
    path('reply_insert/',views.reply_insert),
]




