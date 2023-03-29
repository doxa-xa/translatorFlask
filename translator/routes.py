from flask import render_template, redirect, url_for, flash, request, send_from_directory
from translator import app, db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from translator.forms import LoginForm, UploadForm, DownloadForm, RegisterForm
from translator.models import User
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from translator.google_translate import cleanhtml, translate_text, chunker
import os
import pysrt as srt


@app.route('/', methods=['GET','POST'])
def index_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).first()
        if user and user.check_password(password_attempt=form.password.data):
            login_user(user)
            flash(f'Добре дошъл {user.user_name}!', category='success')
            return redirect(url_for('home_page'))
        else:
            flash(f'Потебителското име: {user.user_name} или паролата са грешни', category='danger')
    return render_template('index.html',form=form)

@app.route('/home', methods=['GET','POST'])
@login_required
def home_page():
    form = UploadForm(CombinedMultiDict((request.files,request.form)))
    if form.validate_on_submit() and request.method =='POST':
        file = form.subtitle.data
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads',filename))
        flash('Качването на файла за превод завърши успешно', category='success')
        return redirect(url_for('download_page'))
    else:
        flash('Случи се грешка с качването на файла моля опитайте отново', category='danger')
    return render_template('home.html',form=form)

@app.route('/download', methods=['GET','POST'])
@login_required
def download_page():
    form = DownloadForm()
    translated_text = []
    count = 0
    msg=''
    if form.validate_on_submit() and request.method == 'POST':
        msg=''
        subs = srt.open(os.path.join('uploads','VampireTranslated.srt'))
        original_text = []  
        
        for sub in subs:
            original_text.append(cleanhtml(sub.text))

        original_text_chunked = chunker(original_text)# limited to 128 translation segments i chose 125 sized chunks
        
        for chunk in original_text_chunked:
            text = translate_text(form.language.data,chunk)
            translated_text.append(text)
            count = count + 1
            print(f'Chunk {count} translated')

        result_list = []
        for chunk in translated_text:
            for item in chunk:
                result_list.append(item['translatedText'])
    
        i=0
        while i<len(result_list):
            subs[i].text = result_list[i]
            i=i+1

        subs.save(os.path.join('downloads','translated.srt') ,encoding='utf-8')
        flash(f"Файлът е успешно преведен", category='success')
        return send_from_directory(os.path.abspath('downloads/'),'translated.srt', as_attachment=True)
    
    return render_template('download.html',form=form, msg=msg)

@app.route('/logout')
def logout_page():
    logout_user()
    flash(f"Довиждане!", category='info')
    return redirect(url_for('index_page'))

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(user_name=form.user_name.data, email=form.email.data,
                              password=form.password.data, score=0)
        with app.app_context():
            db.session.add(user_to_create)
            db.session.commit()
        user = User.query.filter_by(user_name=form.user_name.data).first()
        login_user(user)
        flash(f'Потребителят е създаден успешно! Добре дошли {user.user_name}',category='success')
        return redirect(url_for('home_page'))
    if form.errors!= {}: #if there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f'Настъпи грешка по време на регистрация на потребител:{err_msg}', category='danger')
    return render_template('temp.html', form=form)