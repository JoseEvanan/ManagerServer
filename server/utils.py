import boto3
from botocore.exceptions import ClientError


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