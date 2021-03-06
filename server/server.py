import json
from flask import Flask, request
from items import create_store
from items import initialize_store      # Added to support db init @Janos

app = Flask('REST-test-application')
store = create_store()                  # Function name is modified as it covers better the function behind @Janos

@app.route('/')
def alive():
    return json.dumps({'server': 'ok'})

@app.route('/items/', methods=['GET'])
def list_items():
    data = request.args.to_dict()
    items = store.list_items(**data)
    ser_items = []
    for item in items:
        ser_items.append(item.serialize())
    return json.dumps(ser_items)

@app.route('/items/<name>', methods=['GET'])
def detail_item(name):
    successful, response_msg = store.get_item(name)
    status_code = 200 if successful else 404
    return json.dumps(response_msg), status_code

@app.route('/items/', methods=['POST'])
def add_item():
    data = json.loads(request.data)
    successful, response_msg = store.add_item(**data)
    status_code = 201 if successful else 400
    return json.dumps(response_msg), status_code

@app.route('/items/<name>', methods=['DELETE'])
def delete_item(name):
    successful, response_msg = store.del_item(name)
    status_code = 204 if successful else 404
    return json.dumps(response_msg), status_code

# Added to support db init @Janos
@app.route('/init/', methods=['POST'])
def initialize():
    data = json.loads(request.data)
    successful, response_msg = initialize_store(store, **data)
    status_code = 201 if successful else 400
    return json.dumps(response_msg), status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0')
