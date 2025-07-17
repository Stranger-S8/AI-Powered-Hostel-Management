@app.route('/tenant_login')
def tenant_portal():
    return render_template('tenant-signin.html')