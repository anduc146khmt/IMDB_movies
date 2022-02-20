# -*- coding: utf-8 -*-
"""IDMB movies.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rz7tjgBs9wUQjd6whTpiwRdnRfC2kDzS

# Introduction

As we have a basic understanding of the different data structures in Pandas, let’s explore the fun and and get our hands dirty by performing practical data analysis on real data.

Here's a data set of 1,000 most popular movies on IMDB in the last 10 years . The data included  fields: Title, Genre, Description, Director, Actors, Year, Runtime, Rating, Votes, Revenue, Metascrore

It is an real dataset of kaggle community,  you can download it from [IMDB data from 2006 to 2016](https://www.kaggle.com/PromptCloudHQ/imdb-data)

Feel free to tinker with it and derive interesting insights.

#Usage

This project could be used to revise your knowledge or warming up your data analyst skill using Pandas

# Requirement


*   Having background about Python Programming, basic Data Analyst using Pandas
*   A little knowledge about Data Visualization using Seaborn

#Contributor

This notebook is my project practicing Pandas after finishing the Pandas course in kaggle community. I think it is a good course to begin learning Data Analyst, I recommend this course here [Pandas Course](https://www.kaggle.com/learn/pandas)

Author : [anduc146khmt](https://github.com/anduc146khmt)

#1. Read Data

**Import Pandas and Seaborn**
"""

import pandas as pd
import seaborn as sb

"""**Read CSV**"""

path = '/content/sample_data/IMDB-Movie-Data.csv'
data = pd.read_csv(path)

"""# 2. View Data"""

data.head()

"""#3. Understand some basic information about the data

**Data Info**
"""

data.info()

"""**Data Describe**"""

data.describe()

"""**Data Shape**"""

data.shape

"""#4. Data Selection – Indexing and Slicing data

**Data Selection by columns**
"""

cols = ['Title', 'Genre', 'Actors', 'Director', 'Rating']
some_cols = data[cols]
some_cols.head()

"""**Data Selection using loc**

Now, I would select some information of the movie "Suicide Squad". And I have to do some following tasks

**Create new DataFrame with Titile column**
"""

path = '/content/sample_data/IMDB-Movie-Data.csv'
title_data = pd.read_csv(path, index_col = 'Title')
title_data.head()

"""**Select query movie from new DataFrame**"""

index = ['Suicide Squad']
cols = ['Genre', 'Actors', 'Director', 'Rating', 'Revenue (Millions)']
suicide_squad = title_data.loc[index, cols]
suicide_squad.head()

"""**Select some optional record from dataset**"""

indices = [0,5,10,15,20,25]
cols = ['Title', 'Genre', 'Actors', 'Director', 'Rating']
query_record = data.loc[indices, cols]
query_record.head()

"""**Data Selection using iloc**"""

cols = ['Title', 'Genre', 'Actors', 'Director', 'Rating']
block_record = data.iloc[10:15][cols]
block_record.head()

"""#5. Data Selection – Based on Conditional filtering

Now, I would like to select some movie which has some conditions : 


1.   Movie are released from 2010 to 2016
2.   Genre of movie is Adventure or Sci-Fi
3.   Rating point larger than 6
4.   Movie are topped in terms of revenue
"""

query_movie = data.loc[
      ((data['Year'] >=  2010) &  (data['Year'] <=  2016)) 
      &  data['Genre'].str.contains('Adventure|Sci-Fi', regex = True)
      &   (data['Rating'] > 6.0)  
      &  (data['Revenue (Millions)'] > data['Revenue (Millions)'].quantile(0.95))
]
cols = ['Title', 'Genre', 'Actors', 'Director', 'Rating']
query_movie = query_movie.loc[ : , cols]
print(' We have', len(query_movie.index), 'movies meet the requirements')
query_movie.head()

"""#6. Groupby operations

Now, I want to know the average rating through all movies of directors. In this case, I would use the power of **groupby()**
"""

average_rating = data.groupby('Director').Rating.mean()
average_rating

"""#7. Create DataFrame With Optional Requirements

Also, I would like to count the number of movies in each genre and display information as a DataFrame
"""

genres = ['Action', 'Adventure', 'Sci-Fi', 'Comedy', 'Fantasy', 'Animation', 'Thriller', 'Horror', 'Mystery' ]
numOfGenre = []
for index in range(len(genres)):
      n_genre = data.Genre.map(lambda genre:  genres[index] in  genre).sum()
      numOfGenre.append(n_genre)
genreDataFrame = pd.DataFrame(numOfGenre, index = genres, columns = ['Genres'])
genreDataFrame

"""#8. Sorting operation

In this section, I would like to know which movie has the best rating and its descending order, alongside with its director.
"""

cols = ['Title', 'Director']
sort_data = data.groupby(cols)[['Rating']].mean().sort_values(by = ['Rating'],  ascending = False)
sort_data.head(15)

"""#9. Dealing with missing values

Let's return **data.info()**, you have seen  Revenue (Millions) with  872 non-null, and Metascore  with 936 non-null and others is 1000 non-null. Why ?

It just because in these fields the data is missing, some data cells did not contain any values. So we will cleaning data by using some following steps

**Checking data is missing**
"""

revenue_null = data[pd.isnull(data['Revenue (Millions)'])]
metascope_null = data[pd.isnull(data['Metascore'])]
data_null = pd.concat([revenue_null, metascope_null])
data_null

"""**Replace data missing with particular values. Personally, I will replace missing data with 0**"""

data_null.fillna(0)

"""#10. Dropping columns and null values

Another way to deal with null values is to delete cells with contains null values
"""

data.dropna()

"""As you see, it only contains **838 rows**, **dropna()** is used to drop rows which has null value in its cell.

Optional, you can choose to drop rows by set **axis = 0**, and columns with **axis = 1** (default parameter is **axis = 0**)

Another example, I see that I don't use **Runtime (Minutes)** and **Votes** for my analyst, I care more about rating, genre, revenue,... so that I will drop two columns **Runtime (Minutes)**  and **Votes**
"""

drop_elements = ['Runtime (Minutes)',  'Votes']
data.drop(drop_elements , axis = 1)

"""# 11. Apply( ) functions

After analysting data, I would like to evaluate each movies by following this rules:  

*   If rating is larger than 8.5, the movie is reviewed "Excellent" 
*   If rating in range [7, 8.5), the movie is reviewed "Good"
*   If rating in range [5, 7), the movie is reviewed "Average"
*  If rating in smaller than 5, the movie is reviewed "Bad"
"""

def evaluate (rating):
      if rating >= 8.5:
        return "Excellent"
      elif rating >= 7 and rating < 8.5:
        return "Good"
      elif rating >= 5 and rating < 7:
        return "Average"
      else:
          return "Bad"
data['Evaluation'] = data['Rating'].apply(evaluate)
index = ['Title', 'Genre', 'Director', 'Rating', 'Evaluation', 'Description']
data_query = data.loc[ : , index]
data_query.head()

"""You also can use sorted data **(in 8th section)** and categorize movies from the highest-rating movie to lowest-rating movie."""

sort_data['Evaluation'] = sort_data['Rating'].apply(evaluate)
sort_data

"""# Conclusion

Well, thank you for your reading, I hope you have learned something through my projects.

If you see this notebook is useful, I very glad if you give me a star in my github projects.

See more my projects here : [https://github.com/anduc146khmt](https://github.com/anduc146khmt)

Contact me : ducan1406@gmail.com
"""