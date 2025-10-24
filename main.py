from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import db, Summary
from .forms import ProfileForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('main/index.html')

@main.route('/about')
def about():
    return render_template('main/about.html')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.bio = form.bio.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('main.profile'))
    
    form.bio.data = current_user.bio
    
    # Get recent summaries
    recent_summaries = current_user.summaries.order_by(Summary.timestamp.desc()).limit(5).all()
    
    return render_template('main/profile.html', form=form, recent_summaries=recent_summaries)

@main.route('/dashboard')
@login_required
def dashboard():
    recent_summaries = current_user.summaries.order_by(Summary.timestamp.desc()).limit(5).all()
    return render_template('main/dashboard.html', recent_summaries=recent_summaries)

@main.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.summaries.order_by(Summary.timestamp.desc()).paginate(
        page=page, per_page=10, error_out=False)
    summaries = pagination.items
    return render_template('main/history.html', summaries=summaries, pagination=pagination)

@main.context_processor
def inject_now():
    return {'now': datetime.utcnow()}
