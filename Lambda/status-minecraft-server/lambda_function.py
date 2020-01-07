import json
import boto3

servers = [
        "Minecraft-server-<SERVER-NAME>"
        ]

def lambda_handler(event, context):
    output = {}
    ec2 = boto3.client('ec2')
    r = ec2.describe_instances(Filters=[{'Name':'tag:Name', 'Values':servers}])["Reservations"]
    for i in r:
        s = i["Instances"][0]
        inst_id = s["InstanceId"]
        name = s["Tags"][0]["Value"]
        state = s["State"]["Name"]
        if state == 'running' or state == 'pending':
            state = True
        else:
            state = False
        print(name, inst_id, state)
        output[name.split("-")[-1]] = state
    return {
        'statusCode': 200,
        'body': json.dumps(output)
    }
