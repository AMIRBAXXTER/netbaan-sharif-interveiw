from rest_framework.authentication import TokenAuthentication
from django.db import connection
from rest_framework.exceptions import ValidationError


class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'


def validate_rating(rating):
    print(0 < int(rating) < 5)
    if 0 < int(rating) <= 5:
        return rating
    return None


def get_book_list(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT b.*,r.rating FROM books b LEFT JOIN reviews r ON b.id = r.book_id AND r.user_id = %s;", [user_id])
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]


def get_books_list_by_genre(user_id, genre):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT b.*,r.rating FROM books b LEFT JOIN reviews r ON b.id = r.book_id AND r.user_id = %s WHERE b.genre = %s;",
            [user_id, genre])
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]


def check_review(book_id, user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM reviews WHERE book_id = %s AND user_id = %s;", [book_id, user_id])
        rating = cursor.fetchone()
        if rating:
            return True
        return False


def add_review(user_id, book_id, rating):
    is_rating_exist = check_review(book_id, user_id)
    if not is_rating_exist:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO reviews (book_id, user_id, rating) VALUES (%s, %s, %s);",
                           [book_id, user_id, rating]);
            return True
    return False


def update_review(user_id, book_id, rating):
    is_rating_exist = check_review(book_id, user_id)
    if is_rating_exist:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE reviews SET rating = %s WHERE book_id = %s AND user_id = %s;",
                           [rating, book_id, user_id])
            return True
    return False


def delete_review(user_id, book_id):
    is_rating_exist = check_review(book_id, user_id)
    if is_rating_exist:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM reviews WHERE book_id = %s AND user_id = %s;", [book_id, user_id])
            return True
    return False


def suggest_book_list(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT b.genre,AVG(r.rating) as avg_rating FROM reviews r JOIN books b ON b.id = r.book_id WHERE r.user_id = %s GROUP BY b.genre ORDER BY avg_rating DESC LIMIT 3;",
            [user_id])
        rows = cursor.fetchone()
        favorite_genre = rows[0] if rows else None
        cursor.execute(
            f"SELECT b.*,r.rating FROM books b LEFT JOIN reviews r ON b.id = r.book_id AND r.user_id = {user_id} WHERE b.genre = %s;",
            [favorite_genre])
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]
