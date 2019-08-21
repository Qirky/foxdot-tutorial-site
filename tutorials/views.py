from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

import requests
import json

from .models import Tutorial, Comment
from .utils import GITHUB_URL

class IndexView(generic.ListView): # ListView display a list of objects
    template_name = 'tutorials/index.html'
    context_object_name = 'tutorials_list' 

    def get_queryset(self):
        """ 
        (required method) Return the last 5 published questions,
        not including those set to be published in the future
        """
        # Checks GitHub page and updates database accordingly
        self.make_api_call()
        return Tutorial.objects.all().order_by('order_number')

    def make_api_call(self):
        """ 
        Makes a call to the GitHub API to get URLs of FoxDot tutorials
        and updates the database with any new URLs.
        """
        response = requests.get(GITHUB_URL)
        
        if response.ok:
            
            # Go through returned data and check if in database

            data = json.loads(response.content)

            for item in data:

                # Get order number and title info from file name

                order_number, title = Tutorial.format_title(item["name"])

                api_url = item["download_url"]

                # Test if file name is in the database

                query_set = Tutorial.objects.filter(name=item["name"])

                # If not, add it

                if len(query_set) == 0:

                    new_tutorial = Tutorial(
                        name=item["name"], 
                        title=title, 
                        order_number=order_number,
                        url = api_url
                    )

                    new_tutorial.save()

                # If it is, make sure te order_number is still correct

                else:

                    existing_tutorial = query_set[0]

                    # Check order number

                    if existing_tutorial.order_number != order_number:

                        existing_tutorial.order_number = order_number

                        existing_tutorial.save()

                    # Check url

                    if existing_tutorial.url != api_url:

                        existing_tutorial.url = api_url

                        existing_tutorial.save()

        return                


class DetailView(generic.DetailView): 
    # Displays the tutorial plus options for up and down-voting

    # -- it expects the 'pk' argument to get the details, changed in urlpatterns
    model = Tutorial
    template_name = 'tutorials/detail.html'

    def get_context_data(self, **kwargs):
        """
        Downloads the text for the tutorial file as well as adds information
        about the next/previous tutorial
        """

        context = super().get_context_data(**kwargs)

        # Download tutorial code

        response = requests.get(context['tutorial'].url)

        context['tutorial'].url

        if response.ok:

            context["tutorial_code"] = response.content.decode("utf-8").lstrip()

        # Get the order_number

        order_number = context["tutorial"].order_number

        # Get previous tutorial

        try:

            prev_tutorial = Tutorial.objects.get(order_number=order_number - 1)

            context["prev_tutorial"] = prev_tutorial.id

        except (KeyError, Tutorial.DoesNotExist):

            pass # just don't add prev_tutorial to context

        # Get next tutorial

        try:

            next_tutorial = Tutorial.objects.get(order_number=order_number + 1)

            context["next_tutorial"] = next_tutorial.id

        except (KeyError, Tutorial.DoesNotExist):

            pass

        return context

class ThanksView(generic.DetailView):
    # Displays thank you message
    model = Tutorial
    template_name = 'tutorials/thanks.html'

class CommentsView(generic.DetailView): 
    # List of all the comments on a certain tutorial
    model = Tutorial
    template_name = 'tutorials/comments.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments_list"] = context["tutorial"].comment_set.all().order_by("-pub_date")
        return context


def vote(request, tutorial_id):
    """ Increases a tutorial's upvote counter by 1 and redirects to the appropriate tutorial page """

    tutorial = get_object_or_404(Tutorial, pk=tutorial_id)

    # If "vote" is 1, it's an upvote, if it's a 0 it's a downvote

    upvote = True

    if "vote" in request.POST:

        if int(request.POST["vote"]) == 1:

            tutorial.upvotes += 1

        elif int(request.POST["vote"]) == 0:

            tutorial.downvotes += 1

            upvote = False

        tutorial.save()

    # Create comment

    tutorial.comment_set.create(text=request.POST["text"], upvote=upvote, pub_date=timezone.now())

    # Redirect to thank you page
    
    # dest_view = reverse('tutorials:thanks', args=(tutorial_id,))

    dest_view = reverse('tutorials:comments', args=(tutorial_id,))
    
    return HttpResponseRedirect(dest_view)