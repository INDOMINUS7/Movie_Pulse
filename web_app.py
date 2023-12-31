import streamlit as st
import pickle
import pandas as pd
import requests  # for hitting the API


def poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=b2b04c57c056fa5fb94a0d36d96c2612&language=en-US'.format(movie_id)
    data= requests.get(url)
    data=data.json()
    poster_path= data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = (movies[movies['title'] == movie]).index[0]  # Finding the index of the asked movie in our data frame
    distances = sorted(list(enumerate(similarity_score[movie_index])), reverse=True, key=lambda x: x[1])

    recommended_movies_names= []
    recommended_movies_poster=[]

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_names.append(movies.iloc[i[0]].title)
        # fetching poster from API
        recommended_movies_poster.append(poster(movie_id))
    return recommended_movies_names, recommended_movies_poster


similarity_score = pickle.load(open('similarity_matrix.pkl', 'rb'))

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

st.title('Movie Recommendations System')
user_movie = st.selectbox('Which movie did you like?', (movies['title'].values))

if st.button('Give me more Movies like this!'):
    names, posters = recommend(user_movie)


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])