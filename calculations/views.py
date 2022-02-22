from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm
from .functions import createResults

def frontSite(request):
    projects = Project.objects.all()
    data = {
        'projects': projects
    }
    return render(request, 'front_page.html', data)


def createProject(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('front_site')
    data = {
        'form': form
    }

    return render(request, 'create_form.html', data)

def showProjectResult(request, pk):

    project = Project.objects.get(id=pk)
    file = project.file
    results = createResults(file)

    data = {
        'project': project,
        'results': results,
    }

    return render(request, 'project_results.html', data)