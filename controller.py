import os
from app import *
from flask import Flask, flash, render_template, request, redirect, url_for, session, Response, make_response, jsonify
from model import *
from peewee import *
app = Flask(__name__)
__author__ = 'ibininja'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@app.before_request
def _db_conenct():
    mysql_db.connect()

##############################################################################################################################################################################################


@app.teardown_request
def _db_close(exc):
    if not mysql_db.is_closed():
        mysql_db.close()

##############################################################################################################################################################################################


@app.route('/', methods=['GET', 'POST'])
def search():
    choose = Category.select().order_by(Category.date_create.desc())
    return render_template('search.html', choose=choose)

##############################################################################################################################################################################################


@app.route('/alldoc', methods=['GET', 'POST'])
def alldoc():
    query = Doc_Set.select().order_by(Doc_Set.date_create.desc())
    return render_template('alldoc.html', files=query, title="เอกสารทั้งหมด")

##############################################################################################################################################################################################


@app.route("/doc/<string:doc_set_id>", methods=['GET', 'POST'])
def doc(doc_set_id):
    """ ส่วนการเปิดหน้านั้นๆโดย query ข้อมูล โดย select by id นั้นๆมา"""
    name = Doc_Set.select().where(Doc_Set.id == doc_set_id)
    print(name)
    recent = Doc.select().where(Doc.main_id_doc_id == doc_set_id).order_by(
        Doc.date_create.desc()).limit(1)

    select_summary = Summarys.select().where(Summarys.main_id_doc_id ==
                                     doc_set_id).order_by(Summarys.date_create.desc())
    select_attrach = Attrach.select().where(Attrach.main_id_doc_id ==
                                    doc_set_id).order_by(Attrach.date_create.desc())
    select_doc = Doc.select().where(Doc.main_id_doc_id ==
                            doc_set_id).order_by(Doc.date_create.desc())

    return render_template('doc.html', name=name, recent=recent, select_doc=select_doc, doc_set_id=doc_set_id, select_summary=select_summary, select_attrach=select_attrach)

##############################################################################################################################################################################################


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    allofcate = Category.select().order_by(Category.date_create.desc())
    return render_template('upload.html', allofcate=allofcate, title="อัพโหลดเอกสาร")


@app.route("/upload_doc", methods=['GET', 'POST'])
def upload_doc():
        doc_name = request.form['doc_name']
        order = request.form['fname']+"/"+request.form['lname']
        select = request.form['select']

        Doc_Set.create(name_doc=doc_name, category_id=select)
        QueryDocID = Doc_Set.select().order_by(Doc_Set.id.desc()).limit(1)
        Id_doc = "";
        for row in QueryDocID:
            Id_doc = row.id;

        target = os.path.join(APP_ROOT, 'static'+os.sep+'upload'+os.sep+'doc')
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("file"):
            if file.filename != '':
                print(file)
                filename = file.filename
                dbsave = os.path.join('upload'+os.sep+'doc'+os.sep+filename)
                destination = os.sep.join([target, filename])
                print(destination)
                file.save(destination)
                Doc.create(path_main=dbsave,
                           main_id_doc_id=Id_doc, status=True, doc_order=order)

        target2 = os.path.join(
            APP_ROOT, 'static'+os.sep+'upload'+os.sep+'summary')
        if not os.path.isdir(target2):
            os.mkdir(target2)
        for file_summary in request.files.getlist("file_summary"):
            if file_summary.filename != '':
                print(file_summary)
                filename_summary = file_summary.filename
                dbsave = os.path.join('upload'+os.sep+'summary'+os.sep+filename_summary)
                destination2 = os.sep.join([target2, filename_summary])
                print(destination2)
                file_summary.save(destination2)
                Attrach.create(path_attrach=dbsave,
                               main_id_doc_id=Id_doc, name=filename_summary)

        target3 = os.path.join(
            APP_ROOT, 'static'+os.sep+'upload'+os.sep+'attrach')
        if not os.path.isdir(target3):
            os.mkdir(target3)

        for file_attrach in request.files.getlist("file_attrach"):
            if file_attrach.filename != '':
                print(file_attrach)
                filename_attrach = file_attrach.filename
                dbsave = os.path.join('upload'+os.sep+'attrach'+os.sep+filename_attrach)
                destination3 = os.sep.join([target3, filename_attrach])
                print(destination3)
                file_attrach.save(destination3)
                Summarys.create(path_summary=dbsave,
                                main_id_doc_id=Id_doc, name=filename_attrach)

        flash('เพิ่มเอกสารใหม่เรียบร้อย', 'success')

        return redirect(url_for('alldoc'))


##############################################################################################################################################################################################
@app.route("/adddoc/<string:doc_set_id>", methods=['GET', 'POST'])
def adddoc_id(doc_set_id):
    name = Doc_Set.select().where(Doc_Set.id == doc_set_id)
    return render_template('adddoc.html', doc_set_id=doc_set_id, title="อัพโหลดเอกสาร", name=name)


@app.route("/add_doc", methods=['GET', 'POST'])
def add_doc():
        order = request.form['fname']+"/"+request.form['lname']
        doc_set_id = request.form["doc_set_id"]

        email = request.values['email']
        print(email)
        print(doc_set_id)

        target = os.path.join(APP_ROOT, 'static'+os.sep+'upload'+os.sep+'doc')
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("add_file"):
            if file.filename != '':
                print(file)
                filename = file.filename
                dbsave = os.path.join('upload'+os.sep+'doc'+os.sep+filename)
                destination = os.sep.join([target, filename])
                print(destination)
                file.save(destination)
                Doc.create(path_main=dbsave,main_id_doc_id=doc_set_id, status=True, doc_order=order)

        target2 = os.path.join(
            APP_ROOT, 'static'+os.sep+'upload'+os.sep+'summary')
        if not os.path.isdir(target2):
            os.mkdir(target2)
        for file_summary in request.files.getlist("add_summary"):
            if file_summary.filename != '':
                print(file_summary)
                filename_summary = file_summary.filename
                dbsave = os.path.join('upload'+os.sep+'summary'+os.sep+filename_summary)
                destination2 = os.sep.join([target2, filename_summary])
                print(destination2)
                file_summary.save(destination2)
                Summarys.create(path_summary=dbsave,main_id_doc_id=doc_set_id, name=filename_summary)

        target3 = os.path.join(
            APP_ROOT, 'static'+os.sep+'upload'+os.sep+'attrach')
        if not os.path.isdir(target3):
            os.mkdir(target3)

        for file_attrach in request.files.getlist("add_attrach"):
            if file_attrach.filename != '':
                print(file_attrach)
                filename_attrach = file_attrach.filename
                dbsave = os.path.join('upload'+os.sep+'attrach'+os.sep+filename_attrach)
                destination3 = os.sep.join([target3, filename_attrach])
                print(destination3)
                file_attrach.save(destination3)
                Attrach.create(path_attrach=dbsave,main_id_doc_id=doc_set_id, name=filename_attrach)

        flash('เพิ่มเอกสารใหม่เรียบร้อย', 'success')

        return redirect('doc/'+doc_set_id)

##############################################################################################################################################################################################


@app.route('/allcate', methods=['GET', 'POST'])
def allcate():
    query = Category.select().order_by(Category.date_create.desc())
    return render_template('allcategory.html', files=query, title="หมวดหมู่เอกสารทั้งหมด")
##############################################################################################################################################################################################


@app.route("/addcategory", methods=['GET', 'POST'])
def addcategory():
    multiselect = Doc_Set.select().where(Doc_Set.category_id == "")
    return render_template('addcate.html', title="เพิ่มประเภทเอกสาร",multiselect = multiselect)


@app.route("/addcate", methods=['GET', 'POST'])
def addcate():
    cate_name = request.form['name_cate']
    Category.create(cate_name=cate_name)
    return redirect(url_for('allcate'))
##############################################################################################################################################################################################


@app.route("/cate/<string:category_id>", methods=['GET', 'POST'])
def category(category_id):
    files = Doc_Set.select().where(Doc_Set.category_id == category_id)
    name = Category.select().where(Category.id == category_id)
    return render_template('category.html', files=files, name=name, title="เพิ่มประเภทเอกสาร")


##############################################################################################################################################################################################

@app.route("/editdoc/<string:doc_set_id>", methods=['GET', 'POST'])
def editdoc(doc_set_id):
    
    name = Doc_Set.select().where(Doc_Set.id == doc_set_id)
    select_doc = Doc.select().where(Doc.main_id_doc_id == doc_set_id)
    status_doc = Doc.select().where(Doc.main_id_doc_id == doc_set_id, Doc.status == True)
    status_doc_false = Doc.select().where(Doc.main_id_doc_id == doc_set_id, Doc.status == False)
    return render_template('editdoc.html', doc_set_id=doc_set_id, title="แก้ไขเอกสาร", name=name, alldoc=select_doc, statusTrue=status_doc, statusFalse=status_doc_false)


@app.route("/edit",methods=['GET', 'POST'])
def edit():
    doc_set_id = request.form["doc_set_id"]
    edit_doc_set_id = request.form["select_doc"]
    target = os.path.join(APP_ROOT, 'static'+os.sep+'upload'+os.sep+'doc')
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("add_file"):
        if file.filename != '':
            print(file)
            filename = file.filename
            dbsave = os.path.join('upload'+os.sep+'doc'+os.sep+filename)
            destination = os.sep.join([target, filename])
            print(destination)
            file.save(destination)
            update = Doc.update(path_main=dbsave).where(Doc.id==edit_doc_set_id)
            update.execute()


    target2 = os.path.join(APP_ROOT, 'static'+os.sep+'upload'+os.sep+'summary')
    if not os.path.isdir(target2):
        os.mkdir(target2)
    for file_summary in request.files.getlist("add_summary"):
        if file_summary.filename != '':
            print(file_summary)
            filename_summary = file_summary.filename
            dbsave = os.path.join('upload'+os.sep+'summary'+os.sep+filename_summary)
            destination2 = os.sep.join([target2, filename_summary])
            print(destination2)
            file_summary.save(destination2)
            Summarys.create(path_summary=dbsave,main_id_doc_id=doc_set_id, name=filename_summary)

    target3 = os.path.join(
    APP_ROOT, 'static'+os.sep+'upload'+os.sep+'attrach')
    if not os.path.isdir(target3):
        os.mkdir(target3)

    for file_attrach in request.files.getlist("add_attrach"):
        if file_attrach.filename != '':
            print(file_attrach)
            filename_attrach = file_attrach.filename
            dbsave = os.path.join('upload'+os.sep+'attrach'+os.sep+filename_attrach)
            destination3 = os.sep.join([target3, filename_attrach])
            print(destination3)
            file_attrach.save(destination3)
            Attrach.create(path_attrach=dbsave,main_id_doc_id=doc_set_id, name=filename_attrach)
            flash('แก้ไขเอกสารแนบเรียบร้อย', 'success')
    
    for status in request.form.getlist("selectUnactivate"):
        updatestatus = Doc.update(status=False).where(Doc.id==status)
        updatestatus.execute()
    for status in request.form.getlist("selectActivate"):
        updatestatus = Doc.update(status=True).where(Doc.id==status)
        updatestatus.execute()

    flash('แก้ไขเอกสารเรียบร้อย', 'success')
    return redirect('doc/'+doc_set_id)
##############################################################################################################################################################################################


if __name__ == "__main__":

    app.run(debug=True)
