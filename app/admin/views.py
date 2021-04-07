from flask import render_template
from flask_login import login_required
from . import admin


@admin.route('/admin')
@login_required
def login():
    return render_template('admin/index.html')
