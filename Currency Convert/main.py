import tkinter as tk
import customtkinter as ctk
import requests

CURRENCIES = sorted(
    ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF',
     'BMD', 'BND', 'BOB', 'BOV', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHE', 'CHF', 'CHW', 'CLF',
     'CLP', 'CNY', 'COP', 'COU', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB',
     'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG',
     'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF',
     'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK',
     'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MXV', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD',
     'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR',
     'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'SSP', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND',
     'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'USN', 'UYI', 'UYU', 'UZS', 'VEF', 'VES', 'VND', 'VUV',
     'WST', 'XAF', 'XAG', 'XAU', 'XBA', 'XBB', 'XBC', 'XBD', 'XCD', 'XDR', 'XOF', 'XPD', 'XPF', 'XPT', 'XSU', 'XTS',
     'XUA', 'XXX', 'YER', 'ZAR', 'ZMW', 'ZWL'])


def get_exchange_rates():
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        response.raise_for_status()
        data = response.json()
        # print("API Response:", data)
        base_currency = data.get('base', 'USD')
        rates = data.get('rates', {})
        if not rates:
            raise ValueError("Rates data is empty.")

        rates[base_currency] = 1.0
        return rates
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None
    except ValueError as e:
        print(f"Error processing exchange rates: {e}")
        return None


def convert_currency(from_currency, to_currency, amount):
    rates = get_exchange_rates()
    if rates is None:
        return None

    # print(f"Rates: {rates}")
    # print(f"From Currency: {from_currency}, To Currency: {to_currency}, Amount: {amount}")

    usd_amount = float(amount) / rates[from_currency]
    # print(f"USD Amount: {usd_amount}")
    converted_amount = usd_amount * rates[to_currency]
    # print(f"Converted Amount: {converted_amount}")

    return converted_amount


app = ctk.CTk()
app.title("Currency Converter")
app.geometry("400x350")
app.maxsize(400, 350)

amount_label = ctk.CTkLabel(app, text="Amount:")
amount_label.pack(pady=10)
amount_entry = ctk.CTkEntry(app)
amount_entry.pack(pady=5)

from_currency_label = ctk.CTkLabel(app, text="From:")
from_currency_label.pack(pady=5)
from_currency_var = ctk.StringVar(app)
from_currency_var.set(CURRENCIES[0])
from_currency_dropdown = ctk.CTkComboBox(app, values=CURRENCIES, variable=from_currency_var)
from_currency_dropdown.pack(pady=5)

to_currency_label = ctk.CTkLabel(app, text="To:")
to_currency_label.pack(pady=5)
to_currency_var = ctk.StringVar(app)
to_currency_var.set(CURRENCIES[1])
to_currency_dropdown = ctk.CTkComboBox(app, values=CURRENCIES, variable=to_currency_var)
to_currency_dropdown.pack(pady=5)

result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=10)


def convert():
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_var.get()
        to_currency = to_currency_var.get()

        converted_amount = convert_currency(from_currency, to_currency, amount)
        if converted_amount is not None:
            result_label.configure(text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
        else:
            result_label.configure(text="Error converting currency")
    except ValueError:
        result_label.configure(text="Invalid amount")


convert_button = ctk.CTkButton(app, text="Convert", command=convert)
convert_button.pack(pady=10)

app.mainloop()
