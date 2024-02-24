from Services.DecimalService import toDecimals
from Services.HttpService import get_crypto_price
from config import ANKR_API_KEY
from web3 import Web3

decimals = 18
precision = 4


class CryptoNetwork:
    def __init__(self, provider_url):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))

    def get_balance(self, address):
        address = Web3.to_checksum_address(address.strip())
        balance = self.w3.eth.get_balance(address)
        balance = toDecimals(balance, decimals, precision)
        return balance


def extract_crypto_addresses(input_files, output_file):
    networks = {
        "ETH": CryptoNetwork(f'https://rpc.ankr.com/eth/{ANKR_API_KEY}'),
        "BNB": CryptoNetwork(f'https://rpc.ankr.com/bsc/{ANKR_API_KEY}'),
        "OP": CryptoNetwork(f'https://rpc.ankr.com/optimism/{ANKR_API_KEY}'),
        "OPBNB": CryptoNetwork('https://opbnb-rpc.publicnode.com'),
        "ARB": CryptoNetwork(f'https://rpc.ankr.com/arbitrum/{ANKR_API_KEY}'),
        "BASE": CryptoNetwork(f'https://rpc.ankr.com/base/{ANKR_API_KEY}'),
        "LINEA": CryptoNetwork('https://linea.decubate.com'),

    }

    currency_to_network = {
        "ETH": "ETH",
        "BNB": "BNB",
        "OP": "OP",
        "OPBNB": "BNB",
        "ARB": "ARB",
        "BASE": "BASE",
        "LINEA": "ETH",
    }

    total_balances = {network: {"balance": 0, "usd_balance": 0, "price": 0, "data_print": ""} for network in networks}
    with open(output_file, 'w') as output:
        for file_name in input_files:
            with open(file_name, 'r') as file:
                addresses = file.readlines()

                index = 1
                for address in addresses:

                    for currency, network_obj in networks.items():
                        balance = network_obj.get_balance(address)

                        network_currency = currency_to_network[currency]

                        price = get_crypto_price(network_currency)

                        usd_balance = round(balance * price, 4)
                        data_print = f"||  {currency} - {str(balance).ljust(12)} USD - {str(usd_balance).ljust(12)}"

                        total_balances[currency]["balance"] += balance
                        total_balances[currency]["usd_balance"] += usd_balance
                        total_balances[currency]["price"] = price
                        total_balances[currency]["data_print"] = data_print

                    output.write(f"{str(index).ljust(3)} {address.strip().ljust(44)}")
                    for network, data in total_balances.items():
                        output.write(f" {data['data_print']}")
                    output.write("\n")
                    separator = "-" * 346
                    output.write(f"{separator}\n")
                    index += 1

                for network, data in total_balances.items():
                    write_total_balance(output, network, data["balance"], data["usd_balance"], data["price"])


def write_total_balance(output, network, balance, usd_balance, price):
    output.write(f"\nTotal {network} Balance: {balance:.4f}")
    output.write(f"\nTotal {network} Balance in USD: {usd_balance:.4f}\n\n")
