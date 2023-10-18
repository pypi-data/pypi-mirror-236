from azure.storage.blob import BlobServiceClient
import io
import pandas as pd
#Function to get connection client for ADLS Blob
def azure_blob_connection(connection_string,container_name):
   
	service_client = BlobServiceClient.from_connection_string(connection_string)
	client = service_client.get_container_client(container_name)
	
	return client
	
		

connection_string='qkaain4t7m5unjxy42h5cup774-wpqmpxlqwpfetnjlhu6aoyaile.datawarehouse.pbidedicated.windows.net'
container_name=''
file_path=''


client=azure_blob_connection(connection_string, container_name)

blob_client = client.get_blob_client(blob=file_path)
blob_content = blob_client.download_blob().readall()
csv_io = io.BytesIO(blob_content)
df = pd.read_csv(csv_io)