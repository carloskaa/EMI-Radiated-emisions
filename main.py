import matplotlib.pyplot as plt
from utils import fig_to_image2, E_field_procces
from utils_front import anten_treat 
import streamlit as st
import pandas as pd


st.set_page_config(page_title="Aplicativo de Procesamiento de Medidas de Emisión Radiada",layout="wide",)

st.title(" 🚀 APP - Procesamiento de Medidas de Emisión Radiada  🚀")
# Agregar una sección de instrucciones en la página principal
with st.expander("Instrucciones de uso"):
    st.write("""
    **Instrucciones de uso:**
    1. Utilice el menú lateral para cargar los archivos necesarios.
    2. Cargue los archivos de datos de medida (.csv) y los archivos Touchstone (.s2p) para bajas y altas frecuencias.
    3. Seleccione el tipo de antena utilizada para las mediciones.
    4. Ingrese los valores de inicio y fin de la norma, así como los valores de inicio y fin de la transición (ya hay valores de una norma por defecto).
    5. Haga clic en 'Procesar datos' para procesar los archivos cargados.
    6. Puede descargar la gráfica y los resultados en formato PNG y CSV.
    7. Los resultados se mostrarán en la página principal.
    """)

with st.expander("Presentacion Proyecto"):
    st.title("Aplicativo cálculo de emisiones radiadas 📡")
    st.subheader("Grupo: Inducidos")
    st.title("DESCRIPCIÓN GENERAL")
    st.subheader("OBJETIVO")
    st.markdown(" 📊 Desarrollar un aplicativo para procesar medidas de emisión radiada.")
    st.subheader("DATOS")

    objetivos = [
        "📌 Datos de medida. ",
        "📌 Factores de antena.",
        "📌 Touchstone cables, atenuadores.",
        "📌 Límites de emisión."
    ]

    # Mostrar la lista con Markdown
    st.markdown("### 🚀 Datos de entrada:")
    for obj in objetivos:
        st.markdown(f"- {obj}")
    
    objetivos = [
        "✅ Campo E en dBuV/m vs frecuencia. ",
        "✅ Frecuencias por encima del límite, el valor de E a esa frecuencia en dBuV/m  y la diferencia con respecto al límite.",
        "✅ Frecuencias a menos de 6dB del límite, el valor de E a esa frecuencia en dBuV/m  y la diferencia con respecto al límite",
        "✅ Imagen PNG o SVG con los resultados."
    ]

    # Mostrar la lista con Markdown
    st.markdown("### 📂 Datos de salida:")
    for obj in objetivos:
        st.markdown(f"- {obj}")

    st.title("SITUACIÓN PROBLEMA")
    ##subtitulo
    st.markdown("En la siguiente imagen se presenta gráficamente las fuentes de datos de una medición de emisiones radiadas. ")
    st.markdown("Teniendo como referencia la fuente de los datos, se desarrolla el siguiente tratamiento de los mismos.")
    #image
    st.image("Emi2.png", caption="Fuente de datos de una medición de emisiones radiadas")
    
    st.title("ESTRUCTURACIÓN DEL APLICATIVO")

    objetivos = [
        "✅ Se realiza la lectura de los datos de entrada utilizando la librería de panda para leer archivos csv, estos datos ya se encuentran en unidades de dBm por lo que se pueden operar directamente. ",
    ]
    st.markdown("### 📈 Datos de la medición:")
    for obj in objetivos:
        st.markdown(f"- {obj}")
    
    objetivos = [
        "✅ Se realiza la lectura de los datos del cable los cuales están en formato .s2p por lo cual es necesario usar la librería “scikit-rf” de python para obtener los valores de impedancia de entrada (unidades en dB), necesarios para el cálculo del valor de campo eléctrico.",
    ]
    st.markdown("### 🚀 Datos del cable:")
    for obj in objetivos:
        st.markdown(f"- {obj}")

    objetivos = [
        "✅ Los datos la antena necesarios son el factor de antena (dB/m), los cuales son tomados del datasheet del fabricante. ",
        "✅ Debido a que el factor de antena es una curva en formato de imagen, se procesa la imagen en un software externo (engauge digitizer), los datos extraídos son usados en el cálculo de campo eléctrico. "
    ]
    st.markdown("### 📜 Datos Normativos:")
    for obj in objetivos:
        st.markdown(f"- {obj}")

    objetivos = [
        "✅ Se genera el límite normativo a partir de la información suministrada por el usuario y se genera el muestreo pertinente a partir del muestreo de frecuencia de los datos de medición.,",
    ]
    st.markdown("### 🔊 Datos de la antena:")
    for obj in objetivos:
        st.markdown(f"- {obj}")

    objetivos = [
        "✅ Los datos de medición se tomaron como referencia para delimitar la frecuencia de mediciones (Frecuencia máxima y frecuencia mínima a evaluar) con el fin de optimizar el proceso computacional.",
        "✅ Se unifica el muestreo de frecuencias con un método numérico (interpolación lineal), usando como referencia la frecuencia más extensa en cantidad de datos.,"
    ]
    st.markdown("### 🔘 Ajuste de Datos")
    for obj in objetivos:
        st.markdown(f"- {obj}")
    
    objetivos = [
        "✅ A partir de los datos procesados se realiza el cálculo del campo eléctrico para cada una de las frecuencias muestreadas como:"
    ]
    st.markdown("### 📊 Calculo de campo electrico")
    for obj in objetivos:
        st.markdown(f"- {obj}")
    
    st.image("Ecu2.png", caption="Fuente de datos de una medición de emisiones radiadas")
    objetivos = [
        "M = Medición de potencia en el receptor",
        "C = Atenuación en el Cable",
        "F = Factor de antena",

    ]
    for obj in objetivos:
        st.markdown(f"- {obj}")
    
    objetivos = [
        "✅ Se realiza la comparación entre la el cálculo de campo eléctrico y el valor normativo mostrando los valores que la superan con un a X y los valores cerca por 6 dB con X"
    ]
    st.markdown("### 📑 Comparacion normativa")
    for obj in objetivos:
        st.markdown(f"- {obj}")

    
    objetivos = [
        "[1]. MIL-STD-461G RE102-3: Radiated Emissions, Electric Field – Limits for Aircraft and Space System Applications.",
        "[2]. Sesion 04-05 Repaso Normativa Unidades, Diapositivas de clase CEM, ,Universidad Nacional de Colombia, Nicolas Mora, 2024. ",
        "[3] pandas.pydata.org, 'pandas: Python Data Analysis Library,' Available: https://pandas.pydata.org/. [Accessed: Jan. 28, 2025].",
        "[4] numpy.org, 'NumPy: The fundamental package for scientific computing with Python,' Available: https://numpy.org/. [Accessed: Jan. 28, 2025].",
        "[5] A. Kozak, 'scikit-rf: An object-oriented approach to RF/Microwave engineering,' Available: https://scikit-rf.readthedocs.io/. [Accessed: Jan. 28, 2025].",
        "[6] streamlit.io, 'Streamlit: The fastest way to build and share data apps,' Available: https://streamlit.io/. [Accessed: Jan. 28, 2025].",
        "[7] J. D. Hunter, Matplotlib: A 2D graphics environment, _Computing in Science & Engineering_, vol. 9, no. 3, pp. 90-95, May-June 2007. [Online]. Available: https://matplotlib.org/. [Accessed: Jan. 28, 2025].",



    ]
    st.title("REFERENCIAS")
    for obj in objetivos:
        st.markdown(f"- {obj}")





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

