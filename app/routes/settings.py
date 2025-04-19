from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
import pytz

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    if request.method == 'POST':
        timezone = request.form.get('timezone')
        apply_to_weekends = 'weekend_toggle' in request.form
        
        # Validate timezone
        if timezone not in pytz.all_timezones:
            flash('Invalid timezone selected.', 'danger')
            return redirect(url_for('settings.user_settings'))
        
        current_user.timezone = timezone
        current_user.apply_to_weekends = apply_to_weekends
        
        db.session.commit()
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('settings.user_settings'))
    
    timezones = pytz.all_timezones
    return render_template('settings.html', timezones=timezones)