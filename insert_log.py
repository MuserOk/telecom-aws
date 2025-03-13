import boto3
from datetime import datetime

# Conectar con DynamoDB
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")  
table = dynamodb.Table('pipeline-config')

# Insertar un log
response = table.put_item(
    Item={
        'id_pipeline': 'pipeline_001',
        'status': 'Success',
        'timestamp': datetime.utcnow().isoformat()
    }
)

print("Log registrado con éxito:", response)


#python insert_log.py   #para ejecutar