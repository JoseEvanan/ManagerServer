import boto3
from botocore.exceptions import ClientError


def list_group_security():
    client = boto3.client('ec2')
    list_response = []
    response = client.describe_security_groups()
    #response = client.describe_security_groups(GroupIds=['sg-34c03a4a'])
    #print(response)
    """for group in response['SecurityGroups']:
        print(group)
        print("----")
        print("----")"""
    return response['SecurityGroups']
"""
{'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
                 'IpProtocol': 'tcp',
                 'ToPort': 80,
                 'PrefixListIds': [],
                 'FromPort': 80,
                 'UserIdGroupPairs': [],
                 'Ipv6Ranges': [{'CidrIpv6': '::/0'}]}
"""


def get_details_group(id_group):
    client = boto3.client('ec2')
    response = client.describe_security_groups(GroupIds=[id_group])
    return response


def list_servers(permission=True):
    client = boto3.client('ec2')
    response = client.describe_instances()
    list_servers = []
    if not permission:
        servers_filter = Server.objects.filter(is_active=True).values('id_server')
        list_id_servers = list(servers_filter)

    for ec2 in response['Reservations']:
        dict_servers = {}
        #print("----------------")
        #Revisar se cae cuando esta prendiendo un nuevo servidor
        #print("----------------")
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


def create_group_security():
    ec2 = boto3.client('ec2')

    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    response = ec2.create_security_group(GroupName='SECURITY_GROUP_NAME',
                                         Description='DESCRIPTION',
                                         VpcId=vpc_id)
    security_group_id = response['GroupId']
    return security_group_id


def authorize_group_ingress():
    security_group_id = create_group_security()
    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])


def remove_perm_ingress(id_group, perm):

        ec2 = boto3.resource('ec2')
        sec_group = ec2.SecurityGroup(id_group)
        if perm['ip']:
            print("NO null")
            sec_group.revoke_ingress(IpProtocol=perm['protocol'],
                                         CidrIp=perm['ip'],
                                         FromPort=int(perm['fromport']),
                                         ToPort=int(perm['toport']))
            if perm['protocol'] == -1:
                sec_group.revoke_ingress(IpProtocol=perm['protocol'],
                                         CidrIp=perm['ip'])
            else:
                sec_group.revoke_ingress(IpProtocol=perm['protocol'],
                                         CidrIp=perm['ip'],
                                         FromPort=int(perm['fromport']),
                                         ToPort=int(perm['toport']))
        else:
            print("null")
            sec_group.revoke_ingress(IpProtocol=perm['protocol'],
                                         CidrIp='::/0',
                                         FromPort=int(perm['fromport']),
                                         ToPort=int(perm['toport']))

    
       

def remove_perm_egress(id_group, perm):
    try:
        ec2 = boto3.resource('ec2')
        sec_group = ec2.SecurityGroup(id_group)
        sec_group.revoke_egress(IpProtocol=perm['protocol'],
                                CidrIp=perm['ip'],
                                FromPort=int(perm['fromport']),
                                ToPort=int(perm['toport']))
        return True
    except:
        return False

def add_perm_ingress(id_group, perm):
    try:
        ec2 = boto3.resource('ec2')
        sec_group = ec2.SecurityGroup(id_group)
        sec_group.authorize_ingress(IpProtocol=perm['protocol'],
                                CidrIp=perm['ip'],
                                FromPort=int(perm['fromport']),
                                ToPort=int(perm['toport']))
        return True
    except:
        return False

def add_perm_egress(id_group, perm):
    try:
        ec2 = boto3.resource('ec2')
        sec_group = ec2.SecurityGroup(id_group)
        sec_group.authorize_egress(IpProtocol=perm['protocol'],
                                CidrIp=perm['ip'],
                                FromPort=int(perm['fromport']),
                                ToPort=int(perm['toport']))
        return True
    except:
        return False




#ec2 = boto3.resource('ec2')
#sec_group = ec2.SecurityGroup(id_group)
#sec_group.revoke_egress(IpProtocol="tcp",
#                        CidrIp="0.0.0.0/0",
#                        FromPort=3306,
#                        ToPort=3306)



#sec_group.revoke_ingress(IpProtocol="tcp", CidrIp="0.0.0.0/0", FromPort=3306, ToPort=3306)
# authorize_egress()

#conn = boto3.client('ec2')
#conn.authorize_security_group_ingress(GroupId=my_group_id,IpProtocol="tcp",CidrIp="new_ip/32",FromPort=443,ToPort=443)

#security_group.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=3306,ToPort=3306)

