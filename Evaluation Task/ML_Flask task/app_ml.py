import traceback
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class ML:
    def __init__(self):
        self.available_models = {
            "face_detection": "/additional_drive/ML/face_detection",
            "car_detection": "/additional_drive/ML/car_detection",
            "shoe_detection": "/additional_drive/ML/shoe_detection",
            "cloth_detection": "/additional_drive/ML/cloth_detection",
            "signal_detection": "/additional_drive/ML/signal_detection",
            "water_level_detection": "/additional_drive/ML/water_level_detection",
            "missile_detection": "/additional_drive/ML/missile_detection"
        }
        self.loaded_models_limit = 2
        self.loaded_models = {
            model: self.load_weights(model)
            for model in list(self.available_models)[:self.loaded_models_limit]
        }
        self.requests_count = {model: 0 for model in self.loaded_models}

    def load_weights(self, model):
        return self.available_models.get(model, None)

    def load_balancer(self, new_model):
        # Increment the requests count for each loaded model
        for model in self.loaded_models:
            self.requests_count[model] += 1

        # Check if the new_model is not already loaded
        if new_model not in self.loaded_models:
            # Find the model with the least number of requests
            least_used_model = min(self.requests_count, key=self.requests_count.get)
            # Replace the least used model with the new_model
            del self.loaded_models[least_used_model]
            self.loaded_models[new_model] = self.load_weights(new_model)
            self.requests_count[new_model] = 0

ml = ML()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_loaded_models', methods=['GET','POST'])
def get_loaded_models():
    return ml.loaded_models

@app.route('/process_request', methods=['GET','POST'])
def process_request():
    try:
        model = request.form["model"]
        if model is None:
            return "No model specified in the request.", 400
        if model not in ml.loaded_models:
            ml.load_balancer(model)
        ml.requests_count[model] += 1  # Increment requests count for the processed model
        prediction_result = "processed by " + ml.loaded_models[model]
        return prediction_result
    except Exception as e:
        return str(traceback.format_exc()), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
