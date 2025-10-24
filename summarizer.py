import os
import uuid
import pandas as pd
from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import db, Summary
from .forms import SummarizeForm, BatchSummarizeForm

summarizer = Blueprint('summarizer', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_summary(text, max_length=130, min_length=30):
    try:
        summary = current_app.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        current_app.logger.error(f"Error generating summary: {str(e)}")
        return None

@summarizer.route('/single', methods=['GET', 'POST'])
@login_required
def single():
    form = SummarizeForm()
    if form.validate_on_submit():
        text = form.text.data
        summary_text = generate_summary(text)
        
        if summary_text:
            # Save to database
            summary = Summary(
                original_text=text,
                summary=summary_text,
                user_id=current_user.id,
                is_batch=False
            )
            db.session.add(summary)
            db.session.commit()
            # If AJAX request, return JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'summary': summary_text
                })
            # Otherwise render a result page
            return render_template('summarizer/result.html',
                                   original=text,
                                   summary=summary_text,
                                   is_batch=False)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Error generating summary'}), 500
            flash('Error generating summary. Please try again.', 'danger')
    
    return render_template('summarizer/single.html', form=form)

@summarizer.route('/batch', methods=['GET', 'POST'])
@login_required
def batch():
    form = BatchSummarizeForm()
    
    if form.validate_on_submit():
        if 'file' not in request.files:
            msg = 'No file part'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': msg}), 400
            flash(msg, 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            msg = 'No selected file'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': msg}), 400
            flash(msg, 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Read the CSV file
                df = pd.read_csv(file)
                
                # Check if 'abstract' column exists
                if 'abstract' not in df.columns:
                    msg = "CSV must contain an 'abstract' column"
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({'error': msg}), 400
                    flash(msg, 'danger')
                    return redirect(request.url)
                
                # Generate batch ID
                batch_id = str(uuid.uuid4())
                
                # Process each abstract
                results = []
                for idx, row in df.iterrows():
                    abstract = str(row['abstract'])
                    if len(abstract) > 100:  # Only process if abstract is long enough
                        summary_text = generate_summary(abstract)
                        if summary_text:
                            # Save to database
                            summary = Summary(
                                original_text=abstract,
                                summary=summary_text,
                                user_id=current_user.id,
                                is_batch=True,
                                batch_id=batch_id
                            )
                            db.session.add(summary)
                            results.append({
                                'original': abstract,
                                'summary': summary_text
                            })
                
                db.session.commit()
                
                # Create results DataFrame
                results_df = pd.DataFrame(results)
                
                # Save results to CSV
                filename = f"batch_summary_{batch_id}.csv"
                output_path = os.path.join(current_app.root_path, 'static', 'downloads', filename)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                results_df.to_csv(output_path, index=False)
                
                # AJAX: return redirect URL
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({
                        'redirect_url': url_for('summarizer.batch_result', filename=filename)
                    })
                
                return render_template('summarizer/batch_result.html',
                                       results=results[:5],  # Show first 5 results
                                       total=len(results),
                                       download_url=url_for('static', filename=f'downloads/{filename}'))
                
            except Exception as e:
                current_app.logger.error(f"Error processing batch: {str(e)}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'error': f'Error processing file: {str(e)}'}), 500
                flash(f'Error processing file: {str(e)}', 'danger')
    
    return render_template('summarizer/batch.html', form=form)

@summarizer.route('/api/summarize', methods=['POST'])
@login_required
def api_summarize():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    summary_text = generate_summary(data['text'])
    if summary_text:
        return jsonify({'summary': summary_text})
    else:
        return jsonify({'error': 'Failed to generate summary'}), 500

@summarizer.route('/download-template')
@login_required
def download_template():
    # Provide a simple CSV template with 'abstract' header
    template_content = 'abstract\n"Example abstract goes here..."\n'
    filename = 'abstracts_template.csv'
    path = os.path.join(current_app.root_path, 'static', 'downloads', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    return send_from_directory(os.path.join(current_app.root_path, 'static', 'downloads'), filename, as_attachment=True)

@summarizer.route('/batch/result/<filename>')
@login_required
def batch_result(filename):
    download_url = url_for('static', filename=f'downloads/{filename}')
    # For preview, try to read first few lines
    try:
        path = os.path.join(current_app.root_path, 'static', 'downloads', filename)
        df = pd.read_csv(path)
        results = df.head(5).to_dict(orient='records')
        total = len(df)
    except Exception:
        results, total = [], 0
    return render_template('summarizer/batch_result.html', results=results, total=total, download_url=download_url)
