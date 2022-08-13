from django.contrib import messages
from django.shortcuts import render, redirect
from . forms import *
from django.views import generic
from . models import Homework, Todo
from youtubesearchpython import VideosSearch
import requests
import wikipedia
import random
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, "dashboard/home.html")

@login_required
def notes(request):
    if request.method == "POST":
        form = Notesform(request.POST)
        if form.is_valid():
            note = Notes(user= request.user, title= request.POST['title'],description=request.POST['description'])
            note.save()
        messages.success(request,f"Notes added from {request.user.username} Successfullly!")
    else:
        form = Notesform()
    notes = Notes.objects.filter(user=request.user)
    context = {"notes":notes,"form":form}
    return render(request, "dashboard/notes.html",context)

def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()  
    return redirect("notes")

class notedetail(generic.DetailView):
            model = Notes

@login_required
def homework(request):
    if request.method == "POST":
        form = Homeworkform(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST["subject"],
                title = request.POST["title"],
                description = request.POST["description"],
                due = request.POST["due"],
                is_finished = request.POST.get("is_finished",False)
            )   

            homeworks.save()  
            messages.success(request,f"Homework added from {request.user.username}!!")
    else:
        form = Homeworkform()
    works = Homework.objects.filter(user=request.user)
    if len(works) == 0:
        homework_done = True
    else:
        homework_done = False

    context = {"works":works,"is_homework":homework_done,"form":form}
    return render(request, "dashboard/homework.html",context)

def delete_homework(request,pk=None,page=None):
    Homework.objects.get(id=pk).delete()
    if page =='profile':
        print(page)
        return redirect(page)
    else:
        return redirect("homework")

def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished:
        homework.is_finished = False
    else:
        homework.is_finished = True
 
    homework.save()
    return redirect("homework")

def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        videos = VideosSearch(text,limit=100)

        result_list=[]
        for i in videos.result()['result']:
            result_dict= {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }   
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc +=j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context={"form":form,"result_list":result_list}      
        return render(request, "dashboard/youtube.html",context) 
    else:
        form = DashboardForm()
    context = {"form":form}
    return render(request, "dashboard/youtube.html",context)

@login_required
def todo(request):
    if request.method == "POST":
        form = Todoform(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(user= request.user,title =request.POST['title'],is_finished = finished)
        todos.save()
        messages.success(request,f"Todo Added from {request.user}!!")
    else:
        form = Todoform()
    todos = Todo.objects.filter(user=request.user)
    if len(todos) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {'form':form,'todos':todos,'todo_done':todo_done}
    return render(request,"Dashboard/todo.html",context)

def deletetodo(request,pk=None,page=None):
    Todo.objects.get(id=pk).delete()
    # return redirect('todo')
    
    if page =='profile':
        print(page)
        return redirect(page)

    else:
        return redirect('todo')

def updatetodo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list=[]
        for i in range(10):
            result_dict= {
                'input':text,
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCout'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')
                 
            }   
            result_list.append(result_dict)
            context={"form":form,"result_list":result_list}      
        return render(request,"Dashboard/books.html",context)

    else:
        form = DashboardForm()
    context = {"form":form}
    return render(request,"Dashboard/books.html",context)

def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        print('hhello' + url)
        r = requests.get(url)
        answer = r.json()
        print(answer)
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context= {
                "form":form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context= {
                'form':form,
                'input':''                
            }
        return render(request,"Dashboard/dictionary.html",context)
    else:
        form = DashboardForm()
        context = {'form':form}
        return render(request,"Dashboard/dictionary.html",context)

def wiki(request):
    if request.method == "POST":
        text = request.POST['text']
        form = DashboardForm(request.POST)
        # search = wikipedia.page(text)
        try:
            search = wikipedia.page(text)
        except wikipedia.DisambiguationError as e:
            s = random.choice(e.options)
            search = wikipedia.page(s)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request, "Dashboard/wiki.html",context)
    else:
        form = DashboardForm()
        context = {'form':form}
        return render(request, "Dashboard/wiki.html",context)

def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == "length":
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f"{input} yard = {int(input)*3} foot"
                    
                    if first == 'foot' and second == 'yard':
                        answer = f"{input} yard = {int(input)/3} foot"
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }

        if request.POST['measurement'] == "mass":
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f"{input} pound = {int(input)*0.453592} kilogram"
                    
                    if first == 'kilogram' and second == 'pound':
                        answer = f"{input} kilogram = {int(input)*2.20462} pound"
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
    else:
        form = ConversionForm()
        context = {'form':form,'input':False}
    return render(request,"Dashboard/conversion.html",context )

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created for {username}!!")
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form':form}
    return render(request, "Dashboard/register.html",context)
 

@login_required
def profile(request):
    homework = Homework.objects.filter(user=request.user)
    todos = Todo.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todo_done = True
    else:
        todo_done = False
    
    context = {
        'homework':homework,
        'home_done':homework_done,
        'todos':todos,
        'todo_done':todo_done
    }
    return render(request, "Dashboard/profile.html",context)

# def login(request):
#     return render(request, "Dashboard/login.html")

# def logout(request):
#     return render(request, "Dashboard/logout.html")