import requests
import json
import traceback
from .support import generate_unique_id
from .status_check_inference_collection import main_collection
from .status_check_inference_population import main_population
"""
Class to initiate AutomaticAnalysisClientInterface(class which handles all the API request and responses reagrding to automatic analysis) and handle functions integrated to it
"""


class AutomaticAnalysisInterface:

    def __init__(self, auth_token: str, automatic_analysis_url: str):
        self.auth_token = auth_token
        self.automatic_analysis_url = automatic_analysis_url

    def inference_model_upload(self, storage_url, bucket_name, object_key, model_id, label_list, model_name, task):

        hed = {'Authorization': 'Basic ' + self.auth_token}
        payload = {
            "storage_url": storage_url,
            "bucket_name": bucket_name,
            "object_key": object_key,
            "model_ID": model_id,
            "model_name": model_name,
            "label_list": label_list,
            "task": task
        }
        url = f'{self.automatic_analysis_url}/model_setup'
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            print(response.json())

        # Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Connection error from Data Lake connection")
        # Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from Data Lake connection")
        # Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from Data Lake connection")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
        else:
            print('model upload')
    """
    Making the payload and sending it to the given API endpoint in and handle responses in regarding to autotagging
    """

    def tagger_detail_send(self, application, collection_id, item_type, model_id, input_resolution):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        unique_id = generate_unique_id()
        payload = {
            "Application": application,
            "ItemType": item_type,
            "CollectionID": collection_id,
            "ModelID": model_id,
            "UniqueID": unique_id,
            "InputResolution": input_resolution
        }
        url = f'{self.automatic_analysis_url}'
        try:
            if application == 'collection_autotag':
                main_collection(url, payload, hed, unique_id)
            elif application == 'population_autotag':
                main_population(url, payload, hed, unique_id)
        # Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Connection error from Data Lake connection")
        # Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from Data Lake connection")
        # Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from Data Lake connection")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()

    def annotater_detail_send(self, application, collection_id, model_id, input_resolution, prompt):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        unique_id = generate_unique_id()
        payload = {
            "Application": application,
            "CollectionID": collection_id,
            "ModelID": model_id,
            "UniqueID": unique_id,
            "InputResolution": input_resolution,
            "Prompt": prompt
        }
        # url = f'{self.automatic_analysis_url}/dataIn_annotation'
        url = "http://127.0.0.1:8080/dataIn_annotation"
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            print(response.json())
        # Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Connection error from Data Lake connection")
        # Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from Data Lake connection")
        # Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from Data Lake connection")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()

    def embedding_detail_send(self, collection_id, model_id):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        unique_id = generate_unique_id()
        payload = {
            "CollectionID": collection_id,
            "ModelID": model_id,
            "UniqueID": unique_id,
        }
        # url = "http://127.0.0.1:8080/dataIn_embedding"
        url = f'{self.automatic_analysis_url}/dataIn_embedding'
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            print(response.json())

        # Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Connection error from Data Lake connection")
        # Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from Data Lake connection")
        # Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from Data Lake connection")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
        else:
            print('model upload')

    # def sagemaker_detail_send(self,awsRole,accountID,region,model,instanceType):

    #     hed = {'Authorization': 'Basic ' + self.auth_token}
    #     payload = {
    #     "awsRole":awsRole,
    #     "accountID":accountID,
    #     "region":region,
    #     "model":model,
    #     "instanceType":instanceType
    #     }
    #     url = f'{self.automatic_analysis_url_url}/api/client/cocojson/import/label/create'

    #     try:
    #         response = requests.post(url=url, json=payload, headers=hed)
    #         return response.json()
    #     #Handle connection error
    #     except requests.exceptions.ConnectionError as e:
    #         print("Connection error from Data Lake connection")
    #     #Handle timeout error
    #     except requests.exceptions.Timeout as e:
    #         print("Timeout error from Data Lake connection")
    #     #Handle HTTP errors
    #     except requests.exceptions.HTTPError as e:
    #         print("HTTP error from Data Lake connection")
    #     except requests.exceptions.RequestException as e:
    #         print(f"An unexpected request exception occurred: {format(e)}")
    #         traceback.print_exc()
    #     except Exception as e1:
    #         print(f"An unexpected exception occurred: {format(e1)}")
    #         traceback.print_exc()
