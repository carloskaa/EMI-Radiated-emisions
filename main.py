import matplotlib.pyplot as plt
from utils import fig_to_image2, E_field_procces
from utils_front import anten_treat 
import streamlit as st
import pandas as pd


st.set_page_config(page_title="Aplicativo de Procesamiento de Medidas de Emisión Radiada",layout="wide",)

st.title("Procesamiento de Medidas de Emisión Radiada")

# Sidebar para cargar los datos
st.sidebar.header("Carga de datos")
##input text
title = st.sidebar.text_input('Titulo', 'Measurement XXX')



medidas_file = st.sidebar.file_uploader("Datos de medida Bajas frecuencias (*.csv)", type="csv", accept_multiple_files=False)
medidas_file2 = st.sidebar.file_uploader("Datos de medida Altas frecuencias (*.csv)", type="csv", accept_multiple_files=False)
s2p_file = st.sidebar.file_uploader("Archivos Touchstone Bajas frecuencias (*.s2p)", type="s2p", accept_multiple_files=False)
s2p_file2 = st.sidebar.file_uploader("Archivos Touchstone Altas frecuencias (*.s2p)", type="s2p", accept_multiple_files=False)
anten_factor = st.sidebar.selectbox("Seleccione antena para mediciones a baja frecuencia",["Frankonia", "Lindgren"])
anten_factor2 = st.sidebar.selectbox("Seleccione antena para mediciones a alta frecuencia",["Frankonia", "Lindgren"])

norma = st.sidebar.selectbox("Seleccione normativa a revisar",["MIL-STD-461 – RE102-3"])


## add title
st.sidebar.write('Normativa (MIL-STD-461 – RE102-3)')
start_db = st.sidebar.text_input('Inicio de la norma (dBuV/m)', '34')
end_db = st.sidebar.text_input('Fin de la norma (dBuV/m)', '74')
transition_start = st.sidebar.text_input('Inicio de transición (MHz)', '100')
transition_end = st.sidebar.text_input('Fin de transición (MHz)', '200')



# Botón para procesar los datos
if st.sidebar.button("Procesar datos"):
    if not (medidas_file and s2p_file and medidas_file2 and s2p_file2 and anten_factor and anten_factor2):
        st.error("Por favor, carga todos los archivos necesarios para continuar.")
    else:
        df1, st_fq, en_fq  = E_field_procces(medidas_file, s2p_file,anten_factor,'low',transition_start,transition_end,start_db,end_db)
        df2, st_fq2, en_fq2 = E_field_procces(medidas_file2, s2p_file2,anten_factor2,'high',transition_start,transition_end,start_db,end_db)

        filtered_df1 = df1[(df1['Frecuencia_MHz'] >= 30) & (df1['Frecuencia_MHz'] <= 1000)]
        filtered_df2 = df2[(df2['Frecuencia_MHz'] >= 1000) & (df2['Frecuencia_MHz'] <= 18000)]
        df = pd.concat([filtered_df1, filtered_df2])
        df = df.reset_index(drop=True)
      

        supera_norma = df['Campo_E_dBuV_m'] > df['Límite_dBuV_m']
        cerca_norma = (df['Campo_E_dBuV_m'] <= df['Límite_dBuV_m']) & (df['Campo_E_dBuV_m'] >= df['Límite_dBuV_m'] - 6)

        # Crear gráfico
        fig = plt.figure(figsize=(10, 6))
        plt.plot(df['Frecuencia_MHz'], df['Campo_E_dBuV_m'], label='Field level', color='blue')
        plt.plot(df['Frecuencia_MHz'], df['Límite_dBuV_m'], label="MIL-STD-461 – RE102-3", color="red")

        # Agregar los puntos de superación (rojo) y cercanos (verde)
        plt.scatter(df['Frecuencia_MHz'][supera_norma], df['Campo_E_dBuV_m'][supera_norma], 
                    color='red', marker='x', label='Max above')
        plt.scatter(df['Frecuencia_MHz'][cerca_norma], df['Campo_E_dBuV_m'][cerca_norma], 
                    color='green', marker='x', label='Max within 6dB')

        # Configuración de ejes y diseño
        plt.title(title)
        plt.xlabel("Frequency (MHz)")
        plt.ylabel("Field in dBµV/m")
        plt.legend()
        plt.grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
        plt.xticks(rotation=45)
        plt.xscale('log')
        plt.xlim([st_fq, en_fq2])
        # plt.ylim([0, 80])
        plt.tight_layout()
        
        # Mostrar y descargar gráfica
        st.pyplot(fig)
        st.download_button(
            label="Descargar gráfica (PNG)",
            data=fig_to_image2(fig),
            file_name="grafica_resultados.png",
            mime="image/png",
        )


        #####################################################
        # Identificar frecuencias por encima de los límites
        resultados_sobre_limite = df[df["Campo_E_dBuV_m"] > df["Límite_dBuV_m"]]
        resultados_cercanos_limite = df[
            (df["Campo_E_dBuV_m"] <= df["Límite_dBuV_m"]) &
            (df["Campo_E_dBuV_m"] > df["Límite_dBuV_m"] - 6)
        ]

        # Mostrar tablas procesadas
        st.write("Frecuencias por encima del límite:")
        st.dataframe(resultados_sobre_limite)

        st.write("Frecuencias a menos de 6dB del límite:")
        st.dataframe(resultados_cercanos_limite)

        # Exportar resultados a CSV
        st.download_button(
            label="Descargar resultados sobre limite (CSV)",
            data=resultados_sobre_limite.to_csv(index=False),
            file_name="resultados_sobre_limite.csv",
            mime="text/csv",
        )

        st.download_button(
            label="Descargar resultados cercano limite (CSV)",
            data=resultados_cercanos_limite.to_csv(index=False),
            file_name="resultados_cercanos_limite.csv",
            mime="text/csv",
        )

