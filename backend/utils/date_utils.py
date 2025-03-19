# date_utils.py
import datetime

# Pasa fecha en formato YYYY-mm-dd a datetime de mongo.
def stringDate_to_dateDate(fecha):
    try:
        # Si es de tipo 'date' lo pasa a 'datetime' (Que es el date de mongo)
        if isinstance(fecha, datetime.date):
            return datetime.datetime(fecha.year, fecha.month, fecha.day)
        # Si es de tipo 'str' lo pasa a 'datetime', a menos que sea '', en ese caso lo devuelve.
        elif isinstance(fecha, str):
            if fecha == "":
                return fecha
            return datetime.datetime.strptime(fecha, "%Y-%m-%d")
        else:
            raise TypeError("El tipo de entrada no es válido. Se esperaba 'str' o 'datetime.date'")
    except ValueError as ve:
        raise ValueError(f"Formato de fecha inválido: {fecha}. Error: {ve}")
    except Exception as e:
        raise RuntimeError(f"Ocurrió un error inesperado: {e}")
