def recomendar_con_ia(descripcion, tecnica, desarrollo, dependencias, claridad, riesgos, pivote):
    puntaje_actual = tecnica + desarrollo + dependencias + claridad + riesgos
    puntaje_pivote = pivote[2] + pivote[3] + pivote[4] + pivote[5] + pivote[6]
    diferencia = abs(puntaje_actual - puntaje_pivote)

    if diferencia <= 2:
        return "✅ Historia similar a la pivote. Aceptable."
    elif diferencia <= 5:
        return "⚠️ Historia algo diferente. Considera revisar dependencias o claridad."
    else:
        return "❌ Historia muy distinta a la pivote. Recomendamos dividirla o redefinirla."
