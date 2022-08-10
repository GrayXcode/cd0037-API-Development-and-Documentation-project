# Getting Started

  Trivia app is an app where you could **post question**, **delete question**, **search for question** and also **get questions** based on the available categories.

  ### **Base** **url** 
  *The frontend is hosted at http://localhost:3000, and the backend at http://localhost:5000/*

  ## Guideline 
    You are advised to stick to the PEP18-style

  ## Prerequisite & Installations
  ## Backend
    Note: Make sure you are in the backend folder of the current project.
   You are to install the dependencies in the requirements.txt within the **/backend** directory of the current project using:

    $ pip3 install -r > requirements.txt

You would need to setup up your virtual environment inorder to maintain the organization of the project and dependencies.

  ### Installing Virtual Environment
    For Linux / Unix Users
    $ python3 -m venv venv
    $ source venv/bin/activate

  Before you start the server make sure your database is already created,
    
    $ createdb trivia
    $ psql trivia < trivia.psql # Populates the table 

  ### To start the Server
    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development # for server reload

    # incase FLASK_ENV displays an error use FLASK_DEBUG=True

    $ flask run

## Frontend 
    Note: Make sure you are in the frontend directory of the current project.

  ### Installation
    $ npm install # To install all dependencies
    $ npm start 

  The **frontend** is hosted at http://localhost:3000 and connected to the **backend** by proxy, at http://localhost:5000/


## Test
    Note: You are required to be in the backend directory of the current project 

You have to create a test database so as not to hamper production or the development database
    
    $ createdb trivia_test
    $ psql trivia_test < trivia.psql # Populates the table 

# ERROR HANDLING
  Errors are returned in the form of json, including their success, error type and their error message.

Sample Response

    {
      'success': False,
      'error': 404,
      'message': 'Page not found'
    }

Error covered in this project are:

1. **404** : Page not found
2. **400** : Bad Request
3. **500** : Internal Server Error
4. **422** : Unprocessable entity
   

# API REFEERENCES

`GET /categories`

  **General:**

  - Fetches dictionary of categories, in which the keys are the **ids** and the values are the corresponding strings of the category
  - **Request Argument :** None
  - **Returns :** Key-value representation of id and string of each category

*Sample Response*

```json
 {
  "categories": {
    '1': 'Science',
    '2': 'Art',
    '3': 'Geography,
    '4': 'History',
    '5': 'Entertainment',
    '6': 'Sports'
  }
 }
```

`GET /questions`

  **General:**

  - Fetches lists of questions
  - **Request Argument :** page - Integer
  - **Returns :** Paginated list of questions, total questions,  all category, current category,

*Sample Response*

```json
 {
  "questions": [
    {
      'id': 1,
      'question': 'Who is Christ',
      'answer': 'He is God',
      'difficulty': 3,
      'category': 4,
    }, {
      'id': 2,
      'question': 'Who is instructor Caryn',
      'answer': 'The endowed damsel at udacity',
      'difficulty': 1,
      'category': 5,
    }
  ],
  'totalQuestion': 15,
  'category': {
    '1': 'Science',
    '2': 'Art',
    '3': 'Geography,
    '4': 'History',
    '5': 'Entertainment',
    '6': 'Sports'
  },
  'currentCategory': 3
 }
```

`DELETE /questions/${question_id}`

  **General:**

  - Fetches question for deletion based on variable question_id passed to the URI
  - **Request Argument :** question_id - Integer
  - **Returns :** A key-value of success with value of True

*Sample Request*

    curl -X DELETE http://localhost:5000/questions/5

*Sample Response*

```json
 {
  "success": True
 }
```

`POST /questions`

  **General:**

  - Post request to add a new question
  - **Request Argument :** None
  - **Request Body :** 
    ```json
      {
        'question': "What's Caryn's beauty rate?",
        'answer': "8/10",
        'category': 3,
        'difficulty': 4
      }
    ```
  - **Returns :** A dictionary showing success to be True

*Sample Request*

    curl -X POST http://localhost:5000/question -d '{'question': "What's Caryn's beauty rate? ", 'answer': "8/10", 'category': 3, 'difficulty': 4}'

*Sample Response*

    {
      'success': True
    }


`POST /questions/term`

  **General:**

  - Post a request with a search term
  - **Request Argument :** searchTerm - String
  - **Request Body :** 
    ```json
      {
        'searchTerm': 'clay'
      }
    ```
  - **Returns :** matched questions, number of total questions and current category

*Sample Request*

    curl -X POST http://localhost:5000/questions/term -d '{'searchTerm': 'clay'}'

*Sample Response*

```json
{
'questions': [
    {
      'question': 'Who is cassius clay',
      'answer': 'Muhammed Ali',
      'category': 3,
      'difficulty': 2
    },
    {
      'question': 'Is clay a kind of Soil',
      'answer': 'Yes',
      'category': 3,
      'difficulty': 1
   }
],
  'total_questions': 2,
  'current_Category': 3
}
```



`GET /categories/${category_id}/questions?page=${page_no}`

  **General:**

  - Fetches lists of questions based on the id of the category
  - **Request Argument :** category_id, page - Integer
  - **Request Body :** None
  - **Returns :** Questions that matches category id, current category, and number of total question.

*Sample Request*

    curl -X POST http://localhost:5000/categories/1/questions?page=1'

*Sample Response*

```json
{
'questions': [
    {
      'question': 'Who discovered the effect of gravity',
      'answer': 'Sir Isaac Newton',
      'category': 2,
      'difficulty': 3
    },
    {
      'question': 'Who coined the word Radioactivity',
      'answer': 'Ernest Rutherford',
      'category': 2,
      'difficulty': 4
   },
   {
      'question': 'What is the 15th element in the periodic table',
      'answer': 'Phosphorus',
      'category': 2,
      'difficulty': 5
   }
],
  'total_questions': 3,
  'current_Category': 2
}
```

`POST \quizzed`

  **General:**

  - Fetches a question that has not been displayed/fetched, by checking them with the ids in previous questions list
  - **Request Argument :** quiz_category - Integer, previous_question - list
  - **Request Body :** 

```json
  {
    'quiz_category': 2,
    'previous_questions': [4, 5, 7]
  }
```

  - **Returns :** A question dictionary and previous questions list

*Sample Request*

    curl -X POST http://localhost:5000/quizzes -d '{'quiz_category': 3, 'previous_questions': [4, 5, 10]}''

*Sample Response*

```json
{
'question': {
  'id': 4, 
  'question': 'Who is 2022 world athletic championship in 100m hurdle',
  'answer': 'Tobi Amusan',
  'category': '3',
  'difficulty': 1
},
  'previousQuestions': [3, 4, 10]
}
```


### Authors
  *Holy Spirit*

### Acknowledgement
  **God**

