from flask import (jsonify, Blueprint, request)
import databaseConnection as db

admin_api = Blueprint('admin_api', __name__)

@admin_api.route('/appRegistration', methods=['POST'])
def register_app():
    # TODO
    return None

@admin_api.route('/userRegistration', methods=['POST'])
def register_user():
    # TODO
    return None

@admin_api.route('/playerRegistration', methods=['POST'])
def register_player():
    # TODO
    return None

@admin_api.route('/teamRegistration', methods=['POST'])
def register_team():
    # TODO
    return None

@admin_api.route('/gameRegistration', methods=['POST'])
def register_game():
    dbEntry = db.insertIntoCollection('competitions', request.json)
    return jsonify({'status': True, 'message': 'Game insertion successful.', 'gameid': dbEntry.inserted_id})

@admin_api.route('/seasonRegistration', methods=['POST'])
def register_season():
    # TODO
    return None