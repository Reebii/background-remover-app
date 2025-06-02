from flask import Flask, request, send_file, render_template, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image
import io
import tempfile

app = Flask(__name__)
app.secret_key = 'https://background-remover-app-vdru.onrender.com'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Create upload directory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        try:
            # Read the uploaded file
            input_data = file.read()
            
            # Remove background
            output_data = remove(input_data)
            
            # Create a BytesIO object to return the processed image
            img_io = io.BytesIO(output_data)
            img_io.seek(0)
            
            # Generate filename for download
            original_name = secure_filename(file.filename)
            name_without_ext = os.path.splitext(original_name)[0]
            output_filename = f"{name_without_ext}_no_background.png"
            
            return send_file(
                img_io,
                mimetype='image/png',
                as_attachment=True,
                download_name=output_filename
            )
            
        except Exception as e:
            flash(f'Error processing image: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload an image file.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
