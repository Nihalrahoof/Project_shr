# Web Application Code
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Global variable to hold product array
product_array = []

# Route to update the product array
@app.route('/update_products', methods=['POST'])
def update_products():
    global product_array
    data = request.json
    if 'products' in data:
        product_array = data['products']
        return jsonify({"message": "Product array updated successfully", "products": product_array}), 200
    return jsonify({"error": "Invalid data format. 'products' key is required."}), 400

# Route to get the current product array
@app.route('/get_products', methods=['GET'])
def get_products():
    return jsonify({"products": product_array}), 200

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)