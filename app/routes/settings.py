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
        enable_notifications = 'enable_notifications' in request.form
        notification_advance = request.form.get('notification_advance', 5)
        
        # Validate timezone
        if timezone not in pytz.all_timezones:
            flash('Invalid timezone selected.', 'danger')
            return redirect(url_for('settings.user_settings'))
        
        # Validate notification advance
        try:
            notification_advance = int(notification_advance)
            if notification_advance < 0 or notification_advance > 15:
                raise ValueError
        except ValueError:
            flash('Notification advance time must be between 0 and 15 minutes.', 'danger')
            return redirect(url_for('settings.user_settings'))
        
        current_user.timezone = timezone
        current_user.apply_to_weekends = apply_to_weekends
        current_user.enable_notifications = enable_notifications
        current_user.notification_advance = notification_advance
        
        db.session.commit()
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('settings.user_settings'))
    
    timezones = pytz.all_timezones
    return render_template('settings.html', timezones=timezones)