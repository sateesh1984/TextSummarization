#Request for Document Summary using GenSim Library
import requests
json_data={'path':'Documents/Circle-K---Data-Center-Migration.pdf'}
server='http://dxc-ds-prod-restapi.eastus.cloudapp.azure.com'
port='5000'

host=server+':'+port+'/'+'GenSimSummary'
resp = requests.post(host, json=json_data)
print("Status of POST Request :{}".format(resp.status_code))
if resp.status_code != 200:
    raise ('POST /tasks/ {}'.format(resp.status_code))
else:
    print("Response:{}".format(resp.content))


#Request for Document Summary using Summa Library
import requests
json_data={'path':'Documents/Circle-K---Data-Center-Migration.pdf'}
server='http://dxc-ds-prod-restapi.eastus.cloudapp.azure.com'
port='5000'

host=server+':'+port+'/'+'SummaSummary'
resp = requests.post(host, json=json_data)
print("Status of POST Request :{}".format(resp.status_code))
if resp.status_code != 200:
    raise ('POST /tasks/ {}'.format(resp.status_code))
else:
    print("Response:{}".format(resp.content))
