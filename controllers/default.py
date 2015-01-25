# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
hospitals_list = ('PCH','POW','RGL','RGW','UHL','UHW')
db.theatres.hospital_name.requires=IS_IN_SET(hospitals_list)


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))

def test_date():
    from datetime import datetime
    now = datetime.now()
    rows = db(db.theatres).select()
    for row in rows:
        if row.start_date_and_time < now:
            record_id = row.id
            db(db.theatres.id == record_id).delete()

    return locals()
def med_board():
    hello = "Hello World Cardiff 2015"
    return locals()

@auth.requires_login()
def new_operation():
    form = SQLFORM(db.theatres, fields=['surgeon_name','procedure_name','hospital_name','theatre_name','start_date_and_time','estimated_duration','max_number_of_trainees'],labels={'estimated_duration':'Duration (Hours)'})
    if form.process().accepted:
        redirect(URL('display_operations',args="ALL"))
    return locals()


def display_operations():
    hospital_locations = hospitals_list

    if not request.args(1):
        sort_type = "start"
    else:
        sort_type = request.args(1)

    if request.args(0) == "ALL":
        hospital = "ALL"

        if sort_type == "start":
            rows = db(db.theatres).select(orderby=(db.theatres.start_date_and_time))
        elif sort_type == "duration":
            rows = db(db.theatres).select(orderby=(db.theatres.estimated_duration))
        elif sort_type == "spaces":
            rows = db(db.theatres).select(orderby=~(db.theatres.max_number_of_trainees-db.theatres.number_of_attendees))
    else:
        hospital = request.args(0)
        if sort_type == "start":
            rows = db(db.theatres.hospital_name==hospital).select(orderby=(db.theatres.start_date_and_time))
        elif sort_type == "duration":
            rows = db(db.theatres.hospital_name==hospital).select(orderby=(db.theatres.estimated_duration))
        elif sort_type == "spaces":
            rows = db(db.theatres.hospital_name==hospital).select(orderby=~(db.theatres.max_number_of_trainees-db.theatres.number_of_attendees))



        #ORDER BY SPACES AVAILABLE
#         rows = db(db.theatres).select(orderby=~(db.theatres.max_number_of_trainees-db.theatres.number_of_attendees))

#     rows = db(db.theatres).select(orderby=db.theatres.start_date_and_time)

    return locals()

def sign_up():
    operation_id = request.args(0)
    form = SQLFORM.factory(
        Field('your_name', requires=IS_NOT_EMPTY()))

    if form.process().accepted:
        response.flash = 'form accepted'
        row = db(db.theatres.id==operation_id).select().first()
        current_names = row.attendee_names
        current_attendees = row.number_of_attendees
        current_names.append(form.vars.your_name)
        row.update_record(attendee_names=current_names)
        row.update_record(number_of_attendees=current_attendees+1)
        redirect(URL('display_operations',args="ALL"))

    return locals()
def test_names():
    operation_id = request.args(0)
    data_table = db(db.test).select()
    form = SQLFORM.factory(
        Field('your_name', requires=IS_NOT_EMPTY()))

    if form.process().accepted:
        response.flash = 'form accepted'
        row = db(db.test.id==1).select().first()
        current_names = row.attendee_names
        current_names.append(form.vars.your_name)
        row.update_record(attendee_names=current_names)


    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login()
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
