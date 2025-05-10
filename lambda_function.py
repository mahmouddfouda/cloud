import json
import boto3
import os
from datetime import datetime

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'Orders')
orders_table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    for record in event['Records']:
        # SQS messages contain SNS messages as strings
        sns_message = json.loads(record['body'])
        
        # Parse actual order JSON from SNS
        order_data = json.loads(sns_message['Message'])

        # Log incoming message
        print("Received order:", order_data)

        try:
            # Put item into DynamoDB
            response = orders_table.put_item(
                Item={
                    'orderId': order_data['orderId'],
                    'userId': order_data['userId'],
                    'itemName': order_data['itemName'],
                    'quantity': int(order_data['quantity']),
                    'status': order_data['status'],
                    'timestamp': order_data['timestamp']
                }
            )
            print("Order stored successfully:", response)
        except Exception as e:
            print("Error storing order:", e)
            raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Orders processed successfully')
    }