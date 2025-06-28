from flask import request, render_template, flash, redirect, url_for, Blueprint
from admin.database.firebase import Database

db = Database()
ai_bp = Blueprint("ai", __name__)

class AIRoutes:
    
    @staticmethod
    @ai_bp.route('/predictRoom', methods=['POST'])
    def predict_room():
        
        data = request.json
        ten_type = data.get('ten_type')
        ac = data.get('ac')
        sleeptime = data.get('sleeptime')
        smoking = data.get('smoking')
        
        


    
