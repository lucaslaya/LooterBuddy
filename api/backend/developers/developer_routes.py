from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

developers = Blueprint('developers', __name__)

@developers.route('/performance', methods=['GET'])
def get_all_performance():
    current_app.logger.info(f'developer_routes.py: GET /performance/')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
            p.playerID,
            p.performanceID,
            p.totalKills,
            p.totalDeaths,
            p.DPS,
            p.dateCompleted,
            m.name AS missionName,
            m.description AS missionDescription,
            l.weapon1, l.weapon2, l.armor1, l.armor2, l.armor3
        FROM
            looterbuddy.Performance p
        JOIN
            looterbuddy.Missions m ON p.missionID = m.missionID
        JOIN
            looterbuddy.Loadout l ON p.loadoutID = l.loadoutID;
        '''
    
    cursor.execute(query)

    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(row))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@developers.route('/performance/<playerID>', methods=['GET'])
def get_performance_by_player(playerID):
    current_app.logger.info(f'developer_routes.py: GET /performance/{playerID}')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
            p.playerID,
            p.performanceID,
            p.totalKills,
            p.totalDeaths,
            p.DPS,
            p.dateCompleted,
            m.name AS missionName
        FROM
            looterbuddy.Performance p
        JOIN
            looterbuddy.Missions m ON p.missionID = m.missionID
        JOIN
            looterbuddy.Loadout l ON p.loadoutID = l.loadoutID
        WHERE
            p.playerID = %s;
        '''
    
    cursor.execute(query, (playerID,))
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(row))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@developers.route('/posts', methods=['GET'])
def get_all_posts():
    current_app.logger.info('developer_routes.py: GET /posts')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
            p.postID,
            p.title,
            p.content,
            p.tag,
            p.dateCreated,
            p.dateUpdated,
            d.developerID,
            s.streamerID
        FROM
            looterbuddy.Posts p
        LEFT JOIN
            looterbuddy.Developers d ON p.developerID = d.developerID
        LEFT JOIN
            looterbuddy.ContentCreators s ON p.streamerID = s.streamerID;
        '''
    
    cursor.execute(query)
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(row))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@developers.route('/posts', methods=['POST'])
def create_post():
    current_app.logger.info('developer_routes.py: POST /posts')
    
    data = request.json
    title = data.get('title')
    content = data.get('content')
    tag = data.get('tag')
    developerID = data.get('developerID')  # Assuming developerID is passed in the request

    if not all([title, content, tag, developerID]):
        return make_response(jsonify({"error": "All fields (title, content, tag, developerID) must be provided"}), 400)
    
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO looterbuddy.Posts (title, content, tag, developerID, dateCreated)
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);
    '''
    
    cursor.execute(query, (title, content, tag, developerID))
    db.get_db().commit()
    
    return make_response(jsonify({"message": "Post created successfully"}), 201)

@developers.route('/posts/<postID>', methods=['DELETE'])
def delete_post(postID):
    current_app.logger.info(f'developer_routes.py: DELETE /posts/{postID}')
    
    cursor = db.get_db().cursor()
    query = '''
        DELETE FROM looterbuddy.Posts WHERE postID = %s;
    '''
    
    cursor.execute(query, (postID,))
    db.get_db().commit()
    
    return make_response(jsonify({"message": "Post deleted successfully"}), 200)

@developers.route('/loadoutuse/<missionID>', methods=['GET'])
def get_loadout_use_by_mission(missionID):
    current_app.logger.info(f'developer_routes.py: GET /loadoutuse/{missionID}')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
            lu.loadoutUseID,
            lu.playerID,
            lu.weapon1,
            lu.weapon2,
            lu.armor1,
            lu.armor2,
            lu.armor3,
            lu.dateUsed,
            m.name AS missionName
        FROM
            looterbuddy.LoadoutUse lu
        JOIN
            looterbuddy.Missions m ON lu.missionID = m.missionID
        WHERE
            lu.missionID = %s;
        '''
    
    cursor.execute(query, (missionID,))
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(row))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


