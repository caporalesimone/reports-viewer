from flask import Flask, jsonify, request, render_template, send_from_directory
import os
import re
from datetime import datetime

app = Flask(__name__)
BASE_UPLOAD_FOLDER = "uploads"
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024  # Limite di 300 MB

index_data = {}

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def sanitize_tag_run(tag_run):
    return re.sub(r'[^a-zA-Z0-9-_]', '', tag_run)

def create_upload_path(tag_run):
    now = datetime.now()
    path = os.path.join(
        BASE_UPLOAD_FOLDER,
        tag_run,
        str(now.year),
        f"{now.month:02}",
        f"{now.day:02}",
        f"{now.hour:02}.{now.minute:02}"
    )
    os.makedirs(path, exist_ok=True)
    return path

def initialize_index():
    global index_data
    index_data = {}
    for root, _, files in os.walk(BASE_UPLOAD_FOLDER):
        rel_dir = os.path.relpath(root, BASE_UPLOAD_FOLDER)
        parts = rel_dir.split(os.sep)
        if len(parts) < 2:
            continue
        tag, year, *rest = parts
        
        if tag not in index_data:
            index_data[tag] = {}
        if year not in index_data[tag]:
            index_data[tag][year] = {}

        if rest:
            month_number = int(rest[0])  # Otteniamo il numero del mese come intero
            month_name = MONTH_NAMES[month_number - 1]  # Otteniamo il nome del mese dall'array
            month = f"{month_number} - {month_name}"  # Creiamo la stringa "numero - nome del mese"

            if month not in index_data[tag][year]:
                index_data[tag][year][month] = {}

            if len(rest) > 1:
                day = rest[1]
                if day not in index_data[tag][year][month]:
                    index_data[tag][year][month][day] = {}

                # Aggiungi i file HTML al child "ora"
                for file in files:
                    if file.endswith(".html"):
                        # Estrai ora dal nome della cartella
                        hour_folder = os.path.basename(root)  # Estrae l'ora dal percorso
                        file_path = os.path.join(BASE_UPLOAD_FOLDER, rel_dir, file)
                        # Aggiungi il file come child della specifica ora
                        index_data[tag][year][month][day][hour_folder] = file_path

@app.route('/api/index', methods=['GET'])
def get_index():
    return jsonify(index_data)

@app.route('/upload', methods=['POST'])
def upload_file():
    tag_run = request.form.get('tag_run', '')
    if not tag_run:
        return jsonify({"error": "tag_run parameter is required"}), 400
    tag_run = sanitize_tag_run(tag_run)

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        upload_path = create_upload_path(tag_run)
        file_path = os.path.join(upload_path, file.filename)
        file.save(file_path)

        initialize_index()  # Ricostruisce l'indice ad ogni upload
        return jsonify({"message": f"File {file.filename} uploaded successfully to {upload_path}"}), 200

@app.route(f'/{BASE_UPLOAD_FOLDER}/<path:filename>', methods=['GET'])
def serve_file(filename):
    # Serve il file dalla cartella BASE_UPLOAD_FOLDER
    return send_from_directory(BASE_UPLOAD_FOLDER, filename)

# Route per visualizzare l'index.html del frontend
@app.route('/')
def show_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)
    initialize_index()
    app.run(host="0.0.0.0", port=5000)
