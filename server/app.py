import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas, os
import json
""" 
BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]
print(BOOKS)
"""
BOOKS = [
	{
		"id":"a1z",
		"title":"xOn the Road",
		"author":"Kerouac",
		"read":True
	},
    {
		"id":"b2y",
		"title":"xHarry Potter and the Philosopher's Stone",
		"author":"J.K. Rowling",
		"read":False
	},
    {
		"id":"c3x",
		"title":"xGreen Eggs and Ham",
		"author":"Dr. Seuss",
		"read":True
	}
]
print(BOOKS)

def stopwatchPrint(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__}: {end - start:.3f} s.")
        return result

    return wrapper

def getdatapath(name):
    return os.path.join(os.path.dirname(__file__), "data", name)

df = pandas.read_csv(getdatapath('books.csv'), sep=',')
BOOKS2 = json.loads(df.to_json(orient='records'))
print(BOOKS2)

# configuration
DEBUG = True

# instantiate the apppyth   
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS2
        print(BOOKS2)


    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
