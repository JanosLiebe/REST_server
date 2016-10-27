import json
import requests
from robot.api import logger

def _assert_equal(a, b, message=None):
    """
    Drop AssertionError if 'a' not equal 'b'. Include 'message' if exist.

    Return: AssertionError
    """
    if message is None:
        message = "Failed equal: {} == {}".format(a, b)
    assert a == b, message

def is_item_in_list(address, port, name):
    """
    Get list of items from server and check if item with 'name' is in list.
    Drop AssertionError and write Error log if status of server response not equal with expected.

    Return: 'True' if item on list
            'False' if item not on list
    """
    resp = get_items_from_server(address, port)
    try:
        _assert_equal(resp.status_code, 200)
    except AssertionError as err:
        logger.error(resp.text)
        raise AssertionError(err)
    list_of_items = json.loads(resp.text)
    item_found = False
    for item in list_of_items:
        if item.get('name') == name:
            item_found = True
            break
    return item_found

def get_items_from_server(address, port, name = None):
    """
    Send GET request on server.
    'name' == None
        Request list of existing items from server.
    'name' == <item>
        Request item with specified name from server.

    Return: response of request.get function.
    """
    if name == None:
        url = 'http://{}:{}/items/'.format(address, port)
    else:
        #url = 'http://{}:{}/items/{}/'.format(address, port, name)
        url = 'http://{}:{}/items/{}'.format(address, port, name)
    return requests.get(url)

def post_item_to_server(address, port, data):
    """
    Send POST request on server.

    Return: response of request.post function.
    """
    url = 'http://{}:{}/items/'.format(address, port)
    json_data = json.dumps(eval(data))
    return requests.post(url, json_data)

def delete_item_from_server(address, port, name):
    """
    Send DELETE request to server.

    Return: response of request.delete function.
    """
    #url = 'http://{}:{}/items/{}/'.format(address, port, name)
    url = 'http://{}:{}/items/{}'.format(address, port, name)
    return requests.delete(url)

### Robot Keywords ####
"""
    Next functions are robot keywords. Them drop AssertionError and write Error log in case status or
    text of server response don't equal with expected values.
"""

def verify_server_is_running(address, port):
    url = 'http://{}:{}'.format(address, port)
    resp = requests.get(url)
    try:
        _assert_equal(resp.status_code, 200)
        _assert_equal(json.loads(resp.text), {'server': 'ok'})
    except AssertionError as err:
        logger.error(resp.text)
        raise AssertionError(err)

def verify_initialized_list(address, port, data):
    resp = get_items_from_server(address, port)
    try:
        _assert_equal(resp.status_code, 200)
        _assert_equal(resp.text, data)
    except AssertionError as err:
        logger.error(resp.text)
        raise AssertionError(err)

def create_item(address, port, data):
    resp = post_item_to_server(address, port, data)
    try:
        _assert_equal(resp.status_code, 201)
        _assert_equal(eval(resp.text), eval(data))
    except AssertionError as err:
        logger.error(resp.text)
        raise AssertionError(err)

def create_duplicate_item(address, port, data):
    resp = post_item_to_server(address, port, data)
    try:
        _assert_equal(resp.status_code, 400)
        _assert_equal(json.loads(resp.text), {'error': 'Duplicate name: {}'.format(eval(data)['name'])})
    except AssertionError as err:
        logger.error(resp.text)
        raise AssertionError(err)

def create_item_without_name(address, port, data):
    resp = post_item_to_server(address, port, data)
    try:
        _assert_equal(resp.status_code, 400)
        _assert_equal(json.loads(resp.text), {'error': 'Name required!'})
    except AssertionError as err:
        logger.error(resp.text)
        raise AssertionError(err)

def get_item_exist_in_list(address, port, data):
    resp = get_items_from_server(address, port, eval(data)['name'])
    try:
        _assert_equal(resp.status_code, 200)
        _assert_equal(eval(resp.text), eval(data))
    except AssertionError as err:
        logger.error(resp.text)
        raise AssertionError(err)

def get_item_not_exist_in_list(address, port, data):
    resp = get_items_from_server(address, port, eval(data)['name'])
    try:
        _assert_equal(resp.status_code, 404)
        _assert_equal(json.loads(resp.text), {'error': 'Item not found: {}'.format(eval(data)['name'])})
    except AssertionError as err:
        logger.error(resp.text)
        raise AssertionError(err)

def delete_item(address, port, data):
    resp = delete_item_from_server(address, port, eval(data)['name'])
    try:
        _assert_equal(resp.status_code, 204)
    except AssertionError as err:
        logger.error(resp.text)
        raise AssertionError(err)

def delete_non_existing_item(address, port, data):
    resp = delete_item_from_server(address, port, eval(data)['name'])
    try:
        _assert_equal(resp.status_code, 404)
        _assert_equal(json.loads(resp.text), {'error': 'Item not found: {}'.format(eval(data)['name'])})
    except AssertionError as err:
        logger.error(resp.text)
        raise AssertionError(err)

def verify_item_exist_in_list(address, port, data):
    item_in_list = is_item_in_list(address, port, eval(data)['name'])
    try:
        _assert_equal(item_in_list, True, "Item not found: {}".format(eval(data)['name']))
    except AssertionError as err:
        logger.error(resp.text)
        raise AssertionError(err)

def verify_item_not_exist_in_list(address, port, data):
    item_in_list = is_item_in_list(address, port, eval(data)['name'])
    try:
        _assert_equal(item_in_list, False, "Item found: {}".format(eval(data)['name']))
    except AssertionError as err:
        logger.error(resp.text)
        raise AssertionError(err)

def teardown_suite(address, port, data):
    resp = get_items_from_server(address, port)
    try:
        _assert_equal(resp.status_code, 200)
        _assert_equal(resp.text, data)
    except AssertionError as err:
        logger.warn(err)
        names_of_resp = [x['name'] for x in eval(resp.text)]
        names_of_data = [x['name'] for x in eval(data)]
        diff_names = list(set(names_of_data) - set(names_of_resp)) + list(set(names_of_resp) - set(names_of_data))
        for name in diff_names:
            resp = delete_item_from_server(address, port, name)
            try:
                _assert_equal(resp.status_code, 204)
            except AssertionError as err:
                logger.error(resp.text)
                raise AssertionError(err)
