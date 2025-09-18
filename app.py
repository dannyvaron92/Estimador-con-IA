import os
import sqlite3
from flask import Flask, render_template, request, redirect
from recomendador import redondear_fibonacci, obtener_recomendacion, recomendar_con_ia

app = Flask(__name__)
DB_NAME = 'hu_evaluations.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS evaluations ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "description TEXT,"
        "tecnica INTEGER,"
        "desarrollo INTEGER,"
        "dependencias INTEGER,"
        "claridad INTEGER,"
        "riesgos INTEGER,"
        "total INTEGER,"
        "fibonacci INTEGER,"
        "recomendacion TEXT,"
        "analisis TEXT,"
        "fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS pivote ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "hu TEXT,"
        "tecnica INTEGER,"
        "desarrollo INTEGER,"
        "dependencias INTEGER,"
        "claridad INTEGER,"
        "riesgos INTEGER,"
        "fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        tecnica = int(request.form['tecnica'])
        desarrollo = int(request.form['desarrollo'])
        dependencias = int(request.form['dependencias'])
        claridad = int(request.form['claridad'])
        riesgos = int(request.form['riesgos'])

        claridad_mod = (claridad - 5) * -1
        total = tecnica + desarrollo + dependencias + claridad + riesgos
        fib_valor = redondear_fibonacci(total)
        recomendacion = obtener_recomendacion(fib_valor)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT hu, tecnica, desarrollo, dependencias, claridad, riesgos FROM pivote ORDER BY fecha DESC LIMIT 1")
        pivote = cursor.fetchone()
        if pivote:
            hu_pivote, t_p, d_p, dep_p, c_p, r_p = pivote
            analisis = recomendar_con_ia(descripcion, tecnica, desarrollo, dependencias, claridad, riesgos,
                                         hu_pivote, t_p, d_p, dep_p, c_p, r_p)
        else:
            analisis = "No hay historia pivote definida para comparar."

        cursor.execute(
            "INSERT INTO evaluations (description, tecnica, desarrollo, dependencias, claridad, riesgos, total, fibonacci, recomendacion, analisis) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (descripcion, tecnica, desarrollo, dependencias, claridad, riesgos, total, fib_valor, recomendacion, analisis)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM evaluations ORDER BY fecha DESC')
    historial = cursor.fetchall()
    conn.close()
    return render_template('index.html', historial=historial)

@app.route('/pivote', methods=['GET', 'POST'])
def pivote():
    if request.method == 'POST':
        hu = request.form['hu']
        tecnica = int(request.form['tecnica'])
        desarrollo = int(request.form['desarrollo'])
        dependencias = int(request.form['dependencias'])
        claridad = int(request.form['claridad'])
        riesgos = int(request.form['riesgos'])

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pivote (hu, tecnica, desarrollo, dependencias, claridad, riesgos) VALUES (?, ?, ?, ?, ?, ?)",
                       (hu, tecnica, desarrollo, dependencias, claridad, riesgos))
        conn.commit()
        conn.close()
        return redirect('/pivote')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pivote ORDER BY fecha DESC")
    pivotes = cursor.fetchall()
    conn.close()
    return render_template('pivote.html', pivotes=pivotes)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
