from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_data():
    # Receiving JSON data from the client
    data = request.json

    # Perform some processing
    processed_data = data['input_data'] + '_processed'

    # Creating a JSON response
    response_data = {
        'processed_data': processed_data
    }

    # Sending JSON response
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)