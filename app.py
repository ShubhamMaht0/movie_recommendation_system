import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_title):
    api_key = st.secrets["api_key"]
    response = requests.get(f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}")
    data = response.json()
    return data.get('Poster', "")

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        #movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]].title))
    return recommended_movies,recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movies Recommendation System')

selected_movie_name = st.selectbox(
    "What do you want to watch?",
    movies['title'].values,
)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    

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

