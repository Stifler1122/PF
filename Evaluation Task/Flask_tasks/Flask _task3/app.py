# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table', methods=['POST'])
def generate_table():
    number = request.form.get('number')
    if number.isdigit():
        number = int(number)
        table = [[str(number) + ' x ' + str(i) + ' =', number * i] for i in range(1, 11)]
        return render_template('index.html', table=table, number=number)
    else:
        return render_template('index.html', error_message="Invalid input. Please enter a valid number.")

if __name__ == '__main__':
    app.run(debug=True)

