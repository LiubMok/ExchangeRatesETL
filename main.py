import datetime

import requests
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'exchangerates-435618-45bc1dde0500.json'
SHEET_ID = '12gAzrX5oiCU1mtb0c2_uWjBFDOuboDA8ePThSbJupeY'
RANGE_NAME = 'Exchange Rates!A1'

users = {
    "admin": generate_password_hash("password")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users[username], password):
        return username


def transform_date(date_st):
    return datetime.datetime.strptime(date_st, '%Y-%m-%d').strftime('%Y%m%d')


def validate_dates(update_from, update_to):
    try:
        update_from_date = datetime.datetime.strptime(update_from, '%Y-%m-%d').date()
        update_to_date = datetime.datetime.strptime(update_to, '%Y-%m-%d').date()
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."

    today = datetime.date.today()
    if update_from_date > today or update_to_date > today:
        return "Dates cannot be in the future."

    if update_from_date > update_to_date:
        return "The 'update_from' date cannot be after the 'update_to' date."

    return None


def get_parsed_args(request):
    default_date = datetime.date.today().strftime('%Y-%m-%d')
    update_from = request.args.get('update_from', default_date)
    update_to = request.args.get('update_to', default_date)
    valcode = request.args.get('valcode', 'usd')

    error = validate_dates(update_from, update_to)
    if error:
        return None, None, None, error

    update_from = transform_date(update_from)
    update_to = transform_date(update_to)

    return update_from, update_to, valcode, None


def get_exchange_rate(start_date, end_date, valcode):
    url = (f"https://bank.gov.ua/NBU_Exchange/exchange_site?"
           f"start={start_date}"
           f"&end={end_date}"
           f"&valcode={valcode}"
           f"&sort=exchangedate"
           f"&order=desc"
           f"&json")
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_parsed_exchange_rate_data(update_from, update_to, valcode):
    exchange_rates = get_exchange_rate(update_from, update_to, valcode)

    daily_rates = dict()
    for day_dict in exchange_rates:
        date = datetime.datetime.strptime(day_dict['exchangedate'], '%d.%m.%Y').strftime('%Y-%m-%d')
        daily_rates[date] = day_dict['rate_per_unit']

    return daily_rates


@app.route('/get-currency-exchange-rate', methods=['GET'])
@auth.login_required
def get_currency_data():
    update_from, update_to, valcode, error = get_parsed_args(request)
    if error:
        return jsonify({"status": "error", "message": error}), 400

    exchange_data = get_parsed_exchange_rate_data(update_from, update_to, valcode)
    exchange_data = dict(sorted(exchange_data.items(), key=lambda item: item[0], reverse=True))
    return jsonify(exchange_data) if exchange_data is not None else jsonify(
        {"status": "error", "message": "Не вдалося отримати дані з API НБУ"}), 500


def get_sheets_service():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()


def update_google_sheet(data):
    service = get_sheets_service()
    body = {
        'values': data
    }
    result = service.values().update(
        spreadsheetId=SHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()
    print(f"{result.get('updatedCells')} cells updated.")


def form_and_save_exchange_rates(exchange_data):
    if exchange_data:
        exchange_data = dict(sorted(exchange_data.items(), key=lambda item: item[0], reverse=True))
        sheet_data = [['Dates', 'Rates']]
        print(exchange_data)
        for key, value in exchange_data.items():
            sheet_data.append([key, value])

        print(sheet_data)
        update_google_sheet(sheet_data)

        return jsonify({"status": "success", "message": "Дані оновлено"})
    else:
        return jsonify({"status": "error", "message": "Не вдалося отримати дані з API НБУ"}), 500


@app.route('/update-excel-exchange-rate', methods=['GET'])
@auth.login_required
def update_currency():
    update_from, update_to, valcode, error = get_parsed_args(request)
    if error:
        return jsonify({"status": "error", "message": error}), 400
    exchange_data = get_parsed_exchange_rate_data(update_from, update_to, valcode)
    return form_and_save_exchange_rates(exchange_data)


if __name__ == '__main__':
    app.run(debug=True)
