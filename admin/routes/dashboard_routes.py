from flask import request, render_template, flash, redirect, url_for, Blueprint
from admin.database.firebase import Database

db = Database()
dashboard_bp = Blueprint('dashboard',
                         __name__,
                         template_folder="../templates",
                         static_folder="static",
                         static_url_path="/admin_static")

class DashboardRoutes:
    
    @staticmethod
    @dashboard_bp.route('/dashboard')
    def mainpage():
        tenant_count = db.count_tenants()
        occ_room_count = db.count_rooms(True)
        
        return render_template('index.html',
                               tenant_count=tenant_count,
                               occupied_rooms=occ_room_count
                               )
    
    @staticmethod
    @dashboard_bp.route('/manage_tenants')
    def manage_tenants():
        page = int(request.args.get('page', 1))
        per_page = 5
        
        all_data = db.get_tenants_details()
        
        total_pages = (len(all_data) + per_page -1 ) // per_page
        
        start = (page - 1) * per_page
        end = start + per_page
        data = all_data[start:end]
        
        return render_template('manage_tenants.html', 
                               data = data,
                               page = page,
                               total_pages = total_pages
                               )
    
    @staticmethod
    @dashboard_bp.route('/manage_rooms', methods=['GET'])
    def manage_rooms():
        page = int(request.args.get('page', 1))
        per_page = 5
        
        all_data = db.get_rooms_details()
        
        total_pages = (len(all_data) + per_page -1 ) // per_page
        
        start = (page - 1) * per_page
        end = start + per_page
        data = all_data[start:end]
        
        return render_template('manage_rooms.html',
                               data = data,
                               page = page,
                               total_pages = total_pages
                               )

    @staticmethod
    @dashboard_bp.route('/manage_mess')
    def manage_mess():
        return render_template('mess.html')

    @staticmethod
    @dashboard_bp.route('/manage_complaints')
    def manage_complaints():
        return render_template('complaints.html')
    
    
    
    
    