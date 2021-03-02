from peewee import *
from app import mysql_db
import datetime

class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db

class Tag(BaseModel):
    tag_name = CharField(max_length=255)
    date_create = DateTimeField(default=datetime.datetime.now)

class Category(BaseModel):
    cate_name = CharField(unique=True)
    date_create = DateTimeField(default=datetime.datetime.now)

class Doc_Set(BaseModel):
    name_doc= CharField(max_length=255)
    date_create = DateTimeField(default=datetime.datetime.now)
    category_id = CharField(max_length=255)
    post_by = CharField(max_length=255)

class Doc(BaseModel):
    doc_order = CharField(max_length=255)
    main_id_doc = ForeignKeyField(Doc_Set)
    date_create = DateTimeField(default=datetime.datetime.now)
    note = CharField(max_length=255)
    path_main = CharField(max_length=255)
    status = BooleanField()

class Attrach(BaseModel):
    main_id_doc = ForeignKeyField(Doc_Set)
    date_create = DateTimeField(default=datetime.datetime.now)
    name = CharField(max_length=255)
    path_attrach = CharField(max_length=255)

class Summarys(BaseModel):
    main_id_doc = ForeignKeyField(Doc_Set)
    date_create = DateTimeField(default=datetime.datetime.now)
    name = CharField(max_length=255)
    path_summary = CharField(max_length=255)

class pairing(BaseModel):
    main_id_doc = ForeignKeyField(Doc_Set)
    tags_id = ForeignKeyField(Tag)



if __name__ == '__main__':
    mysql_db.connect()
    # mysql_db.execute_sql("SET FOREIGN_KEY_CHECKS=0")
    # mysql_db.drop_tables([Users])
    # mysql_db.execute_sql("SET FOREIGN_KEY_CHECKS=1")
    mysql_db.create_tables([Summarys,Doc_Set,Doc,Tag,Category,Attrach,pairing])