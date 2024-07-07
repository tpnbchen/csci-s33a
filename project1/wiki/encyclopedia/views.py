from django.shortcuts import render
from django.http import HttpResponseRedirect
from markdown2 import markdown
from . import util
from django import forms
from django.urls import reverse
import requests


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)


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

    # implemented without Django Forms as an exercise
    title = request.POST.get('q')
    if util.get_entry(title):
        return renderEntry(request, title)
    else:

        # return entries with titles containing the search string
        results = [entry for entry in util.list_entries() if title.lower() in entry.lower()]
        if len(results) > 0:
            return render(request, "encyclopedia/results.html", {
                "entries": results
            })
        else:
            return entryNotFound(request, title)


# create a new entry
def new(request):

    # retrieve and validate form input
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # if a entry with already exists
            if title in util.list_entries():
                return render(request, "encyclopedia/entry_exists.html", {
                    "title": title
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("wiki:entry", args=(title,)))
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm(),
            "title": "New Entry"
        })


# edit an existing entry
def edit(request, title):

    # retrieve and validate form input
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:entry", args=(title,)))
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    else:
        content = markdown(util.get_entry(title))
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm(initial={"content": content, "title": "Title cannot be edited"}),
            "title": title
        })

def random():
    


# helper function to display an entry
def renderEntry(request, title):
    content = markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })


# helper function to display entry not found page
def entryNotFound(request, title):
    return render(request, "encyclopedia/entry404.html", {
            "title": title
        })