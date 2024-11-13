from constants import *
from functions import *
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        query = data.get('query')

        if not query:
            return jsonify({"error": "Query is required"}), 400

        response_text = func_response_generator(query)
        print(response_text)
        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500   

if __name__ == '__main__':
    app.run(debug=True)
