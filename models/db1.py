# -*- coding: utf-8 -*-
#table of THEATRE sessions
db.define_table('theatres',
                Field('surgeon_name','string'),
                Field('procedure_name','string'),
                Field('hospital_name','list:string'),
                Field('theatre_name','string'),
                Field('start_date_and_time','datetime'),
                Field('estimated_duration','integer'),
                Field('max_number_of_trainees','integer'),
                Field('number_of_attendees', 'integer',default=0),
                Field('attendee_names','list:string'))

#clean up THEATRE table
from datetime import datetime
now = datetime.now()
rows = db(db.theatres).select()
for row in rows:
    if row.start_date_and_time < now:
        record_id = row.id
        db(db.theatres.id == record_id).delete()
        

#require approval after reg 
auth.settings.registration_requires_approval = True

#testing table
db.define_table('test',
                Field('attendee_names','list:string'))
