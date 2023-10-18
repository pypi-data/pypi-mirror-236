
import io
import pandas as pd
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from pyspark.sql import SparkSession
from delta import DeltaTable

def azure_blob_connection(connection_string, container_name):

        service_client = BlobServiceClient.from_connection_string(connection_string)
        client = service_client.get_container_client(container_name)
        return client


connection_string='DefaultEndpointsProtocol=https;AccountName=fsideveusrkaadl01;AccountKey=GqSGkEGvBA8scaCpUCr+tvggtbIIlw3SzA/uznPhmY12+FGCVHczOEUQrpyl/TJ39M7KpLUNgmUM+AStf6QFGA==;EndpointSuffix=core.windows.net'
container_name='source'
location_name='/'
file_name='check1.csv'


client=azure_blob_connection(connection_string, container_name)
file_path=location_name+file_name
blob_client = client.get_blob_client(blob=file_path)
blob_content = blob_client.download_blob().readall()
csv_io = io.BytesIO(blob_content)
df = pd.read_csv(csv_io)
print('done')
print(df)

# Convert DataFrame to CSV (you can use other formats if needed)
csv_data = df.to_csv(index=False)

container_name='dataquality'
location_name='test/'
file_name='testfile1234'
client=azure_blob_connection(connection_string,container_name)
file_path=location_name+file_name
blob_name=file_path



client.upload_blob(blob_name, csv_data, overwrite=True)



# # Convert DataFrame to Parquet format in memory
# parquet_data = io.BytesIO()
# df.to_parquet(parquet_data, index=False)

# # Upload the Parquet data to the blob
# blob_client.upload_blob(name=file_path,data=parquet_data.getvalue(), overwrite=True)


# # Convert the Pandas DataFrame to a Delta DataFrame
# delta_df = DeltaTable(df)

# # Write the Delta DataFrame to Azure Data Lake Storage
# #delta_df.write.format("delta").save(file_path)

# with blob_client:
#     blob_client = blob_client.get_blob_client(container=container_name, blob=blob_name)
#     blob_client.upload_blob(delta_df.to_pyarrow().serialize(), overwrite=True)

# Your dictionary


# Your list
input_list = ["object", "int64", "float64", "object"]

type_mapping = {
    "object": "string",
    "int64": "int",
    "float64": "float",
    "datetime64": "string"
}
# Lambda function to replace keys in the list
replace_func = lambda x: type_mapping.get(x, x)

# Use map to apply the lambda function to the list
output_list = list(map(replace_func, input_list))

print(output_list)