from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
import math
import random
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content": markdown2.markdown(content)
        })
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

def search(request):
    title = request.GET['q']
    content = util.get_entry(title)
    if content:
        return redirect("title", title=title)
    else:
        fulllist = util.list_entries()
        searchlist = []
        for item in fulllist:
            if title.upper() in item.upper():
                searchlist.append(item)
        return render(request, "encyclopedia/search.html", {
            "entries": searchlist
        })

def create(request):
    if request.method == "POST":
        title = request.POST['title']
        if title in util.list_entries():
            return HttpResponse("<h1>Depulicate Title</h1>")
        else:
            util.save_entry(title, request.POST['content'])
            return redirect("title", title=title)
    else:
        return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "POST":
        util.save_entry(title, request.POST['content'])
        return redirect("title", title=title)
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def random_search(request):
    fulllist = util.list_entries()
    title = (fulllist[math.floor(random.random() * len(fulllist))])
    return redirect("title", title=title)