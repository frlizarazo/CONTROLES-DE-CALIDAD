import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import use

use('Agg')

# PALOGRANDE RUTA 30 y RIO TAPIAS NO APLICAN PARA ESTE FILTRO

def CCal16_ZScoreRobusto(df):
    """
    Elimina valores atípicos usando z-score robusto por hora (mediana y MAD).
    Conserva datos dentro de aproximadamente 99.99% del comportamiento horario.
    """
    eliminados = []
    columnas_consideradas = [c for c in df.columns if c in ['Nivel','Temperatura']]
    umbral = 6  # similar a ±4 desviaciones estándar

    for var in columnas_consideradas:
        df_temp = df[var].dropna()
        if len(df_temp) == 0:
            continue

        idx = pd.to_datetime([])

        for h in range(24):
            df_temp_h = df_temp.between_time(f"{h}:00", f"{h}:59").dropna()
            if len(df_temp_h) < 10:
                continue

            mediana = df_temp_h.median()
            mad     = np.median(np.abs(df_temp_h - mediana))

            if mad == 0:  # evitar división por cero
                continue

            z_score_robusto = 0.6745 * (df_temp_h - mediana) / mad
            idx_h = df_temp_h[np.abs(z_score_robusto) > umbral].index
            idx   = idx.union(idx_h)

        if len(idx) > 0:
            eliminados.append(df.loc[idx, var].copy())

        df.loc[idx, var] = np.nan

    if len(eliminados) > 0:
        eliminados = pd.concat(eliminados, axis=1, sort=True)

    return df, eliminados

CCal16_ZScoreRobusto.variables = ['Nivel']
CCal16_ZScoreRobusto.nombre = 'Z-Score Robusto por hora'
