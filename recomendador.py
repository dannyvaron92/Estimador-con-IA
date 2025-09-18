FIBONACCI = [0, 1, 2, 3, 5, 8, 13, 21]

def redondear_fibonacci(valor):
    return min(FIBONACCI, key=lambda x: abs(x - valor))

def obtener_recomendacion(fib_valor):
    if fib_valor <= 8:
        return "✅ Historia aceptable."
    elif fib_valor <= 13:
        return "⚠️ Considera dividir o refinar la historia."
    else:
        return "❌ División recomendada."

def recomendar_con_ia(descripcion, tecnica, desarrollo, dependencias, claridad, riesgos, pivote):
    if not pivote:
        return "No hay historia pivote definida para comparar."

    diferencias = []
    if tecnica != pivote['tecnica']:
        diferencias.append("Técnica diferente")
    if desarrollo != pivote['desarrollo']:
        diferencias.append("Desarrollo diferente")
    if dependencias != pivote['dependencias']:
        diferencias.append("Dependencias distintas")
    if claridad != pivote['claridad']:
        diferencias.append("Claridad distinta")
    if riesgos != pivote['riesgos']:
        diferencias.append("Riesgos distintos")

    texto = f"Comparando con la historia pivote: {', '.join(diferencias)}. "
    if len(descripcion) < 50:
        texto += "La descripción es muy breve. "
    elif len(descripcion) > 300:
        texto += "La descripción es extensa. "
    else:
        texto += "La descripción tiene una longitud adecuada. "

    if len(diferencias) == 0:
        texto += "La historia parece estar correctamente punteada."
    else:
        texto += "Revisa los criterios que difieren de la historia pivote."

    return texto[:200]
