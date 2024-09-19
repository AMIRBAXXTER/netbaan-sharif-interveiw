from django.urls import path

from MainApp import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('login-check/', views.LoginCheckView.as_view(), name='login-check'),
    path('books/list/', views.BookListView.as_view(), name='book-list'),
    path('books/', views.BookListByGenreView.as_view(), name='book-list-by-genre'),
    path('reviews/add/', views.AddReviewView.as_view(), name='add-review'),
    path('reviews/update/', views.UpdateReviewView.as_view(), name='update-review'),
    path('reviews/delete/', views.DeleteReviewView.as_view(), name='delete-review'),
    path('suggest/', views.SuggestBookListView.as_view(), name='suggest-book-list'),
]
