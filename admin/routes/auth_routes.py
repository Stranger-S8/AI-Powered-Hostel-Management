from flask import request, render_template, flash, redirect, url_for, Blueprint, session
from admin.database.firebase import Database
from datetime import datetime, timedelta
from flask_mail import Message
import random 

db = Database()
auth_bp = Blueprint('auth',
                    __name__,
                    template_folder="../templates",
                    static_folder="../static",
                    static_url_path="/admin_static"
                    )
  
class AuthRoutes:
        
    @staticmethod
    @auth_bp.route('/signup')
    def signup_page():
        return render_template('signup.html')
    
    @staticmethod
    @auth_bp.route("/submit", methods=["POST"])
    def submit():
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['cpassword']
        
        if not name or not email or not password or not c_password:
            flash("All fields are required", "error")
            return redirect(url_for("auth.signup_page"))
        
        if len(str(password)) < 8:
            flash("Password should be atleast 8 characters", "error")
            return redirect(url_for("auth.signup_page"))
            
        if password != c_password:
            flash("Passwords do not match", "error")
            return redirect(url_for("auth.signup_page"))
        
        if db.user_exists(username=name):
            flash("Username already taken", "error")
            return redirect(url_for('auth.signup_page'))
        
        if db.user_exists(email=email):
            flash("Email already registered", "error")
            return redirect(url_for('auth.signup_page'))

        db.add_user(name, email, password)
        flash("Account created successfully", "success")
        return redirect(url_for('auth.signin_page'))
    
    @staticmethod
    @auth_bp.route('/signin')
    def signin_page():
        return render_template('signin.html')
    
    @staticmethod
    @auth_bp.route('/validate', methods=["POST"])
    def validate_login():
        name = request.form['username']
        password = request.form['password']
        
        if not name or not password:
            flash("All fields are required", "error")
            return redirect(url_for("auth.signin_page"))

        result = db.login_user(name, password)
        
        if result:
            return redirect(url_for('dashboard.mainpage'))
        else:
            flash("Password incorrect", "error")
            return redirect(url_for("auth.signin_page"))
    
    @staticmethod
    @auth_bp.route('/signin/verify_user')
    def verify_user():
        return render_template('verify_user.html')
    
    @staticmethod
    @auth_bp.route('/signin/verify_code', methods=["POST"])
    def verify_code():
        from app import mail

        username_or_email = request.form.get('username_or_email')

        if not username_or_email:
            flash("Empty Field", "error")
            return render_template('verify_user.html')

        if db.validate_email(username_or_email):
            if db.user_exists(None, username_or_email):
                code = str(random.randint(100000, 999999))
                session["verification_code"] = code
                session['email_code_expiry'] = (datetime.utc() + timedelta(minutes=5)).timestamp()
                session["user_email"] = username_or_email
                session["email"] = True

                msg = Message('Your Verification Code',
                            sender='zeeshanchudri1234@gmail.com',
                            recipients=[username_or_email])
                msg.body = f"Your Verification Code is: {code}"
                mail.send(msg)
                
                flash("Verification code sent", "success")
                return render_template("verify_code.html")
            else:
                flash("Invalid email", "error")
                return render_template('verify_user.html')

        else:
            if db.user_exists(username_or_email, None):
                
                email = db.get_field("users", "username", username_or_email, "email")

                if not email:
                    flash("No email found for this username", "error")
                    return render_template('verify_user.html')

                code = str(random.randint(100000, 999999))
                session["verification_code"] = code
                session['email_code_expiry'] = (datetime.utc() + timedelta(minutes=5)).timestamp()
                session["user_email"] = username_or_email
                session["email"] = False
                

                msg = Message('Your Verification Code',
                            sender='zeeshanchudri1234@gmail.com',
                            recipients=[email])
                msg.body = f"Your Verification Code is: {code}"
                mail.send(msg)

                flash("Verification code sent to email linked with username", "success")
                return render_template("verify_code.html")
            else:
                flash("Invalid username", "error")
                return render_template('verify_user.html')
        
    @staticmethod
    @auth_bp.route('/signin/verify_code/validate', methods=["POST"])
    def validate_verf_code():
        code = request.form.get("digit_code")
        stored_code = session.get("verification_code")
        expiry = session.get('email_code_expiry')

        
        if not stored_code or not expiry:
             flash("Session expired. Please try again.", "error")
             return render_template("verify_user.html")
        
        if datetime.utc().timestamp() > expiry:
            session.pop('digit_code', None)
            session.pop('email_code_expiry', None)
            return "Code expired", 400
        
        if code == stored_code:
            flash("Verification Successfull", "success")
            return render_template("new_password.html")
        
        else:
            flash("Invalid verification code. Try again.", "error")
            return render_template("verify_code.html")
            
    @staticmethod
    @auth_bp.route('/changepassword', methods=['POST'])
    def change_pass():
        password = request.form['newpass']
        cpassword = request.form['confirmpass']
        
        if not password or not cpassword:
            flash("All fields are required", "error")
            return render_template("new_password.html")
        
        if password != cpassword:
            flash("Passwords do not match", "error")
            return render_template("new_password.html")
            
        if session.get("email"):
            db.change_user_password(password, username=None, email=session.get("user_email"))
        else:
            db.change_user_password(password, username=session.get("user_email"), email=None)
        
        flash("Password Changed Successfully", "success")
        return render_template('signin.html')
            
            
        
        
        
        
            
            
        
        
        
        