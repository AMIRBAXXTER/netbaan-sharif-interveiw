from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from MainApp.serializers import LoginSerializer
from MainApp.models import Users
from MainApp.utils import *


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            sv = serializer.validated_data
            user = authenticate(username=sv['username'], password=sv['password'])
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginCheckView(APIView):

    def get(self, request: Request):
        user = request.user
        return Response({'message': f'You are logged in : {user.username}'}, status=status.HTTP_200_OK)


class BookListView(APIView):

    def get(self, request: Request):
        books = get_book_list(request.user.id)
        return Response(books, status=status.HTTP_200_OK)


class BookListByGenreView(APIView):

    def get(self, request: Request):
        genre = request.query_params.get('genre')
        if genre:
            books = get_books_list_by_genre(request.user.id, genre)
            if books:
                return Response(books, status=status.HTTP_200_OK)
            return Response({'message': 'No books found for this genre'}, status=status.HTTP_200_OK)
        return Response({'message': 'No genre provided'}, status=status.HTTP_200_OK)


class AddReviewView(APIView):

    def post(self, request: Request):
        book_id = request.data.get('book_id')
        rating = request.data.get('rating')
        rating = validate_rating(rating)
        if book_id and rating:
            is_added = add_review(request.user.id, book_id, rating)
            if is_added:
                return Response({'message': 'Review added successfully'}, status=status.HTTP_200_OK)
            return Response({'message': 'you have already added a review for this book'}, status=status.HTTP_200_OK)
        return Response({'message': 'No book_id or rating provided or rating is not valid'}, status=status.HTTP_200_OK)


class UpdateReviewView(APIView):

    def post(self, request: Request):
        book_id = request.data.get('book_id')
        rating = request.data.get('rating')
        rating = validate_rating(rating)
        if book_id and rating:
            is_updated = update_review(request.user.id, book_id, rating)
            if not is_updated:
                return Response({'message': 'you have not added a review for this book'}, status=status.HTTP_200_OK)
            return Response({'message': 'Review updated successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'No book_id or rating provided or rating is not valid'}, status=status.HTTP_200_OK)


class DeleteReviewView(APIView):

    def post(self, request: Request):
        book_id = request.data.get('book_id')
        if book_id:
            is_deleted = delete_review(request.user.id, book_id)
            if is_deleted:
                return Response({'message': 'Review deleted successfully'}, status=status.HTTP_200_OK)
            return Response({'message': 'you have not added a review for this book'}, status=status.HTTP_200_OK)
        return Response({'message': 'No book_id provided'}, status=status.HTTP_200_OK)


class SuggestBookListView(APIView):

    def get(self, request: Request):
        books = suggest_book_list(request.user.id)
        if books:
            return Response(books, status=status.HTTP_200_OK)
        return Response({'message': 'there is not enough data to about you'}, status=status.HTTP_200_OK)
