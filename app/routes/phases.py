from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_required, current_user
from app import db
from app.models import Phase
from datetime import datetime
import pytz

phases_bp = Blueprint('phases', __name__)

@phases_bp.route('/dashboard')
@login_required
def dashboard():
    # Get current time in user's timezone
    timezone = pytz.timezone(current_user.timezone)
    now = datetime.now(timezone)
    
    # Format for time comparison
    current_time = now.strftime("%H:%M")
    current_day = now.strftime("%A")
    
    # Skip weekend check if user wants phases on weekends
    is_weekend = current_day in ['Saturday', 'Sunday'] and not current_user.apply_to_weekends
    
    # Get all phases for the user, ordered by start time
    phases = Phase.query.filter_by(user_id=current_user.id).order_by(Phase.start_time).all()
    
    # Find current phase
    current_phase = None
    next_phase = None
    
    if not is_weekend and phases:
        # Find the current phase based on time
        for i, phase in enumerate(phases):
            if phase.start_time <= current_time < phase.end_time:
                current_phase = phase
                next_index = (i + 1) % len(phases)
                next_phase = phases[next_index]
                break
        
        # If no current phase is found, find the next upcoming phase
        if not current_phase and phases:
            for phase in phases:
                if phase.start_time > current_time:
                    next_phase = phase
                    break
            
            # If no upcoming phase today, set the first phase as next
            if not next_phase and phases:
                next_phase = phases[0]
    
    return render_template('dashboard.html', 
                          current_phase=current_phase, 
                          next_phase=next_phase, 
                          current_time=current_time,
                          is_weekend=is_weekend)

@phases_bp.route('/phases')
@login_required
def manage_phases():
    phases = Phase.query.filter_by(user_id=current_user.id).order_by(Phase.start_time).all()
    return render_template('phases.html', phases=phases)

@phases_bp.route('/phases/add', methods=['POST'])
@login_required
def add_phase():
    name = request.form.get('name')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    color = request.form.get('color', '#3498db')
    
    # Validate time format
    try:
        datetime.strptime(start_time, "%H:%M")
        datetime.strptime(end_time, "%H:%M")
    except ValueError:
        flash('Invalid time format. Please use HH:MM format.', 'danger')
        return redirect(url_for('phases.manage_phases'))
    
    # Validate time order
    if start_time >= end_time:
        flash('End time must be after start time.', 'danger')
        return redirect(url_for('phases.manage_phases'))
    
    # Check for overlapping phases
    existing_phases = Phase.query.filter_by(user_id=current_user.id).all()
    for phase in existing_phases:
        if (start_time < phase.end_time and end_time > phase.start_time):
            flash('Time range overlaps with existing phase.', 'danger')
            return redirect(url_for('phases.manage_phases'))
    
    new_phase = Phase(
        user_id=current_user.id,
        name=name,
        start_time=start_time,
        end_time=end_time,
        color=color
    )
    
    db.session.add(new_phase)
    db.session.commit()
    flash('Phase added successfully!', 'success')
    return redirect(url_for('phases.manage_phases'))

@phases_bp.route('/phases/<int:phase_id>/edit', methods=['POST'])
@login_required
def edit_phase(phase_id):
    phase = Phase.query.get_or_404(phase_id)
    
    # Ensure user owns this phase
    if phase.user_id != current_user.id:
        flash('You are not authorized to edit this phase.', 'danger')
        return redirect(url_for('phases.manage_phases'))
    
    name = request.form.get('name')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    color = request.form.get('color')
    
    # Validate time format
    try:
        datetime.strptime(start_time, "%H:%M")
        datetime.strptime(end_time, "%H:%M")
    except ValueError:
        flash('Invalid time format. Please use HH:MM format.', 'danger')
        return redirect(url_for('phases.manage_phases'))
    
    # Validate time order
    if start_time >= end_time:
        flash('End time must be after start time.', 'danger')
        return redirect(url_for('phases.manage_phases'))
    
    # Check for overlapping phases (excluding current phase)
    existing_phases = Phase.query.filter(
        Phase.user_id == current_user.id,
        Phase.id != phase_id
    ).all()
    
    for other_phase in existing_phases:
        if (start_time < other_phase.end_time and end_time > other_phase.start_time):
            flash('Time range overlaps with existing phase.', 'danger')
            return redirect(url_for('phases.manage_phases'))
    
    phase.name = name
    phase.start_time = start_time
    phase.end_time = end_time
    phase.color = color
    
    db.session.commit()
    flash('Phase updated successfully!', 'success')
    return redirect(url_for('phases.manage_phases'))

@phases_bp.route('/phases/<int:phase_id>/delete', methods=['POST'])
@login_required
def delete_phase(phase_id):
    phase = Phase.query.get_or_404(phase_id)
    
    # Ensure user owns this phase
    if phase.user_id != current_user.id:
        flash('You are not authorized to delete this phase.', 'danger')
        return redirect(url_for('phases.manage_phases'))
    
    db.session.delete(phase)
    db.session.commit()
    flash('Phase deleted successfully!', 'success')
    return redirect(url_for('phases.manage_phases'))

@phases_bp.route('/api/phases')
@login_required
def get_phases():
    phases = Phase.query.filter_by(user_id=current_user.id).order_by(Phase.start_time).all()
    phases_list = [{
        'id': phase.id,
        'name': phase.name,
        'start_time': phase.start_time,
        'end_time': phase.end_time,
        'color': phase.color
    } for phase in phases]
    
    return jsonify(phases_list)