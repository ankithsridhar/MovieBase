# AUTHOR: ANKITH SRIDHAR
# PROGRAM: MOVIES.PY
# DESCRIPTION: This program serves as a simple database for movies where the users can  search,
# receive recommendations, and
# personalize their experience with logins

import random
import rpyc

# Database of registered users
users = {}


# Function to display personalized movie recommendations for a user
def view_personalized_recommendations(user):
    # Check if the user has rated any movies
    if not user['rated_movies']:
        print('Rate some movies first!')
        return

    # Find the highest rated movie
    highest_rating = 0
    highest_rated_movie = ''
    output = []
    for movie in user['rated_movies']:
        if user['rated_movies'][movie] >= highest_rating:
            highest_rated_movie = movie
            highest_rating = user['rated_movies'][movie]
        if user['rated_movies'][movie] >= 8.0:
            output.append(movie)

    # If there are no highly rated movies, use the highest rated movie
    if not output:
        output.append(highest_rated_movie)

    # Select a random movie from the high-rated ones
    rand_movie = output[random.sample(range(len(output)), 1)[0]]
    num_of_recs = int(input("Enter the number of recommendations you would like: "))
    user["recommended_movies"] = remote_service.movie_recommendation(rand_movie, num_of_recs)
    if user["recommended_movies"]:
        print(f"Your Personalized Movie Recommendations based on {rand_movie}: ")
        for movie in user["recommended_movies"]:
            print(movie)
    else:
        print("You have not received any personalized recommendations yet.")


# Function to call personalized movie recommendations
def view_personalized_recommendations_call():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in users and users[username]["password"] == password:
        view_personalized_recommendations(users[username])
    else:
        print("Invalid username or password.")


# Function to get random movie recommendations by genre
def random_recs_by_genre():
    num_recs = int(input("How many random movie recommendations do you want?: "))
    genre = input("What genre would you like recommendations in?: ")
    movie_recs = remote_service.movie_recommendation('', num_recs, genre)
    for movie_rec in movie_recs:
        print(f"{movie_rec}\n")


# Function to call random movie recommendations by genre
def random_recs_by_genre_call():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in users and users[username]["password"] == password:
        random_recs_by_genre()
    else:
        print("Invalid username or password.")


# Function to remove a rating for a movie
def remove_rating(user):
    if user["rated_movies"]:
        print("Your Rated Movies:")
        for movie_title, rating in user["rated_movies"].items():
            print(f"{movie_title} - Your Rating: {rating}")

        movie_title = input("Enter the movie title to remove your rating: ")
        if movie_title in user["rated_movies"]:
            del user["rated_movies"][movie_title]
            print(f"Your rating for '{movie_title}' has been removed.")
        else:
            print("You haven't rated this movie.")
    else:
        print("You have not rated any movies yet.")


# Function to view rated movies and perform related actions
def view_rated_movies(user):
    while True:
        if user["rated_movies"]:
            print("Your Rated Movies:")
            for movie_title, rating in user["rated_movies"].items():
                print(f"{movie_title} - Your Rating: {rating}")
        else:
            print("You have not rated any movies yet.")

        print("\nOptions:")
        print("1. Remove a rating")
        print("2. Add a rating")
        print("3. Back to rating screen")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            remove_rating(user)
        elif choice == "2":
            rate_movie_ui(user)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


# Function to rate a movie interactively
def rate_movie_ui(user):
    while True:
        print("1. Rate a movie")
        print("2. View rated movies")
        print("3. Back to the main screen")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            found_movie = False
            while not found_movie:
                movie_name = input("Enter the name of the movie you want to rate: ")
                movie_search = remote_service.search_movie(movie_name, 5)
                response = input(
                    f"Confirm that this is the correct movie (enter the movie number, or n if result isn't here)\n"
                    f"Optionally, enter '0' to exit.\n"
                    f"1. {movie_search[0][0][7:]}\n"
                    f"2. {movie_search[1][0][7:]}\n"
                    f"3. {movie_search[2][0][7:]}\n"
                    f"4. {movie_search[3][0][7:]}\n"
                    f"5. {movie_search[4][0][7:]}\n"
                    f">> ")
                if response == '0':
                    break
                if response != 'n':
                    found_movie = True
                    movie_name = movie_search[int(response) - 1][0][7:]
                    movie_rating = float(input("Give the movie a rating between 0.0 - 10.0\n>> "))
                    user['rated_movies'][movie_name] = movie_rating
                else:
                    print("Sorry we couldn't find it. Try being more specific in your movie title.")
        elif choice == "2":
            view_rated_movies(user)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


# Function to call rating movie UI
def rate_call():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in users and users[username]["password"] == password:
        rate_movie_ui(users[username])
    else:
        print("Invalid username or password.")


# Function to unregister a user
def unregister_user():
    if not users:
        print("There are no registered usernames. Please make sure to register first.")
    else:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username in users and users[username]["password"] == password:
            del users[username]
            print("Account deleted successfully.")
        else:
            print("Invalid username or password.")


# Function to register a user
def register_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in users:
        print("User already exists.")
    else:
        users[username] = {
            "password": password,
            "rated_movies": {},
        }
        print("Registration successful!")


def register_or_unregister():
    while True:
        print("\nRegister/Unregister")
        print("1. Register")
        print("2. Unregister")
        print("3. Back to main screen")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            register_user()
        elif choice == "2":
            unregister_user()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


# function to search the movies
def search_movie():
    search_query = input("Enter the movie title you want to search for: ")
    movie_search = remote_service.search_movie(search_query, 5)
    response = input(
        f"Confirm that this is the correct movie (enter the movie number, or n if result isn't here)\n"
        f"Optionally, enter '0' to exit.\n"
        f"1. {movie_search[0][0]}\n"
        f"2. {movie_search[1][0]}\n"
        f"3. {movie_search[2][0]}\n"
        f"4. {movie_search[3][0]}\n"
        f"5. {movie_search[4][0]}\n"
        f">> ")
    if response == '0':
        return
    if response != 'n':
        for info in movie_search[int(response)-1]:
            print(info)
            print()
    else:
        print("Sorry we couldn't find it. Try being more specific in your movie title.")


# Function to display the main menu and get user's choice
def display_menu():
    print("\nMovieBase!")
    print("1. Search: Just type in a movie and we will give you the genre and rating!")
    print("2. Register/Unregister: You are able to register and log in so you can store your movie experiences!")
    print("3. Rate a movie: Rate any movie so you will have your own rating!")
    print("4. Get random movie recommendations by genre: See what movies you can see next based on a genre!")
    print("5. View personalized recommendations: See the movies we recommended you!")
    print("6. Exit")

    choice = input("Enter your choice (1/2/3/4/5/6): ")
    return choice


def main():
    while True:

        choice = display_menu()

        if choice == "1":
            search_movie()
        elif choice == "2":
            register_or_unregister()
        elif choice == "3":
            rate_call()
        elif choice == "4":
            random_recs_by_genre_call()
        elif choice == "5":
            view_personalized_recommendations_call()
        elif choice == "6":
            print("Exiting the app. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    conn = rpyc.connect("localhost", 11895)
    remote_service = conn.root

    main()
