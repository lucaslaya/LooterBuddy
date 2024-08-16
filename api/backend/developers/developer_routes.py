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
            m.description AS missionDescription
        FROM
            looterbuddy.Performance p
        JOIN
            looterbuddy.Missions m ON p.missionID = m.missionID
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

@developers.route('/performance/mission/<missionID>', methods=['GET'])
def get_performance_by_mission(missionID):
    current_app.logger.info(f'developer_routes.py: GET /performance/mission/{missionID}')
    
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
            m.description AS missionDescription
        FROM
            looterbuddy.Performance p
        JOIN
            looterbuddy.Missions m ON p.missionID = m.missionID
        WHERE
            p.missionID = %s;
    '''
    
    cursor.execute(query, (missionID,))
    theData = cursor.fetchall()

    if not theData:
        current_app.logger.info(f'No performance data found for mission ID: {missionID}')
        return make_response(jsonify({"message": f"No data found for mission ID: {missionID}"}), 404)

    json_data = []
    for row in theData:
        json_data.append(dict(row))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@developers.route('/missions', methods=['GET'])
def get_all_missions():
    current_app.logger.info(f'developer_routes.py: GET /missions/')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
            missionID,
            name,
            description
        FROM
            looterbuddy.Missions;
    '''
    
    cursor.execute(query)
    theData = cursor.fetchall()
    
    if not theData:
        current_app.logger.info('No missions found.')
        return make_response(jsonify({"message": "No missions found"}), 404)

    json_data = []
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

@developers.route('/items/names', methods=['POST'])
def get_item_names():
    current_app.logger.info('developer_routes.py: POST /items/names')
    
    cursor = db.get_db().cursor()
    query = f'''
        SELECT 
            itemID, 
            name 
        FROM 
            looterbuddy.Items;
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

@developers.route('/posts/<postID>', methods=['GET'])
def get_post_by_id(postID):
    current_app.logger.info(f'developer_routes.py: GET /posts/{postID}')
    
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
            looterbuddy.ContentCreators s ON p.streamerID = s.streamerID
        WHERE
            p.postID = %s;
    '''
    
    cursor.execute(query, (postID,))
    theData = cursor.fetchone()

    if not theData:
        current_app.logger.info(f'No post found for post ID: {postID}')
        return make_response(jsonify({"message": f"No data found for post ID: {postID}"}), 404)

    json_data = dict(theData)
    
    # Get the number of likes
    like_query = '''
        SELECT COUNT(*) AS like_count
        FROM looterbuddy.Likes
        WHERE postID = %s;
    '''
    cursor.execute(like_query, (postID,))
    like_data = cursor.fetchone()
    json_data['likes'] = like_data['like_count'] if like_data else 0
    
    # Get the comments
    comment_query = '''
        SELECT c.content, u.username
        FROM looterbuddy.Comments c
        JOIN looterbuddy.Users u ON c.userID = u.userID
        WHERE c.postID = %s;
    '''
    cursor.execute(comment_query, (postID,))
    comments = cursor.fetchall()
    json_data['comments'] = comments if comments else []

    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response