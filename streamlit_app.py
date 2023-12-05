
git add app.py top50contry.csv


st.set_page_config(layout="wide")

scaler = MinMaxScaler(feature_range=(0, 100))
df = pd.read_csv("top50contry.csv")
df = df.dropna()
df= df.drop('Unnamed: 0',axis=1)
df = df.drop("added", axis=1)

df['country'] = df['country'].str.capitalize()

genre_counts = df['top genre'].value_counts()
valid_genres = genre_counts[genre_counts > 1].index
mask = df['top genre'].isin(valid_genres)
df = df[mask]

df.loc[df['top genre'].str.contains('pop'), 'top genre'] = 'pop'
df.loc[df['top genre'].str.contains('rap'), 'top genre'] = 'rap'
df.loc[df['top genre'].str.contains('r&b'), 'top genre'] = 'r&b'
df.loc[df['top genre'].str.contains('rock'), 'top genre'] = 'rock'
df.loc[df['top genre'].str.contains('house'), 'top genre'] = 'house'
df.loc[df['top genre'].str.contains('hip hop'), 'top genre'] = 'hip hop'
df.loc[df['top genre'].str.contains('funk'), 'top genre'] = 'funk'
df.loc[df['top genre'].str.contains('punk'), 'top genre'] = 'punk'
df.loc[df['top genre'].str.contains('soul'), 'top genre'] = 'soul'
df.loc[df['top genre'].str.contains('cumbia'), 'top genre'] = 'cumbia'
df.loc[df['top genre'].str.contains('trap'), 'top genre'] = 'trap'

df = df.loc[df['top genre'] != 'NA']

# MENU

menu = option_menu(None, ["Inicio", "Explorar por País",  "Top Global", "Glosario"],
    icons=['house', 'search', 'globe', 'book' ], menu_icon="cast",
    default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "3!important", "background-color": "#1e1e1e"},
        "icon": {"color": "white", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px"},
        "nav-link-selected": {"background-color": "black"},
    }
)
menu

#INICIO


def pagina_inicio():
    st.title("Top Songs Spotify")

    logo_url = "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg"
    st.image(logo_url, width=100)

    texto = "Spotify es una plataforma de streaming de música líder que ofrece a los usuarios acceso a una amplia biblioteca de millones de canciones. Fundada en 2006, permite descubrir, reproducir y compartir música de manera personalizada. Ofrece una versión gratuita con anuncios y una suscripción premium sin anuncios con funciones adicionales. Destaca por su algoritmo de recomendación, funciones sociales, y contenido exclusivo como podcasts y sesiones en vivo. Con presencia global, Spotify ha redefinido la forma en que las personas disfrutan de la música, proporcionando una experiencia musical accesible y personalizada."
    st.write(texto)


    st.header("Canciones Más Populares en el Mundo")


    df_filtered = df[(df['pop'] >= 70) & (df['pop'] <= 100)]

    # Crear el gráfico con el DataFrame filtrado
    fig = px.bar(df_filtered, x="title", y="pop", hover_data=["artist","year", "bpm", "dnce", "val"],
                labels={"pop": "Popularidad"},
                title="")

    fig.update_layout(
        xaxis_title="Canción",
        yaxis_title="Popularidad",
        hovermode="x",
        autosize=True,
    )

    st.plotly_chart(fig)

    most_popular_song = df.loc[df_filtered["pop"].idxmax()]

    st.markdown(
        f"<style>.highlight {{ background-color: #1ED761; padding: 5px; border-radius: 5px; }}</style>",
        unsafe_allow_html=True
    )

    st.subheader("Canción Más Escuchada")
    st.markdown(
        f"**Título:** <span class='highlight'>{most_popular_song['title']}</span>",
        unsafe_allow_html=True
    )
    st.write(f"**Artista:** {most_popular_song['artist']}")
    st.write(f"**Año:** {most_popular_song['year']}")


#SUNBURST

    st.header("Países, Géneros y Artistas Más Escuchados")

    top_countries = df['country'].value_counts().head(5).index
    top_genres = {}
    for country in top_countries:
        top_genres[country] = df[df['country'] == country]['top genre'].value_counts().idxmax()

    top_artists = {}
    for country, genre in top_genres.items():
        top_artists[(country, genre)] = df[(df['country'] == country) & (df['top genre'] == genre)]['artist'].value_counts().idxmax()

    data = []
    for country, genre in top_genres.items():
        data.append([country, genre, top_artists[(country, genre)]])

    fig = px.sunburst(data, path=[0, 1, 2], title="", color_continuous_scale="greens")
    st.plotly_chart(fig)

##artista y cancion popular
    selected_artist = st.selectbox("Selecciona un artista:", df["artist"].unique())

    # Filtrar datos según el artista seleccionado
    df_selected_artist = df[df["artist"] == selected_artist]

    # Verificar si hay datos seleccionados
    if not df_selected_artist.empty:
        # Encontrar la canción más popular del artista
        most_popular_song = df_selected_artist.loc[df_selected_artist["pop"].idxmax()]

        # Mostrar la información en una tabla
        st.subheader(f"Información de la Canción Más Popular de {selected_artist}:")

        # Crear el diccionario de datos
        table_data = {
            "Canción": [most_popular_song['title']],
            "Año": [most_popular_song['year']],
            "Género": [most_popular_song['top genre']],
            "Popularidad": [most_popular_song['pop']]
        }

        # Convertir el diccionario en un DataFrame y ocultar los índices
        table_df = pd.DataFrame(table_data)

        # Mostrar la tabla en Streamlit
        st.table(table_df)
    else:
        st.info("No hay datos disponibles para el artista seleccionado.")


def explorar_por_pais():
    st.title("Explorar por País")

    selected_country = st.selectbox("Selecciona un país:", df["country"].unique())
    df_selected_country = df[df["country"] == selected_country]
    df_selected_country_top10 = df[df["country"] == selected_country].sort_values(by="pop", ascending=False).head(10)
    columns_to_display = ["title", "artist", "top genre"]
    df_selected_country_top10 = df_selected_country_top10[columns_to_display]

    custom_css = """
    <!--
    <style>
        table {
            font-family: 'Arial', sans-serif;
            border-collapse: collapse;
            width: 100%;
        }

        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        th {
            background-color: #f2f2f2;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
    </style>
    -->
    """

# Aplicar el estilo
    st.markdown(custom_css, unsafe_allow_html=True)
    st.subheader(f"Top 10 en {selected_country}")
    st.table(df_selected_country_top10)



    #PIECHART

    st.header("Géneros más escuchados")
    est = df_selected_country['top genre'].value_counts().reset_index()
    est.columns = ['top genre', 'Conteo',]
    fig = px.pie(est, names='top genre', values='Conteo')
    st.plotly_chart(fig)


def top_global():

    ##Generos mas populares en el Mundo


    st.header("Género y Año Populares a Nivel Global")

    selected_years = st.multiselect("Selecciona años:", df["year"].unique(), key="years_selector")

    # Widget de selección para el género
    selected_genre = st.selectbox("Selecciona un género:", df["top genre"].unique(), key="genre_selector")

    # Iterar sobre los años seleccionados
    for selected_year in selected_years:
        # Filtrar datos según el año y el género seleccionados
        df_selected_data = df[(df["year"] == selected_year) & (df["top genre"] == selected_genre)]

        # Verificar si hay datos seleccionados
        if not df_selected_data.empty:
            # Crear un gráfico de barras
            fig = px.bar(df_selected_data, x="country", y="pop",
                        title=f"Popularidad de {selected_genre} en el Año {selected_year}",
                        labels={"pop": "Popularidad"},
                        hover_data=["title", "artist"])

            # Configurar diseño y estilo del gráfico
            fig.update_layout(
                xaxis_title="País",
                yaxis_title="Popularidad",
                hovermode="x",
            )

            # Mostrar el gráfico en Streamlit
            st.plotly_chart(fig)
        else:
            st.info(f"No hay datos disponibles para el año {selected_year} y género seleccionados.")



    ##Generos a lo largo del tiempo


    st.header("Popularidad de Género a lo Largo de los Años")

    selected_genre = st.selectbox("Selecciona un género:", df["top genre"].unique(), key="genre")

    # Filtrar datos según el género seleccionado
    df_selected_data = df[df["top genre"] == selected_genre]

    # Verificar si hay datos seleccionados
    if not df_selected_data.empty:
        # Crear un gráfico de área apilada
        fig = px.area(df_selected_data, x="year", y="pop", title=f"Popularidad de {selected_genre} a lo Largo de los Años",
                      labels={"pop": "Popularidad"},
                      hover_data=["title", "artist"],
                      color_discrete_sequence=px.colors.qualitative.Set1)

        # Configurar diseño y estilo del gráfico
        fig.update_layout(
            xaxis_title="Año",
            yaxis_title="Popularidad",
            hovermode="x",
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)
    else:
        st.info(f"No hay datos disponibles para el género seleccionado.")


#mapa


    selected_genre = st.selectbox("Selecciona un género:", df["top genre"].unique())
    df_selected_genre = df[df["top genre"] == selected_genre]
    df_sorted = df_selected_genre.sort_values(by="year")


    fig = px.scatter_geo(df_sorted, locations='country', size='pop', animation_frame="year", title=f'Mapa de Popularidad por País ({selected_genre})', locationmode='country names',projection='natural earth', size_max=40,color_discrete_sequence=['green'],width=900, height=550)
    fig.update_geos(projection_scale=3)
    st.plotly_chart(fig, use_container_width=True)


def glosario():

    st.header("Glosario")

    st.markdown("""
        **dnce:** Danceability. Describe qué tan adecuada es una canción para bailar, basándose en una combinación de elementos musicales que incluyen tempo, estabilidad del ritmo, fuerza del beat y regularidad general. Un valor de 0.0 es la menos adecuada para bailar y 1.0 es la más adecuada.

        **bpm:** Beats per minute. El tempo estimado general de una canción en pulsaciones por minuto (BPM). En términos musicales, el tempo es la velocidad o ritmo de una pieza musical y se deriva directamente de la duración promedio de los pulsos.

        **val:** Valence. Una medida de 0.0 a 1.0 que describe la positividad musical transmitida por una canción. Las canciones con una alta valencia suenan más positivas (por ejemplo, felices, alegres, eufóricas), mientras que las canciones con una baja valencia suenan más negativas (por ejemplo, tristes, deprimidas, enojadas).

        **acous:** Acousticness. Una medida de confianza de 0.0 a 1.0 que indica si la pista es acústica. 1.0 representa una alta confianza de que la pista es acústica.

        **Fuente:** Spotify for Developers
        [Enlace](https://developer.spotify.com/documentation/web-api/reference/get-audio-features)
        """)



if menu == "Inicio":
    pagina_inicio()
elif menu == "Explorar por País":
    explorar_por_pais()
elif menu == "Top Global":
    top_global()
else:
    menu == "Glosario"
    glosario()










