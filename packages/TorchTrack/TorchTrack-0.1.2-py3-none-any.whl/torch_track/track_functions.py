import json
import requests

global_error_msg = "Something went wrong!"

class TorchModelData:
    def __init__(self, _model_name: str, _model_architecure, 
                 _model_optimizer): 
        self._model_name = _model_name
        self._model_architecture = _model_architecure
        self._model_optimizer = _model_optimizer

    def save_model_data(self):
            if self._model_name == "":
                raise ValueError("model_name param and file_path cannot be null")
            else:
                json_model_data = TorchModelData(self._model_name, self._model_architecture, 
                                                self._model_optimizer)
                parse_model_data(json_model_data)

    def print_saved_model_data(self) -> bool:
        print(f"---------------------------------")
        print(f"\n--- Model Name: {self._model_name} ---")
        print(f"\n--- Model Architecture: {self._model_architecture} ---")
        print(f"\n--- Model Optimizer: {self._model_optimizer} ---")
        print(f"---------------------------------")

        return True

class TorchTrainingData:
    def __init__(self, _model_training_data): 
        self._model_training_data = _model_training_data

    def save_training_data(self):
                json_model_data = TorchTrainingData(self._model_training_data)

                parse_training_data(json_model_data)

    def print_saved_model_data(self) -> bool:
        print(f"---------------------------------")
        print(f"\n--- Model Traing Data: {self._model_training_data} ---")
        print(f"---------------------------------")

        return True

"""
Parses model training data
from a pytorch model to this json file: "model_data.json"
"""
def parse_training_data(json_training_data):
    json_string_model_train = json.dumps(json_training_data._model_training_data)

    training_data = {
                "model_training_data": str(json_string_model_train),
                
    }
    
    post_endpoint = "https://torchtrackapp.azurewebsites.net/api/TorchTrack/PostTrainginData"
    requests.post(post_endpoint, json = training_data)

    with open("json_data/training_data.json", "w+") as write_file:
        json.dump(training_data, write_file, indent=2)

"""
Parses model architecture & model op
from a pytorch model to this json file: "model_data.json"
"""
def parse_model_data(json_model_data):
    json_string_model_opti = json.dumps(json_model_data._model_optimizer)

    model_data = {
                "model_name": json_model_data._model_name,
                "model_architecure": str(json_model_data._model_architecture),
                "model_optimizer": str(json_string_model_opti),
                
    }
    
    post_endpoint = "https://torchtrackapp.azurewebsites.net/api/TorchTrack/PostModelData"
    requests.post(post_endpoint, json = model_data)

    with open("json_data/model_data.json", "w+") as write_file:
        json.dump(model_data, write_file, indent=2)
