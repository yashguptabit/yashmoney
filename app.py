from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount, 2)
    response = {
        'fulfillmentText': "{} {} is {} {}".format(amount, source_currency, final_amount, target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source, target):
    # Change this to your actual API key
    api_key = 'YOUR-API-KEY'
    url = 'https://v6.exchangerate-api.com/v6/0960b1194ef95dd7372daaca/latest/{}'.format(api_key, source)

    response = requests.get(url)
    data = response.json()

    if data['result'] == 'success':
        rates = data['conversion_rates']
        conversion_factor = rates[target]
    else:
        conversion_factor = None  # Handle errors or invalid responses here

    return conversion_factor

if __name__ == "__main__":
    app.run(debug=True)
