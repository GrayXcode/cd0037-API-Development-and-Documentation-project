import os
import resource
import sys
from traceback import print_exception
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy import func
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"*": {
                "origins": "*"}})

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after 
    completing the TODOs
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods',
                             'POST, GET, PUT, PATCH, DELETE')
        return response

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @ app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories_all = Category.query.all()
            categories = {}
            for cat in categories_all:
                categories[cat.id] = cat.type

            data = {
                'categories': categories
            }
            return jsonify(data)
        except:
            abort(400)

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    def get_question_objects(questions):
        question_collection = []

        for ques in questions:
            question_collection.append({'question': ques.question, 'answer':
                                        ques.answer, 'difficulty':
                                        ques.difficulty, 'category':
                                        ques.category, 'id': ques.id})
        return question_collection

    def splice(page, array):
        start = ((page - 1) * QUESTIONS_PER_PAGE)
        end = page * QUESTIONS_PER_PAGE

        return array[start:end]

    @ app.route('/questions', methods=['GET'])
    def get_paginated_questions():
        total_questions = Question.query.all()
        all_category = Category.query.all()
        categories = {}
        page_no = request.args.get('page', 1, type=int)

        questions = []

        paginated_ques = splice(page_no, total_questions)

        if len(paginated_ques) == 0:
            abort(404)

        questions = get_question_objects(paginated_ques)

        for cat in all_category:
            categories[cat.id] = cat.type

        return jsonify({
            'questions': questions,
            'totalQuestions': len(total_questions),
            'categories': categories,
            'currentCategory': None,
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three
    pages. Clicking on the page numbers should update the questions.
    """

    @ app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        if question is None:
            abort(422)

        Question.delete(question)

        return jsonify({
            'success': True,
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will
    be removed. This removal will persist in the database and when you refresh 
    the page.
    """

    @ app.route('/question', methods=['POST'])
    def create_question():

        try:
            question = request.get_json()['question']
            answer = request.get_json()['answer']
            difficulty = request.get_json()['difficulty']
            category = request.get_json()['category']
            newQuestion = Question(
                question=question, answer=answer, difficulty=difficulty,
                category=category)

            Question.insert(newQuestion)

            return jsonify({
                'success': True,
                'message': 'OK'
            })
        except:
            abort(500)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @ app.route('/questions/term', methods=['POST'])
    def get_search_question():
        searchTerm = request.get_json()['searchTerm']
        current_category = request.args.get('category')
        data = []

        # Convert js(null) to python (None)
        # Still don't know why null !== None
        if current_category == 'null':
            current_category = None

        if current_category is None:
            questions = Question.query.filter(
                Question.question.ilike(f'%{searchTerm}%')).all()
        else:
            questions = Question.query.filter(
                Question.category == current_category).\
                filter(Question.question.ilike(f'%{searchTerm}%')).all()

        if len(questions) == 0:
            abort(404)

        data = get_question_objects(questions)

        return jsonify({
            'questions': data,
            'total_questions': len(questions),
            'current_category': current_category
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @ app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_category_questions(category_id):
        category_questions = Question.query.filter(
            Question.category == category_id).all()
        num_of_questions = len(category_questions)
        page_no = request.args.get('page', 1, type=int)
        questions = []

        if len(category_questions) == 0:
            abort(404)

        paginated_ques = splice(page_no, category_questions)

        questions = get_question_objects(paginated_ques)

        return jsonify({
            'questions': questions,
            'total_questions': len(category_questions),
            'current_category': category_id
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        try:
            category_id = request.get_json()['quiz_category']['id']
            past_questions = request.get_json()['previous_questions']
            question_to_display = None
            questions = None

            if category_id == 0:
                questions = Question.query.order_by(func.random()).all()

            else:
                questions = db.session.query(Question).filter(
                    Question.category == category_id).order_by(func.random()).\
                    all()

            for question in questions:
                if question.id in past_questions:
                    continue
                else:
                    past_questions.append(question.id)
                    question_to_display = question
                    break

            if question_to_display is None:
                abort(404)

            return jsonify({
                'question': {
                    'id': question_to_display.id,
                    'question': question_to_display.question,
                    'answer': question_to_display.answer,
                    'difficulty': question_to_display.difficulty,
                    'category': question_to_display.category
                },
                'previousQuestions': past_questions
            })

        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.errorhandler(404)
    def page_not_found(err):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Page not found'
        }), 404

    @app.errorhandler(400)
    def bad_request(err):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(500)
    def server_error(err):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    @app.errorhandler(422)
    def unprocessable_entity(err):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
