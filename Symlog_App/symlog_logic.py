# symlog_logic.py

import pandas as pd
from symlog_data import all_scales_data, scaling_table, BASE_SIZE, SCALE_FACTOR, MIN_MARKER_SIZE

def scale_score(raw_score, table):
    if raw_score == 0: return 0
    abs_score = abs(raw_score)
    scaled_value = table[-1][1]
    for limit, unit in table:
        if abs_score <= limit:
            scaled_value = unit
            break
    return scaled_value if raw_score > 0 else -scaled_value

def calculate_from_manual_scores(participant_name, scale_name, scores_dict):
    items = all_scales_data.get(scale_name)
    if not items:
        return None, False, f"Error: Escala '{scale_name}' no encontrada."
    
    raw_sums = {'U': 0, 'D': 0, 'P': 0, 'N': 0, 'F': 0, 'B': 0}
    is_ok = True
    messages = []
    
    for item_data in items:
        item_text = item_data['item']
        dimension_code = item_data['dimension']
        weighted_scores = item_data['weighted_scores']
        score_index = scores_dict.get(item_text, 0)
        
        try:
            if not (0 <= score_index < len(weighted_scores)):
                raise IndexError(f"Índice {score_index} fuera de rango para el ítem '{item_text[:20]}...'")
            
            weight = weighted_scores[score_index]
            for char in dimension_code:
                if char in raw_sums:
                    raw_sums[char] += weight
                else:
                    messages.append(f"Advertencia: Dimensión '{char}' desconocida en el código '{dimension_code}' para el ítem '{item_text[:20]}...'.")
        except IndexError as e:
            messages.append(f"Error de índice: {e}. Se usará 0.")
            is_ok = False
        except Exception as e:
            messages.append(f"Error al calcular para '{item_text[:20]}...': {e}")
            is_ok = False
            
    if not is_ok:
        messages.append("El cálculo manual falló debido a errores críticos.")
        return None, False, "\n".join(messages)

    ud_raw = raw_sums['U'] - raw_sums['D']
    pn_raw = raw_sums['P'] - raw_sums['N']
    fb_raw = raw_sums['F'] - raw_sums['B']
    
    ud_scaled = scale_score(ud_raw, scaling_table)
    pn_scaled = scale_score(pn_raw, scaling_table)
    fb_scaled = scale_score(fb_raw, scaling_table)
    
    result = {
        'name': participant_name, 'scale': scale_name,
        'ud': ud_scaled, 'pn': pn_scaled, 'fb': fb_scaled,
        'raw_ud': ud_raw, 'raw_pn': pn_raw, 'raw_fb': fb_raw
    }
    
    final_message = "\n".join(messages) if messages else "Cálculo manual exitoso."
    return result, True, final_message

def calculate_from_excel(df, scale_name):
    items = all_scales_data.get(scale_name)
    if not items:
        return [], [f"Error Crítico: No se encontraron ítems para la escala '{scale_name}'."]
    
    num_items = len(items)
    if df.shape[0] != num_items:
        return [], [f"Error Crítico: El número de filas ({df.shape[0]}) no coincide con los ítems de la escala ({num_items})."]

    results = []
    warnings = []
    participant_columns = df.columns[1:]

    for p_col in participant_columns:
        p_name = str(p_col).strip()
        if not p_name:
            warnings.append(f"Advertencia: Omitiendo columna con nombre vacío: '{p_col}'")
            continue
        
        p_scores = df[p_col]
        raw_sums = {'U': 0, 'D': 0, 'P': 0, 'N': 0, 'F': 0, 'B': 0}
        
        for i, item_info in enumerate(items):
            score_index = 0
            raw_score = p_scores.iloc[i]
            if pd.isna(raw_score) or raw_score is None:
                warnings.append(f"Advertencia [{p_name}]: Valor nulo en fila {i+1}. Se usará 0.")
            else:
                try:
                    score_index = int(raw_score)
                    if not (0 <= score_index <= 4):
                        warnings.append(f"Advertencia [{p_name}]: Valor '{raw_score}' en fila {i+1} fuera de rango (0-4). Se usará 0.")
                        score_index = 0
                except (ValueError, TypeError):
                    warnings.append(f"Advertencia [{p_name}]: Valor '{raw_score}' en fila {i+1} no es un número. Se usará 0.")

            weight = item_info['weighted_scores'][score_index]
            for char in item_info['dimension']:
                if char in raw_sums:
                    raw_sums[char] += weight

        ud_raw = raw_sums['U'] - raw_sums['D']
        pn_raw = raw_sums['P'] - raw_sums['N']
        fb_raw = raw_sums['F'] - raw_sums['B']

        results.append({
            'name': p_name, 'scale': scale_name,
            'ud': scale_score(ud_raw, scaling_table), 
            'pn': scale_score(pn_raw, scaling_table), 
            'fb': scale_score(fb_raw, scaling_table),
            'raw_ud': ud_raw, 'raw_pn': pn_raw, 'raw_fb': fb_raw
        })

    return results, warnings

def calculate_marker_size(ud_score):
    if not isinstance(ud_score, (int, float)):
        ud_score = 0
    marker_size = BASE_SIZE + ud_score * SCALE_FACTOR
    return max(MIN_MARKER_SIZE, marker_size)