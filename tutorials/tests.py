from django.test import TestCase
from django.urls import reverse

from .models import Tutorial
from .utils import GITHUB_URL

import requests

class GitHubAPITests(TestCase):

    def test_failed_auth(self):
        """ 
        If GitHub API authentication fails, display a user friendly error
        """
        response = requests.get(GITHUB_URL)
        self.assertEqual(response.ok, True)


class TutorialTests(TestCase):

    def test_format_name(self):
        """
        Test correct formatting of file names
        """
        # Correct
        self.assertEqual(Tutorial.format_title("01_basic_tutorial_name.py"), (1, "Basic Tutorial Name"))
        self.assertEqual(Tutorial.format_title("1_basic_tutorial_name.py"), (1, "Basic Tutorial Name"))
        self.assertEqual(Tutorial.format_title("999_basic_tutorial_name.py"), (999,"Basic Tutorial Name"))
        self.assertEqual(Tutorial.format_title("01_bAsIc_tuTorIal_Name.py"), (1, "Basic Tutorial Name"))

        # In-correct
        error_output = None
        self.assertEqual(Tutorial.format_title("01_basic_tutorial_name"), error_output)
        self.assertEqual(Tutorial.format_title("basic_tutorial_name.py"), error_output)
        self.assertEqual(Tutorial.format_title("01"), error_output)
        self.assertEqual(Tutorial.format_title(".py"), error_output)
        self.assertEqual(Tutorial.format_title(""), error_output)
        self.assertEqual(Tutorial.format_title("-1_basic_tutorial.py"), error_output)

    def test_tutorial_id(self):
        """ Test valid and invalid IDs """
        response = self.client.get(reverse('tutorials:detail', args=(999,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The requested resource was not found on this server.")




