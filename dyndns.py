import json
import logging
import os
import pathlib
import requests
from domeneshop import Client

from config import API_ENDPOINT, API_TOKEN, API_SECRET, DOMAIN, SUBDOMAIN, TTL

working_path = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    filename=os.path.join(working_path, "dns_update.log"),
    level=logging.INFO,
    format="[%(asctime)s] <%(levelname)s> %(message)s",
)


def main():
    prev_file = pathlib.Path(os.path.join(working_path, "previous_ip.txt"))
    prev_file.touch(exist_ok=True)

    with open(prev_file, "r") as f:
        prev_ip = f.read()
        current_ip = requests.get("https://api.ipify.org").content.decode("utf8")
        if prev_ip == current_ip:
            return

    client = Client(API_TOKEN, API_SECRET)

    try:
        domain_id = [
            domain["id"]
            for domain in client.get_domains()
            if domain["domain"] == DOMAIN
        ][0]
    except IndexError:
        logging.error(f"Domain {DOMAIN} not found for this account")

    try:
        record_id = [
            record["id"]
            for record in client.get_records(domain_id)
            if record["host"] == SUBDOMAIN
        ][0]
    except IndexError:
        logging.error(f"Subdomain {SUBDOMAIN} not found for domain {DOMAIN}")

    try:
        client.modify_record(
            domain_id,
            record_id,
            {"host": SUBDOMAIN, "ttl": TTL, "type": "A", "data": current_ip},
        )
    except TypeError as e:
        logging.error(f"Could not update record entry: {e}")

    logging.info(f"DNS record for {SUBDOMAIN}.{DOMAIN} updated to {current_ip}")

    with open(prev_file, "w") as f:
        f.truncate()
        f.write(current_ip)


if __name__ == "__main__":
    main()
