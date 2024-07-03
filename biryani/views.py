# views.py
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection


def main_page(request):
    # Retrieve the top 10 reviews with the highest ratings
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_name, review_text, rating FROM reviews ORDER BY rating DESC LIMIT 10")
        reviews = cursor.fetchall()

    # Add any other logic here
    user_email = request.session.get('user_email', None)  # Retrieve user_email from session
    return render(request, 'main_page.html', {'user_email': user_email, 'reviews': reviews})



def sign_up(request):
    if request.method == 'POST':
        name = request.POST.get('signup-name')
        email = request.POST.get('signup-email')
        password = request.POST.get('signup-password')

        # Execute raw SQL query to insert data into the signin table
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO signin (name,email, password) VALUES ( %s, %s, %s)", [name ,email, password])

        # Optionally, you can commit the transaction if you're not using autocommit
        # connection.commit()

        # Add a success message
        messages.success(request, 'Sign up successful!')

        # Redirect back to the main page or any other page you prefer
        return redirect('main_page')
    else:
        return render(request, 'main_page.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the provided credentials exist in the database
        with connection.cursor() as cursor:
            cursor.execute("SELECT email FROM signin WHERE email = %s AND password = %s", [email, password])
            user_row = cursor.fetchone()

        if user_row is not None:
            # If the email and password combination exists in the database, proceed with login
            user_email = user_row[0]

            # Store user's email in session
            request.session['user_email'] = user_email

            messages.success(request, 'Logged in successfully!')
            return redirect('main_page')
        else:
            # If no matching user found, display an error message
            messages.error(request, 'Invalid email or password')
            return redirect('main_page')
    else:
        return redirect('main_page')

def logout(request):
    # Delete user's session
    request.session.flush()
    # Redirect to the main page or any other page after logout
    return redirect('main_page')


def submit_review(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        if user_email:
            # Fetch the name associated with the user's email
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM signin WHERE email = %s", [user_email])
                row = cursor.fetchone()
                if row:
                    user_name = row[0]
                    print("User Name:", user_name)  # Debug print
                    review_text = request.POST.get('review')
                    rating = request.POST.get('rating')

                    # Execute raw SQL query to insert data into the reviews table
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO reviews (user_name, review_text, rating) VALUES (%s, %s, %s)",
                                       [user_name, review_text, rating])

                    # Optionally, you can commit the transaction if you're not using autocommit
                    # connection.commit()

                    # Add a success message
                    messages.success(request, 'Review submitted successfully!')

                    # Redirect to a page showing all reviews or wherever you want
                    return redirect('main_page')
                else:
                    messages.error(request, 'No name found associated with the email.')
        else:
            messages.error(request, 'You need to be logged in to submit a review.')
    return redirect('main_page')


def retrieve_reviews(request):
    # Fetch reviews from the database
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_name, review_text, rating FROM reviews")
        reviews = cursor.fetchall()

    # Assuming the maximum rating is 5
    max_rating = 5

    # Construct a list of dictionaries containing review data
    review_data = []
    for review in reviews:
        review_dict = {
            'user_name': review[0],
            'review_text': review[1],
            'rating': review[2]
        }
        review_data.append(review_dict)

    return JsonResponse({'reviews': review_data, 'max_rating': max_rating})




