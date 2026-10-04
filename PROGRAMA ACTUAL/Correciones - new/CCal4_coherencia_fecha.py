# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal6_coherencia_fecha.py                                                            #
# DESCRIPCIÓN: Verifica la coherencia de las fechas en el DataFrame                                     #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal6_coherencia_fecha(df)                                                                     #
#                                                                                                  #
# PARAMETROS DE ENTRADA:                                                                           #
#   df: DataFrame con los datos de la serie temporal                                               #
#                                                                                                  #
# PARAMETROS DE SALIDA:                                                                            #
#   df         : DataFrame con los datos corregidos                                                #
#   eliminados : DataFrame con las entradas duplicadas eliminadas                                  #
#                                                                                                  #
# ================================================================================================ #

# LIBRERÍAS DE PYTHON ============================================================================ #
import numpy as np
import pandas as pd
from Funciones.instrumentar import Instrumentar

# CONTROL DE CALIDAD ============================================================================= #
def CCal4_coherencia_fecha(df):

    Coherencia_Fecha   = Instrumentar('Verificar coherencia de las fechas')
    eliminados = 0
    col_ppt = "PPT"

    cols_num = df.select_dtypes(include=[np.number]).columns.tolist()
    cols_secundarias = [c for c in cols_num if c != col_ppt]

    i = 1
    # Se usa while dinámico porque el reordenamiento cambia la posición de los elementos
    while i < len(df) - 1:
        fecha_actual = df.index[i]

        # Una fecha es potencialmente ambigua si el día <= 12 y día != mes
        if fecha_actual.day <= 12 and fecha_actual.day != fecha_actual.month:

            # Construir la fecha swap (intercambiando día y mes)
            try:
                fecha_swap = pd.Timestamp(
                    year=fecha_actual.year,
                    month=fecha_actual.day,
                    day=fecha_actual.month,
                    hour=fecha_actual.hour,
                    minute=fecha_actual.minute,
                    second=fecha_actual.second,
                )
            except ValueError:
                # Fecha inválida (ej. 31 de Febrero)
                i += 1
                continue

            # Evitar colisión si la fecha_swap ya existe en la serie
            if fecha_swap in df.index:
                i += 1
                continue

            # --- VECINOS Y SCORE 1: FECHA ACTUAL (ORIGINAL) ---
            fecha_prev_orig = df.index[i - 1]
            fecha_next_orig = df.index[i + 1]

            score_orig = 0.0

            # 1.1 Coherencia temporal
            if fecha_prev_orig < fecha_actual < fecha_next_orig:
                score_orig += 10.0
            else:
                score_orig -= 10.0

            # 1.2 Monotonía PPT
            if col_ppt in df.columns:
                v_prev = df.at[fecha_prev_orig, col_ppt]
                v_act = df.at[fecha_actual, col_ppt]
                v_next = df.at[fecha_next_orig, col_ppt]

                if not pd.isna(v_act):
                    if not pd.isna(v_prev) and v_act >= v_prev:
                        score_orig += 15.0
                    elif not pd.isna(v_prev) and v_act < v_prev:
                        score_orig -= 15.0

                    if not pd.isna(v_next) and v_next >= v_act:
                        score_orig += 15.0
                    elif not pd.isna(v_next) and v_next < v_act:
                        score_orig -= 15.0

            # 1.3 Continuidad Variables Secundarias
            for c in cols_secundarias:
                v_act = df.at[fecha_actual, c]
                v_prev = df.at[fecha_prev_orig, c]
                v_next = df.at[fecha_next_orig, c]

                if not pd.isna(v_act):
                    d_prev = abs(v_act - v_prev) if not pd.isna(v_prev) else np.nan
                    d_next = abs(v_next - v_act) if not pd.isna(v_next) else np.nan

                    if not pd.isna(d_prev) and not pd.isna(d_next):
                        score_orig += 2.0 / (1.0 + d_prev + d_next)

            # --- VECINOS Y SCORE 2: FECHA SWAP (INVERTIDA) ---
            # Se identifican los verdaderos vecinos temporales si la fecha fuera 'fecha_swap'
            fechas_menores = df.index[df.index < fecha_swap]
            fechas_mayores = df.index[df.index > fecha_swap]

            # Si la fecha swap queda aislada en los extremos de la serie, se omite
            if len(fechas_menores) == 0 or len(fechas_mayores) == 0:
                i += 1
                continue

            fecha_prev_swap = fechas_menores[-1]
            fecha_next_swap = fechas_mayores[0]

            score_swap = 0.0

            # 2.1 Coherencia temporal estricta en el nuevo punto
            if fecha_prev_swap < fecha_swap < fecha_next_swap:
                score_swap += 10.0
            else:
                score_swap -= 10.0

            # 2.2 Monotonía PPT con sus nuevos vecinos
            if col_ppt in df.columns:
                v_prev = df.at[fecha_prev_swap, col_ppt]
                v_act = df.at[fecha_actual, col_ppt]  # El dato meteorológico no cambia, solo su fecha
                v_next = df.at[fecha_next_swap, col_ppt]

                if not pd.isna(v_act):
                    if not pd.isna(v_prev) and v_act >= v_prev:
                        score_swap += 15.0
                    elif not pd.isna(v_prev) and v_act < v_prev:
                        score_swap -= 15.0

                    if not pd.isna(v_next) and v_next >= v_act:
                        score_swap += 15.0
                    elif not pd.isna(v_next) and v_next < v_act:
                        score_swap -= 15.0

            # 2.3 Continuidad Variables Secundarias con sus nuevos vecinos
            for c in cols_secundarias:
                v_act = df.at[fecha_actual, c]
                v_prev = df.at[fecha_prev_swap, c]
                v_next = df.at[fecha_next_swap, c]

                if not pd.isna(v_act):
                    d_prev = abs(v_act - v_prev) if not pd.isna(v_prev) else np.nan
                    d_next = abs(v_next - v_act) if not pd.isna(v_next) else np.nan

                    if not pd.isna(d_prev) and not pd.isna(d_next):
                        score_swap += 2.0 / (1.0 + d_prev + d_next)

            # --- DECISIÓN Y CORRECCIÓN ---
            if score_swap > score_orig and score_swap > 0:
                # Reemplazar la etiqueta en el índice y reordenar el DataFrame
                idx_series = df.index.to_series()
                idx_series.iloc[i] = fecha_swap
                df.index = pd.DatetimeIndex(idx_series)
                df = df.sort_index()

                # Al reordenar la serie, reiniciamos el recorrido desde la posición previa
                i = max(1, i - 1)
                continue

            elif (
                abs(score_swap - score_orig) < 5.0
                and score_orig <= 0
                and score_swap <= 0
            ):
                print(
                    f"[CCal17 - Indeterminado] Fecha Orig: {fecha_actual} | "
                    f"Fecha Prop: {fecha_swap} | Score Orig: {score_orig:.2f} | "
                    f"Score Swapped: {score_swap:.2f} | Motivo: Ambigüedad no resoluble por ruptura de secuencia/PPT."
                )

        i += 1
    
    Coherencia_Fecha.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal4_coherencia_fecha.variables   = ['Precipitación Acumulada'] # Variables requeridas para funcionar
CCal4_coherencia_fecha.nombre      = 'Coherencia de Fechas'  # Nombre visible
CCal4_coherencia_fecha.obligatorio = True
CCal4_coherencia_fecha.visible     = True