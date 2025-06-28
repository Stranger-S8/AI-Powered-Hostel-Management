from flask import request, render_template, flash, redirect, url_for, Blueprint
from admin.database.firebase import Database

db = Database()
tenant_bp = Blueprint('tenant',
                      __name__,
                      template_folder="../templates",
                      static_folder="static",
                      static_url_path="/admin_static")

class TenantRoutes:
    
    @staticmethod
    @tenant_bp.route('/registertenant')
    def register_tenant():
        room_names = db.get_rooms()
        return render_template('register.html', room_names = room_names)
    
    @staticmethod
    @tenant_bp.route('/registertenant/adding', methods=['POST'])
    def adding_tenant():
        id = request.form.get('idproof')
        name = request.form.get('name')
        t_type = request.form.get('ten-type')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date = request.form.get('movein')
        ac = request.form.get('ac')
        sleep = request.form.get('sleeptime')
        smoking = request.form.get('smoking')
        room = request.form.get('room')
        
        if not id or not name or not t_type or not email or not phone or not room or not date or not ac or not sleep or not smoking:
            flash("All fields are required", "error")
            return render_template('register.html')
        
        if room == "--Select Room--":
            flash("Please select valid room", "error")
            return render_template('register.html')
                
        db.add_tenant(id, name, t_type, email, phone, date, ac, sleep, smoking, room)
        flash("Tenant added successfully", "success")
        return redirect(url_for('tenant.register_tenant'))
    
    @staticmethod
    @tenant_bp.route('/delete/<tenant_id>', methods=['POST'])
    def delete_tenant(tenant_id):
        
        db.delete_document("tenants", "id", int(tenant_id))
        return redirect(url_for('dashboard.manage_tenants'))
    
    @staticmethod
    @tenant_bp.route('/ViewTenants/<ten_id>')
    def view_tenants(ten_id):
        
        data = db.get_tenants_details(ten_id, True)
        return render_template('tenant_details.html',
                               data=data)
        
        