import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question
from django.utils import timezone

# Create your tests here.
class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns false for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text= "¿Quién es el mejor Course Director de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_recently_with_past_questions(self):
        """Was published recently returns false for questions whose pub_date was in the past"""
        time = timezone.now() - datetime.timedelta(days=10)
        past_question = Question(question_text="¿Cuál es la mejor escuela de Platzi?", pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)


    def test_was_published_recently_with_now_questions(self):
        """was_published_recently should returns true for questions whose pub_date is now"""
        time = timezone.now()
        now_question = Question(question_text="¿Quién es el mejor profesor de Platzi?", pub_date=time)
        self.assertIs(now_question.was_published_recently(), True)

def create_question(question_text, days):
    """This function make a model of questions"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date = time)
    
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_future_questions(self):
        """If we have a future question, it does not showed"""
        response = self.client.get(reverse('polls:index'))
        now = timezone.now()
        future_question = Question(question_text="¿Blablabla?", pub_date=now)
        self.assertNotIn(future_question, response.context["latest_question_list"])

    def test_past_question(self):
        """This, verificate if questions publicated on past, is showed"""
        question = create_question("past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
        
    def test_future_question_and_past_question(self):
        """Even if both past and future question exist, only past questions are displayed"""
        past_question = create_question(question_text='Past question', days=-30)
        future_question = create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question]
        )
    
    def test_two_past_questions(self):
        """The questions index page may displaye multiple questions"""
        past_question1 = create_question(question_text='Past question 1', days=-30)
        past_question2 = create_question(question_text='Past question 2', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2] 
        )