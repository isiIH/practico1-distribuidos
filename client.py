from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Renderiza la página de inicio con el formulario para unirse al juego
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)