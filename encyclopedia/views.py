import random
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown
from django import forms

from . import util

markdowner = Markdown()

class NewPageForm(forms.Form):
    pgTitle = forms.CharField(label="Page Title", widget=forms.TextInput(attrs={
        'style': 'width: max-width; min-width: 40vw; margin: 8px;',
        'placeholder': 'Your Title here'
        }))
    pgContent = forms.CharField(label="Page Content", widget=forms.Textarea(attrs={
        'rows': 2, 'cols': 2, 'style': 'height: 150px; width: max-width; min-width: 40vw; margin: 8px;',
        'placeholder': 'Your Markdown Content here'
        }))
    
class EditPageForm(forms.Form):

    pgContent = forms.CharField(label="Page Content", widget=forms.Textarea(attrs={
        'rows': 2, 'cols': 2, 'style': 'height: 250px; width: max-width; min-width: 40vw; margin: 8px;',
        'placeholder': 'Your Markdown Content here'
        }))

def index(request):
    if (request.method == 'GET'):
        search_content = request.GET.get('q')
        if search_content:
            if (util.get_entry(search_content) is None):
                return search_page(request, search_content)
            else:
                return visit_page(request, search_content) 
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def visit_page(request, title):
    rawContent = util.get_entry(title)
    if rawContent is None:
        return render(request, "encyclopedia/error/404.html")
    
    return render(request, "encyclopedia/concept.html", {
        "title": title,
        "content": markdowner.convert(rawContent)
    })

def create_page(request):
    if request.method == 'POST':
        newPgForm = NewPageForm(request.POST)
        if newPgForm.is_valid():
            pgTitle = newPgForm.cleaned_data["pgTitle"]
            pgContent = newPgForm.cleaned_data["pgContent"]
            if (util.get_entry(pgTitle) is None):
                util.save_entry(pgTitle, pgContent)
                return HttpResponseRedirect(reverse("visit_page", args=[pgTitle]))
            else:
                newPgForm.add_error("pgTitle", "Content already exists!")
                
        return render(request, "encyclopedia/create.html", {
            "newPgForm": newPgForm
        })
        
    
    return render(request, "encyclopedia/create.html", {
        "newPgForm": NewPageForm()
    })

def search_page(request, query):
    matching_entries = util.list_entries(query)
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": matching_entries
    })

def edit_page(request, title):
    if request.method == "POST":
        editPgForm = EditPageForm(request.POST)
        if editPgForm.is_valid():
            pgContent = editPgForm.cleaned_data["pgContent"]
            util.save_entry(title, pgContent)
            return HttpResponseRedirect(reverse("visit_page", args=[title]))

    rawContent = util.get_entry(title)
    editPgForm = EditPageForm()
    editPgForm.fields["pgContent"].initial = rawContent

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "editPgForm": editPgForm
    })

def random_page(request):
    pages = util.list_entries()
    random_page = random.choice(pages)
    return HttpResponseRedirect(reverse("visit_page", args=[random_page]))