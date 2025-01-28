import streamlit as st


def anten_treat(anten_factor):
    if anten_factor == "Añadir dato de antena":
        st.sidebar.write("Sube un archivo Excel para crear un nuevo factor:")
        uploaded_file = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])
        return uploaded_file
