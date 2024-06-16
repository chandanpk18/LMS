from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout,name='signout'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('add-book/', views.add_book, name='add_book'),
    path('issue-book/<int:book_id>/', views.issue_book, name='issue_book'),
    path('return-book/<int:issued_book_id>/', views.return_book, name='return_book'),
    path('search/', views.search_books, name='search_books'),
]
