from django.test import TestCase
import requests
import os

if not os.path.exists("../media/images/applications_default.jpg"):
    response = requests.get("https://clipground.com/images/application-clip-art-17.jpg")
    with open("../media/images/applications_default.jpg", "wb") as f:
        f.write(response.content)