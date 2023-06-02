import requests
import json
import csv
import re
from unidecode import unidecode

N = 50000 #number of users to base the movies on (the more users the better the results would be)

def translate_csv(filename,n):
  with open("rating.csv", "r") as f:
    reader = csv.reader(f)
    with open(filename, "w", newline= "") as file:
      writer = csv.writer(file)
      for lines in reader:
        if lines[0] == "userId" or int(lines[0]) < n:
          writer.writerow(lines)
  file.close()
  f.close()
# translate_csv("rating.csv",N)



def get_movie(movie_name, year):  #returns movie id from the name

  include_adult = "false"
  url = f'https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult={include_adult}&language=en-US&page=1&year=' + str(year)

  headers = {
    "accept":
    "application/json",
    "Authorization":
    "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZjZiYzYxMDZlZTE5NzU5MjBhOTQ1MjVlZTM0OTI4MCIsInN1YiI6IjY0NmQyYmMwNTRhMDk4MDE3MjhiYTk3YSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.qKxT93gXNgcML9qOqhG1Di5Hn7dDvx4d4R4oKNAhzec"
  }


  response = requests.get(url, headers=headers)
  response = response.text
  
  response = json.loads(response)
  retval = []
  if len(response["results"]) == 0:
      url = f'https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult={include_adult}&language=en-US&page=1&year=""' 
      response = requests.get(url, headers=headers)
      response = response.text
  
      response = json.loads(response)
      if len(response["results"]) == 0:
        return []
  
  for r in response["results"]:
    dic = {}
    dic["year"] = r["release_date"][:4]
    dic["title"] = r["title"]
    dic["id"] = r["id"]
    dic["genre"] = r["genre_ids"]
    dic["popularity"] = r["popularity"]
    dic["vote_average"] = r["vote_average"]
    # dic["overview"] = r["overview"]
    retval.append(dic)
  if len(retval) != 1:
    # print("More than 1 movie found, please include year or full title, or choose from the found movies below:")
    return retval
  return retval

def get_actors(movie_id):  #returns list of actors from a movie

  url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US'

  headers = {
    "accept":
    "application/json",
    "Authorization":
    "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZjZiYzYxMDZlZTE5NzU5MjBhOTQ1MjVlZTM0OTI4MCIsInN1YiI6IjY0NmQyYmMwNTRhMDk4MDE3MjhiYTk3YSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.qKxT93gXNgcML9qOqhG1Di5Hn7dDvx4d4R4oKNAhzec"
  }

  response = requests.get(url, headers=headers)
  response = response.text
  response = json.loads(response)
  retval = []

  for p in response["cast"]:
    dic = {}
    dic["name"] = p["name"]
    dic["id"] = p["id"]
    dic["character"] = p["character"]
    if p["gender"] == 2:
      dic["gender"] = "Male"
    else:
      dic["gender"] = "Female"
    dic["known_for_department"] = p["known_for_department"]
    retval.append(dic)

  return retval

def get_genres(movie_id):
  if movie_id == -1:
    return []
  url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US'

  headers = {
    "accept":
    "application/json",
    "Authorization":
    "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZjZiYzYxMDZlZTE5NzU5MjBhOTQ1MjVlZTM0OTI4MCIsInN1YiI6IjY0NmQyYmMwNTRhMDk4MDE3MjhiYTk3YSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.qKxT93gXNgcML9qOqhG1Di5Hn7dDvx4d4R4oKNAhzec"
  }

  response = requests.get(url, headers=headers)
  response = response.text
  response = json.loads(response)

  retval = []
  for g in response["genres"]:
    dic = {}
    dic["name"] = g["name"]
    dic["id"] = g["id"]
    retval.append(dic)
  return retval

def actor_movies(actor_id):  #returms id based off of a actors name

  url = f'https://api.themoviedb.org/3/person/{actor_id}/movie_credits?language=en-US'
  
  headers = {
      "accept": "application/json",
      "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZjZiYzYxMDZlZTE5NzU5MjBhOTQ1MjVlZTM0OTI4MCIsInN1YiI6IjY0NmQyYmMwNTRhMDk4MDE3MjhiYTk3YSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.qKxT93gXNgcML9qOqhG1Di5Hn7dDvx4d4R4oKNAhzec"
  }
  
  response = requests.get(url, headers=headers)
  response = response.text
  response = json.loads(response)
  retval = []
  #cast, crew, id
  for m in response["cast"]:
    dic = {}
    dic["title"] = m["title"]
    dic["vote_average"] = m["vote_average"]
    dic["genre_ids"] = m["genre_ids"]
    dic["release_date"] = m["release_date"]
    retval.append(dic)
  return retval

def all_genres():
  
  url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
  
  headers = {
      "accept": "application/json",
      "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZjZiYzYxMDZlZTE5NzU5MjBhOTQ1MjVlZTM0OTI4MCIsInN1YiI6IjY0NmQyYmMwNTRhMDk4MDE3MjhiYTk3YSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.qKxT93gXNgcML9qOqhG1Di5Hn7dDvx4d4R4oKNAhzec"
  }
  
  response = requests.get(url, headers=headers)
  response = response.text
  response = json.loads(response)
  return response["genres"]


def clean(title):
    new_title = title[:len(title)-7]
    if ", The" in new_title:
      new_title = new_title[:len(new_title)-5]
      new_title = "The " + new_title
    elif ", Les" in new_title:
      new_title = new_title[:len(new_title)-5]
      new_title = "Les " + new_title
    if "(" in new_title:
      for i in range(0,len(new_title)):
        if new_title[i] == "(":
          new_title = new_title[:i-1]
          break
    new_title = unidecode(new_title)
    return re.sub("[^a-zA-Z0-9 ,]", "", new_title)


#API Based on https://developer.themoviedb.org/reference/search-movie

