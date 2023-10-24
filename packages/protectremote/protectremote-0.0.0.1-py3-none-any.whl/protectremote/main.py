import os
import requests
import socket
from python_settings import settings 
from ipaddress import ip_address, IPv4Address, IPv6Address
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def get_html():
    with open(os.path.join(BASE_DIR, "templates", "Forbidden403Page.html"), 'r') as file:  # r to open file in READ mode
        html_as_string = file.read()
    return html_as_string


class RuleService:
    def __init__(self):
        self.api_url = settings.API_URL
        print("settings",settings.TOKEN)
        if settings.TOKEN is None or settings.TOKEN == "":
            raise Exception("You have set your API KEY. see: https://protectremote.com/sss")
        self.token = settings.TOKEN

    def post_rules(self):
        try:
            response = requests.get(self.api_url, headers={"X-Token": self.token,"Accept": "application/json"})
            response.raise_for_status()
            response_json = response.json()
            print("response_json",response_json)
            return response_json
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
        except Exception as e:
            return e


def get_local_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return IPAddr


def has_ip_access()->bool:
    # Get local IP address

    if settings.DEBUG_MODE:
        IPAddr = settings.DEBUG_MODE_IP_ADDRESS
        print("Local ip address:", IPAddr)
    else:
        IPAddr =  get_local_ip()

    # get api rules from settings
    data = settings.RULES_DATA


    if "rules" not in data:
        print("Cachede data mevcut değil")
        return False

    rules = data["rules"]
    hasAccess = False
    for rule in rules:
        # check first ipv4
        if type(ip_address(IPAddr)) == IPv4Address:
            if "ipAddressV4List" in rule and IPAddr in rule["ipAddressV4List"]:
                    hasAccess= True
        elif type(ip_address(IPAddr)) == IPv6Address:
            if "ipAddressV6List" in rule and IPAddr in rule["ipAddressV6List"]:
                    hasAccess= True
        else:
            raise Exception("ipv4 veya ipv6 ip adresi göndermelisiniz")
    return hasAccess


    



