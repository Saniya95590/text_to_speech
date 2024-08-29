from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import pyttsx3
import os
import time
app = Flask(__name__)
app.secret_key = 'asdjhasdaasdasd'
RESULTS_FOLDER = os.path.join('static', 'results')
if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)


# Initialize TTS engine and get available voices
engine = pyttsx3.init()
voices = engine.getProperty('voices')
available_voices = [(voice.id, voice.name) for voice in voices]

@app.route('/')
def index():
    flash('Welcome to text to speech', 'info')
    return render_template('index.html')

@app.route('/about')
def about():
    flash('About this app', 'info')
    return render_template('about.html')

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        text = request.form['text']
        voice = request.form['voice']
        rate = request.form['rate']
        filename = request.form['filename'] or 'output.mp3'
        print(text, voice, rate, filename)
        if text:
            if os.path.exists(os.path.join(RESULTS_FOLDER, filename)):
                filename = f"{round(time.time())}_{filename}"
            session['filename'] = filename
            engine.setProperty('voice', voice)
            # pitch: 50-200, volume: 0-1
            engine.setProperty('rate', int(rate)) # from 50 to 200
            filepath = os.path.join(RESULTS_FOLDER, filename)
            engine.save_to_file(text, filepath)
            engine.runAndWait()
            return redirect(url_for('result'))
    return render_template('form.html' , voices=available_voices)

@app.route('/result')
def result():
    return render_template('result.html', audio_file=url_for('static', filename=f'results/{session["filename"]}'))


@app.route('/delete/<filename>')
def delete(filename):
    filepath = os.path.join('static/uploads', filename)
    os.remove(filepath)
    flash('File deleted successfully', 'success')
    return redirect(url_for('upload'))

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('static/uploads', filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)