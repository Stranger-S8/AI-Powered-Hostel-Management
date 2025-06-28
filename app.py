from flask import Flask, render_template
from flask_mail import Mail
import secrets

from admin.routes.auth_routes import auth_bp
from admin.routes.tenant_routes import tenant_bp
from admin.routes.dashboard_routes import dashboard_bp
from admin.routes.room_routes import room_bp
from admin.routes.mess_routes import mess_bp

from tenant.routes.t_auth_routes import t_auth_bp
from tenant.routes.t_dashboard_routes import t_dashboard_bp
from tenant.routes.t_messroutes import t_mess_bp
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "stranger_s8"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "zeeshanchudri1234@gmail.com"
app.config['MAIL_PASSWORD'] = "sncy xxla apqx mufv"
app.config['SESSION_PERMANENT'] = True


mail = Mail(app)
app.mail = mail

# Admin Blueprints

app.register_blueprint(auth_bp, url_prefix="/admin")
app.register_blueprint(tenant_bp, url_prefix="/manage_tenants")
app.register_blueprint(dashboard_bp, url_prefix="/AdminDashboard")
app.register_blueprint(room_bp, url_prefix="/manage_rooms")
app.register_blueprint(mess_bp, url_prefix="/AdminMess")

# Tenant Blueprints

app.register_blueprint(t_auth_bp, url_prefix="/tenant")
app.register_blueprint(t_dashboard_bp, url_prefix="/TenantDashboard")
app.register_blueprint(t_mess_bp, url_prefix="/TenantMess")

app.permanent_session_lifetime = timedelta(days=30)

@app.route('/')
def starting_splash():
    return render_template('splash.html')

@app.route('/HostelManager')
def starting_menu():
    return render_template('portal.html')

@app.route('/admin_login')
def admin_portal():
    return render_template('signin.html')

@app.route('/tenant_login')
def tenant_portal():
    return render_template('tenant-signin.html')
 
if __name__ == "__main__":
    app.run(debug=True)