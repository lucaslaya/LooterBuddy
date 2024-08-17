from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

streamers = Blueprint('streamers', __name__)

@streamers.route('/loadoutuse/<missionID>', methods=['GET'])
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

@streamers.route('/loadoutuse', methods=['GET'])
def get_all_loadout_use():
    current_app.logger.info(f'streamer_routes.py: GET /loadoutuse')
    
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
            looterbuddy.Missions m ON lu.missionID = m.missionID;
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

@streamers.route('/items/names', methods=['GET'])
def get_item_names():
    current_app.logger.info('developer_routes.py: GET /items/names')
    
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

@streamers.route('/missions', methods=['GET'])
def get_all_missions():
    current_app.logger.info(f'streamers_routes.py: GET /missions/')
    
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

@streamers.route('/posts', methods=['POST'])
def create_post_for_streamer():
    current_app.logger.info('streamer_routes.py: POST /posts')
    
    data = request.json
    title = data.get('title')
    content = data.get('content')
    tag = data.get('tag')
    streamerID = data.get('streamerID')  # Assuming streamerID is passed in the request

    if not all([title, content, tag, streamerID]):
        return make_response(jsonify({"error": "All fields (title, content, tag, streamerID) must be provided"}), 400)
    
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO looterbuddy.Posts (title, content, tag, streamerID, dateCreated)
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);
    '''
    
    cursor.execute(query, (title, content, tag, streamerID))
    db.get_db().commit()
    
    return make_response(jsonify({"message": "Post created successfully"}), 201)

@streamers.route('/follows/count/<streamerID>', methods=['GET'])
def get_follow_count(streamerID):
    current_app.logger.info(f'streamer_routes.py: GET /follows/count/{streamerID}')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT COUNT(*) AS follow_count
        FROM looterbuddy.Follows f
        JOIN looterbuddy.ContentCreators c ON f.streamerID = c.streamerID
        WHERE c.streamerID = %s;
    '''
    
    cursor.execute(query, (streamerID,))
    result = cursor.fetchone()

    if not result:
        return make_response(jsonify({"follow_count": 0}), 200)

    return make_response(jsonify({"follow_count": result['follow_count']}), 200)

@streamers.route('/posts/<streamerID>', methods=['GET'])
def get_posts_by_streamer(streamerID):
    current_app.logger.info(f'streamer_routes.py: GET /posts/{streamerID}')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
            p.postID,
            p.title,
            p.content,
            p.tag,
            p.dateCreated,
            p.dateUpdated,
            s.streamerID
        FROM
            looterbuddy.Posts p
        JOIN
            looterbuddy.ContentCreators s ON p.streamerID = s.streamerID
        WHERE
            p.streamerID = %s;
    '''
    
    cursor.execute(query, (streamerID,))
    theData = cursor.fetchall()

    if not theData:
        return make_response(jsonify([]), 200)

    json_data = []
    for row in theData:
        json_data.append(dict(row))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@streamers.route('/posts/details/<postID>', methods=['GET'])
def get_post_details(postID):
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