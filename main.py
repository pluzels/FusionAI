import os
import importlib
from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# fungsi untuk memuat model secara dinamis dari folder "models" atau "models/visionmodels"
def load_model(model_name, is_vision=False):
    try:
        if is_vision:
            model_module = importlib.import_module(f"models.visionmodels.{model_name}")
        else:
            model_module = importlib.import_module(f"models.{model_name}")
        return model_module
    except ModuleNotFoundError:
        return None

# konversi base64 image menjadi objek image
def image_base64_to_pil(image_base64):
    try:
        if image_base64.startswith('data:image/jpeg;base64,'):
            image_base64 = image_base64.replace('data:image/jpeg;base64,', '')
        elif image_base64.startswith('data:image/png;base64,'):
            image_base64 = image_base64.replace('data:image/png;base64,', '')
        
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))
        return image
    except Exception:
        return None

# endpoint untuk model teks
@app.route('/models/<model_name>', methods=['GET'])
def text_model_endpoint(model_name):
    model_module = load_model(model_name)
    
    if model_module is None:
        return jsonify({"error": "model not found"}), 404

    prompt = request.args.get('prompt', '')
    response = model_module.generate_response(prompt=prompt)

    return jsonify(response)

# endpoint untuk model vision
@app.route('/models/visionmodels/<model_name>', methods=['POST'])
def vision_model_endpoint(model_name):
    prompt = request.json.get('prompt', '')
    image_base64 = request.json.get('image_base64', '')

    model_module = load_model(model_name, is_vision=True)
    
    if model_module is None:
        return jsonify({"error": "model not found"}), 404

    if image_base64:
        image = image_base64_to_pil(image_base64)
        if not image:
            return jsonify({"error": "invalid image data"}), 400
    else:
        image = None

    response = model_module.generate_response(prompt, image_base64)

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
