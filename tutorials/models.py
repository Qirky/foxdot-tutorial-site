from django.db import models

import re

NAME_RE = re.compile(r"(\d*)_([\w\s]+)(\.py)")

# Create your models here.

class Tutorial(models.Model):
    name  = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url   = models.CharField(max_length=150)
    order_number = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    @staticmethod
    def format_title(string):
        """ 
        Takes the filename of tutorial as an input and return the order
        number and display-title for the file. Returns None if the name
        is incorrectly formatted. 
        """

        match = NAME_RE.match(string)
        
        if match:
        
            output = int(match.group(1)), " ".join(match.group(2).split("_")).title()
        
        else:
        
            output = None
        
        return output

class Comment(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    upvote = models.BooleanField(default=True)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.text
