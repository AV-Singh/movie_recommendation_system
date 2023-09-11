import streamlit as st
import pickle
import requests

moviesdf = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=79a25005788b3a440d676b33dfffe082&language=en-US'.format(movie_id))
    data = response.json()
    if data['poster_path']==None:
        return 'https://cdn.pixabay.com/photo/2016/03/31/18/36/cinema-1294496__340.png'
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']


response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=79a25005788b3a440d676b33dfffe082&language=en-US'.format(250546))
data = response.json()
st.image('https://image.tmdb.org/t/p/w500/'+data['poster_path'])
st.write(data['poster_path'])

def recommend(movie):
    index = moviesdf[moviesdf['title'] == movie].index[0]
    dist = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    poster=[]
    rec = []
    for i in dist[1:6]:
        rec.append(moviesdf.iloc[i[0]].title)
        poster.append(fetch_poster(moviesdf.iloc[i[0]].movie_id))
    return rec, poster

movies_list = moviesdf['title'].values

st.title('Movie Recommender System')

option = st.selectbox(
'',
    (movies_list))

if st.button('Recommend'):
    recommendations, posters = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommendations[0])
        st.image(posters[0])

    with col2:
        st.text(recommendations[1])
        st.image(posters[1])

    with col3:
        st.text(recommendations[2])
        st.image(posters[2])

    with col4:
        st.text(recommendations[3])
        st.image(posters[3])

    with col5:
        st.text(recommendations[4])
        st.image(posters[4])