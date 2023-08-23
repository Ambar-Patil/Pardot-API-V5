import requests
import pandas as pd

response = requests.post('https://login.salesforce.com/services/oauth2/token', data = {
                'client_id':'Enter your Client ID',
                'client_secret':'Enter your Client Secret',
                'grant_type':'password',
                'username':'Enter your Username',
                'password':'Enter your Password(Password+Token Combination)'
                })

json_res = response.json()
access_token = json_res['access_token']

auth_header = {'Authorization':'Bearer ' + access_token,'Pardot-Business-Unit-Id':'Enter Your Pardot Business Unit ID'}

campaign_url ='https://pi.pardot.com/api/v5/objects/campaigns?fields=id,name,folderId,cost,parentCampaignId,isDeleted,createdById,updatedById,createdAt,updatedAt,salesforceId'

file_path ='Enter your folder path to store CSV'
object_list =[campaign_url] 

for i in object_list:
    file_name= i.split('?')[0][37::]
    data = pd.DataFrame()
    while i:
        object_response = requests.get(i,headers=auth_header)
        res = object_response.json()['values']
        new_data = pd.DataFrame(res)
     
        if not res:
            break
        data = pd.concat([data,new_data], axis=0,ignore_index=True)
        i = object_response.json()['nextPageUrl']

    data.to_csv(file_path + file_name+".csv",index=False)
