from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

players = Blueprint('players', __name__)

@players.route('/inventory/<playerID>', methods=['GET'])
def get_inventory(playerID):
    current_app.logger.info(f'player_routes.py: GET /inventory/{playerID}')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
            looterbuddy.Items.itemID AS itemID,
            looterbuddy.Items.name AS itemName,
            looterbuddy.Items.type AS itemType,
            looterbuddy.Items.rarity AS itemRarity,
            looterbuddy.Armor.defense AS itemDefense,
            looterbuddy.Weapons.damage AS itemDamage,
            looterbuddy.Weapons.magSize AS itemMagSize,
            looterbuddy.Weapons.fireRate AS itemFireRate
        FROM
            looterbuddy.Inventory
        JOIN
            looterbuddy.Items ON Inventory.itemID = Items.itemID
        LEFT JOIN
            looterbuddy.Armor ON Items.itemID = Armor.itemID
        LEFT JOIN
            looterbuddy.Weapons ON Items.itemID = Weapons.itemID
        WHERE
            Inventory.playerID = {0};
        '''.format(playerID)
    
    cursor.execute(query)

    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(row))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@players.route('/loadout/<playerID>', methods=['GET'])
def get_loadout(playerID):
    current_app.logger.info(f'player_routes.py: GET /loadout/{playerID}')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
            l.weapon1 AS weapon1_id,
            w1.name AS weapon1,
            l.weapon2 AS weapon2_id,
            w2.name AS weapon2,
            l.armor1 AS armor1_id,
            a1.name AS armor1,
            l.armor2 AS armor2_id,
            a2.name AS armor2,
            l.armor3 AS armor3_id,
            a3.name AS armor3
        FROM
            looterbuddy.Loadout l
        LEFT JOIN
            looterbuddy.Items w1 ON l.weapon1 = w1.itemID
        LEFT JOIN
            looterbuddy.Items w2 ON l.weapon2 = w2.itemID
        LEFT JOIN
            looterbuddy.Items a1 ON l.armor1 = a1.itemID
        LEFT JOIN
            looterbuddy.Items a2 ON l.armor2 = a2.itemID
        LEFT JOIN
            looterbuddy.Items a3 ON l.armor3 = a3.itemID
        WHERE
            l.playerID = {0};
        '''.format(playerID)
    
    cursor.execute(query)

    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(row))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@players.route('/loadout/<playerID>', methods=['PUT'])
def update_loadout(playerID):
    current_app.logger.info(f'player_routes.py: PUT /loadout/{playerID}')
    
    # Get the new loadout details from the request body
    data = request.json
    weapon1 = data.get('weapon1')
    weapon2 = data.get('weapon2')
    armor1 = data.get('armor1')
    armor2 = data.get('armor2')
    armor3 = data.get('armor3')

    if not all([weapon1, weapon2, armor1, armor2, armor3]):
        return make_response(jsonify({"error": "All loadout items (weapon1, weapon2, armor1, armor2, armor3) must be provided"}), 400)

    cursor = db.get_db().cursor()

    # Check if the player exists
    query = "SELECT userID FROM looterbuddy.Players WHERE playerID = %s;"
    cursor.execute(query, (playerID,))
    user_id = cursor.fetchone()

    if not user_id:
        return make_response(jsonify({"error": "Player not found"}), 404)

    # Update the player's loadout
    query = '''
        UPDATE looterbuddy.Loadout
        SET
            weapon1 = %s,
            weapon2 = %s,
            armor1 = %s,
            armor2 = %s,
            armor3 = %s,
            dateUpdated = CURRENT_TIMESTAMP
        WHERE playerID = %s;
    '''
    cursor.execute(query, (weapon1, weapon2, armor1, armor2, armor3, playerID))
    db.get_db().commit()

    return make_response(jsonify({"message": "Loadout updated successfully"}), 200)

@players.route('/performance/<playerID>', methods=['GET'])
def get_performance(playerID):
    current_app.logger.info(f'player_routes.py: GET /performance/{playerID}')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
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
            p.playerID = {0};
        '''.format(playerID)
    
    cursor.execute(query)

    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(row))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all update articles
@players.route('/posts/update-articles', methods=['GET'])
def get_update_articles():
    current_app.logger.info('players_routes.py: GET /update-articles')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT 
            *
        FROM 
            looterbuddy.Posts
        WHERE 
            tag = 'update'
        ORDER BY dateCreated DESC;
    '''
    
    cursor.execute(query)
    articles = cursor.fetchall()
    
    json_data = [dict(row) for row in articles]
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all articles from streamers followed by the player
@players.route('/posts/streamer-articles/<player_id>', methods=['GET'])
def get_streamer_articles(player_id):
    current_app.logger.info(f'players_routes.py: GET /streamer-articles/{player_id}')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT 
            p.*
        FROM 
            looterbuddy.Posts p
        JOIN 
            looterbuddy.Follows f ON p.streamerID = f.streamerID
        WHERE 
            f.userID = {0}
        ORDER BY p.dateCreated DESC;
    '''.format(player_id)
    
    cursor.execute(query)
    articles = cursor.fetchall()
    
    json_data = [dict(row) for row in articles]
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get detailed information of a post
@players.route('/posts/details/<post_id>', methods=['GET'])
def get_post_details(post_id):
    current_app.logger.info(f'players_routes.py: GET /details/{post_id}')
    
    cursor = db.get_db().cursor()
    
    # Get post details
    post_query = '''
        SELECT 
            * 
        FROM 
            looterbuddy.Posts 
        WHERE 
            postID = {0};
    '''.format(post_id)
    
    cursor.execute(post_query)
    post = cursor.fetchone()
    
    # Get number of likes
    likes_query = '''
        SELECT 
            COUNT(*) as likes 
        FROM 
            looterbuddy.Likes 
        WHERE 
            postID = {0};
    '''.format(post_id)
    
    cursor.execute(likes_query)
    likes = cursor.fetchone()
    
    # Get comments
    comments_query = '''
        SELECT 
            c.content, 
            u.username
        FROM 
            looterbuddy.Comments c
        JOIN 
            looterbuddy.Users u ON c.userID = u.userID
        WHERE 
            c.postID = {0};
    '''.format(post_id)
    
    cursor.execute(comments_query)
    comments = cursor.fetchall()
    
    post_details = {
        'post': dict(post),
        'likes': likes['likes'],
        'comments': [dict(row) for row in comments]
    }
    
    the_response = make_response(jsonify(post_details))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Like a post
@players.route('/posts/like', methods=['POST'])
def like_post():
    current_app.logger.info('players_routes.py: POST /like')
    
    data = request.json
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO looterbuddy.Likes (userID, postID)
        VALUES (%s, %s);
    '''
    
    cursor.execute(query, (data['userID'], data['postID']))
    db.get_db().commit()
    
    the_response = make_response(jsonify({"message": "Post liked successfully!"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Comment on a post
@players.route('/posts/comment', methods=['POST'])
def comment_on_post():
    current_app.logger.info('players_routes.py: POST /comment')
    
    data = request.json
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO looterbuddy.Comments (userID, postID, content)
        VALUES (%s, %s, %s);
    '''
    
    cursor.execute(query, (data['userID'], data['postID'], data['content']))
    db.get_db().commit()
    
    the_response = make_response(jsonify({"message": "Comment added successfully!"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all followed streamers for a player
@players.route('/follows/followed/<player_id>', methods=['GET'])
def get_followed_streamers(player_id):
    current_app.logger.info(f'players_routes.py: GET /followed/{player_id}')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT 
            cc.streamerID, 
            u.username
        FROM 
            looterbuddy.ContentCreators cc
        JOIN 
            looterbuddy.Follows f ON cc.streamerID = f.streamerID
        JOIN 
            looterbuddy.Users u ON cc.userID = u.userID
        WHERE f.userID = {0};
    '''.format(player_id)
    
    cursor.execute(query)
    streamers = cursor.fetchall()
    
    json_data = [dict(row) for row in streamers]
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all streamers
@players.route('/streamers', methods=['GET'])
def get_all_streamers():
    current_app.logger.info('players_routes.py: GET /streamers')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT 
            cc.streamerID, 
            u.username, 
            cc.followCount, 
            cc.category, 
            cc.description
        FROM 
            looterbuddy.ContentCreators cc
        JOIN 
            looterbuddy.Users u ON cc.userID = u.userID;
    '''
    
    cursor.execute(query)
    streamers = cursor.fetchall()
    
    json_data = [dict(row) for row in streamers]
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Follow a streamer
@players.route('/follows/follow', methods=['POST'])
def follow_streamer():
    current_app.logger.info('players_routes.py: POST /follow')
    
    data = request.json
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO looterbuddy.Follows (userID, streamerID)
        VALUES (%s, %s);
    '''
    
    cursor.execute(query, (data['userID'], data['streamerID']))
    db.get_db().commit()
    
    the_response = make_response(jsonify({"message": "Streamer followed successfully!"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Unfollow a streamer
@players.route('/follows/unfollow', methods=['POST'])
def unfollow_streamer():
    current_app.logger.info('players_routes.py: POST /unfollow')
    
    data = request.json
    cursor = db.get_db().cursor()
    query = '''
        DELETE FROM looterbuddy.Follows 
        WHERE userID = %s AND streamerID = %s;
    '''
    
    cursor.execute(query, (data['userID'], data['streamerID']))
    db.get_db().commit()
    
    the_response = make_response(jsonify({"message": "Streamer unfollowed successfully!"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response