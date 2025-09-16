def format_time(time_seconds: float) -> str:
    minutes = int(time_seconds / 60)
    seconds = round(time_seconds - minutes * 60, 3)
    return f"{minutes}:{seconds:06.3f}" if minutes > 0 else f"{seconds:06.3f}"

def unformat_time(time_str: str) -> float:
    split_time = time_str.split(":")
    if len(split_time) == 2:
        minutes, seconds = split_time
        return float(minutes) * 60 + float(seconds)
    else:
        return float(split_time[0])
    
def decode_mbld_result(n: float) -> str:
    """Decodifica un número compacto del tipo que usas en ejemplos.

    Regla aplicada:
    - Los últimos 4 dígitos del entero representan segundos totales.
    - La parte entera previa (leading) se usa para extraer los dos primeros dígitos.
        corrects = 99 - int(first_two_digits)
    - El decimal (dos cifras) representa errores; attempts = corrects + errors

    Ejemplo: 7403273.0 -> leading=740 -> first_two='74' -> corrects=25, errors=0 -> 25/25 54:33
    """
    val_int = int(n)
    # errores desde el decimal (por ejemplo .03 -> 3)
    errors = int(round((n - val_int) * 100))

    # parte leading (todo menos los últimos 4 dígitos)
    leading = val_int // 10000
    leading_s = str(leading)
    if len(leading_s) < 2:
        first_two = int(leading_s)
    else:
        first_two = int(leading_s[:2])

    corrects = 99 - first_two
    attempts = corrects + errors

    # tiempo: últimos 4 dígitos -> segundos totales
    seconds = val_int % 10000
    if seconds >= 3600:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        time_str = f"{h}:{m:02d}:{s:02d}"
    else:
        m = seconds // 60
        s = seconds % 60
        time_str = f"{m:02d}:{s:02d}"

    return f"{corrects}/{attempts} {time_str}"

def convert_mbld_kinch(text: str) -> float:
    """Convierte un texto del tipo 'C/A M:SS' o 'C/A H:MM:SS' a un número según la regla:

    - Primero: resultado1 = corrects - (attempts - corrects) = 2*corrects - attempts
    - Segundo: calcular horas totales del tiempo; time_hours = hours + minutes/60 + seconds/3600
        time_component = 1 - time_hours
    - Resultado final = resultado1 + time_component

    Ejemplo: '25/25 54:33' -> resultado1 = 25, time_hours = 54.55/60 = 0.909166...,
    time_component = 0.090833..., resultado final ≈ 25.090833
    """
    if not text or '/' not in text:
        raise ValueError("Texto inválido, se espera 'corrects/attempts time'")

    parts = text.split()
    if len(parts) < 2:
        raise ValueError("Formato inválido, falta la parte de tiempo")

    # parse corrects/attempts
    try:
        corr_str, att_str = parts[0].split('/')
        corrects = int(corr_str)
        attempts = int(att_str)
    except Exception as e:
        raise ValueError(f"No se pudo parsear corrects/attempts: {e}")

    # parse time (supports M:SS or H:MM:SS)
    time_str = parts[1]
    time_parts = time_str.split(':')
    if len(time_parts) == 2:
        m = int(time_parts[0])
        s = int(time_parts[1])
        h = 0
    elif len(time_parts) == 3:
        h = int(time_parts[0])
        m = int(time_parts[1])
        s = int(time_parts[2])
    else:
        raise ValueError("Formato de tiempo inválido")

    # resultado1
    points = 2 * corrects - attempts

    # tiempo en horas
    total_hours = h + m / 60.0 + s / 3600.0
    time_component = 1.0 - total_hours

    return round(points + time_component, 3)


def encode_mbld_result(text: str) -> float:
    """Convierte un texto 'C/A M:SS' o 'C/A H:MM:SS' al número compacto usado en el API.

    Regla inversa de decode_mbld_result:
    - corrects/attempts parsing
    - errors = attempts - corrects
    - first_two = 99 - corrects
    - leading = first_two * 10  (se añade un 0 como sufijo para reproducir el formato "74" -> 740)
    - val_int = leading * 10000 + seconds_total
    - resultado = val_int + errors/100

    Esta función asume que la representación usada por el API sigue el patrón observado
    en los ejemplos (p.ej. 7403273.0 -> 25/25 54:33).
    """
    if not text or '/' not in text:
        raise ValueError("Texto inválido, se espera 'corrects/attempts time'")

    parts = text.split()
    if len(parts) < 2:
        raise ValueError("Formato inválido, falta la parte de tiempo")

    # parse corrects/attempts
    try:
        corr_str, att_str = parts[0].split('/')
        corrects = int(corr_str)
        attempts = int(att_str)
    except Exception as e:
        raise ValueError(f"No se pudo parsear corrects/attempts: {e}")

    # parse time (supports M:SS or H:MM:SS)
    time_str = parts[1]
    time_parts = time_str.split(':')
    if len(time_parts) == 2:
        m = int(time_parts[0])
        s = int(time_parts[1])
        h = 0
    elif len(time_parts) == 3:
        h = int(time_parts[0])
        m = int(time_parts[1])
        s = int(time_parts[2])
    else:
        raise ValueError("Formato de tiempo inválido")

    # compute errors and first_two
    errors = attempts - corrects
    first_two = 99 - corrects

    # build leading as first_two followed by a zero (observed pattern)
    leading = first_two * 10

    # compute total seconds
    total_seconds = h * 3600 + m * 60 + s

    val_int = leading * 10000 + total_seconds
    result = float(val_int) + float(errors) / 100.0
    return round(result, 2)

def kinch_to_mbld_text(kinch: float | str) -> str:
    """Convierte un valor kinch (p. ej. 2.75) a texto 'C/C M:SS' o 'C/C H:MM:SS'.

    Regla:
    - La parte entera se usa como corrects y attempts iguales: corrects/attempts = N/N.
    - La parte fraccional f = kinch - N corresponde a time_component = f.
    - time_hours = 1 - time_component  => tiempo real en horas.
    - Se formatea el tiempo a M:SS o H:MM:SS según corresponda.
    """
    k = float(kinch)
    corrects = int(k)
    frac = k - corrects
    if frac < 0:
        frac = 0.0
    # time_component = frac  => total_hours = 1 - frac
    total_hours = 1.0 - frac
    if total_hours < 0:
        total_hours = 0.0

    total_seconds = int(round(total_hours * 3600))
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60

    time_str = f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
    return f"{corrects}/{corrects} {time_str}"