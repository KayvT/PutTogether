# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core import serializers
from models import *
from func.Auth import *
from func.TasksHandler import *
from func.PlansHandler import  *
from func.PasswordHandler import *
from func.ProjectHandler import  *
from func.StatesHandler import  *
from django.http import JsonResponse



def page_Home(response):
    """
        :returns Home Page
    """""
    return render(response,'index.html')

@login_required(login_url='/PutTogether/')
def page_Projects(response, p_id):
    """
        
    :param response: 
    :param p_id: Project id
    :return: the user request project page ( tasks and states )
    """""
    proj_obj = Projects.objects.get(project_id=p_id)
    proj_users = [str(usrProjobj.usr_email.email) for usrProjobj in UsrProjects.objects.filter(project_id=proj_obj)] + [str(proj_obj.usr_email.email)]
    if str(response.user) not  in proj_users:
        return render(response, '404.html')

    tasks = Tasks.objects.filter(task_project_id=proj_obj).order_by('task_position')
    states = state.objects.filter(project_id=proj_obj)
    users = [ usrObj.usr_email for usrObj in UsrProjects.objects.filter(project_id=proj_obj)]
    users.append(proj_obj.usr_email)

    return render(response, 'project.html', {"tasks": tasks, 'states': states, "users": users,'project_name':proj_obj.project_name})


@login_required(login_url='/PutTogether/')
def display_projects(response):
    """

    :param response: 
    :return: All the projects related to the user
    """""
    usrobj = Users.objects.get(email=response.user)
    proj = Projects.objects.filter(usr_email=usrobj)
    users = [user.email for user in Users.objects.exclude(email=usrobj.email)]
    allow = True
    if (usrobj.account_type == 'F' and len(proj) == 5):
        allow = False
    elif (usrobj.account_type == 'P' and len(proj) == 200):
        allow = False
    elif usrobj.account_type == 'B':
        allow = True

    all_projects = list(proj)+[p.project_id for p in UsrProjects.objects.filter(usr_email=usrobj)]

    return render(response,'projects_page.html',{"projects":all_projects,'allow':allow,'users':users})


"""THE END"""
def contact_us(response):
    """
        a handler for the user email sender 
    :param response: 
    :return:  
    """""
    data = dict(response.POST)
    message=data['message'][0]
    subject=data['subject'][0]
    if data['email'][0]=="":
        email=response.user.email
    else:
        email=data['email'][0]

    message = Email_Contact_Us(email,subject,message)
    Email_SendServer(message,'puttogethersoftware@gmail.com')

    response = JsonResponse({"message":"mail is send"})
    response.status_code = 200
    return response







