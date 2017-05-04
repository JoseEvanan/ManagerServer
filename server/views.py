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
from .utils import start_server, stop_server, reboot_server, list_servers
from .models import Servers

class ManagerServerView(View):
    """ View Manager server AWS """
    def get(self, request):
        """ Get method """
        #https://github.com/aws/aws-cli
        list_server = list_servers()
        return render(request, 'server/index.html', {'servers': list_server})


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