#!/usr/bin/python
import cgi
import cgitb
cgitb.enable()
from string import Template
import sqlite3
from datetime import date

def main(show_history):
    global left, right
    conn = sqlite3.connect("data.db")
    left = gen_fields(conn)
    if show_history:
        right = gen_history(conn)
    else:
        right = gen_pending(conn)

def gen_history(conn):
    c = conn.cursor()
    c.execute("select id,name,payer from groups")
    groups = c.fetchall()
    result = """<span id="heading">Lessons History</span><br />
    <a href="index.py?show_history=no" style="position: absolute; right: 0px; top:0px;">Hide History</a>"""
    for group_id, group_name,payer in groups:
        result += "<br /><span id='group'>%s:</span><br />" % group_name
        c.execute("select * from entries where group_id=:id order by date_string desc", {"id": group_id, "pending": 1})
        entries = c.fetchall()
        if not entries:
            result += "No Entries Yet"
        for entry in entries:
            if entry[6] == 0:
                result += "[<a href='return.py?entry=%s'>r</a>] " % (entry[0],)
            result += "[<a href='delete.py?entry=%s'>x</a>] <span id='entry'>Lesson on %s for %s minutes at $%s</span><br />" % ( entry[0], entry[2], entry[3], entry[4])
            if entry[5]:
                result += "<div id='entry_notes'>%s</div>" % entry[5].replace('\r\n','<br />')
    return result

def gen_pending(conn):
    c = conn.cursor()
    c.execute("select id,name,payer from groups where active=1")
    groups = c.fetchall()
    result = """<span id="heading">Pending Entries</span><br />
    <a href="index.py?show_history=yes" style="position: absolute; right: 10px; top:0px;">Show History</a>"""
    for group_id, group_name,payer in groups:
        result += "<br /><span id='group'>%s:</span><br />" % group_name
        c.execute("select * from entries where group_id=:id and pending=:pending order by date_string asc", {"id": group_id, "pending": 1})
        entries = c.fetchall()
        if not entries:
            result += "No Pending Entries"
        for entry in entries:
            result += "[<a href='delete.py?entry=%s'>x</a>] <span id='entry'>Lesson on %s for %s minutes at $%s</span><br />" % (entry[0], entry[2], entry[3], entry[4])
            if entry[5]:
                result += "<div id='entry_notes'>%s</div>" % entry[5].replace('\r\n','<br />')
        result += """<form action="process.py" method="post">
        <input type="hidden" name="who" value="{group_id}" />
        <input type="submit" value="Send Invoice to {payer}" style="width: 20em" />
        </form>""".format(group_id = group_id, payer = payer)
    return result

def gen_fields(conn):
    c = conn.cursor()
    c.execute("select id,name from groups where active=1")
    groups = c.fetchall()
    field_template = """<span id="fieldname">{name}: </span><input type="text" name="{id}" id="field" value="{value}" /><br />"""
    new_entry_fields = [
        ('date', date.today().strftime("%m/%d/%Y")),
        ('time', ''),
        ('fee', '')
    ]
    result = """
    <span id="heading">New Entry</span><br />
    <form action="submit.py" method="post">
    <span id="fieldname">Who: </span><select name="who" id="field">
    """
    for group in groups:
        result += """<option value="%s">%s</option>""" % (group[0], group[1])
    result += "</select><br />"
    for name, value in new_entry_fields:
        result += field_template.format(name=name.capitalize(), id=name, value=value)
    result += """<input type="hidden" name="type" value="entry" />
    Notes:<br />
    <textarea cols="40" rows="10" name="notes"></textarea><br />
    <input type="submit" value="Submit" />
    </form>
    """
    result += """
    <span id="heading">New Group</span><br />
    <form action="submit.py" method="post">
    """
    result += field_template.format(name="Who", id="who", value="")
    result += field_template.format(name="Email", id="email", value="")
    result += field_template.format(name="Payer", id="payer", value="")
    result += """
    <input type="hidden" name="type" value="group" />
    <input type="submit" value="Submit" />
    </form>
    """
    return result

message, left, right = '', '', ''
form = cgi.FieldStorage()
password = form.getfirst("pass")
title = "Piano Teaching Form"
header = "Content-Type:text/html\n"
if form.getfirst("show_history") == 'yes':
    show_history=True
else:
    show_history=False
main(show_history)
message = form.getfirst("message", "")

print header
print 

wrapper = Template("""
<html>
 <head>
  <title>$title</title>
  <style type="text/css">
  #message { 
    position: fixed;
    bottom: 0px;
    width: 100%;
    background-color: #FF2222;
  }
  #left {
    position: absolute;
    top: 10px;
    left: 2%;
    width: 48%;
  }
  #right {
    position: absolute;
    top: 10px;
    right: 5%;
    width: 48%;
  }
  #field {
    position: absolute;
    left: 4em;
  }
  #heading {
    font-size: large;
    text-decoration: underline;
  }
  #fieldname {
    line-height: 1.5em;
  }
  #entry {
    font-family: Courier;
    letter-spacing: -1.5px;
  }
  #entry_notes {
    position: relative;
    left: 2em;
  }
  </style>
 </head>
 <body>
 <div id="message">$message</div>
 <div id="left">$left</div>
 <div id="right">$right</div>
 </body>
</html>
""")
print wrapper.substitute(title=title, message=message, left=left, right=right)
