# Description: Accesses the IMDb API to allow for calls and returns of movies. Will also allow the user to get movie
# recommendations (based on the most current movie releases).

# Install RPyC in order for this to work

import rpyc
from rpyc.utils.server import ThreadedServer
from imdb import Cinemagoer
from random import sample


class MoviesService(rpyc.Service):
    def __init__(self):
        super().__init__()
        self._port = 11895
        self._ia = Cinemagoer()

    def get_port(self):
        """Returns the port number for the server"""
        return self._port

    def on_connect(self, conn):
        """Print to console when someone connects to the server"""
        print("Client has connected to the server")

    def on_disconnect(self, conn):
        """Print to console when someone disconnects to the server"""
        print("Client has disconnected from the server")

    def start_server(self):
        """Starts the server on specified port that the microservice will run on"""
        server = ThreadedServer(self, port=self._port)
        server.start()

    def exposed_movie_methods(self, method_name: str, *args, **kwargs):
        """This should be able to facilitate exposing of all methods inside the Cinemagoer class"""
        try:
            method = getattr(self._ia, method_name)
            return method(*args, **kwargs)
        except AttributeError:
            raise NotImplementedError(f"The method '{method_name}' could not be found.")

    def exposed_search_movie(self, movie_title, mov_num=1):
        """
        Takes a movie title and returns the top result. Can set second argument to False to return a list of movies
        instead of the top search result.
        """
        results = self._ia.search_movie(movie_title)
        if mov_num == 1:
            movie = results[0]
            self._ia.update(movie)
            try:
                genres = ', '.join(movie['genres'])
            except KeyError:
                genres = 'n/a'

            try:
                directors = ', '.join(director['name'] for director in movie['director'])
            except KeyError:
                directors = 'n/a'

            try:
                actors = ', '.join(actor['name'] for actor in movie['cast'])
            except KeyError:
                actors = 'n/a'

            movie_info = [f"Title: {movie['title']}", f"Genres: {genres}",
                          f"Directors: {directors}", f"Cast: {actors}",
                          f"Description: {movie.get('plot outline', 'na')}"]
        else:
            movie = results[0:mov_num]
            movie_info = []
            for mov in movie:
                self._ia.update(mov)
                try:
                    genres = ', '.join(mov['genres'])
                except KeyError:
                    genres = 'n/a'

                try:
                    directors = ', '.join(director['name'] for director in mov['director'])
                except KeyError:
                    directors = 'n/a'

                try:
                    actors = ', '.join(actor['name'] for actor in mov['cast'])
                except KeyError:
                    actors = 'n/a'

                movie_info.append([f"Title: {mov['title']}", f"Genres: {genres}",
                                   f"Directors: {directors}", f"Cast: {actors}",
                                   f"Description: {mov.get('plot outline', 'na')}"])
        return movie_info

    def exposed_movie_recommendation(self, movie_title, amount, genre_to_search=None, query_num=200):
        """Returns a number of movie recommendations based on the movie title given"""
        movie_recs = []

        if genre_to_search is None:
            try:
                movie = self._ia.search_movie(title=movie_title)[0]
            except(IndexError):
                return f"The movie '{movie_title}' couldn't be found in the IMDb database."

            self._ia.update(movie)
            genres = movie.data.get('genres', [])

            genre_to_search = []

            genre_num = 3
            if len(genres) == 0:
                return [f'There was an issue finding recommendations for the movie {movie["title"]}']
            elif genre_num > len(genres):
                genre_num = len(genres)

            for ind in sample(range(len(genres)), genre_num):
                genre_to_search.append(genres[ind])
        else:
            genre_to_search = [genre_to_search]

        recommendations = self._ia._search_movie_advanced(genres=genre_to_search[0], results=query_num)
        search_results = []
        for rec in recommendations:
            if 'rating' in rec[1].keys():
                if rec[1]['rating'] >= 8.0 and rec[1]['kind'] == 'movie':
                    search_results.append(rec[1])

        for ind in sample(range(len(search_results)), amount):
            movie_recs.append(search_results[ind]['title'])
        return movie_recs


if __name__ == "__main__":
    server = MoviesService()
    print(f'Server is listening to port {server.get_port()}')
    server.start_server()