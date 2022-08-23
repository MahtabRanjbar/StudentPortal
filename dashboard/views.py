from gc import is_finalized
import requests
import wikipedia
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
from youtubesearchpython import VideosSearch
from django.contrib.auth.decorators import login_required

from .forms import (ConversionForm, ConversionLengthForm, ConversionMassForm,
                    DashboardForm, HomeworkForm, NotesForm, ToDoForm,
                    UserregistrationForm)
from .models import Homework, Notes, ToDo


# Create your views here.
def home(request):
    return render(request, "dashboard/home.html")

@login_required
def notes_view(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user,
                title=request.POST["title"],
                description=request.POST["description"],
            )
            notes.save()
        messages.success(
            request, f"Notes Added From {request.user.username} Successfully!"
        )
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {"notes": notes, "form": form}
    return render(request, "dashboard/notes.html", context=context)

@login_required
def delete_note(request, pk):
    Notes.objects.get(id=pk).delete()
    return redirect("dashboard:notes-page")

@login_required
class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = "notes_detail"

@login_required
def homework_view(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False

            except:
                finished = False

            homework = Homework(
                user=request.user,
                subject=request.POST["subject"],
                title=request.POST["title"],
                description=request.POST["description"],
                due=request.POST["due"],
                is_finished=finished,
            )
            homework.save()
            messages.success(request,
                             f"Homework Added from {request.user.username}")
    else:
        form = HomeworkForm()
    homeworks = Homework.objects.filter(user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False

    context = {"homeworks": homeworks,
               "homework_dones": homework_done,
               "form": form}
    return render(request, "dashboard/homework.html", context=context)

@login_required
def update_homework_view(request, pk):
    homework = Homework.objects.get(id=pk)

    if homework.is_finished is True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()

    return redirect("dashboard:homework")

@login_required
def delete_homework_view(request, pk):
    Homework.objects.get(id=pk).delete()
    return redirect("dashboard:homework")


def youtube_view(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        videos = VideosSearch(text, limit=10)
        res_list = []
        for response in videos.result()["result"]:
            res_dict = {
                "input": text,
                "title": response["title"],
                "duration": response["duration"],
                "thumbnail": response["thumbnails"][0]["url"],
                "channel": response["channel"]["name"],
                "link": response["link"],
                "views": response["viewCount"]["short"],
                "published": response["publishedTime"],
            }
            desc = ""
            if response["descriptionSnippet"]:
                for x in response["descriptionSnippet"]:
                    desc += x["text"]
            res_dict["description"] = desc
            res_list.append(res_dict)
        context = {"form": form, "results": res_list}
        return render(request, "dashboard/youtube.html", context)

    else:
        form = DashboardForm()
    context = {"form": form}
    return render(request, "dashboard/youtube.html", context)

@login_required
def todo_view(request):
    if request.method == 'POST':

        form = ToDoForm(request.POST)

        if form.is_valid():
            try:
                if request.POST['is_finished'] == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todo = ToDo(user=request.user,
                        title=request.POST['title'],
                        is_finished=finished
                        )
            todo.save()
            messages.success(request,
                             f"Todo Added From { request.user.username }")

    else:
        form = ToDoForm()
    tasks = ToDo.objects.all()
    if len(tasks) == 0:
        tasks_done = True
    else:
        tasks_done = False

    context = {'tasks': tasks,
               'tasks_done': tasks_done,
               'form': form
               }
    return render(request, 'dashboard/todo.html', context=context)

@login_required
def delete_todo_view(request, pk=None):
    ToDo.objects.get(id=pk).delete()
    return redirect(reverse('dashboard:todo'))

@login_required
def update_todo_view(request, pk=None):
    task = ToDo.objects.get(id=pk)
    if task.is_finished is True:
        task.is_finished = False
    else:
        task.is_finished = True
    task.save()

    return redirect('dashboard:todo')


def book_view(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        books_url = 'https://www.googleapis.com/books/v1/volumes?q=' + text
        r = requests.get(books_url)
        response = r.json()
        res_list = []
        for i in range(10):
            res_dict = {
                "title": response["items"][i]['volumeInfo']['title'],
                "subtitle": response["items"][i]['volumeInfo'].get('subtitle'),
                "description": response["items"][i]['volumeInfo'].get('description'),
                "count": response["items"][i]['volumeInfo'].get('pageCount'),
                "categories": response["items"][i]['volumeInfo'].get('categories'),
                "rating": response["items"][i]['volumeInfo'].get('pageRating'),
                "thumbnail": response["items"][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                "preview": response["items"][i]['volumeInfo'].get('previewLink'),
            }

            res_list.append(res_dict)
        context = {"form": form, "results": res_list}
        return render(request, "dashboard/books.html", context)

    else:
        form = DashboardForm()
    context = {"form": form}
    return render(request, "dashboard/books.html", context)


def dictionary_view(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + text
        r = requests.get(url)
        response = r.json()
        try:
            phonetics = response[0]['phonetics'][0]['text']
            audio = response[0]['phonetics'][0]['audio']
            definition = response[0]['meanings'][0]['definitions'][0]['definition']
            example = response[0]['meanings'][0]['definitions'][0]['example']
            synonyms = response[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms,
            }
        except:
            context = {
                'form': form,
                'input': "",
            }
            return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
    return render(request, 'dashboard/dictionary.html', context)


def wikipedia_view(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        try:
            search = wikipedia.page(text)
        except wikipedia.DisambiguationError as e:

            search = wikipedia.page(e.options[1])

        context = {'form': form,
                   'title': search.title,
                   'link': search.url,
                   'details': search.summary
                   }
    else:
        form = DashboardForm()
        context = {'form': form}
    return render(request, 'dashboard/wiki.html', context)


def conversion_view(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)

        if request.POST['measurment'] == 'length':
            measurment_form = ConversionLengthForm()
            context = {
                    'form': form,
                    'm_form': measurment_form,
                    'input': True,
                }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if (first == 'yard') and (second == 'foot'):
                        answer = f'{input} yard={int(input)*3} foot'
                    elif (first == 'foot') and (second == 'yard'):
                        answer = f'{input} foot={int(input)/3} yard'
                context = {
                    'form': form,
                    'm_form': measurment_form,
                    'input': True,
                    'answer': answer
                }
        elif request.POST['measurment'] == 'mass':
            measurment_form = ConversionMassForm()
            context = {
                'form': form,
                'm_form': measurment_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if (first == 'pound') and (second == 'kilogram'):
                        answer = f"{input} ound = {int(input)*0.453592} kilogram "
                    elif (first == 'kilogram') and (second == 'pound'):
                        answer = f" {input} kilogram = {int(input)*2.20462} pound "
                context = {
                    'form': form,
                    'm_form': measurment_form,
                    'input': True,
                    'answer': answer
                }
        return render(request, 'dashboard/conversion.html', context)
    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
            }
    return render(request, 'dashboard/conversion.html', context=context)


def register_view(request):
    if request.method == 'POST':
        form = UserregistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account Created for {username} Successfuly")
            return redirect('sign_in')
            
    else:
        form = UserregistrationForm()
    context = {'form': form}
    return render(request, 'dashboard/register.html', context)
    
@login_required
def profile_view(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    to_do = ToDo.objects.filter(is_finished=False, user=request.user)
    homework_done = False
    to_do_done = False
    if len(homeworks)== 0:
        homework_done = True
    if len(to_do) == 0:
        to_do_done = True
        
    context = {'homework_done': homework_done,
               'homeworks': homeworks,
               'todos': to_do,
               'todo_done': to_do_done}
    return render(request, 'dashboard/profile.html', context)
