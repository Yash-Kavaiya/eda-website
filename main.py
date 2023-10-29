from flask import Flask, render_template, request, send_file
import pandas as pd
from pandas_profiling import ProfileReport
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Function to perform pandas profiling
def generate_report(csv_file_path):
    df = pd.read_csv(csv_file_path)
    
    # Generate profiling report
    profile = ProfileReport(df)
    report_path = 'static/report.html'
    profile.to_file(report_path)
    
    return report_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = os.path.join('uploads', secure_filename(file.filename))
        file.save(filename)

        # Generate profiling report
        report_path = generate_report(filename)
        return render_template('report.html', report_path=report_path)

@app.route('/download_report')
def download_report():
    return send_file('static/report.html', as_attachment=True)
 
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
