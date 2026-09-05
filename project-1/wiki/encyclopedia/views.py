from django.shortcuts import render, redirect
# Import the render function to render HTML templates

from django.http import HttpResponse
# Import HttpResponse for returning simple HTTP responses

from django.http import HttpResponseRedirect
# Import HttpResponseRedirect for redirecting the user to another URL

from django.urls import reverse
# Import reverse function to resolve URLs dynamically

from . import util  # CS50W provided functions
# Import utility functions from the local "util" module

import markdown2    # Text-to-HTML convertor, see: https://github.com/trentm/python-markdown2
# Import markdown2 to convert markdown content into HTML

import random   # For random page
# Import random module to select random pages

from django.utils.safestring import mark_safe


def index(request):
    """Lists all current entries"""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    # Renders the "index.html" template, passing the list of all entries to the template

def page(request, entry):
    """Renders markdown file in HTML page"""
    content = util.get_entry(entry)
    # Retrieve the content of the specified entry

    if content == None:
        return render(request, "encyclopedia/result.html", {
            "title": "Oh no! Page not found",
            "message": mark_safe("No results found. Click <a href="/">here</a> to go back.")
        })
        # If the entry does not exist, render a "page not found" message

    markdown_text = markdown2.markdown(content)
    # Convert the markdown content to HTML using markdown2

    return render(request, "encyclopedia/page.html", {
        "entry": entry,
        "content": markdown_text
    })
    # Render the entry page with the markdown content converted to HTML

def new(request):
    """Creates a new markdown file via an HTML form"""
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
        # If the request method is GET, render the "new.html" form for creating a new entry

    elif request.method == "POST":
        form = request.POST
        title = form["title"]
        content = form["content"]
        # Extract the title and content from the form data

        entries = util.list_entries()
        # Get the list of existing entries

        print(title)
        print(entries)
        # Print the title and existing entries for debugging

        for item in entries:
            if title.lower() == item.lower():
                return render(request, "encyclopedia/result.html", {
                    "title": "Oh no! Error",
                    "message": f"A post with the title '{title}' already exists. Please choose a different title."
                })
                # If an entry with the same title already exists, show an error message

        util.save_entry(title, content)
        # Save the new entry to the file system

        # Redirect to the new entry"s page after successful creation
        return redirect(f"/wiki/{title}")

def edit(request, entry):
    """Edit markdown file via HTML form"""
    if request.method == "GET":
        content = util.get_entry(entry)
        # Retrieve the content of the entry to be edited

        return render(request, "encyclopedia/edit.html", {
            "title": entry,
            "content": content,
        })
        # Render the "edit.html" template with the entry"s current content

    elif request.method == "POST":
        form = request.POST
        title = form["title"]
        content = form["content"]
        # Extract the updated title and content from the form data

        util.save_entry(title, content)
        # Save the updated entry

        return HttpResponseRedirect(reverse("wiki:page", kwargs={"entry": title}))
        # Redirect the user to the updated entry"s page

def random_page(request):
    """Display random entry"""
    entries = util.list_entries()
    # Get the list of all entries

    page = random.choice(entries)
    # Select a random entry from the list

    return HttpResponseRedirect(reverse("wiki:page", kwargs={"entry": page}))
    # Redirect the user to the randomly selected entry"s page

def search(request):
    """Search for markdown file"""
    if request.method == "POST":
        term = request.POST
        term = term["q"]
        # Extract the search term from the form data

        entries = util.list_entries()
        page = None
        # Initialize a variable to store the found page

        for item in entries:
            if term.lower() == item.lower():
                page = item
                print(f"Exact Match Found! -", page)
                # If an exact match is found, set the page variable and print a debug message

        if page != None:
            return HttpResponseRedirect(reverse("wiki:page", kwargs={"entry": page}))
            # If an exact match is found, redirect to the corresponding page

        list = []
        for item in entries:
            if term.lower() in item.lower():
                list.append(item)
        # If no exact match, find all entries that contain the search term

        if not list:
            return render(request, "encyclopedia/results.html")
            # If no entries match the search term, render the results page with no results

        else:
            return render(request, "encyclopedia/results.html", {
                "results": list
            })
            # If there are results, render the results page with the matching entries

    else:
        return HttpResponse("Error")
        # If the request method is not POST, return an error message