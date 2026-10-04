import numpy as np
import pandas as pd


def CCal17_FechasAmbiguas(df):
    """Control de Calidad N°17: Detección y corrección de fechas ambiguas (DD/MM/YYYY vs MM/DD/YYYY).

    Asume que el DataFrame ya viene indexado por DatetimeIndex y ordenado
    cronológicamente.

    Entrada:
        df: DataFrame indexado por DatetimeIndex.

    Salida:
        return df, eliminados
    """
    eliminados = 0

    # Variable explícita de texto para la columna de PPT acumulada
    col_ppt = "PPT"

    # Identificar variables secundarias
    cols_num = df.select_dtypes(include=[np.number]).columns.tolist()
    cols_secundarias = [c for c in cols_num if c != col_ppt]

    # Recorrido por el DataFrame evaluando ambigüedad en día/mes
    indices = df.index

    for i in range(1, len(indices) - 1):
        fecha_actual = indices[i]

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
                # Si el intercambio genera una fecha inválida (ej: 31 de Febrero), se ignora
                continue

            fecha_prev = indices[i - 1]
            fecha_next = indices[i + 1]

            # --- SCORE 1: FECHA ACTUAL (ORIGINAL) ---
            score_orig = 0.0

            # 1.1 Coherencia temporal estricta
            if fecha_prev < fecha_actual < fecha_next:
                score_orig += 10.0
            else:
                score_orig -= 10.0

            # 1.2 Coherencia PPT Acumulada (Monotonía)
            if col_ppt in df.columns:
                val_prev = df.at[fecha_prev, col_ppt]
                val_act = df.at[fecha_actual, col_ppt]
                val_next = df.at[fecha_next, col_ppt]

                if not pd.isna(val_act):
                    if not pd.isna(val_prev) and val_act >= val_prev:
                        score_orig += 15.0
                    elif not pd.isna(val_prev) and val_act < val_prev:
                        score_orig -= 15.0

                    if not pd.isna(val_next) and val_next >= val_act:
                        score_orig += 15.0
                    elif not pd.isna(val_next) and val_next < val_act:
                        score_orig -= 15.0

            # 1.3 Coherencia Variables Secundarias
            for c in cols_secundarias:
                v_act = df.at[fecha_actual, c]
                v_prev = df.at[fecha_prev, c]
                v_next = df.at[fecha_next, c]

                if not pd.isna(v_act):
                    diff_prev = (
                        abs(v_act - v_prev) if not pd.isna(v_prev) else np.nan
                    )
                    diff_next = (
                        abs(v_next - v_act) if not pd.isna(v_next) else np.nan
                    )

                    if not pd.isna(diff_prev) and not pd.isna(diff_next):
                        score_orig += 2.0 / (1.0 + diff_prev + diff_next)

            # --- SCORE 2: FECHA SWAP (INVERTIDA) ---
            score_swap = 0.0

            # 2.1 Coherencia temporal estricta
            if fecha_prev < fecha_swap < fecha_next:
                score_swap += 10.0
            else:
                score_swap -= 10.0

            # 2.2 Coherencia PPT Acumulada
            if col_ppt in df.columns:
                val_prev = df.at[fecha_prev, col_ppt]
                val_act = df.at[fecha_actual, col_ppt]
                val_next = df.at[fecha_next, col_ppt]

                if not pd.isna(val_act):
                    if not pd.isna(val_prev) and val_act >= val_prev:
                        score_swap += 15.0
                    elif not pd.isna(val_prev) and val_act < val_prev:
                        score_swap -= 15.0

                    if not pd.isna(val_next) and val_next >= val_act:
                        score_swap += 15.0
                    elif not pd.isna(val_next) and val_next < val_act:
                        score_swap -= 15.0

            # 2.3 Coherencia Variables Secundarias
            for c in cols_secundarias:
                v_act = df.at[fecha_actual, c]
                v_prev = df.at[fecha_prev, c]
                v_next = df.at[fecha_next, c]

                if not pd.isna(v_act):
                    diff_prev = (
                        abs(v_act - v_prev) if not pd.isna(v_prev) else np.nan
                    )
                    diff_next = (
                        abs(v_next - v_act) if not pd.isna(v_next) else np.nan
                    )

                    if not pd.isna(diff_prev) and not pd.isna(diff_next):
                        score_swap += 2.0 / (1.0 + diff_prev + diff_next)

            # --- RESOLUCIÓN Y ACCIÓN ---
            # Caso 1: La fecha invertida es claramente superior y coherente
            if score_swap > score_orig and score_swap > 0:
                idx_list = df.index.to_series()
                idx_list.iloc[i] = fecha_swap
                df.index = pd.DatetimeIndex(idx_list)

            # Caso 2: Ambas opciones son incoherentes o no se puede definir con certeza
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

    return df, eliminados