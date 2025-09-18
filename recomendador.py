from difflib import SequenceMatcher

FIBONACCI = [0, 1, 2, 3, 5, 8, 13, 21]

def redondear_fibonacci(valor):
    return min(FIBONACCI, key=lambda x: abs(x - valor))

def obtener_recomendacion(fib_valor):
    if fib_valor <= 8:
        return "✅ Historia aceptable."
    elif fib_valor < 13 and fib_valor > 8:
        return "⚠️ Considera dividir o refinar la historia."
    else:
        return "❌ División recomendada."

def recomendar_con_ia(hu, tecnica, desarrollo, dependencias, claridad, riesgos,
                      hu_pivote, t_p, d_p, dep_p, c_p, r_p):
    similitud = SequenceMatcher(None, hu, hu_pivote).ratio()
    diferencia_puntaje = abs((tecnica + desarrollo + dependencias + claridad + riesgos) -
                             (t_p + d_p + dep_p + c_p + r_p))
    analisis = f"Similitud textual: {similitud:.2f}. "
    if similitud > 0.7 and diferencia_puntaje <= 3:
        analisis += "La historia parece estar correctamente puntuada."
    elif similitud > 0.7:
        analisis += "La historia es similar pero el puntaje difiere significativamente."
    else:
        analisis += "La historia es diferente a la pivote, se recomienda revisión."
    return analisis[:200]
