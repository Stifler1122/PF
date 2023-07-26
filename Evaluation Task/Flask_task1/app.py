from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/square', methods=['POST'])
def square_number():
    number = request.form.get('number')
    if number is not None and number.isdigit():
        number = int(number)
        result = number ** 2
        return f"The square of {number} is {result}"
    else:
        return "Invalid input. Please provide a valid number.", 400

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

