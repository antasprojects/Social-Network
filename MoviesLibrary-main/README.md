# MoviesLibrary
Movies Library is a dynamic web application where users can register, search for movies, rate them and create personalised rankings. 
This application uses IMBD API to request movie information and SQL database to store user data. 
The back end of the project was handled by Python and Flask framework. 
The database was built and managed using SQLite3 and the front end was completed using HTML, CSS and Bootstrap.


To use Movies Library, users need to create an account. The username is stored in the database, 
and during registration, the system checks for username uniqueness. For security reasons, 
passwords are hashed before being sent to the database. Subsequently, users can log in to the app using their credentials.


Upon logging in, users can conveniently search for movies through the search bar. 
The app sends a request to the IMDB API, retrieving a list of movies that match the entered phrase. 
The search results include the movie's image, title, and main actors. Users can then add a movie to their 
watchlist if they plan to watch it in the future or mark it as watched if they've already seen it. 
These choices are recorded in the database and associated with the user's ID.


On the "To watch" page, users can view movies added through the search function. 
If a user has watched a movie, they can transfer it to the "Watched" list to provide a rating.

In the "Watched" section, users can rate the movies they've watched on a scale from 1 to 5 stars. 
In the event of an error, users also have the option to delete movies from this list.

The final page, "Ranking," displays all movies previously rated by the user, 
arranged in descending order based on their ratings. Users can edit their rankings by deleting movies if necessary. 
Movies Library aims to offer a straightforward and user-friendly experience, 
combining registration security, real-time movie data retrieval, and personalized movie management.


