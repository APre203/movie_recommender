# movie_recommender
This project recommends movies to a user based on the user's watched movies. The project utilizes Matrix Singular Value Decomposition to guess movies that the user would like based on the movies that they watched and a rating matrix.

What you need to use this:
1. Install dataset "movie.csv" and "rating.csv" from "https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset"

2. Upload your watched movies to the "mymovie.csv" file

3. Change these variables to change the movies returned:
      
      1. GENRE - Change genre to specify which movies will be produced - Leave as "" if no genre needed
      
      2. YEAR - Change year if you want the movies to be produced during and after the YEAR variable - Leave as "" if no genre needed
      
      3. MOVIE_AMOUNT - Change movie amount to produce more recommended movies
      
      4. N (in data.py) - Change N to import more user ratings - The more user ratings the better the results and the slower the algorithm runs
      
