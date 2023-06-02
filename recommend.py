from sklearn.decomposition import TruncatedSVD
import pandas as pd
import csv
from data import clean, get_movie
import re

def get_year(string):
   mov_re = re.sub("[^a-zA-Z0-9 ,]", "", string)
   year = mov_re[len(mov_re) - 4:]
   return year

def id_to_movie(movie_id, movie):
   try:
      mov = movie.loc[movie["movieId"] == movie_id, "title"].values[0]
      year = get_year(mov)
      mov = clean(mov) + " (" + year + ")" 
      return mov
   except:
      # print(f"No movie found for {movie_id}")
      return -1

def movie_to_id(title, movie):
   try:
      retval = movie.loc[movie["title"].apply(clean) == clean(title), "movieId"].values[0] 
      return retval
   except:  
      # print(f"No id found for {title}")
      return -1

def user_db(filename, movie): #creates a row for the user's movies and finds their movie id's in the movie.csv file
   rating = []
   title_id = []
   with open(filename, "r") as f:
      reader = csv.reader(f)
      for lines in reader:
         if lines[0] == "title":
            pass
         else:
            dic = get_movie(lines[0],"")
            if dic == []:
               pass
            else:
               title = dic[0]["title"] + " (" + dic[0]["year"] + ")"

               id = movie_to_id(title, movie)
               if id == -1:
                  pass
               else:
                  title_id.append(id)
                  rating.append(lines[1])
   
   userId = [0]
   
   data = {col: rating for col, rating in zip(title_id, rating)}
   u_matrix = pd.DataFrame(data, index=userId)

   return u_matrix

def rating(filename, genre, topN, ratings_df, movie, year):
   user_id = 0
   svd = TruncatedSVD(n_components=35)
   
   u_matrix = user_db(filename, movie)

   ratings_matrix = ratings_df.pivot(index= "userId", columns= "movieId", values="rating")
   ratings_matrix = pd.concat([u_matrix, ratings_matrix])

   ratings_matrix = ratings_matrix.apply(pd.to_numeric, errors="coerce")
   ratings_matrix = ratings_matrix[sorted(ratings_matrix.columns)]
   ratings_matrix = ratings_matrix.fillna(ratings_matrix.mean())
   
   U = svd.fit_transform(ratings_matrix)
   V = svd.components_
   movie_list = []

   for index in movie.T:

      movie_id = int(movie["movieId"][index])
      if movie_id in ratings_matrix.columns:
         col_idx = ratings_matrix.columns.get_loc(movie_id)
         if genre != "" or year != "" :
            try:
               if genre != "" and year == "":
                  if genre in movie["genres"][index].split("|"):
                     movie_list.append([movie_id, U[user_id] @ V[:, col_idx], id_to_movie(movie_id, movie)])
               elif year != "" and genre == "":
                  
                  title = movie["title"][index]
                  y = get_year(title)
                  if int(y) >= int(year):
                     movie_list.append([movie_id, U[user_id] @ V[:, col_idx], id_to_movie(movie_id, movie)])
               else:
                  title = movie["title"][index]
                  y = get_year(title)
                  if genre in movie["genres"][index].split("|") and int(y) >= int(year):
                     movie_list.append([movie_id, U[user_id] @ V[:, col_idx], id_to_movie(movie_id, movie)])
            except:
               pass
         else:
            movie_list.append([movie_id, U[user_id] @ V[:, col_idx], id_to_movie(movie_id, movie)]) 
   movie_list.sort(key = lambda x: x[1])
   return movie_list[len(movie_list)-topN:]
