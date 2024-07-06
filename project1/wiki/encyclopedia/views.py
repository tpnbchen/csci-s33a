from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import markdown_path
from . import util
from django import forms
import requests


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    entry = forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# return a wiki entry
def entry(request, title):     
    if util.get_entry(title):
        return renderEntry(request, title)
    else:
        return entryNotFound(request, title)


# search
def search(request):
    title = request.POST.get('q')
    if util.get_entry(title):
        return renderEntry(request, title)
    else:    
        results = [entry for entry in util.list_entries() if title.lower() in entry.lower()]
        if len(results) > 0:
            return render(request, "encyclopedia/results.html", {
                "entries": results
            })
        else:
            return entryNotFound(request, title)


# create a new entry
def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]
            if title in util.list_entries():
                return render(request, "encyclopedia/entry_exists.html", {
                    "title": title
                })
            else: 
                path = ("entries/")
                file = open(f"{path}{title}.md", "w")
                file.write(entry)
                file.close()
                return renderEntry(request, title)
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
        
    return render(request,"encyclopedia/new.html", {
        "form": NewEntryForm()
    })
              

# helper function to display an entry
def renderEntry(request, title):
    html = markdown_path(f"entries/{title}.md")
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html
    })


# helper function to display entry not found page
def entryNotFound(request, title):
    return render(request, "encyclopedia/entry404.html", {
            "title": title
        })