from django.db import models

QUESTIONS = [
    {
        "id": f"{i}",
        "title": f"Title {i}",
        "text": f"Text {i}"
    } for i in range(0, 10)
]

ANSWERS = [
    {
        "id": f"{i}",
        "title": f"Answer {i}",
        "text": f"Answer text {i}"
    } for i in range(0, 3)
]
