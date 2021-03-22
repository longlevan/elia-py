"""
@author: nicolasquintin
"""
import pandas as pd
import ssl
import urllib.request
import xml.etree.ElementTree as ElementTree

URL_PRICE_EXCEL = 'https://publications.elia.be/Publications/Publications/ImbalanceNrvPrice.v3.svc/GetImbalanceNrvPricesExcel?day=%s'
URL_PRICE_XML = "https://publications.elia.be/Publications/Publications/ImbalanceNrvPrice.v1.svc/GetImbalanceNrvPrices?day=%s"
PREFIX = r'{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.ImbalanceNrvPrice.V1}'

ALPHA = "Alpha"
BETA = "Beta"
DATETIME = "DateTime"
MDP = "MDP"
MIP = "MIP"
NRV = "NRV"
P_NEG = "PNeg"
P_POS = "PPos"
SI = "SI"
columns = [ALPHA, BETA, MDP, MIP, NRV, SI, P_POS, P_NEG]


def imbalance_prices(date):
    ssl._create_default_https_context = ssl._create_unverified_context
    df_imbalance_prices = pd.read_excel(URL_PRICE_EXCEL % date, header=1)
    df_imbalance_prices.index = pd.to_datetime(df_imbalance_prices.Date + " " + df_imbalance_prices.Quarter.str[0:5],
                                               dayfirst=True)
    return df_imbalance_prices


def imbalance_prices_xml(date):
    with urllib.request.urlopen(URL_PRICE_XML % date, context=ssl.SSLContext()) as url:
        price_data = url.read().decode("iso-8859-1")
        xml = ElementTree.fromstring(price_data)

        # Retrieve columns
        dic_imbalance = {}
        for column in columns:
            elements = xml.findall(PREFIX + 'ImbalanceNrvPrices/' + PREFIX + 'ImbalanceNrvPrice/' + PREFIX + column)
            dic_imbalance[column] = [float(elem.text) for elem in elements]

        # Retrieve index
        elements = xml.findall(PREFIX + 'ImbalanceNrvPrices/' + PREFIX + 'ImbalanceNrvPrice/' + PREFIX + DATETIME)
        index = pd.to_datetime([elem.text for elem in elements])

        # Convert to dataframe
        df = pd.DataFrame(dic_imbalance, index=index)
        df.index.name = DATETIME

        return df


if __name__ == '__main__':
    df_test = imbalance_prices_xml("2020-03-20")
    print(df_test)
