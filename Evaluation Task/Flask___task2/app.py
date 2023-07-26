from flask import Flask, request, render_template
import hashlib

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=[ 'POST'])
def upload():
    if request.method == 'POST' and 'image' in request.files:
        image_file = request.files['image']
        if image_file.filename == '':
            return "No selected image file.", 400

        # Calculate the MD5 hash of the image file
        md5_hash = hashlib.md5()
        while chunk := image_file.read(8192):
            md5_hash.update(chunk)

        image_file.seek(0)  # Reset the file pointer to the beginning

        return render_template('index.html', hash=md5_hash.hexdigest())

if __name__ == '__main__':
    app.run(debug=True)


