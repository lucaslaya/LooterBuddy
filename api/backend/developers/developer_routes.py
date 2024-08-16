from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

developers = Blueprint('developers', __name__)