import pandas as pd
from recommend import rating

GENRE = "" #leave "" if no genre needed
YEAR = "2010" #leave "" if no year needed
MOVIE_AMOUNT = 5

def main():
   ratings_d = pd.read_csv("ratingsample.csv")
   movi = pd.read_csv("movie.csv")
   movie_list = rating("mymovie.csv",GENRE,MOVIE_AMOUNT,ratings_d,movi,YEAR)
   return movie_list

print(main())
