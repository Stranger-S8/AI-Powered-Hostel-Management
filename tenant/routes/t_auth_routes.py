from flask import request, render_template, flash, redirect, url_for, Blueprint, session
from tenant.database.firebase import Database
from flask_mail import Message
import random 

db = Database()
t_auth_bp = Blueprint('t_auth',
                      __name__,
                    template_folder="../templates",
                    static_folder="../static",
                    static_url_path="/tenant_static"
                    )
  
class TAuthRoutes:
    
    @staticmethod
    @t_auth_bp.route('/signup')
    def signup_page():
        return render_template('tenant-signup.html')
    
    @staticmethod
    @t_auth_bp.route('/signin')
    def signin_page():
        return render_template('tenant-signin.html')
    
    @staticmethod
    @t_auth_bp.route('/ForgetPass')
    def forget_pass():
        return render_template("student-forget-password.html")
    
    @staticmethod
    @t_auth_bp.route('/validateSignup', methods=["POST"])
    def submit_reg():
        ten_id = request.form.get('TenantId')
        password = request.form.get('password')
        confirm_p = request.form.get('confirmPassword')
        
        if not ten_id or not password or not confirm_p:
            flash("All fields are required", "error")
            return redirect(url_for("t_auth.signup_page"))
        
        if not db.validate_tenant(ten_id):
            flash("Tenant ID does not exist", "error")
            return redirect(url_for("t_auth.signup_page"))
        
        if len(str(password)) < 8:
            flash("Password should be atleast 8 characters", "error")
            return redirect(url_for("t_auth.signup_page"))
            
        if password != confirm_p:
            flash("Passwords do not match", "error")
            return redirect(url_for("t_auth.signup_page"))
                        
        if db.signup_tenant(int(ten_id), password):
            flash("Account created successfully", "success")
            return redirect(url_for('t_auth.signin_page'))
        else:
            flash("Unknown error occured", "error")
            return redirect(url_for('t_auth.signup_page'))
    
    @staticmethod
    @t_auth_bp.route('/validateSignin', methods=['POST'])
    def validate_signin():
        ten_id = request.form['tenantId']
        password = request.form['password']
        
        if not ten_id or not password:
            flash("All fields are required", "error")
            return redirect(url_for("t_auth.signin_page"))
        
        if not db.validate_tenant(ten_id):
            flash("Tenant ID does not exist", "error")
            return redirect(url_for("t_auth.signin_page"))
        
        if db.login_tenant(int(ten_id), password):
            session['tenant_id'] = ten_id
            session.permanent = True
            return redirect(url_for('t_dashboard.dashboard_page'))
        else:
            flash("Unknown error occured", "error")
            return redirect(url_for('t_auth.signin_page'))
            
        
    

        
        
        
        
    
    
            
    