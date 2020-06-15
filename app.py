import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='shreesh'
app.config['MYSQL_PASSWORD']='shreesh'
app.config['MYSQL_DB']='intern_assign'

mysql=MySQL(app)
user_input_attendance=0


# route for processing admin page queries

@app.route('/admin',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('admin.html')
    if request.method=='POST':
        cur=mysql.connection.cursor()
        cur1=mysql.connection.cursor()
        
        action="Submit Attendance"
        global user_input_attendance
        
        user_input_attendance=request.form['var1']
        user_input_class=str(request.form['var2'])
        user_input_section=str(request.form['var3'])
        result=cur.execute("select student_id, student_name, guardian_name,guardian_number from students where class=%s and section=%s",(user_input_class,user_input_section))
        result1=cur1.execute("SELECT status from student_attendance_map where attendance_date=%s",[user_input_attendance]) 
        
        if result1 >0:
            flag=1
            stored_attend=cur1.fetchall()
            action="Update Attendance"
        else:
            flag=0
            stored_attend=0
        if result>0:
            to_admin_info=cur.fetchall()
            return render_template("admin.html",to_admin_info=to_admin_info,flag=flag,stored_attend=stored_attend,action=action)
        else:
            return render_template("admin.html")

#route for processing teacher page queries

@app.route('/teacher',methods=['GET','POST'])
def page():
    if request.method=='GET':
        return render_template('teacher.html')
    if request.method=='POST':
        cur=mysql.connection.cursor()
        cur1=mysql.connection.cursor()
        action="Submit Attendance"
        global user_input_attendance
        user_input_attendance=request.form['var1']
        user_input_class=str(request.form['var2'])
        user_input_section=str(request.form['var3'])
        result=cur.execute("select student_id, student_name, guardian_name,guardian_number from students where class=%s and section=%s",(user_input_class,user_input_section))
        result1=cur1.execute("SELECT status from student_attendance_map where attendance_date=%s",[user_input_attendance])        
        
        if result1 >0:
            flag=1
            stored_attend=cur1.fetchall()
            action="Update Attendance"
        else:
            flag=0
            stored_attend=0
        
        if result>0:
            to_admin_info=cur.fetchall()
            return render_template("teacher.html",to_admin_info=to_admin_info,flag=flag,stored_attend=stored_attend,action=action)
        else:
            return render_template("teacher.html")

# route for adding attendance in the mysql database

@app.route('/post_attend',methods=['GET','POST'])
def update():
    data=request.get_json()
    global user_input_attendance
    for i in data['html_data']:
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO student_attendance_map (attendance_date, status, student_id, set_at) VALUES (%s, %s, %s,1) ",(user_input_attendance,i[0],i[1]))
        mysql.connection.commit()
        cur.close()
    return("ok")

# route for updating the attendance in the mysql database

@app.route('/update_attend',methods=['GET','POST'])
def update_attd():
    data=request.get_json()
    for i in data['html_data']:
        global user_input_attendance
        cur=mysql.connection.cursor()
        s1=user_input_attendance
        cur.execute("UPDATE student_attendance_map set status=%s where attendance_date=date(%s) and student_id=%s",(i[0],s1,i[1]))
        mysql.connection.commit()
        cur.close()

    return("ok")

if __name__=="__main__":
    app.run(debug=True)