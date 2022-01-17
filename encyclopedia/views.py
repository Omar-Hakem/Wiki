from . import util
from django.shortcuts import render
import markdown2
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random


class userEntryForm(forms.Form):
    userInput = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Search Encyclopedia'}))


class newEntryForm(forms.Form):
    entryTitle = forms.CharField(label='Page Title', widget=forms.TextInput(
        attrs={'placeholder': 'enter page title'}))
    entryContent = forms.CharField(label='Page Content', widget=forms.Textarea(
        attrs={'placeholder': 'enter <markdown> content'}))


class contentForm(forms.Form):
    entryContent = forms.CharField(
        label='', widget=forms.Textarea(), required=False)


def getRandomEntry(request):
    entries = util.list_entries()
    maxIndex = len(entries)-1
    index = random.randint(0, maxIndex)
    entryTitle = entries[index]
    return HttpResponseRedirect(reverse("encyclopedia:viewEntry", kwargs={'entryName': entryTitle}))


def editContent(request, entryTitle):
    editContentForm = contentForm(
        initial={'entryContent': util.get_entry(entryTitle)})
    if request.method == "POST":
        editContentForm = contentForm(request.POST)
        if editContentForm.is_valid():
            content = editContentForm.cleaned_data["entryContent"]
            util.save_entry(entryTitle, content)
            return HttpResponseRedirect(reverse("encyclopedia:viewEntry", kwargs={'entryName': entryTitle}))
    return render(request, "encyclopedia/editEntryContent.html", {'title': entryTitle, 'editContentForm': editContentForm})


def viewEntry(request, entryName):
    md = util.get_entry(entryName)
    if md:
        md = markdown2.markdown(md)
    return render(request, "encyclopedia/viewEntry.html", {"title": entryName, "content": md})


def createNewEntry(request):
    entries = util.list_entries()
    repeated = False
    if request.method == "POST":
        entryForm = newEntryForm(request.POST)
        if entryForm.is_valid():
            title = entryForm.cleaned_data["entryTitle"]
            content = entryForm.cleaned_data["entryContent"]
            for entry in entries:
                if entry.lower() == title.lower():
                    repeated = True
                    return render(request, "encyclopedia/errorMessage.html")
            if not repeated:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:viewEntry", kwargs={'entryName': title}))
        else:
            return render(request, "encyclopedia/createNewEntry.html", {"newEntryForm": entryForm})

    return render(request, "encyclopedia/createNewEntry.html", {"newEntryForm": newEntryForm()})


def errorMessage(request):
    return render(request, "encyclopedia/errorMessage.html")


def index(request):
    entries = util.list_entries()
    results = []
    if request.method == "POST":
        form = userEntryForm(request.POST)
        if form.is_valid():
            flag = False
            userInput = form.cleaned_data["userInput"]
            for entry in entries:
                if entry.lower() == userInput.lower():
                    return HttpResponseRedirect(reverse("encyclopedia:viewEntry", kwargs={'entryName': userInput}))

            for entry in entries:
                if userInput.lower() in entry.lower():
                    results.append(entry)
                    flag = True
            if flag:
                return render(request, "encyclopedia/resultsPage.html", {"title": userInput, "results": results})

        else:
            return render(request, "encyclopedia/index.html", {
                "entries": entries, "form": form})

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": userEntryForm()
    })
