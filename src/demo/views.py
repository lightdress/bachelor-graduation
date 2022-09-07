from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from utils import name_split, transport
from core import ctrl

from .models import PaperConfig


# Create your views here.


def handle_uploaded_file(f):
    filename = '/tmp/tmp.' + name_split.main(f.name)[0][1]
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # with open('config.yaml', 'r') as file:
    #     yaml: str = file.read()
    #     PaperConfig(
    #         owner='Beijing Institution of Technology',
    #         type='Bachelor\'s Thesis',
    #         config=yaml,
    #     ).save()
    config: str = PaperConfig.objects.get(
        owner='Beijing Institution of Technology',
        type='Bachelor\'s Thesis',
    ).config
    return ctrl.main(filename, config).replace('\n', '\n<br/>')


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponse(handle_uploaded_file(request.FILES['file']))
    else:
        form = UploadFileForm()
    return render(request, 'demo/index.html', {'form': form})
