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

    def save_model(self,name,model):
            mlflow.set_tracking_uri(self.server_uri)
            # Start an MLflow run
            with mlflow.start_run():
                # Log the PyTorch model with an artifact_path
                self.uri = mlflow.pytorch.log_model(
                    model, 
                    artifact_path="models",
                    registered_model_name=name)

    #Update and send new metadata file to repository
    def save_metadata(self,data):
        subprocess.run(['cd', os.path.dirname(self.csv_filepath)], check=True)
        try:
            # Pull the latest changes
            subprocess.run(['git', 'pull'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
        if len(data[0]) == 0:
            s = "Please insert a name for the model"
            return s
        
        elif data[0] in self.models:

            data.append(self.uri.model_uri)

            # Define the path to your original CSV file and the list of new values
            original_csv_file = self.csv_filepath  # Replace with your actual values

            # Read the original CSV file and store its data in a list
            rows = []
            with open(original_csv_file, "r") as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    rows.append(row)

            # Find the index of the row with the specified value in the first column
            search_value = data[0]  # Value to search for in the first column
            row_to_replace_index = None

            for i, row in enumerate(rows):
                if row and row[0] == search_value:
                    row_to_replace_index = i
                    break

            # Check if the row was found
            if row_to_replace_index is not None:
                # Replace the row's values with the new values
                rows[row_to_replace_index] = data

                # Rewrite the original CSV file with the updated data
                with open(original_csv_file, "w", newline="") as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerows(rows)
            try:
                # Add, commit and push
                subprocess.run(['git', 'add', 'metadata.csv'], check=True)
                subprocess.run(['git', 'commit', '-m', "Model updated"], check=True)
                subprocess.run(['git', 'push','-u', 'origin', 'HEAD:master'], check=True)
                
            except subprocess.CalledProcessError as e:
                print(f"Error occurred: {e}")


        else:
                
            data.append(self.uri.model_uri)

            # Ensure the file ends with a newline
            with open(self.csv_filepath, 'ab+') as file:
                if file.tell() > 0:  # Check if file is not empty
                    file.seek(-1, 2)  # Move the cursor one step back from the end
                    last_byte = file.read(1)
                    if last_byte != b'\n':
                        file.write(b'\n')
            # Now, append the new data
            with open(self.csv_filepath, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)

            try:
                # Add, commit and push
                subprocess.run(['git', 'add', 'metadata.csv'], check=True)
                subprocess.run(['git', 'commit', '-m', "Model uploaded"], check=True)
                subprocess.run(['git', 'push','-u', 'origin', 'HEAD:master'], check=True)
                
            except subprocess.CalledProcessError as e:
                print(f"Error occurred: {e}")

            

    #Inspect metadata of a given model
    def inspect_model(self,model):
        df = pd.read_csv(self.csv_filepath)
        s = ""
        row = df[df['name'] == model].iloc[0]
        if not row.empty :
            for col_name, value in row.items():
                    if col_name == 'name':
                        s += '- **' + str(col_name) + '** ' + ": " + str(value) + '  \n'
                    else:
                        s += '**' + str(col_name) + '** ' + ": " + str(value) + '  \n'
            return s
        return "Model does not exist"


    def filter_by(self,array):
        print(array)
        # Load the CSV file into a list of lists
        with open(self.csv_filepath, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            csv_data = [row for row in csv_reader]

        # Mapping from array index to csv row index
        index_mapping = {
            3: 4,
            4: 5,
            5: 3,
            9: 14,
            10: 15,
            11: 17
        }

        matching_first_elements = []

        # For each row in the CSV data
        for row in csv_data:
            match = True

            # Check each element in the array
            for i, value in enumerate(array):
                csv_index = index_mapping.get(i, i)  # Get the corresponding index in the row, default to i

                # Comparison based on type of the value
                if isinstance(value, list) and value != []:
                    for item in value:
                        if item not in row[csv_index]:
                            match = False
                elif isinstance(value, float) and value != row[csv_index] and value != 0.0:  # float comparison with a tolerance
                    match = False
                elif isinstance(value, str) and value != row[csv_index] and value != '':
                    match = False

            # If all elements matched, add the first element of the row to the result
            if match:
                matching_first_elements.append(row[0])

        return matching_first_elements
    
    #'model' is the name of the model, 'path' is the path to the directory you want to store the model in
    def load_local_ptmodel(self,path,weights,arch):

        module_name = arch.split('.')[0]
        sys.path.insert(0, path)
        __import__(module_name)

        self.model = torch.load(path + '/' + weights ,map_location=torch.device('cpu'))

    def load_mlflow_ptmodel(self,model):
        #sys.path.insert(0, self.arch_path)
        #__import__(model)

        df = pd.read_csv(self.csv_filepath)

        desired_row = df[df['name'] == model]

        uri = desired_row['uri'].values[0]

        # Load model as a PyFuncModel.
        self.model = mlflow.pytorch.load_model(uri)

    def model_summary(self):
        summary(self.model)

    # layers is a list with the name of the layers
    def freeze_layers(self,layers):
        #Freezing layers
        for layer in layers:
            for name, param in self.model.named_parameters():
                if param.requires_grad and layer in name:
                    param.requires_grad = False
    
    def change_layer(self, layer_name, new_layer):
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

