from multiprocessing import context
from turtle import title
from django.shortcuts import render
import markdown
import random

from . import util

def converthtml(title):
    htmlcontent = util.get_entry(title)
    markdowner = markdown.Markdown()
    if htmlcontent == None:
        return None
    else:
        return markdowner.convert(htmlcontent)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = converthtml(title)
    if html_content == None :
        return render(request, "encyclopedia/error.html", {
            "message" : "Entry doesn't exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "content" : html_content
        } )

def search(request):
    entry_search = request.POST['q']
    htmlcontent = converthtml(entry_search)
    if htmlcontent is not None:
        return render(request, "encyclopedia/entry.html", {
            "title" : entry_search,
            "content" : htmlcontent
        })
    else:
        all= util.list_entries()
        recomend = []
        for entry in all:
            if entry_search.lower() in entry.lower():
                recomend.append(entry)
        return render (request, "encyclopedia/search.html", {
            "recomend" : recomend
        })

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titlethis = util.get_entry(title)
        if titlethis is not None:
            return render(request, "encyclopedia/error.html", {
                "message" : "This page already exist in Database"
            })
        else:
            util.save_entry(title, content)
            htmlcontent = converthtml(title)
            return render(request, "encyclopedia/entry.html", {
                "title" : title,
                "content" : htmlcontent
            })

def edit(request):
    if request.method == 'POST':
        title = request.POST['header']
        content = util.get_entry(title)
        return render (request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        htmlcontent = converthtml(title)
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "content" : htmlcontent
        })

def ran(request):
    all = util.list_entries()
    ranentry = random.choice(all)
    htmlcontent = converthtml(ranentry)
    return render(request, "encyclopedia/entry.html", {
        "title" : ranentry,
        "content" : htmlcontent
    })