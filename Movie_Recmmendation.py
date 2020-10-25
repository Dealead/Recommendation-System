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


