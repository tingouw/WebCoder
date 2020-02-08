from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
from django.template import loader
import psutil
import os
import uuid
import subprocess

def index(request):
    context = {
        'CPU' : str(psutil.cpu_percent()) + "%",
    }
    return render(request, "coder/index.html", context)

def upload_file(request):
    if request.method == "POST":
        myFile =request.FILES.get("myfile", None)
        if not myFile:
            returnHttpResponse("no files for upload!")
        ProjectId = uuid.uuid1()
        os.mkdir(os.path.join("/var/CoderUpload",str(ProjectId)))
        destination = open(os.path.join("/var/CoderUpload",str(ProjectId),myFile.name),'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        context = {
            'ProjectId' : str(ProjectId),
            'FileName' : myFile.name,
        }
        return render(request, "coder/uploadFile.html", context)

def project_view(request):
    if 'file' in request.GET:
        context = {
            'ProjectId' : request.GET['id'],
            'FileName' : request.GET['file'],
        }
        return render(request, "coder/SetTranscode.html", context)
    else:
        context = {
            'ProjectId' : request.GET['id'],
            'FileList' : os.listdir("/var/CoderUpload/" + str(request.GET['id'])),
        }
        return render(request, "coder/ProjectViewFiles.html", context)

def trans_code(request):
    comm = "ffmpeg -i '/var/CoderUpload/" + request.POST['ProjectId'] + "/" + request.POST['FileName'] + "' " + request.POST['Ffmpeg'] + " '/var/CoderUpload/" + request.POST['ProjectId'] + "/" + request.POST['OutputFileName'] + "'"
    SubProcess = subprocess.check_output(comm , shell=True)
    Return = str(SubProcess)
    context = {
        'return' : Return,
        'ProjectId' : request.POST['ProjectId'],
        'OutputFileName' : request.POST['OutputFileName'],
    }
    return render(request, "coder/TransCode.html", context)

def download_file(request):
    file=open("/var/CoderUpload/" + request.GET['ProjectId'] + "/" + request.GET['FileName'],'rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="' + request.GET['ProjectId'] + "_" + request.GET['FileName'] + '"'
    return response

# Create your views here.
