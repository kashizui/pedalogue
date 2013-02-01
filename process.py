#!/usr/bin/python
import sqlite3
import cgi, cgitb
from urllib import quote_plus as escape
from datetime import date
cgitb.enable()

def gen_invoice(group_id):
    c = conn.cursor()
    c.execute("select date_string,fee from entries where group_id=? and pending=? order by date_string asc", (group_id, 1))
    entries = c.fetchall()
    entries_block_list = []
    total_fee = 0
    for entry in entries:
        entries_block_list.append("Lesson %s________________$%s" % entry)
        total_fee += entry[1]
    entries_block = '\n'.join(entries_block_list)
    c.execute("select email,payer from groups where id=? and active=1", (group_id,))
    email, payer = c.fetchone()
    issue_date = date.today().strftime("%m/%d/%Y")
    body = """PIANO LESSONS INVOICE

Stephen Koo
2147 Amherst St
Palo Alto, CA 94306
(650) 815-9952

Date Issued: {issue_date}
Recipient: {payer}

{entries}

TOTAL: ${total_fee}

===============================
This message is automatically generated.
Please don't hesitate to let me know if 
there are any mistakes.
Thank you!""".format(issue_date=issue_date, payer=payer, entries=entries_block, total_fee=total_fee)
    subject = "Piano Lessons Invoice [%s]" % issue_date
    return email, subject, body

def send_email(recipient, subject, body):
    global mail_open
    address = """mailto:%s?subject=%s&body=%s""" % (recipient, escape(subject), escape(body))
    mail_open = """window.open("%s")""" % address

def dequeue(group_id):
    pass

def main():
    global message
    group_id = form.getfirst("who")
    if not group_id:
        message = "Invalid form submission."
        return
    recipient, subject, body = gen_invoice(group_id)
    send_email(recipient, subject, body)
    dequeue(group_id)

conn = sqlite3.connect("data.db")
form = cgi.FieldStorage()
message = ''
mail_open = ''
auto_submit = ''
main()
conn.commit()
if message:
    auto_submit = 'document.getElementById("message").submit()'
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
 <form action="clear.py" method="post">
 <input type="hidden" name="who" value="%s" />
 <input type="submit" value="Clear Pending Requests" style="width: 20em;" />
 </form>
 <form action="index.py" method="post">
 <input type="hidden" name="message" value="No requests cleared." />
 <input type="submit" value="Cancel" style="width: 20em;" />
 </form>
 <script type="text/javascript">
 %s
 %s
 </script>
 </body>
</html>
""" % (message, form.getfirst("who"), mail_open, auto_submit)
