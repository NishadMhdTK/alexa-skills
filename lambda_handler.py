import json
import urllib3

CURRENCY_MAP = {'AED': 'United Arab Emirates Dirham',
                    'ARS': 'Argentine Peso',
                    'AUD': 'Australian Dollar',
                    'BGN': 'Bulgarian Lev',
                    'BND': 'Brunei Dollar',
                    'BOB': 'Bolivian Boliviano',
                    'BRL': 'Brazilian Real',
                    'CAD': 'Canadian Dollar',
                    'CHF': 'Swiss Franc',
                    'CLP': 'Chilean Peso',
                    'CNY': 'Chinese Yuan Renminbi',
                    'COP': 'Colombian Peso',
                    'CZK': 'Czech Republic Koruna',
                    'DKK': 'Danish Krone',
                    'EGP': 'Egyptian Pound',
                    'EUR': 'Euro',
                    'FJD': 'Fijian Dollar',
                    'GBP': 'British Pound Sterling',
                    'HKD': 'Hong Kong Dollar',
                    'HRK': 'Croatian Kuna',
                    'HUF': 'Hungarian Forint',
                    'IDR': 'Indonesian Rupiah',
                    'ILS': 'Israeli New Sheqel',
                    'INR': 'Indian Rupee',
                    'JPY': 'Japanese Yen',
                    'KES': 'Kenyan Shilling',
                    'KRW': 'South Korean Won',
                    'LTL': 'Lithuanian Litas',
                    'MAD': 'Moroccan Dirham',
                    'MXN': 'Mexican Peso',
                    'MYR': 'Malaysian Ringgit',
                    'NOK': 'Norwegian Krone',
                    'NZD': 'New Zealand Dollar',
                    'PEN': 'Peruvian Nuevo Sol',
                    'PHP': 'Philippine Peso',
                    'PKR': 'Pakistani Rupee',
                    'PLN': 'Polish Zloty',
                    'RON': 'Romanian Leu',
                    'RSD': 'Serbian Dinar',
                    'RUB': 'Russian Ruble',
                    'SAR': 'Saudi Riyal',
                    'SEK': 'Swedish Krona',
                    'SGD': 'Singapore Dollar',
                    'THB': 'Thai Baht',
                    'TRY': 'Turkish Lira',
                    'TWD': 'New Taiwan Dollar',
                    'UAH': 'Ukrainian Hryvnia',
                    'USD': 'US Dollar',
                    'VEF': 'Venezuelan Bolívar Fuerte',
                    'VND': 'Vietnamese Dong',
                    'ZAR': 'South African Rand'}

def lambda_handler(event, context):
    http = urllib3.PoolManager()
    data = http.request('GET', 'https://api.exchangeratesapi.io/latest', {})
    d = json.loads(data.data.decode())
    
    speech = "considering "+CURRENCY_MAP[d['base']]+" as base currency, one euro equals to  "
    for rate in d['rates']:
        speech += (CURRENCY_MAP[rate] if rate in CURRENCY_MAP else rate) + " " + str(round(d['rates'][rate], 2)) + ", "
    c= context.__dict__
    return {
        'inp':str(list(c)),
        'oup': str(event),
        'version': '1.0',
        'sessionAttributes': {"speech_output": speech,
                              "reprompt_text": speech
                              },
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': speech
            },
            'card': {
                'type': 'Simple',
                'title': "Currency Rate",
                'content': "Currency Rate"
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': "Currency Rate"
                }
            },
            'shouldEndSession': True
        }
    }
