from .automatic_analysis_interface import AutomaticAnalysisInterface
from .support import make_tarfile_in_memory
"""
Class to initiate AutomaticAnalysisClient and handle functions integrated to it
"""
class AutomaticAnalysisClient:

    def __init__(self,encoded_key_secret: str, layernext_url: str):
        _automatic_analysis_url = f'{layernext_url}/analytics' 
        self.encoded_key_secret=encoded_key_secret
        self.layernext_url=layernext_url
        self.automatic_analysis_interface = AutomaticAnalysisInterface(encoded_key_secret, _automatic_analysis_url)

    """
    Upload models for Datalake collection automatic_analysis_models and send the stored location details in to flask app
    @param input_model_path: path of the model folder which needed to be uploaded
    @param model_id:id/name of the model which is registered in the datalake
    @param _datalake_client: datalake_client instance in order to acquire datalake SDK s inside this function
    """ 
    def register_model(self,input_model_path,model_id, _datalake_client, task):
        storage_url,bucket_name, object_key, label_list,model_name=make_tarfile_in_memory(input_model_path, model_id, _datalake_client)
        self.automatic_analysis_interface.inference_model_upload(storage_url,bucket_name, object_key,model_id,label_list,model_name, task)

    """
    initiate the API call to the flask app to autotagging a given collection through tagger_detail_send
    @param collection_id: id of the image or video collection
    @param model_id:id/name of the model which is registered in the datalake
    @param input_resolution:resolution of the frames which should be considered at inference(image or video)
    """ 
    def model_inference_collection(self,collection_id,model_id,input_resolution):
        application='collection_autotag'
        item_type=""
        self.automatic_analysis_interface.tagger_detail_send(application,collection_id,item_type,model_id,input_resolution)
    """
    initiate the API call to the flask app to autotagging a given item type files through tagger_detail_send
    @param item_type: "image", "video", "other", "image_collection", "video_collection", "other_collection", "dataset"
    @param model_id:id/name of the model which is registered in the datalake
    @param input_resolution:resolution of the frames which should be considered at inference(image or video)
    """    
    def model_inference_population(self,item_type,model_id,input_resolution):
        application='population_autotag'
        collection_id=""
        self.automatic_analysis_interface.tagger_detail_send(application,collection_id,item_type,model_id,input_resolution)

    def model_annotate_collection(self, collection_id, model_id, prompt, input_resolution):
        application='collection_autoannotate'
        self.automatic_analysis_interface.annotater_detail_send(application,collection_id,model_id,input_resolution,prompt)

    def embedding_model_inference_collection(self,collection_id,model_id):
        self.automatic_analysis_interface.embedding_detail_send(collection_id,model_id)
