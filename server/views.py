""" Views for Sale Application """
import json #@UnresolvedImport

import boto3
from botocore.exceptions import ClientError
from django.shortcuts import redirect
from django.views.generic import View
from django.http.response import JsonResponse, HttpResponse
from django.template.response import TemplateResponse
from django.contrib import messages
from .utils import start_server, stop_server, reboot_server

class ManagerServerView(View):
    """ View Manager server AWS """
    def get(self, request):
        """ Get method """
        #https://github.com/aws/aws-cli
        client = boto3.client('ec2')
        response = client.describe_instances()
        list_servers = []
        for ec2 in response['Reservations']:
            dict_servers = {}
            dict_servers['name'] = ec2['Instances'][0]['Tags'][0]['Value']
            dict_servers['instance_id'] = ec2['Instances'][0]['InstanceId']
            status = ec2['Instances'][0]['State']['Name']
            if status == 'running':
                color = '04B404'
            elif status == 'stopped':
                color = 'FF0000'
            else:
                color = 'F7FE2E' #pending
            dict_servers['state'] = {'name': status, 'col': color}
            dict_servers['ip_private'] =  ec2['Instances'][0]['PrivateIpAddress']
            list_servers.append(dict_servers)
            if ec2['Instances'][0]['State']['Name'] == 'running':
                dict_servers['ip_public'] =  ec2['Instances'][0]['PrivateIpAddress']
                dict_servers['dns_public'] =  ec2['Instances'][0]['PublicDnsName']
        list_servers.sort(key=lambda server: server['name'])
        return TemplateResponse(request, 'server/index.html', {'servers': list_servers})
class StartServerView(View):
    """ View Start server AWS """
    def get(self, request):
        """ Get method """
        #https://github.com/aws/aws-cli
        instance_id = request.GET['instance_id']
        client = boto3.client('ec2')
        start_server(client, instance_id)
        return redirect('server:manager_server')


class StopServerView(View):
    """ View Stop server AWS """
    def get(self, request):
        """ Get method """
        #https://github.com/aws/aws-cli
        instance_id = request.GET['instance_id']
        client = boto3.client('ec2')
        stop_server(client, instance_id)
        return redirect('server:manager_server')

class ResetServerView(View):
    """ View Reset server AWS """
    def get(self, request):
        """ Get method """
        #https://github.com/aws/aws-cli
        instance_id = request.GET['instance_id']
        client = boto3.client('ec2')
        reboot_server(client, instance_id)
        return redirect('server:manager_server')