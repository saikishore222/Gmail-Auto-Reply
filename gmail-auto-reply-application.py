from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from tkcalendar import *
from imap_tools import MailBox, AND
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
l=[]
root=Tk()
root.title("Gmail-Auto-Reply")
root.geometry("860x500")
root.configure(bg="#11E5DB")
p1=PhotoImage(file='Gmail-icon.png')
root.iconphoto(False,p1)
frame=Frame(root,height=30)
frame.pack(side=TOP)
lbl_title = Label(frame, text="Gmail-Auto-Reply", font="Arial 15 bold", bg="orange",  width = 300,fg="green")
lbl_title.pack(fill=X)
l1=Label(root,text="Username:-",bg="#11E5DB",fg="blue",font="Arial 15 bold")
l1.place(x=120,y=80)
user_field=Entry(root,width=30,font="Arial 15 ")
user_field.place(x=280,y=85)
l2=Label(root,text="password:-",bg="#11E5DB",fg="blue",font="Arial 15 bold")
l2.place(x=120,y=120)
passw_field=Entry(root,show="*",width=30,font="Arial 15")
passw_field.place(x=280,y=120)
l1=Label(root,text="Date:-",bg="#11E5DB",fg="blue",font="Arial 15 bold")
l1.place(x=120,y=160)
cal=DateEntry(root,text="Select Date",fg="white",font="Arial 15")
cal.place(x=280,y=160)
l4=Label(root,text="message:-",bg="#11E5DB",fg="blue",font="Arial 15 bold")
l4.place(x=120,y=200)
msg1=Text(root,height=5,width=60,font="Arial 13")
msg1.place(x=280,y=200)
l4=Label(root,text="Attachments:-",bg="#11E5DB",fg="blue",font="Arial 15 bold")
l4.place(x=120,y=320)
def send():
    if(user_field.get()=='' or passw_field.get()==''  or  msg1.get('1.0',END)=='' ):
            messagebox.showinfo("information","fill the details")
    else:
        k1=cal.get()
        m=k1.split("/")
        year=2000+int(m[2])
        d=datetime.date(year,int(m[0]),int(m[1]))
        print(d)
        print(user_field.get())
        print(passw_field.get())
        mailbox = MailBox('imap.gmail.com')
        mailbox.login(user_field.get(), passw_field.get(), initial_folder='INBOX')
        c=0
        for msg in mailbox.fetch(AND(seen=False,date=d)):
            c=1
            print(msg.date)
            print(msg.subject)
            print(msg.from_)
            print(msg.text)
            email_sender = user_field.get()
            msg2 = MIMEMultipart() 
            msg2['From'] =email_sender
            msg2['To'] = msg.from_
            msg2['Subject']=  "RE: "+msg.subject.replace("Re: ", "").replace("RE: ", "") 
            body = 'hi everyone ! this email is from python'
            msg2.attach(MIMEText(body, 'plain'))
            print(l)
            for filename in l:
                    print(filename)
                    attachment = open(filename, 'rb')
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition",
                    f"attachment; filename= {filename}")
                    msg2.attach(part)
            text = msg2.as_string()
            try:
                connection = smtplib.SMTP('smtp.gmail.com', 587)
                connection.starttls()
                connection.login(email_sender, passw_field.get())
                connection.sendmail(email_sender,msg.from_, text )
                if(len(l)!=0):
                    messagebox.showinfo("information","successfully sent the reply to all mails  with %d attachments"%(len(l)))
                else:
                    messagebox.showinfo("information","successfully sent the reply to all mails")
            except:
                    messagebox.showinfo("information","there is a problem while sending")
            mailbox.logout()
        if(c==0):
            messagebox.showinfo('information',"there is no new unseen emails on your selected date")
def browsefiles():
        filename = fd.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
        l.append(filename)
def clear():
    user_field.delete(first=0,last=100)
    passw_field.delete(first=0,last=100)
    msg1.delete('1.0',END)
    l=[]
direct=Button(root, text = "Browse",command=browsefiles,width = 70)
direct.place(x=280,y=320)
b1=Button(root,text="send",bg="pink",font="Arial 15 bold",activebackground="pink",command=send)
b1.place(x=320,y=400)
b2=Button(root,text="clear",bg="pink",font="Arial 15 bold",activebackground="pink",command=clear)
b2.place(x=420,y=400)
root.mainloop()
