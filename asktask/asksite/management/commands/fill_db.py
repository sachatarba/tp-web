import random

import pydenticon
from django.core.management.base import BaseCommand
from asksite.models import *
from django.conf import settings
from django.core.files import File

class Command(BaseCommand):
    help = "fills db with sample data"

    icon_generator = pydenticon.Generator(10, 10)

    def add_arguments(self, parser):
        parser.add_argument("ratio", nargs=1, type=int)

    def handle(self, *args, **options):
        ratio = int(options["ratio"][0])
        profiles_to_create = ratio
        questions_to_create = ratio * 10
        answers_to_create = ratio * 100
        tags_to_create = ratio
        question_likes_to_create = ratio * 100

        import os
        print(os.path.dirname(__file__))

        profiles = []
        for i in range(profiles_to_create):
            profiles.append(self.profile_generator(i))
        Profile.objects.bulk_create(profiles)
        del profiles

        questions = []
        for i in range(questions_to_create):
            questions.append(self.question_generator(i, profiles_to_create))
        Question.objects.bulk_create(questions)
        del questions

        answers = []
        for i in range(answers_to_create):
            answers.append(self.answer_generator(i, questions_to_create, profiles_to_create))
        Answer.objects.bulk_create(answers)
        del answers

        tags = []
        for i in range(tags_to_create):
            tags.append(self.tag_generator(i))
        Tag.objects.bulk_create(tags)
        del tags

        for i in range(questions_to_create):
            self.set_tags(i, tags_to_create)

        likes = []
        for i in range(question_likes_to_create):
            likes.append(self.question_likes_generator(questions_to_create, profiles_to_create))
        QuestionLike.objects.bulk_create(likes)
        del likes

    def profile_generator(self, i):
        # from io import BytesIO
        # from PIL import Image
        user = User(username=f"{i}", password="1!opopopa")
        user.save()
        tmp = Profile(name="User {}".format(i + 1), avatar="avatar_{}.png".format(i + 1), user=user)
        return tmp


    def question_generator(self, i, max_users):
        tmp = Question(
            title="Question title {}".format(i + 1),
            text="Question text {} ipsum dolor sit amet, consectetur adipiscing elit, "
                 "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
                 "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi".format(i + 1),
            author=Profile.objects.get(name="User {}".format(random.randrange(max_users) + 1)))
        return tmp

    def answer_generator(self, i, max_questions, max_users):
        tmp = Answer(
            title="Answer title {}".format(i + 1),
            text="Answer body {} ipsum dolor sit amet, consectetur adipiscing elit, "
                 "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
                 "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi "
                 "ut aliquip ex ea commodo consequat. Duis aute irure dolor".format(i + 1),
            question=Question.objects.get(title="Question title {}".format(random.randrange(max_questions) + 1)),
            author=Profile.objects.get(name="User {}".format(random.randrange(max_users) + 1)),
            is_correct=(random.choice([True, False]))
        )
        return tmp

    def question_likes_generator(self, max_questions, max_users):
        tmp = QuestionLike(
            question=Question.objects.get(title="Question title {}".format(random.randrange(max_questions) + 1)),
            liker=Profile.objects.get(name="User {}".format(random.randrange(max_users) + 1))
        )
        return tmp

    def tag_generator(self, i):
        tmp = Tag(name="Tag {}".format(i + 1))
        return tmp

    def set_tags(self, i, max_tags):
        question = Question.objects.get(title="Question title {}".format(i + 1))
        tags_cnt = random.randrange(1, 4)
        tags = [Tag.objects.get(name="Tag {}".format(i % max_tags + 1)).id,
                Tag.objects.get(name="Tag {}".format((i + max_tags // 3) % max_tags + 1)).id,
                Tag.objects.get(name="Tag {}".format((i + 2 * max_tags // 3) % max_tags + 1)).id]
        for i in range(tags_cnt):
            question.tags.add(tags[i])
        question.save()
