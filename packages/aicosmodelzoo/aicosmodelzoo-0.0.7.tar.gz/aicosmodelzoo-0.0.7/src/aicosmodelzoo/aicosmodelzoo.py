import os
import csv
import pandas as pd
import subprocess
import torch
import torch.nn as nn
from torchinfo import summary
from sklearn.metrics import accuracy_score
import torch.optim as optim
import importlib.util
import sys
import mlflow

class ModelZoo:

    #Initialize connection to minio bucket
    server_uri = "http://i-1342.cloud.fraunhofer.pt:8001"
    mlflow.set_tracking_uri(server_uri)

    os.environ["MLFLOW_TRACKING_USERNAME"] = "modelzoo"
    os.environ["MLFLOW_TRACKING_PASSWORD"] = "modelzoo"

    # Minio/AWS are required to upload artifacts to S3 Bucket
    os.environ["AWS_ACCESS_KEY_ID"] = "jorge"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "1234567890"
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://i-1342.cloud.fraunhofer.pt:9000"


    def __init__(self,path):

        self.models = []
        self.uri = ''
        self.model = None
        self.csv_filepath = path
        
        with open(self.csv_filepath, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Optionally skip the header
            for row in reader:
                self.models.append(row[0])

    def save_model(self,name,model,framework):
            mlflow.set_tracking_uri(self.server_uri)
            # Start an MLflow run
            if framework == 'pytorch':
                with mlflow.start_run():
                    # Log the PyTorch model with an artifact_path
                    self.uri = mlflow.pytorch.log_model(
                        model, 
                        artifact_path="models",
                        registered_model_name=name)
            elif framework == 'tensorflow':
                with mlflow.start_run():
                    # Log the PyTorch model with an artifact_path
                    self.uri = mlflow.tensorflow.log_model(
                        model, 
                        artifact_path="models",
                        registered_model_name=name)

    def save_metadata(self, data):
        dir = os.path.dirname(self.csv_filepath)
        os.chdir(dir)

        try:
            # Pull the latest changes
            subprocess.run(['git', 'pull'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")

        if 'name' not in data or not data['name']:
            s = "Please insert a name for the model"
            return s

        if data['name'] in self.models:
            data['uri'] = self.uri.model_uri

            original_csv_file = self.csv_filepath

            # Read the original CSV file and store its data in a list
            rows = []
            with open(original_csv_file, "r") as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    rows.append(row)

            # Find the index of the row with the specified name in the first column
            search_name = data['name']
            row_to_replace_index = None

            for i, row in enumerate(rows):
                if row and row[0] == search_name:
                    row_to_replace_index = i
                    break

            if row_to_replace_index is not None:
                # Replace the row's values with the new values and fill missing keys with empty values
                existing_data = rows[row_to_replace_index]
                new_data =[]
                # Replace 'your_file.csv' with your actual CSV file path
                with open(self.csv_filepath, 'r') as csvfile:
                    csvreader = csv.reader(csvfile)

                    header = next(csvreader)
                    
                    # Iterate over the column names
                    for col_name in header:
                        # Check if the column name is a key in the dictionary
                        if col_name in data:
                            value = data[col_name]
                        else:
                            value = ''  # Empty value for columns without a matching key
                        
                        new_data.append(value)
                print(new_data)

                rows[row_to_replace_index] = new_data

                # Rewrite the original CSV file with the updated data
                with open(original_csv_file, "w", newline="") as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerows(rows)

            try:
                # Add, commit, and push
                subprocess.run(['git', 'add', 'metadata.csv'], check=True)
                subprocess.run(['git', 'commit', '-m', "Model updated"], check=True)
                subprocess.run(['git', 'push', '-u', 'origin', 'HEAD:master'], check=True)

            except subprocess.CalledProcessError as e:
                print(f"Error occurred: {e}")

        else:
            data['uri'] = self.uri.model_uri

            # Ensure the file ends with a newline
            with open(self.csv_filepath, 'ab+') as file:
                if file.tell() > 0:
                    file.seek(-1, 2)
                    last_byte = file.read(1)
                    if last_byte != b'\n':
                        file.write(b'\n')
            # Now, append the new data and fill missing keys with empty values
            new_data =[]
            # Replace 'your_file.csv' with your actual CSV file path
            with open(self.csv_filepath, 'r') as csvfile:
                csvreader = csv.reader(csvfile)

                header = next(csvreader)
                
                # Iterate over the column names
                for col_name in header:
                    # Check if the column name is a key in the dictionary
                    if col_name in data:
                        value = data[col_name]
                    else:
                        value = ''  # Empty value for columns without a matching key
                    
                    new_data.append(value)
                print(new_data)
            with open(self.csv_filepath, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(new_data)

            try:
                # Add, commit, and push
                subprocess.run(['git', 'add', 'metadata.csv'], check=True)
                subprocess.run(['git', 'commit', '-m', "Model uploaded"], check=True)
                subprocess.run(['git', 'push', '-u', 'origin', 'HEAD:master'], check=True)

            except subprocess.CalledProcessError as e:
                print(f"Error occurred: {e}")
            

    #Inspect metadata of a given model
    def model_info(self,model):
        df = pd.read_csv(self.csv_filepath)
        s = ""
        row = df[df['name'] == model].iloc[0]
        if not row.empty :
            for col_name, value in row.items():
                    if col_name == 'name':
                        s += '- **' + str(col_name) + '** ' + ": " + str(value) + '  \n'
                    else:
                        s += '**' + str(col_name) + '** ' + ": " + str(value) + '  \n'
            print(s)
        print("Model does not exist")


    def filter_by(self, filter_dict):
        # Load the CSV file into a list of lists and extract the header
        with open(self.csv_filepath, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            header_lower = [col.lower() for col in header]  # Convert header to lowercase
            csv_data = [row for row in csv_reader]

        matching_first_elements = []

        # For each row in the CSV data
        for row in csv_data:
            match = True

            # Check each key-value pair in the filter_dict
            for key, value in filter_dict.items():
                key_lower = key.lower()  # Convert key to lowercase
                if key_lower in header_lower:
                    csv_index = header_lower.index(key_lower)
                    cell_value = row[csv_index]

                    if isinstance(value, list) and value:
                        # If value is a list, check if any element matches the cell_value
                        if all(item not in cell_value for item in value):
                            match = False
                    elif isinstance(value, float) and abs(value - float(cell_value)) > 1e-6:
                        match = False
                    elif isinstance(value, str) and value != cell_value:
                        match = False
                else:
                    # Key not found in the header, so it cannot be filtered
                    match = False

            # If all key-value pairs matched, add the first element of the row to the result
            if match:
                matching_first_elements.append(row[0])

        print(matching_first_elements)
    
    #'model' is the name of the model, 'path' is the path to the directory you want to store the model in
    def load_local_ptmodel(self,path,weights,arch):

        module_name = arch.split('.')[0]
        sys.path.insert(0, path)
        __import__(module_name)

        self.model = torch.load(path + '/' + weights ,map_location=torch.device('cpu'))

    def load_model(self,model):
        #sys.path.insert(0, self.arch_path)
        #__import__(model)

        df = pd.read_csv(self.csv_filepath)

        desired_row = df[df['name'] == model]

        uri = desired_row['uri'].values[0]

        fw = desired_row['framework'].values[0]

        if fw == 'PyTorch':
            # Load model as a PyFuncModel.
            self.model = mlflow.pytorch.load_model(uri)

        elif fw == 'TensorFlow':
            # Load model as a PyFuncModel.
            self.model = mlflow.tensorflow.load_model(uri)

    def model_summary(self):
        summary(self.model)

    # layers is a list with the name of the layers
    def freeze_layers(self,layers):
        #Freezing layers
        for layer in layers:
            for name, param in self.model.named_parameters():
                if param.requires_grad and layer in name:
                    param.requires_grad = False
    
    def replace_layer(self, layer_name, new_layer):
        # Replace the old layer with the new layer
        setattr(self.model, layer_name, new_layer)
    
    def train_model(self, epochs, criterion, optimizer, X_train, y_train):
        # Training loop
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self.model(X_train)
            loss = criterion(outputs, y_train)
            loss.backward()
            optimizer.step()

    def test_model(self, X_test, y_test):
        # Evaluate the model on the test set
        self.model.eval()
        with torch.no_grad():
            test_outputs = self.model(X_test)
            _, predicted = torch.max(test_outputs, 1)
        accuracy = accuracy_score(y_test, predicted)
        print(f"Accuracy on the test set: {accuracy:.2f}")

