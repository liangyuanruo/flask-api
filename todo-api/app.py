# Following online tutorial at
# http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

#Our "in memory database"
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

#Return all tasks
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify( {'tasks': tasks} )


#Return one task by task_id
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    
    if len(task) == 0:
        abort(404)
    
    return jsonify( {'task': task[0]} )


#Create task
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():

    #If request was not JSON or no 'title' field
    if not request.json or 'title' not in request.json:
        abort(400) #Bad request error code

    task = {
        'id': tasks[-1]['id'] + 1, #Get ID of last element in list + 1
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }

    tasks.append(task)
    return jsonify( {'task': task} ), 201 #HTTP "Created" number code


#Update tasks
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):

    task = [task for task in tasks if task['id'] == task_id]

    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])

    return jsonify({'task': task[0]})


#Delete tasks
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


#404 Error Handling
@app.errorhandler(404)
def not_found(error):
    return make_response( jsonify( {'error': 'Not found'}), 404 )


if __name__ == '__main__':
    app.run(debug=True)
