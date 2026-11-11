import fitparse
import os

# Fator de conversão do formato interno da Garmin (Semicircles) para Graus Decimais
SEMICIRCLE_TO_DEGREE = 180 / (2**31)

def parse_fit_file(file_path: str) -> dict:
    """
    Lê um ficheiro .FIT do Garmin e extrai estatísticas globais e a linha do tempo (timeline)
    com GPS e ritmo cardíaco para análise tática e física do árbitro.
    """
    fitfile = fitparse.FitFile(file_path)
    
    # Dicionário principal que será devolvido e guardado na Base de Dados
    stats = {
        "total_distance_km": 0.0,
        "max_speed_kmh": 0.0,
        "sprints_count": 0,
        "avg_heart_rate": 0,
        "max_heart_rate": 0,
        "calories": 0,
        "gps_heatmap_data": []  # Agora vai guardar a fita do tempo completa
    }

    sprint_threshold_kmh = 25.0
    is_sprinting = False

    # 1. Extrair os dados resumidos (Mensagem 'session')
    for record in fitfile.get_messages('session'):
        for data in record:
            if data.name == 'total_distance' and data.value is not None:
                stats["total_distance_km"] = round(data.value / 1000, 2)
            elif data.name == 'max_speed' and data.value is not None:
                stats["max_speed_kmh"] = round(data.value * 3.6, 2)
            elif data.name == 'avg_heart_rate' and data.value is not None:
                stats["avg_heart_rate"] = data.value
            elif data.name == 'max_heart_rate' and data.value is not None:
                stats["max_heart_rate"] = data.value
            elif data.name == 'total_calories' and data.value is not None:
                stats["calories"] = data.value

    # 2. Extrair a linha do tempo segundo a segundo (Mensagem 'record')
    for record in fitfile.get_messages('record'):
        lat = None
        lon = None
        speed_kmh = 0.0
        heart_rate = None
        timestamp = None

        for data in record:
            if data.name == 'timestamp' and data.value is not None:
                # Converter para formato de texto ISO 8601 (JSON friendly)
                timestamp = data.value.isoformat() 
            elif data.name == 'position_lat' and data.value is not None:
                lat = data.value * SEMICIRCLE_TO_DEGREE
            elif data.name == 'position_long' and data.value is not None:
                lon = data.value * SEMICIRCLE_TO_DEGREE
            elif data.name == 'speed' and data.value is not None:
                speed_kmh = data.value * 3.6
            elif data.name == 'heart_rate' and data.value is not None:
                heart_rate = data.value

        # Construir a timeline (só guardamos se houver timestamp válido)
        if timestamp:
            stats["gps_heatmap_data"].append({
                "time": timestamp,
                "lat": lat,
                "lon": lon,
                "hr": heart_rate,
                "speed_kmh": round(speed_kmh, 2) if speed_kmh else 0.0
            })

        # Lógica de deteção de Sprints (velocidade > 25 km/h)
        if speed_kmh > sprint_threshold_kmh:
            if not is_sprinting:
                stats["sprints_count"] += 1
                is_sprinting = True
        else:
            is_sprinting = False

    return stats