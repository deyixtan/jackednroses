from flask import jsonify


def serialize_data(data):  
    # serialize single data
    if type(data) is not list:
        return data.serialize()

    # serialize a list of data
    return list(map(lambda entry: entry.serialize(), data))


def render_data(serialized_data):
    data = {
        "data": serialized_data
    }
    return jsonify(data)
