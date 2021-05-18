
# Hedieh Moradi- 2021- Hybrid Atelier
#  This program will go through a JSON files which contains list of API call links for glazy.org
#  This code will open each link from the file and extract the informaiton bellow
#  These data are formated to match my MongoDB schema, and you need to format it based on your needs.

# Packages
import urllib.request as request
import json

#  Create a JSON file from the extracted data
def create_json(data_id):
    res ={}
    metadata_res={}
    chemistry_list= []
    properties_dic={}
    application_dic={}

    for chem in data_id['materialComponents']:
        material_temp={}
        material_temp['material']= chem['material']['name']
        material_temp['amount']= chem['percentageAmount']
        material_temp['unit']= 'gram'
        chemistry_list.append(material_temp)
    
   

    res['rfid']= None
    res['container']= None
    res['icon']= {}
    metadata_res['parent']= None
    metadata_res['children']= []
    metadata_res['class_name']= "GlazeRFID"
    metadata_res['name']= data_id['name']
    metadata_res["manufacturer"]= data_id['createdByUser']['name']
    if data_id['description']:
        metadata_res["description"]= data_id['description']
    else:
        metadata_res["description"]= None
    metadata_res['url']= 'glazy.org/recipes/'+ str(data_id['id'])
    metadata_res['keys']=[]

    metadata_res['images']=  data_id['selectedImage']['filename']
    properties_dic['firing']= data_id.get('toOrtonConeName', None)

    properties_dic["recipe"]= chemistry_list
    properties_dic["total_amount"]=  data_id['materialComponentTotalAmount']

    application_dic["food_safe"]= None
    application_dic["brushable"]= None
    application_dic["dippable"]= None
    application_dic["pourable"]= None
    application_dic["sprayable"]= None


    properties_dic['application']=application_dic
    metadata_res['properties']= properties_dic
    
    res['metadata'] = metadata_res
    return res

# Open file containing API links and send request to each link 
with open('YOUR_FIle_Local', 'r') as f:
    links= json.load(f)
    for link in links:
        with request.urlopen(link) as response:
            if response.getcode() == 200:
                source = response.read()
                data = json.loads(source)
                for entry in data['data']:
                    result = create_json(entry)
                    file_name= f'./glazy_glazes/glaze_{str(entry["id"])}.json' #Save each JSON file using this method "glaze_ID"
                        
                    with open(file_name, 'w') as outfile:
                        json.dump(result, outfile, indent=4)


            else:
                print('An error occurred while attempting to retrieve data from the API.')

