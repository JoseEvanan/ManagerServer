""" Views for Sale Application """
import json #@UnresolvedImport
import ast
import boto3

from botocore.exceptions import ClientError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.http.response import JsonResponse, HttpResponse
from django.template.response import TemplateResponse
from django.contrib import messages
from .utils import start_server, stop_server, reboot_server,\
list_servers, list_group_security, get_details_group,\
remove_perm_ingress, add_perm_ingress, remove_perm_egress,\
add_perm_ingress, add_perm_egress
from .models import Servers







class ManagerServerView(View):
    """ View Manager server AWS """
    def get(self, request):
        """ Get method """
        #https://github.com/aws/aws-cli
        list_server = list_servers()
        list_groups = list_group_security()
        return render(request, 'server/index.html', {'servers': list_server,
                                                     'group_security': list_groups})



class DetailGroupView(View):
    def get(self, request):
        """ Get method """
        #https://github.com/aws/aws-cli
        id_group = request.GET['id_group']
        list_group = get_details_group(id_group)
        return JsonResponse({'detail_group': list_group})

class RemovePermView(View):
    def get(self, request):
        """ Get method """
        data_perm = {}
        id_group = request.GET['id_group']
        action = request.GET['action']
        type_perm = request.GET['type']
        data_perm['protocol'] = request.GET['Protocol']
        data_perm['fromport'] = request.GET['FromPort']
        data_perm['toport'] = request.GET['ToPort']
        
        data_perm['ip'] = request.GET['IpRanges']
        if data_perm['ip'] == 'null':
            data_perm['ip'] = None
        if type_perm == 'inbound':
            status = remove_perm_ingress(id_group, data_perm)
        else:
            status = remove_perm_egress(id_group, data_perm)
        
        if status:
            response = "Cambios Actualizados"
        else:
            response = "Cambios NO Actualizados"
        return JsonResponse({'status': response})


class ChangePermView(View):
    def get(self, request):
        """ Get method """
        id_group = request.GET['id_group']
        type_event = request.GET['type_event']
        perm_present = {}
        perm_past = {}
        perm_past['protocol'] = request.GET['past_protocol']
        perm_past['fromport'] = request.GET['past_frmoip']
        perm_past['toport'] = request.GET['past_toip']
        perm_past['ip'] = request.GET['past_ips']
        perm_present['protocol'] = request.GET['present_protocol']
        perm_present['fromport'] = request.GET['present_frmoip']
        perm_present['toport'] = request.GET['present_toip']
        perm_present['ip'] = request.GET['present_ips']
        if data_perm['ip'] == 'null':
            data_perm['ip'] = None
        if type_event == 'inbound':
            status = remove_perm_ingress(id_group, perm_past)
            if status:
                status = add_perm_ingress(id_group, perm_present)
        else:
            status = remove_perm_egress(id_group, perm_past)
            if status:
                status = add_perm_egress(id_group, perm_present)

        if status:
            response = "Cambios Actualizados"
        else:
            response = "Cambios NO Actualizados"
        return JsonResponse({'status': response})


"""
{'id_group': id_group,
       'past_protocol': perm_past['protocol'],
       'past_frmoip': perm_past['frmoip'],
       'past_toip': perm_past['toip'],
       'past_ips': perm_past['ips'],
       'present_protocol': perm_past['protocol'],
       'present_frmoip': perm_past['frmoip'],
       'present_toip': perm_past['toip'],
       'present_ips': perm_past['ips']
     },
IpProtocol=perm.protocol,
                             CidrIp=perm.ip,
                             FromPort=perm.fromport,
                             ToPort=perm.toport)
"""
class ListServerView(View):
    """ View Start server AWS """
    def get(self, request):
        """ Get method """
        #https://github.com/aws/aws-cli
        list_server = list_servers()
        
        return JsonResponse({'servers': list_server})


class SaveServerView(View):
    """ View Start server AWS """
    def get(self, request):
        """ Get method """
        #https://github.com/aws/aws-cli
        string_server = request.GET['servers']
        list_server = ast.literal_eval(string_server)
        for server in list_server:
            if server['status'] == 'true':
                server, created = Servers.objects.get_or_create(id_server=server['server'])
                print('creado ', created)
        print('-----------')
        return JsonResponse({})

class StartServerView(View):
    """ View Start server AWS """
    def get(self, request):
        """ Get method """
        #https://github.com/aws/aws-cli
        instance_id = request.GET['instance_id']
        client = boto3.client('ec2')
        start_server(client, instance_id)
        return redirect(reverse('server:manager_server'))


class StopServerView(View):
    """ View Stop server AWS """
    def get(self, request):
        """ Get method """
        #https://github.com/aws/aws-cli
        instance_id = request.GET['instance_id']
        client = boto3.client('ec2')
        stop_server(client, instance_id)
        print(reverse('server:manager_server'))
        return redirect(reverse('server:manager_server'))


class ResetServerView(View):
    """ View Reset server AWS """
    def get(self, request):
        """ Get method """
        #https://github.com/aws/aws-cli
        instance_id = request.GET['instance_id']
        client = boto3.client('ec2')
        reboot_server(client, instance_id)
        return redirect(reverse('server:manager_server'))


