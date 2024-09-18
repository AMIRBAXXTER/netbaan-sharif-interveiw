from rest_framework.authentication import TokenAuthentication
from django.db import connection


class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'


def get_book_list(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT b.*,r.rating FROM books b LEFT JOIN reviews r ON b.id = r.book_id AND r.user_id = {user_id};")
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]


def get_books_list_by_genre(user_id, genre):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT b.*,r.rating FROM books b LEFT JOIN reviews r ON b.id = r.book_id AND r.user_id = {user_id} WHERE b.genre = '{genre}';")
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]


def check_review(book_id, user_id):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM reviews WHERE book_id = {book_id} AND user_id = {user_id};")
        rating = cursor.fetchone()
        if rating:
            return True
        return False


def add_review(user_id, book_id, rating):
    is_rating_exist = check_review(book_id, user_id)
    if not is_rating_exist:
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO reviews (book_id, user_id, rating) VALUES ({book_id}, {user_id}, {rating});")
            return True
    return False


def update_review(user_id, book_id, rating):
    is_rating_exist = check_review(book_id, user_id)
    if is_rating_exist:
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE reviews SET rating = {rating} WHERE book_id = {book_id} AND user_id = {user_id};")
            return True
    return False


def delete_review(user_id, book_id):
    is_rating_exist = check_review(book_id, user_id)
    if is_rating_exist:
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM reviews WHERE book_id = {book_id} AND user_id = {user_id};")
            return True
    return False


def suggest_book_list(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT b.genre,AVG(r.rating) as avg_rating FROM reviews r JOIN books b ON b.id = r.book_id WHERE r.user_id = {user_id} GROUP BY b.genre ORDER BY avg_rating DESC LIMIT 3;")
        rows = cursor.fetchall()
        favorite_genres = tuple(row[0] for row in rows)
        print('*' * 50)
        print(favorite_genres)
        cursor.execute(
            f"SELECT b.*,r.rating FROM books b LEFT JOIN reviews r ON b.id = r.book_id AND r.user_id = {user_id} WHERE b.genre IN {favorite_genres};")
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]
