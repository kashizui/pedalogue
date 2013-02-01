#!/usr/bin/python
import sqlite3
import cgi, cgitb
cgitb.enable()


def new_entry(form):
    cur = conn.cursor() 
    entry = (
        int(form.getfirst("who")),
        form.getfirst("date"),
        int(form.getfirst("time")),
        int(form.getfirst("fee")),
        form.getfirst("notes")
    )
    cur.execute("insert into entries (group_id, date_string, time, fee, notes) values (?,?,?,?,?)", entry)

def new_group(form):
    cur = conn.cursor() 
    cur.execute("insert into groups (name, email, payer) values (?,?,?)", (form.getfirst("who"),form.getfirst("email"), form.getfirst("payer")))
    

def main():
    global message
    if form.getfirst("type") == 'entry':
        new_entry(form)
    elif form.getfirst("type") == 'group':
        new_group(form)
    else:
        message = "Invalid form submission."

conn = sqlite3.connect("data.db")
form = cgi.FieldStorage()
message = ''
main()
conn.commit()
print "Content-Type: text/html"
print 
print """<html>
 <head>
  <title>submission</title>
 </head>
 <body>
 <form action="index.py" method="post" id="message">
 <input type="hidden" name="message" value="%s" />
 </form>
 <script type="text/javascript">
 document.getElementById("message").submit()
 </script>
 </body>
</html>
""" % message
