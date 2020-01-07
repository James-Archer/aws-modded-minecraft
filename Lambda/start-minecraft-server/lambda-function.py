import json
import base64
import boto3

PASSWORDS = {
    '<SERVER-NAME>': '<SERVER-PASSWORD>',
}

def lambda_handler(event, context):
    # TODO implement
    if event['httpMethod'] == 'POST':
        body = str(base64.decodestring(str.encode(event["body"])))
        split = body.split("&")
        svr = split[0].split("=")[1]
        pwd = split[1].split("=")[1][:-1]
        if PASSWORDS[svr] == pwd:
            # TODO switch server on
            ec2 = boto3.client('ec2')
            r = ec2.describe_instances(Filters=[{'Name':'tag:Name', 'Values':[f"Minecraft-server-{svr}"]}])["Reservations"][0]
            r = r["Instances"][0]
            inst_id = r["InstanceId"]
            resp = ec2.start_instances(InstanceIds=[inst_id])
            if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return {
                    'statusCode': 200,
                    'body': json.dumps(['Correct password!', svr, pwd, True])
                }
            else:
                return {
                    'statusCode': 200,
                    'body': json.dumps(['Correct password!', svr, pwd, False])
                }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(['Incorrect password!', svr, pwd])
            }
    else:
        return {
            'statusCode': 501,
            'body': json.dumps('No POST request made!')
        }
