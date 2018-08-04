#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
from google.appengine.api import urlfetch
import json
from random import shuffle
import jinja2
from models import Trivia
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        question_template = JINJA_ENVIRONMENT.get_template('templates/question.html')
        self.response.write(question_template.render())

#remove and transfer code data to the quesiton.html file
        # trivia_endpoint = "https://opentdb.com/api.php?amount=10&category=9"
        # response = urlfetch.fetch(trivia_endpoint).content
        # json_response = json.loads(response)
        #
        # first_result = json_response["results"][0]
        # question = first_result["question"]
        # correct_answer = first_result["correct_answer"]
        # incorrect_answers = first_result["incorrect_answers"]
        # all_answers = [correct_answer]
        #
        # for a in incorrect_answers:
        #     all_answers.append(a)
        # shuffle(all_answers)
        #
        # self.response.write("<h3> Q: " + question + "</h3>")
        # for a in all_answers:
        #     self.response.write("<p> A: " + a + "</p>")
        #
        # print correct_answer #prints correct answer to the terminal
        #
class TriviaPage(webapp2.RequestHandler):
    #For each question and answer pairing that we get
    #Create a new Question object, and write it to our database

    def get(self):
        API_endpoint = "https://opentdb.com/api.php?amount=10&category=9"
        result = urlfetch.fetch(API_endpoint).content
        json_result = json.loads(result)

        for x in json_result["results"]:
            question = x["question"]
            correct = x["correct_answer"]
            incorrect = x["incorrect_answers"]
            new_question = Trivia(question = question, correct_answer = correct, incorrect_answers = incorrect)
            new_question.put()


class QuestionPage(webapp2.RequestHandler):
    #Query the database using .query(), .fetch() and .filter()/.order()
    #Write the quesiton, answer, and incorrect answers to the resposne

    def get(self):
        answer_template = JINJA_ENVIRONMENT.get_template('templates/question.html')
        all_questions = Trivia.query().fetch()

        # for x in all_questions:
        #     question = x.question
        #     correct_answer = x.correct_answer
        #     incorrect_answers = x.incorrect_answers
        #     all_answers = [correct_answer]
        #     for a in incorrect_answers:
        #         all_answers.append(a)
        #     shuffle(all_answers)
        #     template = {"q": question,
        #                 "a1": all_answers[0],
        #                 "a2": all_answers[1],
        #                 "a3": all_answers[2],
        #                 "a4": all_answers[3],
        #                 "correct": correct_answer}
        #     self.response.write(answer_template.render(template))

        q1 = all_questions[0]

        question = q1.question
        correct_answer = q1.correct_answer
        incorrect_answers = q1.incorrect_answers
        all_answers = [correct_answer]

        for a in incorrect_answers:
            all_answers.append(a)
        shuffle(all_answers)

        template = {"q": question,
                    "a1": all_answers[0],
                    "a2": all_answers[1],
                    "a3": all_answers[2],
                    "a4": all_answers[3],
                    "correct": correct_answer}
        self.response.write(answer_template.render(template))

class AnswerPage(webapp2.RequestHandler):
    def post(self):
        if self.request.get("option") == self.request.get("answer"):
            self.response.write("<h3>Correct!</h3>")
        else:
            self.response.write("<h3>Your Answer: </h3>")
            self.response.write(self.request.get("option"))
            self.response.write("<p></p>")
            self.response.write("<h3>Correct Answer: </h3>")
            self.response.write(self.request.get("answer"))
            self.response.write("<p></p>")
        self.response.write(self.request.get("Next"))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/trivia', TriviaPage),
    ('/question', QuestionPage),
    ('/answer', AnswerPage)
], debug=True)
