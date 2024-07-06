from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import markdown_path
from . import util
from django import forms
import requests


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# return a wiki entry
def entry(request, title):     
    if util.get_entry(title):
        return renderPage(request, title)
    else:
        return render(request, "encyclopedia/entry404.html", {
            "title": title
        })


# search
def search(request):
    title = request.POST.get('q')
    if util.get_entry(title):
        return renderPage(request, title)
    else:    
        results = [entry for entry in util.list_entries() if title.lower() in entry.lower()]
        return render(request, "encyclopedia/results.html", {
            "entries": results
         })


def renderPage(request, title):
    html = markdown_path(f"entries/{title}.md")
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html
    })