

import boto3
import json
from datetime import datetime
import pandas as pd
import pymysql as MySQLdb
import mysql.connector

session = boto3.Session(
    aws_access_key_id="AKIAROKTYHBUCLPHXFH6",
    aws_secret_access_key="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",
    region_name="eu-west-2"
)
sqs_client = session.client("sqs")


def get_connection():

    host='oak-api.ceedji5fvimj.eu-west-2.rds.amazonaws.com'
    port=3306
    username='oak-api-micro'
    password='ThOak@Ap!M!cr012'
    database='consumption'
    
    mydb = mysql.connector.connect(
                                host=host,
                                user=username,
                                password=password,
                                database=database
                                )
    return mydb

def write_to_db(id_, device_id, device_name, site_id, site_name, phase,
       start, end, value, threshold, created_at, updated_at,
       alert_tag):
    mydb = get_connection()
    mycursor = mydb.cursor()
    sql = """INSERT INTO consumption.alerts
            (id, device_id, device_name, site_id, site_name, phase,start, end, value, threshold, created_at, updated_at,alert_tag)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    val = (id_, device_id, device_name, site_id, site_name, phase,
           start, end, value, threshold, created_at, updated_at,
           alert_tag)
    
    mycursor.execute(sql, val)
    mydb.commit()
    
    return 

def get_device_info():

    q="""select D.site_id,S.name as site_name, D.device_id,D.name as device_name,D.type as device_Type,D.category as device_category,D.description as device_description 
    from customer.devices AS D
    inner join customer.sites AS S
    on D.site_id =S.slug"""

    host='oak-api-readreplica.ceedji5fvimj.eu-west-2.rds.amazonaws.com'
    port=3306
    username='oak-api-micro'
    password='ThOak@Ap!M!cr012'
    database='consumption'

    mysql_cn= MySQLdb.connect(host=host, 
                    port=port,user=username, passwd=password, 
                    db=database)
    device_df = pd.read_sql(q, con=mysql_cn)  

    device_df=device_df[['site_id','site_name','device_id','device_name']]
    
    return device_df


def get_writing_parameters(df,type_):
    # type_=df['type'].iloc[0]
    # df=df.drop(columns=['type']).T
    device_df=get_device_info()
    df=df.merge(device_df,on='device_id',how='left')
    id_=df['id'].iloc[0]
    device_id=int(df['device_id'].iloc[0])
    device_name=df['device_name'].iloc[0]
    site_id=df['site_id'].iloc[0]
    site_name=df['site_name'].iloc[0]
    phase=df['phase'].iloc[0]
    start=df['measurement_time'].iloc[0]
    end=df['measurement_time'].iloc[0]

    if type_=="VoltageAlert":
        value=df['voltage'].iloc[0]
        threshold=2
        alert_tag="Voltage Imbalance"
    elif type_=="CurrentAlert":
        value=df['current'].iloc[0]
        threshold=15
        alert_tag="Load Imbalance"
    elif type_=="PowerFactorAlert":
        value=df['power_factor'].iloc[0]
        threshold=0.95
        alert_tag="Low Power Factor"
    else:
        value=df['energy'].iloc[0]
        alert_tag="Abnormal Change in Energy Consumption"
        threshold=0

    created_at=datetime.now()
    updated_at=datetime.now()
    
    return id_, device_id, device_name, site_id, site_name, phase,\
           start, end, value, threshold, created_at, updated_at,\
           alert_tag

def get_queue_url():
    
    response = sqs_client.get_queue_url(
        QueueName="Oak-Alert-Queue",
    )
    return response["QueueUrl"]

def receive_message():
    response = sqs_client.receive_message(
        QueueUrl=get_queue_url(),
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20,
    )

    print(f"Number of messages received: {len(response.get('Messages', []))}")

    for message in response.get("Messages", []):
        message_body = message["Body"]

        print(f"Message body: {message_body}")
        delete_message(message['ReceiptHandle'])
        
        #***********************************************************
        #SQL code goes here
#         try: 
        # df=pd.DataFrame(json.loads(message_body))

        type_=message_body.split("=")[1].split("\n")[0].strip()
        df=pd.DataFrame(json.loads(message_body.split("data =")[1]).items())
        df=df.set_index(0).T

        id_, device_id, device_name, site_id, site_name, phase,\
        start, end, value, threshold, created_at, updated_at,\
        alert_tag=get_writing_parameters(df,type_)

        write_to_db(id_, device_id, device_name, site_id, site_name, phase,
                   start, end, value, threshold, created_at, updated_at,
                   alert_tag)

        
#         except:
#             pass
        #*************************************************************

        #print(f"Receipt Handle: {message['ReceiptHandle']}")
        



def delete_message(receipt_handle):
    
    print("Deleting message")

    response = sqs_client.delete_message(
        QueueUrl=get_queue_url(),
        ReceiptHandle=receipt_handle,
    )
    print(response)

# sampleJson = {
# 	"type": "VoltageAlert",
# 	"data": {
# 		"id": 27924,
# 		"device_id": "134916",
# 		"energy": "386.7000",
# 		"current": 21.5,
# 		"voltage": 0.4745194991626117,
# 		"power": "4640.0000",
# 		"power_factor": 0.8643,
# 		"reactive_power": 2.5300000000000002,
# 		"consumed_active_energy": "null",
# 		"frequency": "null",
# 		"measurement_time": "2021-08-05 16:55:00",
# 		"phase": "R",
# 		"voltage_deviation": 0.4745194991626117
# 	}
# }

sampleJson="""type = CurrentAlert 

data = {
"id": 27924,
"device_id": "134916",
"energy": "386.7000",
"current": 37.673425827107806,
"voltage": 249.59,
"power": "4640.0000",
"power_factor": 0.8643,
"reactive_power": 2.5300000000000002,

"consumed_active_energy": null,

"frequency": null,
"measurement_time": "2021-08-05 16:55:00",
"phase": "R",
"current_deviation": 37.673425827107806
}"""

#Method to trigger a new message
def send_message():
    message = {"key": "value"}
    response = sqs_client.send_message(
        QueueUrl=get_queue_url(),
        MessageBody=sampleJson
    )
    print(response)

#Infinite Loop for receiving messages indefinately 
#send_message()
while(True):
    receive_message()