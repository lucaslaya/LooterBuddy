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

@players.route('/posts', methods=['GET'])
def get_posts():
    current_app.logger.info(f'player_routes.py: GET /posts')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
            title,
            content,
            tag,
            dateCreated,
            developerID,
            streamerID
        FROM
            looterbuddy.Posts;
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

@players.route('/streamers', methods=['GET'])
def get_streamers():
    current_app.logger.info(f'player_routes.py: GET /streamers')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
            u.username,
            c.category,
            c.description
        FROM
            looterbuddy.ContentCreators c
        JOIN
            looterbuddy.Users u ON c.userID = u.userID;
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

@players.route('/follows/<playerID>', methods=['GET'])
def get_follows(playerID):
    current_app.logger.info(f'player_routes.py: GET /follows/{playerID}')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
            u.username
        FROM 
            looterbuddy.Follows f
        JOIN
            looterbuddy.ContentCreators c ON f.streamerID = c.streamerID
        JOIN
            looterbuddy.Users u ON c.userID = u.userID
        JOIN
            looterbuddy.Players p ON f.userID = p.userID
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

@players.route('/follows/<playerID>/<streamerID>', methods=['POST'])
def add_follow(playerID, streamerID):
    current_app.logger.info(f'player_routes.py: POST /follows/{playerID}/{streamerID}')
    
    cursor = db.get_db().cursor()

    # Fetch the userID of the player
    query = "SELECT userID FROM looterbuddy.Players WHERE playerID = %s;"
    cursor.execute(query, (playerID,))
    user_id = cursor.fetchone()

    if not user_id:
        return make_response(jsonify({"error": "Player not found"}), 404)
    
    # Insert a new follow record
    query = '''
        INSERT INTO looterbuddy.Follows (userID, streamerID) 
        VALUES (%s, %s);
    '''
    cursor.execute(query, (user_id[0], streamerID))
    db.get_db().commit()

    return make_response(jsonify({"message": "Follow added successfully"}), 201)

@players.route('/follows/<playerID>/<streamerID>', methods=['DELETE'])
def remove_follow(playerID, streamerID):
    current_app.logger.info(f'player_routes.py: DELETE /follows/{playerID}/{streamerID}')
    
    cursor = db.get_db().cursor()

    # Fetch the userID of the player
    query = "SELECT userID FROM looterbuddy.Players WHERE playerID = %s;"
    cursor.execute(query, (playerID,))
    user_id = cursor.fetchone()

    if not user_id:
        return make_response(jsonify({"error": "Player not found"}), 404)
    
    # Delete the follow record
    query = '''
        DELETE FROM looterbuddy.Follows 
        WHERE userID = %s AND streamerID = %s;
    '''
    cursor.execute(query, (user_id[0], streamerID))
    db.get_db().commit()

    return make_response(jsonify({"message": "Follow removed successfully"}), 200)

@players.route('/likes/<postID>', methods=['GET'])
def get_likes(postID):
    current_app.logger.info(f'player_routes.py: GET /likes/{postID}')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
            u.username
        FROM 
            looterbuddy.Likes l
        JOIN
            looterbuddy.Users u ON l.userID = u.userID
        WHERE
            l.postID = %s;
        '''
    
    cursor.execute(query, (postID,))

    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(row))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Route to add a like to a post
@players.route('/likes/<playerID>/<postID>', methods=['POST'])
def add_like(playerID, postID):
    current_app.logger.info(f'player_routes.py: POST /likes/{playerID}/{postID}')
    
    cursor = db.get_db().cursor()

    # Fetch the userID of the player
    query = "SELECT userID FROM looterbuddy.Players WHERE playerID = %s;"
    cursor.execute(query, (playerID,))
    user_id = cursor.fetchone()

    if not user_id:
        return make_response(jsonify({"error": "Player not found"}), 404)
    
    # Insert a new like record
    query = '''
        INSERT INTO looterbuddy.Likes (userID, postID) 
        VALUES (%s, %s);
    '''
    cursor.execute(query, (user_id[0], postID))
    db.get_db().commit()

    return make_response(jsonify({"message": "Like added successfully"}), 201)

# Route to retrieve comments for a certain postID
@players.route('/comments/<postID>', methods=['GET'])
def get_comments(postID):
    current_app.logger.info(f'player_routes.py: GET /comments/{postID}')
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT
            u.username,
            c.content,
            c.dateCreated
        FROM 
            looterbuddy.Comments c
        JOIN
            looterbuddy.Users u ON c.userID = u.userID
        WHERE
            c.postID = %s;
        '''
    
    cursor.execute(query, (postID,))

    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(row))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Route to add a comment to a post
@players.route('/comments/<playerID>/<postID>', methods=['POST'])
def add_comment(playerID, postID):
    current_app.logger.info(f'player_routes.py: POST /comments/{playerID}/{postID}')
    
    content = request.json.get('content', '')
    if not content:
        return make_response(jsonify({"error": "Comment content is required"}), 400)

    cursor = db.get_db().cursor()

    # Fetch the userID of the player
    query = "SELECT userID FROM looterbuddy.Players WHERE playerID = %s;"
    cursor.execute(query, (playerID,))
    user_id = cursor.fetchone()

    if not user_id:
        return make_response(jsonify({"error": "Player not found"}), 404)
    
    # Insert a new comment record
    query = '''
        INSERT INTO looterbuddy.Comments (userID, postID, content) 
        VALUES (%s, %s, %s);
    '''
    cursor.execute(query, (user_id[0], postID, content))
    db.get_db().commit()

    return make_response(jsonify({"message": "Comment added successfully"}), 201)