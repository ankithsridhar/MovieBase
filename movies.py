import random
import rpyc


# Database of movies
movies = [
    {"title": "the shawshank redemption", "genre": "drama", "rating": 9.3},
    {"title": "the godfather", "genre": "crime", "rating": 9.2},
    {"title": "the dark knight", "genre": "action", "rating": 9.0},
    {"title": "pulp fiction", "genre": "crime", "rating": 8.9},
    {"title": "forrest gump", "genre": "drama", "rating": 8.8},
    {"title": "inception", "genre": "action", "rating": 8.8},
    {"title": "the matrix", "genre": "action", "rating": 8.7},
    {"title": "the lord of the rings: the return of the king", "genre": "adventure", "rating": 8.9},
    {"title": "gladiator", "genre": "action", "rating": 8.5},
    {"title": "the avengers", "genre": "action", "rating": 8.0},
    {"title": "interstellar", "genre": "sci-fi", "rating": 8.6},
    {"title": "schindler's list", "genre": "drama", "rating": 8.9},
    {"title": "oppenhiemer", "genre": "crime", "rating": 8.5},
    {"title": "the godfather: part ii", "genre": "crime", "rating": 9.0},
    {"title": "the lord of the rings: the fellowship of the ring", "genre": "adventure", "rating": 8.8},
    {"title": "saving private ryan", "genre": "drama", "rating": 8.6},
    {"title": "the lion king", "genre": "animation", "rating": 8.5},
    {"title": "get out", "genre": "horror", "rating": 8.8},
    {"title": "the green mile", "genre": "drama", "rating": 8.6},
    {"title": "the dark knight rises", "genre": "action", "rating": 8.4},
    {"title": "the pianist", "genre": "drama", "rating": 8.5},
    {"title": "barbie", "genre": "action", "rating": 8.5},
    {"title": "the prestige", "genre": "drama", "rating": 8.5},
    {"title": "us", "genre": "horror", "rating": 8.3},
    {"title": "the silence of the lambs", "genre": "crime", "rating": 8.6},
    {"title": "avatar", "genre": "sci-fi", "rating": 7.8},
    {"title": "django unchained", "genre": "drama", "rating": 8.4},
    {"title": "the departed", "genre": "crime", "rating": 8.5},
]

# Database of registered users 
users = {}

#function to search the movies
def search_movie():
    search_query = input("Enter the movie title you want to search for (in lowercase): ")
    
    
    if search_query:
        print("Found movies:")
        movie_search = remote_service.search_movie(search_query)
        for info in movie_search:
            print(info)
    else:
        print("No movies found.")


#
def register_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    if username in users:
        print("User already exists.")
    else:
        users[username] = {
            "password": password,
            "rated_movies": {},
            #"recommended_movies": []
        }
        print("Registration successful!")

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

def rate_movie(user):
    while True:
        print("1. Rate a movie")
        print("2. View rated movies")
        print("3. Back to the main screen")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            print("Movies available for rating:")
            for i, movie in enumerate(movies, 1):
                print(f"{i}. {movie['title']} - Genre: {movie['genre']}, Rating: {movie['rating']}")

            movie_index = int(input("Enter the number corresponding to the movie you want to rate: ")) - 1
            if 0 <= movie_index < len(movies):
                rating = float(input("Enter your rating (0.0 to 10.0): "))
                if 0 <= rating <= 10.0:
                    movie_title = movies[movie_index]['title']
                    user["rated_movies"][movie_title] = rating
                    print(f"Thank you! You rated '{movie_title}' as {rating}.")
                else:
                    print("Invalid rating. Please enter a number between 0.0 and 10.0.")
            else:
                print("Invalid movie selection. Please try again.")
        elif choice == "2":
            view_rated_movies(user)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


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

def generate_random_recommendations(user):
    num_recommendations = 3
    unrated_movies = [movie for movie in movies if movie['title'] not in user["rated_movies"]]
    if len(unrated_movies) >= num_recommendations:
        random_recommendations = random.sample(unrated_movies, num_recommendations)
        #user["recommended_movies"] = random_recommendations
        print("Random Movie Recommendations:")
        for movie in random_recommendations:
            print(f"{movie['title']} - Genre: {movie['genre']}, Rating: {movie['rating']}")
    else:
        print("Not enough unrated movies to provide recommendations.")

def view_personalized_recommendations(user):
    movie_name = input ("Enter a movie title so we can give you similar movies: ")
    num_of_recs = int(input ("Enter the number of reccomendations you would like: "))
    user["recommended_movies"] = remote_service.movie_recommendation(movie_name, num_of_recs)
    if user["recommended_movies"]:
        print("Your Personalized Movie Recommendations:")
        for movie in user["recommended_movies"]:
            print(movie)
    else:
        print("You have not received any personalized recommendations yet.")

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
            rate_movie(user)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


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

def main():
    while True:
        print("\nMovieBase!")
        print("1. Search: Just type in a movie and we will give you the genre and rating!")
        print("2. Register/Unregister: You are able to register and log in so you can store your movie experiences!")
        print("3. Rate a movie: Rate any movie so you will have your own rating!")
        print("4. Get random movie recommendations: See what movies you can see next!")
        print("5. View personalized recommendations: See the movies we reccomended you!")
        print("6. Exit")
        
        choice = input("Enter your choice (1/2/3/4/5/6): ")
        
        if choice == "1":
            search_movie()
        elif choice == "2":
            register_or_unregister()
        elif choice == "3":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if username in users and users[username]["password"] == password:
                rate_movie(users[username])
            else:
                print("Invalid username or password.")
        elif choice == "4":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if username in users and users[username]["password"] == password:
                generate_random_recommendations(users[username])
            else:
                print("Invalid username or password.")
        elif choice == "5":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if username in users and users[username]["password"] == password:
                view_personalized_recommendations(users[username])
            else:
                print("Invalid username or password.")
        elif choice == "6":
            print("Exiting the app. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    conn = rpyc.connect("localhost", 11895)
    remote_service = conn.root

    main()
