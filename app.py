import os
import sqlite3
from flask import Flask, render_template, request, redirect, flash
from recomendador import recomendar_con_ia

app = Flask(__name__)
app.secret_key = 'supersecretkey'
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
        "fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS hu_pivote ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "descripcion TEXT,"
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
        try:
            tecnica = int(request.form['tecnica'])
            desarrollo = int(request.form['desarrollo'])
            dependencias = int(request.form['dependencias'])
            claridad = int(request.form['claridad'])
            riesgos = int(request.form['riesgos'])
        except ValueError:
            flash("Todos los criterios deben ser valores numéricos.")
            return redirect('/')

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hu_pivote ORDER BY fecha DESC LIMIT 1")
        pivote = cursor.fetchone()
        conn.close()

        if not pivote:
            flash("No hay historia pivote definida. Por favor ingresa una primero.")
            return redirect('/')

        recomendacion = recomendar_con_ia(
            descripcion, tecnica, desarrollo, dependencias, claridad, riesgos, pivote
        )

        total = tecnica + desarrollo + dependencias + claridad + riesgos
        fibonacci = min([0, 1, 2, 3, 5, 8, 13, 21], key=lambda x: abs(x - total))

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO evaluations (description, tecnica, desarrollo, dependencias, claridad, riesgos, total, fibonacci, recomendacion) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (descripcion, tecnica, desarrollo, dependencias, claridad, riesgos, total, fibonacci, recomendacion)
        )
        conn.commit()
        cursor.execute('SELECT * FROM evaluations ORDER BY fecha DESC')
        historial = cursor.fetchall()
        conn.close()
        flash("Historia evaluada exitosamente.")
        return render_template('index.html', historial=historial)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM evaluations ORDER BY fecha DESC')
    historial = cursor.fetchall()
    conn.close()
    return render_template('index.html', historial=historial)

@app.route('/pivote', methods=['GET', 'POST'])
def pivote():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        try:
            tecnica = int(request.form['tecnica'])
            desarrollo = int(request.form['desarrollo'])
            dependencias = int(request.form['dependencias'])
            claridad = int(request.form['claridad'])
            riesgos = int(request.form['riesgos'])
        except ValueError:
            flash("Todos los criterios deben ser valores numéricos.")
            return redirect('/pivote')

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO hu_pivote (descripcion, tecnica, desarrollo, dependencias, claridad, riesgos) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (descripcion, tecnica, desarrollo, dependencias, claridad, riesgos)
        )
        conn.commit()
        conn.close()
        flash("Historia pivote actualizada correctamente.")
        return redirect('/pivote')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hu_pivote ORDER BY fecha DESC LIMIT 1")
    pivote_actual = cursor.fetchone()
    conn.close()
    return render_template('pivote.html', pivote=pivote_actual)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
