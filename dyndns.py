
import json
import logging
import os
import pathlib
import requests

from config import (
    API_ENDPOINT,
    API_TOKEN,
    API_SECRET,
    DOMAIN_ID,
    RECORD_ID,
    HOST,
    TTL
)

working_path = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    filename=os.path.join(working_path, 'dns_update.log'),
    level=logging.INFO,
    format='[%(asctime)s] <%(levelname)s> %(message)s'
)

def main():
    prev_file = pathlib.Path(os.path.join(working_path, 'previous_ip.txt'))
    prev_file.touch(exist_ok=True)

    with open(prev_file, 'r') as f:
        prev_ip = f.read()
        current_ip = requests.get('https://api.ipify.org').content.decode('utf8')
        if prev_ip == current_ip:
           return

    response = requests.put(
        f"{API_ENDPOINT}/domains/{DOMAIN_ID}/dns/{RECORD_ID}",
        auth=(API_TOKEN, API_SECRET),
        data=json.dumps({
            "host": HOST,
            "ttl": TTL,
            "type": "A",
            "data": current_ip
        })
    )
    if response.status_code != 204:
        logging.error(f"Could not update DNS record: API token not valid")
        return
    logging.info(f"DNS record for {HOST} updated to {current_ip}")

    with open(prev_file, 'w') as f:
        f.truncate()
        f.write(current_ip)


if __name__ == "__main__":
    main()
