from app import *
from flask import Flask, flash, render_template, request, redirect, url_for, session, Response, make_response, jsonify
from model import *
import os
app = Flask(__name__)


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
    return render_template('search.html')

##############################################################################################################################################################################################
@app.route('/alldoc', methods=['GET', 'POST'])
def alldoc():
    query = Doc_Set.select()
    return render_template('alldoc.html', files=query, title="เอกสารทั้งหมด")

##############################################################################################################################################################################################
@app.route("/doc/<string:doc_set_id>", methods=['GET', 'POST'])
def doc(doc_set_id):
    """ ส่วนการเปิดหน้านั้นๆโดย query ข้อมูล โดย select by id นั้นๆมา"""
    name = Doc_Set.select().where(Doc_Set.id == doc_set_id )
    recent = Doc.select().where(Doc.main_id_doc_id == doc_set_id).limit(1)

    select_summary = Summarys.select().where(Summarys.main_id_doc_id == doc_set_id)
    select_attrach = Attrach.select().where(Attrach.main_id_doc_id == doc_set_id)
    select_doc = Doc.select().where(Doc.main_id_doc_id == doc_set_id)
    for file in select_doc:
        titles = file.path_main
    tytle = "เอกสาร-"+titles
    return render_template('doc.html',name = name,recent= recent, select_doc=select_doc, doc_set_id=doc_set_id, title=tytle,select_summary = select_summary,select_attrach =select_attrach)

##############################################################################################################################################################################################
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        doc_name = request.form['doc_name']
        order = request.form['fname']+"/"+request.form['lname']
        select = request.form['select']

        Doc_Set.create(name_doc=doc_name, id_cate=select)

        doc_file = os.path.join(APP_ROOT,'static/upload/doc/')
        if not os.path.isdir(doc_file):
            os.mkdir(doc_file)
        docFile_main = ""
        for doc in request.files.getlist("doc"):
            if doc.filename!="":
                filename = doc.filename
                docFile_main = filename
                destination1 = "/".join([doc_file,filename])
                doc.save(destination1)
        print(docFile_main)

        summary_file = os.path.join(APP_ROOT,'static/upload/summary/')
        if not os.path.isdir(summary_file):
            os.mkdir(summary_file)
        summaryFile_main = ""
        for summary in request.files.getlist("summary"):
            if summary.filename!="":
                summaryfilename = summary.filename
                summaryFile_main = summaryfilename
                destination2 = "/".join([summary_file,summaryfilename])
                summary.save(destination2)
        print(summaryFile_main)
        

        attrach_file = os.path.join(APP_ROOT,'static/upload/attrach/')
        if not os.path.isdir(attrach_file):
            os.mkdir(attrach_file)
        attrachFile_main = ""
        for attrach in request.files.getlist("attrach"):
            if attrach.filename!="":
                attrachfilename = attrach.filename
                attrachFile_main = attrachfilename
                destination3 = "/".join([attrach_file,attrachfilename])
                attrach.save(destination3)
        print(attrachFile_main)


        QueryDocID = Doc_Set.select().order_by(Doc_Set.id.desc()).limit(1)
        Id_doc = "";
        for row in QueryDocID:
            Id_doc = row.id;
        
        Doc.create(path_main=docFile_main,main_id_doc_id=Id_doc,status=True,doc_order = order)
        Attrach.create(path_attrach=attrachFile_main,main_id_doc_id=Id_doc)
        Summarys.create(path_summary=summaryFile_main,main_id_doc_id=Id_doc)
        flash('เพิ่มเอกสารใหม่เรียบร้อย', 'success')

        return redirect(url_for('alldoc'))


    return render_template('upload.html',title="อัพโหลดเอกสาร")
##############################################################################################################################################################################################

@app.route("/adddoc/<string:doc_set_id>", methods=['GET', 'POST'])
def adddoc(doc_set_id):
    name = Doc_Set.select().where(Doc_Set.id == doc_set_id )
    if request.method == "POST":
        order = request.form['fname']+"/"+request.form['lname']
        doc_file = request.form['doc']
        summary_file = request.form['summary']
        attrach_file = request.form['attrach']
        Doc.create(path_main = doc_file,main_id_doc_id = doc_set_id,doc_order = order,status = True)
        Attrach.create(path_attrach = attrach_file,main_id_doc_id = doc_set_id)
        Summarys.create(path_summary = summary_file,main_id_doc_id = doc_set_id)
        flash('เพิ่มเอกสารใหม่เรียบร้อย', 'success')
        return redirect('/doc/'+doc_set_id)
        
    return render_template('adddoc.html',doc_set_id= doc_set_id,title="เพิ่มเอกสาร",name = name)
##############################################################################################################################################################################################
@app.route("/category", methods=['GET', 'POST'])
def category():
    return render_template('category.html',title="ประเภทเอกสาร")
##############################################################################################################################################################################################
@app.route("/addcategory", methods=['GET', 'POST'])
def addcategory():
    return render_template('addcate.html',title="เพิ่มประเภทเอกสาร")
##############################################################################################################################################################################################

@app.route("/editdoc/<string:doc_set_id>", methods=['GET', 'POST'])
def editdoc(doc_set_id):
    name = Doc_Set.select().where(Doc_Set.id == doc_set_id )
    select_doc = Doc.select().where(Doc.main_id_doc_id == doc_set_id)
    return render_template('editdoc.html',doc_set_id=doc_set_id,title="แก้ไขเอกสาร",name = name,alldoc = select_doc)
##############################################################################################################################################################################################
if __name__ == "__main__":

    app.run(debug=True)
