## DYNDNS-Domeneshop

This is a super simple python script to automatically update the DNS record of a subdomain to reflect the current public IP address of the machine running the script. It's meant to be run with CRON or any other scheduling tool. There are five config variables that needs to be updated:

```
API_TOKEN="TOKEN"
API_SECRET="SECRET"

DOMAIN="domain.no"
SUBDOMAIN="subdomain"
```

The token and secret can be found by creating an API key here: [https://www.domeneshop.no/admin?view=api](https://www.domeneshop.no/admin?view=api).

The domain and subdomain needs to be already created, as this script only attempts to modify an existing record.


## Installing
As with all python projects, you should create a virtual environment where the requirements can be installed. 

```
cd 
git clone https://github.com/blixhavn/dyndns-domeneshop.git
cd dyndns-domeneshop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Then, copy the config template to config.py and update the variables (`<esc>:wq` saves and exits vim):
```
cp config_template.py config.py
vim config.py
```

then you can add it to CRON by writing `crontab -e` and adding a line:
```
*/30 * * * * /home/<user>/dyndns-domeneshop/venv/bin/python /home/<user>/dyndns-domeneshop/dyndns.py 