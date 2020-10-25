"""
MOVIE RECOMMENDATION SYSTEM
Recommendation systems predict user preference and ratings of an item. They are one of the most popular applications used in data science. Various companies make use of them to make suggestion based on their clients’ preferences, to help them meet their needs. Media companies like Netflix, make use of recommendation systems to help users decide which movie or documentary they would enjoy watching. Other product based companies like Amazon, utilize this system in order to suggest products for customers.

It turns out that there are (mostly) three ways to build a recommendation engine:
1.	Popularity based recommendation engine
This is popularly referred to as the simplest kind of recommendation engine that you will come across. Companies like Netflix and YouTube make use of this algorithm to to make trending lists. For each movie or video, it records the number of views and subsequently lists them in descending order (from views with the most frequency to lowest number of views).
2.	Content based recommendation engine
Netflix makes use of this type of recommendation when you initially set up your account (movies in ‘Your List’). This type of recommendation systems, takes in a movie that a user currently likes as input; it analyzes the contents (storyline, genre, cast, director etc.) of the movie to find out other movies which have similar content. Then it ranks similar movies according to their similarity scores and finally recommends the most relevant movies to the user.

3.	Collaborative filtering based recommendation engine
This algorithm at first tries to find similar users based on their activities and preferences (for example, both the users watch same type of movies or movies directed by the same director). Now, between these users (say, A and B) if user A has seen a movie that user B has not seen yet, then that movie gets recommended to user B and vice-versa. In other words, the recommendations get filtered based on the collaboration between similar user’s preferences (thus, the name “Collaborative Filtering”). One typical application of this algorithm can be seen in the Amazon e-commerce platform, where you get to see the “Customers who viewed this item also viewed” and “Customers who bought this item also bought” list.
The algorithm used in here will be solely based on the content-based recommendation system.
 	a. Importing the libraries
 	b. Reading the data
 	c. Renaming and cleaning the dataset
 	d. Importing Scikit-learn’s Tfidfvectorizer. Tfidfvectorizer aims to convert a collection of raw documents to a matrix of TF-IDF features. The TF stands for “Term frequency”, while the IDF stands for “Inverse Data Frequency”.
 	e. Fitting the TF-IDF on the 'overview' text.
        It should be noted that, this is dtype object; hence, conversion to Unicode string is necessary. The “astype('U').values” function makes it possible to transform text data into Unicode.
 	f. Importing scikit-Learn’s sigmoid kernel
 	g. Computing the sigmoid kernel
 	h. Reverse mapping of indices and movie titles
    i. Defining a function “give_recommendation” that returns 10 movies that are similar to the one requested. It involves the following;
            o	Getting the index corresponding to original title
            o	Getting the pairwise similarity scores
            o	Sorting the movies
            o	Obtaining the scores of the 10 most similar movies
            o	Indexing the movies
            o	Finally, returning the Top 10 most similar movies

"""

import pandas as pd
import numpy as np

credits_data = pd.read_csv("C:/Users/mowab/Downloads/archive/tmdb_5000_credits.csv")
movies_data = pd.read_csv("C:/Users/mowab/Downloads/archive/tmdb_5000_movies.csv")


print(credits_data.head())
print(movies_data.head())

print("Credits Data Shape: ", credits_data.shape)
print("Movies Data Shape: ", movies_data.shape)


credits_data_columnrenamed = credits_data.rename(index=str, columns={"movie_id": "id"})
movies_datamerge = movies_data.merge(credits_data_columnrenamed, on='id')
print(movies_datamerge.head())

movies_datacleaned = movies_datamerge.drop(columns=['homepage', 'title_x', 'title_y', 'status', 'production_countries'])
print(movies_datacleaned.head())
print(movies_datacleaned.info())
print(movies_datacleaned.head(1)['overview'])


from sklearn.feature_extraction.text import TfidfVectorizer
tfidfv = TfidfVectorizer(min_df = 3, max_features = None, strip_accents = 'unicode', analyzer = 'word',
                         token_pattern = r'\w{1,}', ngram_range = (1, 3), stop_words = 'english')


tfidfv_matrix = tfidfv.fit_transform(movies_datacleaned['overview'].astype('U').values)
print(tfidfv_matrix)
print(tfidfv_matrix.shape)


from sklearn.metrics.pairwise import sigmoid_kernel
sigmd = sigmoid_kernel(tfidfv_matrix, tfidfv_matrix)
print(sigmd[0])

indices = pd.Series(movies_datacleaned.index, index = movies_datacleaned['original_title']).drop_duplicates()
print(indices)
print(indices['Newlyweds'])
print(sigmd[4799])
print(list(enumerate(sigmd[indices['Newlyweds']])))
print(sorted(list(enumerate(sigmd[indices['Newlyweds']])), key=lambda x: x[1], reverse=True))



def movie_recomendations(title, sig=sigmd):
    idx = indices[title]
    sigmd_scores = list(enumerate(sig[idx]))
    sigmd_scores = sorted(sigmd_scores, key=lambda x: x[1], reverse=True)
    sigmd_scores = sigmd_scores[1:11]
    movie_indices = [i[0] for i in sigmd_scores]
    return movies_datacleaned['original_title'].iloc[movie_indices]


print(movie_recomendations('The Avengers'))

print(movie_recomendations('Titanic'))
