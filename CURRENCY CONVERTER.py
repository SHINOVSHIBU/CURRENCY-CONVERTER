"""Currency Converter Sytem
To calculate the value of one currency to another
using real-time rates from  https://api.exchangerate-api.com/v4/latest/USD

Users may convert currency using currency name or currency code   
"""

import urllib.request
import json

def exchangeRates():
        """
        read the data from the api
        return a dictionary of {currency code: rate}
        """
        exchangeRateApi = "https://api.exchangerate-api.com/v4/latest/USD"

        with urllib.request.urlopen(exchangeRateApi) as f:
            data = f.read()
        exchangeRates = json.loads(data)

        return dict(exchangeRates['rates']) 

def currencyCodes():
    """read the data from the api
    return a dictionay of {currency name (uppercase): currency code}
    """
    codesApi = "https://pkgstore.datahub.io/core/currency-codes/codes-all_json/data/029be9faf6547aba93d64384f7444774/codes-all_json.json"

    with urllib.request.urlopen(codesApi) as f:
        data = f.read()
        currencyCodes = json.loads(data)   
    return {country["Currency"].upper():country["AlphabeticCode"] for country in currencyCodes}


class CurrencyConverter:
    def __init__(self):
        self.rates = exchangeRates()
        self.codes = currencyCodes()       

    def getRates(self):
        return self.rates

    def getCodes(self):
        return self.codes 

    def checkCurrency(self, currency):
        cNames = [name for name in self.codes.keys()]                      
        cCodes = [code for code in self.rates.keys()]         
        
        while True:
            if len(currency) == 3:
                list_check = cCodes
            else:
                list_check = cNames                         
            currency = currency.upper()
            matching =[]
            if not currency in list_check:
                for i in range(len(currency)):
                    currency = currency[0:-1]           
                    matching = [cCheck for cCheck in list_check if currency in cCheck]
                    if matching:                    
                        break   
                print(f'Do you mean: {matching}?')
                currency = str.upper(input('Please enter again: ')) 
            else:
                break
        return currency
    
    def searchRate(self, currency):
        if len(currency) == 3: # search rates based on Currency code
            rate = self.rates[currency]
        else:
            rate = self.rates[self.codes[currency]] if self.codes[currency] in self.rates.keys() else None
        return rate

    def convert(self, src_currency, dest_currency, amount):
        srcRate = self.searchRate(src_currency)
        destRate = self.searchRate(dest_currency)

        if not srcRate:
            print(f'Sorry, the exchange rate data of {src_currency.title()} is not available')
        elif not destRate:
            print(f'Sorry, the exchange rate data of {dest_currency.title()} is not available')
        else:
            return round(amount * destRate/srcRate, 2)

def printHeader():
    print("Welcome to Currency Convert System!")
    print("-"*80)

def getFloat(number):
    while True:
        try:
            number = float(number)
        except:
            number = input("Please enter a number: ")    
        else:
            break
    return number

def main(): 

    converter = CurrencyConverter()    

    printHeader()
    
    while True:        
        option = input("Please enter any key to continue or 'q' to quit > ")

        if option != 'q':          
            src_currency = converter.checkCurrency(input("FROM currency: "))            
            dest_currency = converter.checkCurrency(input("TO currency: "))
            amount = getFloat(input("Amount: "))                  
            result = converter.convert(src_currency, dest_currency, amount)

            if result:
                print(f'{amount} {src_currency} = {result} {dest_currency}')
        else:
            break    

if __name__ == "__main__":
    main()   

   





