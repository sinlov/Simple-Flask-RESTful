# coding=utf-8

__author__ = 'sinlov'

from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

version = Flask(__name__)

host_name = '127.0.0.1'
port_number = 38080
str_def_version_desc = u'this is version of crate4.0 python code'
route_version = 'v1.0'
route_path = '/api/' + route_version

version_code = [
    {
        'id': 1,
        'vc': 1,
        'description': str_def_version_desc,
        'message': False
    },
    {
        'id': 2,
        'vc': 3,
        'description': str_def_version_desc,
        'message': False
    }
]


@version.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@version.route('/')
def index():
    return "create_4.0 version service is running!"


def make_public_version(vc):
    new_vc = {}
    for field in vc:
        if field == 'id':
            new_vc['uri'] = url_for('get_version', version_id=vc['id'], _external=True)
        else:
            new_vc[field] = vc[field]
    return new_vc


@version.route(route_path + '/version', methods=['GET'])
def get_versions():
    return jsonify({'version': map(make_public_version, version_code)})


@version.route(route_path + '/all_version', methods=['GET'])
def get_all_versions():
    return jsonify({'version_code': version_code})


@version.route(route_path + '/last_version', methods=['GET'])
def get_all_last_version():
    vc_size = len(version_code)
    if vc_size > 0:
        return jsonify({'last_version': version_code[vc_size - 1]})
    else:
        return jsonify({'last_version': "not version of data"})


@version.route(route_path + '/version', methods=['POST'])
def create_version():
    print request.json
    if not request.json or not 'vc' in request.json:
        abort(400)
    e_version = {
        'id': version_code[-1]['id'] + 1,
        'vc': request.json['vc'],
        'description': request.json.get('description', str_def_version_desc),
        'message': request.json.get('message', "")
    }
    version_code.append(e_version)
    return jsonify({'version': e_version}), 201


@version.route(route_path + '/version/<int:version_id>', methods=['PUT'])
def update_version(version_id):
    e_version = filter(lambda t: t['id'] == version_id, version_code)
    if len(e_version) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'vc' in request.json and type(request.json['vc']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'message' in request.json and type(request.json['message']) is not unicode:
        abort(400)
    version_code[0]['vc'] = request.json.get('vc', version_code[0]['vc'])
    version_code[0]['description'] = request.json.get('description', version_code[0]['description'])
    version_code[0]['message'] = request.json.get('message', version_code[0]['message'])
    return jsonify({'version': version_code[0]})


@version.route(route_path + '/version/<int:version_id>', methods=['DELETE'])
def delete_version(version_id):
    e_version = filter(lambda t: t['id'] == version_id, version_code)
    if len(e_version) == 0:
        abort(404)
    version_code.remove(e_version[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    version.run(host=host_name, port=port_number, debug=True)
