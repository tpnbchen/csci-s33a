from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import markdown_path
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request):
    return render(request, "encyclopedia/page.html", {
        "items":[1, 2, 3]
    })


def entry(request, title):
    if util.get_entry(title):
        html = markdown_path(f"entries/{title}.md")
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "content": html
        })
    else:
        return render(request, "encyclopedia/entry404.html", {
            "title":title
        })
    # return HttpResponse(f"Entry, {title}")



