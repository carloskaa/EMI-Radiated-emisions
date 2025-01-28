import pandas as pd
import numpy as np
import skrf as rf
from io import BytesIO
from io import StringIO
import streamlit as st

def E_field_procces(medidas_file, s2p_file, anten_factor, freq_range,transition_start,transition_end,start_db,end_db):

    df = pd.read_csv(StringIO(medidas_file.read().decode('utf-8')), skiprows=31, header=None, names=['freq', 'dbm', 'd'], sep=';')
    
    df['freq'] = df['freq']/1000000
    df.drop(columns=['d'],inplace=True)

    if freq_range == 'low':  ### usar antena FRANKONIA
        if anten_factor == 'Frankonia':
            df_ant = pd.read_csv('antenas\Frankonia_ALX_4000.csv')
        elif anten_factor == 'Lindgren':
            st.error("Lindgren no sirve para mediciones a baja frecuencia")
        else:
            df_ant = pd.read_csv(StringIO(medidas_file.read().decode('utf-8')))

        df_ant = df_ant[(df_ant['freq']>=30) & (df_ant['freq']<=1000)]
        df_norma = creation_normative_data(transition_start,transition_end,start_db,end_db)
        st_fq = 30
        en_fq = 1000

    elif freq_range == 'high': ###usar antena lindgren
        if anten_factor == 'Frankonia':
            st.error("Frankonia no sirve para mediciones a alta frecuencia")
        elif anten_factor == 'Lindgren':
            df_ant = pd.read_csv('antenas\Lindgren.csv')
        else:
            df_ant = pd.read_csv(StringIO(medidas_file.read().decode('utf-8')))
        df_ant['freq'] = df_ant['freq']*1000
        df_ant = df_ant[(df_ant['freq']>=1000) & (df_ant['freq']<=18000)]
        df_norma = creation_normative_data(transition_start,transition_end,start_db,end_db)
        st_fq = 1000
        en_fq = 18000

    df_cable = creation_db_cable(s2p_file)

    df = pd.merge(df, df_ant, on='freq', how='outer', suffixes=('', '_ant'))
    df = pd.merge(df, df_norma, on='freq', how='outer', suffixes=('', '_norma'))
    df = pd.merge(df, df_cable, on='freq', how='outer', suffixes=('', '_cable'))

    df = df.sort_values('freq')  # Ordenar por frecuencia
    df = df.interpolate(method='linear')
    df.rename(columns={'dbm_norma' : 'Límite_dBuV_m'},inplace=True)
    df.rename(columns={'freq' : 'Frecuencia_MHz'},inplace=True)

    df['Campo_E_dBuV_m'] = df['dbm'] + df['dbm_ant'] - df['dbm_cable'] + 107 + 36
    return df, st_fq, en_fq


def fig_to_image(fig):
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf.getvalue()

def creation_normative_data(transition_start,transition_end,start_db,end_db):
    # transition_start = 100e6 # Inicio de transición (100 MHz)
    # transition_end = 18e9    # Final de transición (18 GHz)
    # start_db = 34            # Nivel constante antes de la transición
    # end_db = 79              # Nivel constante después de la transición
    transition_start = int(transition_start)*1000000 # Inicio de transición (100 MHz)
    transition_end = int(transition_end)*1000000    # Final de transición (18 GHz)
    start_db = int(start_db)            # Nivel constante antes de la transición
    end_db = int(end_db)            # Nivel constante después de la transición
    start_frequency = 100e3  # Frecuencia inicial (100 kHz)
    end_frequency = 100e9    # Frecuencia final (100 GHz)

    # Crear datos de frecuencia en escala logarítmica
    frequencies = np.logspace(np.log10(start_frequency), np.log10(end_frequency), 1000)
    print(transition_start)
    print(transition_end)
    print(start_db)
    print(end_db)
    # Crear valores de dB
    db_values = np.piecewise(
        frequencies,
        [frequencies < transition_start, 
        (frequencies >= transition_start) & (frequencies <= transition_end), 
        frequencies > transition_end],
        [start_db, 
        lambda x: np.linspace(start_db, end_db, len(x)),  # Interpolación lineal en el espacio logarítmico
        end_db]
    )
    frequencies = frequencies/1000000
    df = pd.DataFrame({'freq':frequencies, 'Límite_dBuV_m':db_values})

    return df

def creation_db_cable(file_name):
    # Cargar el archivo Touchstone
    s_params = rf.Network(file_name)

    frequencies = s_params.f  # Frecuencia en Hz
    S11 = s_params.s[:, 0, 0]  # S11
    S12 = s_params.s[:, 0, 1]  # S12
    S21 = s_params.s[:, 1, 0]  # S21
    S22 = s_params.s[:, 1, 1]  # S22

    # Definir la impedancia de referencia (por defecto es 50 ohmios)
    Z0 = s_params.z0[1,1]

    # Convertir S11 a Zin
    # Zin = Z0 * ((1 + S11) * (1 - S22) + S12 * S21) / ((1 - S11) * (1 - S22) - S12 * S21)
    Zin = Z0 * (1 + S11) / (1 - S11)


    # Calcular la magnitud de Zin
    magZin = np.abs(Zin)

    # Convertir la magnitud de Zin a dB
    magZin_dB = 20 * np.log10(magZin)
    frequencies = frequencies/1000000
    df = pd.DataFrame({'freq':frequencies, 'dbm':magZin_dB})
    return df

def fig_to_image2(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)  # Volver al inicio del archivo en memoria
    return buf