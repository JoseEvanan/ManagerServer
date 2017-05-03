import boto3
from botocore.exceptions import ClientError

def list_servers(permission=True):
    client = boto3.client('ec2')
    response = client.describe_instances()
    list_servers = []
    if not permission:
        servers_filter = Server.objects.filter(is_active=True).values('id_server')
        list_id_servers = list(servers_filter)

    for ec2 in response['Reservations']:
        dict_servers = {}
        dict_servers['name'] = ec2['Instances'][0]['Tags'][0]['Value']
        dict_servers['instance_id'] = ec2['Instances'][0]['InstanceId']
        status = ec2['Instances'][0]['State']['Name']
        if status == 'running':
            color = '62c462'
        elif status == 'stopped':
            color = 'ee5f5b'
        else:
            color = 'faa732' #pending
        dict_servers['state'] = {'name': status, 'col': color}
        dict_servers['ip_private'] =  ec2['Instances'][0]['PrivateIpAddress']
        list_servers.append(dict_servers)
        if ec2['Instances'][0]['State']['Name'] == 'running':
            dict_servers['ip_public'] =  ec2['Instances'][0]['PrivateIpAddress']
            dict_servers['dns_public'] =  ec2['Instances'][0]['PublicDnsName']
    list_servers.sort(key=lambda server: server['name'])
    return list_servers

def start_server(client, instance_id):
    # Do a dryrun first to verify permissions
    print("START_SERVER")
    try:
        client.start_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances witout dryrun
    try:
        response = client.start_instances(InstanceIds=[instance_id],
                                         DryRun=False)
        print(response)
    except ClientError as e:
        print(e)


def stop_server(client, instance_id):
    # Do a dryrun first to verify permissions
    print("STOP_SERVER")
    try:
        client.stop_instances(InstanceIds=[instance_id],
                               DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = client.stop_instances(InstanceIds=[instance_id],
                                          DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

def reboot_server(client, instance_id):
    print("REBOOT_SERVER")
    try:
        client.reboot_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            print("You don't have permission to reboot instances.")
            raise

    try:
        response = client.reboot_instances(InstanceIds=[instance_id],
                                                        DryRun=False)
        print('Success', response)
    except ClientError as e:
        print('Error', e)