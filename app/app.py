
import os
import sys
import cx_Oracle
from flask import Flask ,render_template, request, redirect, url_for,session
from flask import *  
from flask_mail import Mail, Message
import random
import datetime
from datetime import date,timedelta
import re
import string
import requests
import pathlib
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
db_user = os.environ.get('DBAAS_USER_NAME', 'SYSTEM')
db_password = os.environ.get('DBAAS_USER_PASSWORD', 'Sreyas@2002')
db_connect = os.environ.get('DBAAS_DEFAULT_CONNECT_DESCRIPTOR', "localhost:1521/ORCL")
service_port = port=os.environ.get('PORT', '1512')


app = Flask("ICONIC TRAVELS")
mail = Mail(app)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "3916653145-gcvfu4l9iiakaf98epn1a7htjst5ha2k.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'iconictravels6@gmail.com'
app.config['MAIL_PASSWORD'] = 'jopzjsxdrgpjmvbl'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.secret_key = 'your secret key'

def date(a):
    if a[5:7]=="01":
       k="jan" 
    if a[5:7]=="02":
       k="feb" 
    if a[5:7]=="03":
       k="mar" 
    if a[5:7]=="04":
       k="apr" 
    if a[5:7]=="05":
       k="may" 
    if a[5:7]=="06":
       k="jun" 
    if a[5:7]=="07":
       k="jul" 
    if a[5:7]=="08":
       k="aug" 
    if a[5:7]=="09":
       k="sep" 
    if a[5:7]=="10":
       k="oct" 
    if a[5:7]=="11":
       k="nov" 
    if a[5:7]=="12":
       k="dec" 
    return a[-2:]+"-"+k+"-"+a[:4]

def day(a):
    if a[5:7]=="01":
       k=1 
    if a[5:7]=="02":
       k=2
    if a[5:7]=="03":
       k=3
    if a[5:7]=="04":
       k=4
    if a[5:7]=="05":
       k=5
    if a[5:7]=="06":
       k=6
    if a[5:7]=="07":
       k=7
    if a[5:7]=="08":
       k=8
    if a[5:7]=="09":
       k=9
    if a[5:7]=="10":
       k=10
    if a[5:7]=="11":
       k=11
    if a[5:7]=="12":
       k=12
    f=int(a[8:10])
    if f<10:
        f=int(a[9:10])
    b=int(a[:4])
    k=datetime.datetime(b,k,f)
    k=k.strftime("%w")
    return k

def dayfind(a):
    if a[3:6]=="jan":
       k=1 
    if a[3:6]=="feb":
       k=2
    if a[3:6]=="mar":
       k=3
    if a[3:6]=="apr":
       k=4
    if a[3:6]=="may":
       k=5
    if a[3:6]=="jun":
       k=6
    if a[3:6]=="jul":
       k=7
    if a[3:6]=="aug":
       k=8
    if a[3:6]=="sep":
       k=9
    if a[3:6]=="oct":
       k=10
    if a[3:6]=="nov":
       k=11
    if a[3:6]=="dec":
       k=12
    f=int(a[:2])
    if f<10:
        f=int(a[1:2])
    b=int(a[7:])
    k=datetime.datetime(b,k,f)
    k=k.strftime("%w")
    return k





@app.route('/')
def index():
    session['loggedin']=False
    session['centry']=False
    session['cbook']=False
    session['cavailible']=False
    session['manager']=False
    session['forgotpassword']=False
    session['vc']=False
    session['bid']=0
    session['protected area']=False
    return render_template('loginonly.html')

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper


@app.route('/logon')
def logon():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session["x"]=id_info.get("email")
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/protected_area")

@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    session['loggedin']=False
    if(session['protected area']):
        msg='account already exists'
        session['protected area']=False
        return render_template('loginonly.html',msg=msg)
    if request.method == 'POST' and 'EMAIL' in request.form and 'Password' in request.form:
        EMAIL = request.form['EMAIL']
        Password=request.form['Password']
        manageremail="manager@gmail.com"
        managerpassword="manager"
        if EMAIL==manageremail and Password==managerpassword:
            session['manager']=True
            msg='dear manager loggedin successfully '
            return render_template('managerhome.html',msg=msg)
        else:
            connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
            cur = connection.cursor()
            cur.execute("""SELECT * FROM customer where EMAIL=:EMAIL and c_pass=:Password""",EMAIL=EMAIL,Password=Password)
            connection.commit()
            touple=cur.fetchone()
            if touple:
                session['EMAIL']=EMAIL
                session['loggedin']=True
                msg="logged in sucessfully"
                return render_template('customerprofile.html',msg=msg)
            else:
                msg="incorrect email/password"
                return render_template('loginonly.html',msg=msg)
            cur.close()
            connection.close() 
        
    return render_template('loginonly.html')

@app.route("/protected_area")
@login_is_required
def protected_area():
    EMAIL=session['x']
    session['protected area']=True
    connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
    cursor = connection.cursor()
    cursor.execute("""SELECT EMAIL FROM customer WHERE EMAIL = :EMAIL""",EMAIL=EMAIL)
    connection.commit()
    account = cursor.fetchone()
    if account:
        EMAIL=account
        return redirect(url_for('login'))
    return redirect(url_for('signuponly'))

@app.route('/signuponly',methods=['GET','POST'])
def signuponly():
    msg=''
    session['loggedin']=False
    if request.method == 'POST'  and 'password' in request.form and 'confirm password' in request.form and 'username' in request.form and 'gender' in request.form and 'ph' in request.form:
        EMAIL = session['x']
        password = request.form['password']
        confirm_password=request.form['confirm password']
        username = request.form['username']
        dob=request.form['dob']
        gender=request.form['gender']
        ph=request.form['ph']
        connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
        cursor = connection.cursor()
        cursor.execute("""SELECT EMAIL FROM customer WHERE EMAIL = :EMAIL""",EMAIL=EMAIL)
        connection.commit()
        account = cursor.fetchone()
        if account:
            session['EMAIL']=account
            msg = 'Account already exists !'
            return render_template('loginonly.html',msg=msg)
        elif password!=confirm_password:
            msg = 'please enter same password for confirmation'
            return render_template('signuponly.html',msg=msg)
        elif not username or not password or not confirm_password or not EMAIL or not dob or not gender or not ph:
            msg = 'Please fill out the form !'
            return render_template('signuponly.html',msg=msg)
        else:
            dob=date(dob)
            sql="""insert into customer(c_name,EMAIL,c_pass,dob,gender,phonenumber) values(:username,:EMAIL,:password,:dob,:gender,:phonenumber)"""
            cursor.execute(sql,[username,EMAIL,password,dob,gender,ph])
            connection.commit()
            msg = 'You have successfully registered !'
            return render_template('loginonly.html',msg=msg)

        cursor.close()
        connection.close()
    return render_template('signuponly.html', msg = msg)
@app.route('/cprofile',methods=['GET','POST'])
def cprofile():
    msg=''
    return render_template('customerprofile.html')

@app.route('/customerentry' ,methods=['GET','POST'])
def customerentry():
    msg=''
    msg1=''
    msg2=''
    msg3=''
    msg4=''
    if not session['loggedin']:
        return render_template('loginonly.html')
    if session['loggedin']:
        if request.method == 'POST' and 'startdate' in request.form and 'returndate' in request.form and 'travellers' in request.form and 'pickup point' in request.form and 'DROP point' in request.form and 'startmode of transport' in request.form and 'returnmode of transport' in request.form:
             start_date = request.form['startdate']
             return_date = request.form['returndate']
             travellers = request.form['travellers']
             pickup_point = request.form['pickup point']
             drop_point = request.form['DROP point']
             startmode_of_transport = request.form['startmode of transport']
             returnmode_of_transport = request.form['returnmode of transport']
             if pickup_point==drop_point:
                 msg='you have chosen same source and destination locations please change it'
                 return render_template('customerentry.html',msg=msg)
             booking_id=random.randint(100000000,999999999)
             EMAIL=session['EMAIL']
             session['bid2']=0
             session['booking_id']=booking_id
             if not EMAIL or not start_date or not return_date or not travellers or not pickup_point or not drop_point or not startmode_of_transport or not returnmode_of_transport:
                 msg='please fill out the form'
                 return render_template('customerentry.html',msg=msg)
             connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
             cursor = connection.cursor()
             startdate=date(start_date)
             returndate=date(return_date)
             session['startdate']=start_date
             session['returndate']=return_date
             session['travellers']=travellers
             sql="""INSERT INTO travel_website(booking_id,start_date,return_date,travellers,sourcee,destination,start_mode,return_mode,EMAIL) values(:bookingid,:startdate,:returndate,:travellers,:p_p,:d_p,:startmode,:returnmode,:EMAIL)"""
             cursor.execute(sql,[booking_id,startdate,returndate,travellers,pickup_point,drop_point,startmode_of_transport,returnmode_of_transport,EMAIL])
             connection.commit()
             sql="  INSERT INTO travel_agency(booking_id) values(:booking_id)"
             cursor.execute(sql,[booking_id])
             connection.commit()
             cursor.execute("""select * from vehicledetails where start_place=:start_place  and reach_place=:return_place and s_date=:s_date and (seat_capacity-booked_seats)>:k  AND V_TYPE=:v_type""",start_place=pickup_point,return_place=drop_point,s_date=startdate,k=travellers,v_type=startmode_of_transport)
             connection.commit()
             account=cursor.fetchone()
             if account:
                 x=int(account[3])+1
                 k=int(travellers)*int(account[4])
                 cost1=k
                 session['seat_cost_s']=k
                 session['booked_seats_s1']=x
                 session['booked_seats_s2']=int(travellers)+x
                 session['vnod_s']=account[0]
                 session['vno_s']=account[1]
                 msg1=str(x)+" to "+str(int(travellers)+x-1)
             else:
                 cursor.execute("""DELETE from travel_website where booking_id=:booking_id """,booking_id=booking_id)
                 connection.commit()
                 return render_template('customerna.html',msg=msg) 
             cursor.execute("""select * from vehicledetails where start_place=:start_place and s_date=:s_date and reach_place=:reach_place and (seat_capacity-booked_seats)>:k and v_type=:v_type  """,start_place=drop_point,s_date=returndate,reach_place=pickup_point,k=travellers,v_type=returnmode_of_transport)
             connection.commit()
             touple=cursor.fetchone()
             if touple:
                 x=int(touple[3])+1
                 k=int(travellers)*int(touple[4])
                 cost2=k
                 session['seat_cost_r']=k
                 session['booked_seats_r1']=x
                 session['booked_seats_r2']=int(travellers)+x
                 session['vnod_r']=touple[0]
                 session['vno_r']=touple[1]
                 msg2=str(x)+" to "+str(int(travellers)+x-1)
             else:
                 cursor.execute("""DELETE from travel_website where booking_id=:booking_id """,booking_id=booking_id)
                 connection.commit()
                 return render_template('customerna.html',msg=msg)
            
             sql="""INSERT INTO hotel_site(booking_id,no_of_travellers,stay_place,bs_date,be_date) values (:booking_id,:travellers,:place,:sdate,:rdate)"""
             cursor.execute(sql,[booking_id,travellers,drop_point,startdate,returndate])
             connection.commit()
             cursor.execute("""select * from hoteldetails where place=:drop_point""",drop_point=drop_point)
             connection.commit()
             room=cursor.fetchall()
             for row in room:
                 k2=int(row[5])
                 k1=int(row[4])*int(travellers)
                 k3=int(travellers)
                 if k3%2==0:
                    k3=int(k3/2)
                 else:
                    k3=int(int(k3+1)/2)
                 k4=int(row[4])
                 k5=row[0]
                 k6=k3
                 p=0
                 s=int(day(start_date))
                 r=int(day(return_date))+1
                 if (r-s)<=1:
                     return render_template('customerna.html',msg=msg)
                 for y in range(1,k2+1): 
                     count=0
                     for x in range(s,r):
                        cursor.execute(""" SELECT * FROM hotelrooms where h_name=:h_name and place=:place and room_no=:rno and status=:status and s_day=:x""",h_name=k5,place=drop_point,rno=y,status=p,x=x)
                        connection.commit()
                        free=cursor.fetchone()
                        if free:
                            count=count+1
                     if count==r-s:
                        sql="""INSERT INTO c_bookings (booking_id,h_name,place,r_no) values (:booking_id,:h_name,:place,:r_no)"""
                        cursor.execute(sql,[booking_id,k5,drop_point,y])
                        connection.commit()
                        count=0
                        k6=k6-1
                     if k6==0:
                         session['seat_cost']=cost1+cost2
                         session['rooms_cost']=k1
                         k8=session['rooms_cost']
                         k1=k1+cost1+cost2
                         msg5=str(k1)
                         session['trip_cost']=k1
                         cursor.execute("""select r_no from c_bookings where booking_id=:b_id""",b_id=booking_id)
                         connection.commit()
                         room_numbers=cursor.fetchall()
                         for ro in room_numbers:
                             h=str(ro)
                             msg4=msg4+h[1:-1]
                         msg4=msg4[:-1]
                         vno_s=session['vno_s']
                         vno_r=session['vno_r']
                         session['centry']=True
                         session['hotel']=row
                         cursor.execute("""update travel_website set trip_expenses=:trip where booking_id=:b_id""",trip=msg5,b_id=booking_id )
                         cursor.execute("""update travel_agency set start_vno=:s_vno,return_vno=:r_vno,travelling_charges=:charges where booking_id=:b_id""",s_vno=vno_s,r_vno=vno_r,charges=cost1+cost2,b_id=booking_id)
                         cursor.execute("""update hotel_site set accomodation_charges=:ac,booked_rooms=:k3,hotel_name=:h_name where booking_id=:b_id""",ac=k8,k3=k3,h_name=k5,b_id=booking_id)
                         connection.commit()
                         session['roomnumbers']=msg4
                         session['seats_s']=msg1
                         session['seats_r']=msg2
                         return render_template('cavailible.html',account=account[1],touple=touple[1],msg1=msg1,msg2=msg2,msg3=row,msg4=msg4,msg5=msg5)
                 if k6!=0:
                     cursor.execute("""DELETE FROM C_BOOKINGS WHERE booking_id=:booking_id""",booking_id=booking_id)
                     connection.commit()
             cursor.execute("""DELETE FROM travel_website where booking_id=:booking_id""",booking_id=booking_id)
             connection.commit() 
             cursor.close()
             connection.close()
             return render_template('customerna.html',msg=msg)
        return render_template('customerentry.html',msg=msg)
    return render_template('loginonly.html',msg=msg)
            
    
@app.route('/customerhome',methods=['GET','POST'])
def customerhome():
    msg=''
    return render_template('customerprofile.html')
@app.route('/cavalible',methods=['GET','POST'])
def cavalible():
    if session['loggedin']:
        if session['centry']:
            session['cavailible']=True
            return render_template('cavailible.html')
        else:
            return render_template('customerentry.html')
    else:
        return render_template('loginonly.html')
@app.route('/customerbook',methods=['GET','POST'])
def customerbook():
    msg=''
    if session['loggedin']:
        if session['centry']:
            if session['bid2']==session['booking_id']:
                return redirect(url_for('booking'))
            connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
            cursor = connection.cursor()
            booking_id=session['booking_id']
            s_date=session['startdate']
            r_date=session['returndate']
            sdate=date(s_date)
            rdate=date(r_date)
            vnod1=session['vnod_s']
            vnod2=session['vnod_r']
            vno1=session['vno_s']
            vno2=session['vno_r']
            tra=int(session['travellers'])
            cursor.execute("""select booked_seats from vehicledetails where vnod=:vnod""",vnod=vnod1)
            connection.commit()
            booked_seats=cursor.fetchone()
            booked_seats=str(booked_seats)
            bs1=int(booked_seats[1:-2])
            if int(session['booked_seats_s1'])>bs1+1 and session['bid2']==0:
                msg="you have waited too long for booking"
                cursor.execute("""DELETE FROM TRAVEL_WEBSITE WHERE BOOKING_ID=:BID""",BID=booking_id)
                connection.commit()
                return redirect(url_for('customerentry'),msg=msg)
            vno2=session['vno_r']
            cursor.execute("""select booked_seats from vehicledetails where vnod=:vnod""",vnod=vnod2)
            connection.commit()
            booked_seats=cursor.fetchone()
            booked_seats=str(booked_seats)
            bs=int(booked_seats[1:-2])
            if int(session['booked_seats_r1'])>bs+1 and session['bid2']==0:
                msg="you have waited too long for booking"
                cursor.execute("""DELETE FROM TRAVEL_WEBSITE WHERE BOOKING_ID=:BID""",BID=booking_id)
                connection.commit()
                return redirect(url_for('customerentry'))
            n=session['hotel']
            place=n[2]
            name=n[0]
            place=str(place)
            name=str(name)
            msg6=''
            msg6=str(session['roomnumbers'])
            msg7=''
            msg7=str(session['trip_cost'])
            msg1=str(session['seats_s'])
            msg2=str(session['seats_r'])
            s=int(day(s_date))
            r=int(day(r_date))+1
            cursor.execute("""select r_no from c_bookings where booking_id=:bid""",bid=booking_id)
            connection.commit()
            x=cursor.fetchall()
            for rno in x:
                for k in range(s,r):
                     cursor.execute("""select status from hotelrooms where h_name=:name and place=:place and room_no=:rno and s_day=:sdate""",name=name,place=place,rno=int(str(rno)[1:-2]),sdate=k) 
                     connection.commit()
                     stat=cursor.fetchone()
                     stat=int(str(stat)[1:-2])
                     if stat==1 and session['bid2']==0:
                         msg="you have waited too long for booking"
                         cursor.execute("""DELETE FROM TRAVEL_WEBSITE WHERE BOOKING_ID=:BID""",BID=booking_id)
                         connection.commit()
                         return redirect(url_for('customerentry'))

            tra_s=tra+bs1
            cno1=bs1+1
            if tra!=1:
               cno2=bs1+2
            else:
                cno2=0
            cursor.execute("""update vehicledetails set booked_seats=:booked_seats where vno=:vno1 and s_date=:sdate""",booked_seats=tra_s,vno1=vno1,sdate=sdate)
            connection.commit()
            for x in range(session['booked_seats_s1'],tra_s+1):
                cursor.execute("""update v_seats set s_status=:s where vnod=:vnod and s_no=:x""",s="1",vnod=vnod1,x=x)
                connection.commit()
            
            tra_r=tra+bs
            cno3=bs+1
            if tra!=1:
               cno4=bs+2
            else:
                cno4=0
            cursor.execute("""update vehicledetails set booked_seats=:booked_seats where vno=:vno2 and s_date=:sdate""",booked_seats=tra_r,vno2=vno2,sdate=rdate)
            connection.commit()
            for x in range(session['booked_seats_r1'],tra_r+1):
                cursor.execute("""update v_seats set s_status=:s where vnod=:vnod and s_no=:x""",s="1",vnod=vnod2,x=x)
                connection.commit()
            cursor.execute("""select r_no from c_bookings where booking_id=:booking_id""",booking_id=booking_id)
            connection.commit()
            x=cursor.fetchall()
            for rno in x:
                for k in range(s,r):
                    cursor.execute("""update hotelrooms set status=:status where h_name=:h_name and place=:place and room_no=:rno and s_day=:day""",status="1",h_name=name,place=place,rno=int(str(rno)[1:-2]),day=k)
                    connection.commit()
                cursor.execute("""update c_bookings set c_no1=:cno1,c_no2=:cno2,c_no3=:cno3,c_no4=:cno4 where r_no=:q and booking_id=:bid and h_name=:h_name and place=:place""",cno1=cno1,cno2=cno2,cno3=cno3,cno4=cno4,q=int(str(rno)[1:-2]),bid=booking_id,h_name=name,place=place)
                connection.commit()
                cno1=cno1+2
                if cno1==tra_s:
                    cno2=0
                else:
                    cno2=cno2+2
                cno3=cno3+2
                if cno3==tra_r:
                    cno4=0
                else:
                    cno4=cno4+2
            session['bid2']=booking_id
            return render_template('customerbook.html',booking_id=booking_id,account=vno1,msg1=msg1,touple=vno2,msg2=msg2,msg3=n,msg4=msg6,msg5=msg7)
        else:
            return render_template('customerprofile.html')
    else:
        return render_template('loginonly.html')
    return render_template('customerbook.html')

@app.route('/managerhome',methods=['GET','POST'])
def managerhome():
    msg=''
    return render_template('managerhome.html',msg=msg)

@app.route('/vadd',methods=['GET','POST'])
def vadd():
    msg=''
    if session['manager']:
        if request.method == 'POST' and 'vehiclenumber' in request.form and 'capacity' in request.form and 'cost' in request.form and 'type' in request.form and 'startplace' in request.form and 'reachplace' in request.form and 'start_date' in request.form :
            vehiclenumber=request.form['vehiclenumber']
            capacity=request.form['capacity']
            cost=request.form['cost']
            vtype=request.form['type']
            startplace=request.form['startplace']
            returnplace=request.form['reachplace']
            start_date=request.form['start_date']
            connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
            cursor =connection.cursor()
            cursor.execute("""SELECT * FROM vehicledetails WHERE vno=:vehiclenumber""",vehiclenumber=vehiclenumber)
            connection.commit()
            account = cursor.fetchone()
            if not vehiclenumber or not capacity or not cost or not vtype or not startplace or not returnplace or not start_date:
                msg='please fill out the form'
                return render_template('manageradd.html',msg=msg)
            elif account:
                startdate=date(start_date)
                if startdate==str(account[8])[2:-3]:
                    msg="vehicle already present in the database"
                    return render_template('manageradd.html',msg=msg)
                else:
                   startdate=date(start_date)
                   vnod=vehiclenumber+start_date[:4]+start_date[5:7]+start_date[8:10]
                   sql="""INSERT INTO vehicledetails(vnod,vno,seat_capacity,start_place,reach_place,booked_seats,seat_cost,v_type,s_date) VALUES(:vnod,:vehiclenumber,:capacity,:startplace,:returnplace,:bs,:sc,:vt,:sd) """
                   cursor.execute(sql,[vnod,vehiclenumber,capacity,startplace,returnplace,0,cost,vtype,startdate])
                   connection.commit()

                   for x in range(1,int(capacity)+1):
                       sql=""" INSERT INTO V_SEATS(vnod,s_no,s_status) VALUES(:vnod,:s_no,:s_status)"""
                       cursor.execute(sql,[vnod,x,0])
                       connection.commit()
                   msg='vehicle has been added successfully'
                   return render_template('managerhome.html',msg=msg)
            else:
                startdate=date(start_date)
                vnod=vehiclenumber+start_date[:4]+start_date[5:7]+start_date[8:10]
                sql="""INSERT INTO vehicledetails(vnod,vno,seat_capacity,start_place,reach_place,booked_seats,seat_cost,v_type,s_date) VALUES(:vnod,:vehiclenumber,:capacity,:startplace,:returnplace,:bs,:sc,:vt,:sd) """
                cursor.execute(sql,[vnod,vehiclenumber,capacity,startplace,returnplace,0,cost,vtype,startdate])
                connection.commit()

                for x in range(1,int(capacity)+1):
                    sql=""" INSERT INTO V_SEATS(vnod,s_no,s_status) VALUES(:vnod,:s_no,:s_status)"""
                    cursor.execute(sql,[vnod,x,0])
                    connection.commit()
                msg='vehicle has been added successfully'
                return render_template('managerhome.html',msg=msg)      
            cursor.close()
            connection.close()
    else:
        return render_template('loginonly.html')
    return render_template('manageradd.html',msg=msg)

@app.route('/vdelete',methods=['GET','POST'])
def vdelete():
    msg=''
    if(session['manager']):
        if request.method == 'POST' and 'vehiclenumber' in request.form and 'start_date' in request.form:
            vehiclenumber=request.form['vehiclenumber']
            start_date=request.form['start_date']
            connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
            cursor =connection.cursor()
            cursor.execute("""SELECT * FROM vehicledetails WHERE vno =:vehiclenumber""",vehiclenumber=vehiclenumber)
            connection.commit()
            account = cursor.fetchone()
            if account and not start_date:
                cursor.execute("""DELETE FROM vehicledetails where vno=:vno""",vno=vehiclenumber)
                connection.commit()
                msg='vehicle has been deleted successfully'
                return render_template('managerhome.html',msg=msg)
            elif not vehiclenumber: 
                msg='please fill out the form'
                return render_template('managerremove.html',msg=msg)
            elif account:
                startdate=date(start_date)
                cursor.execute("""DELETE FROM vehicledetails where vno=:vno and s_date=:s_date""",vno=vehiclenumber,s_date=startdate)
                connection.commit()
            else:
                msg='vehicle is not present in the database'
                return render_template('managerremove.html',msg=msg)
            cursor.close()
            connection.close()
        return render_template('managerremove.html',msg=msg)
    else:
        return render_template('loginonly.html',msg=msg)
    return render_template('managerremove.html')
@app.route('/vupdatebefore',methods=['GET','POST'])
def vupdatebefore():
    if session['manager']:
        return render_template('vupdatebefore.html')
    else:
        return render_template('loginonly.html')
@app.route('/vupdate',methods=['GET','POST'])
def vupdate():
    msg=''
    if(session['manager']):
        if request.method == 'POST' and 'vehiclenumber' in request.form and 'cost' in request.form and 'startplace' in request.form and 'reachplace' in request.form and 'startdate' in request.form and 'psp' in request.form:
            vehiclenumber=request.form['vehiclenumber']
            cost=request.form['cost']
            startplace=request.form['startplace']
            returnplace=request.form['reachplace']
            sd=request.form['startdate']
            psp=request.form['psp']
            connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
            cursor =connection.cursor()
            if not vehiclenumber or not cost or not startplace or not returnplace: 
                msg='please fill out the form'
                return render_template('managerupdate.html',msg=msg)
            if sd and psp:
                cursor.execute("""SELECT * FROM vehicledetails WHERE vno =:vehiclenumber and s_date=:sd AND start_place=:psp""",vehiclenumber=vehiclenumber,sd=date(sd),psp=psp)
                connection.commit()
                account = cursor.fetchone()
                if account:
                    cursor.execute("""UPDATE vehicledetails SET start_place=:startplace,reach_place=:returnplace,seat_cost=:cost where vno=:vehiclenumber and s_date=:sd and start_place=:psp""",startplace=startplace,returnplace=returnplace,cost=cost,vehiclenumber=vehiclenumber,sd=date(sd),psp=psp)
                    connection.commit()
                    msg='vehicle updated successfully'
                    return render_template('managerhome.html',msg=msg)
                else:
                    msg='vehicle is not present in the database with this start date and start place'
                    return render_template('managerupdate.html',msg=msg)
            elif sd:
                cursor.execute("""SELECT * FROM vehicledetails WHERE vno =:vehiclenumber and s_date=:sd""",vehiclenumber=vehiclenumber,sd=date(sd))
                connection.commit()
                account = cursor.fetchone()
                if account:
                    cursor.execute("""UPDATE vehicledetails SET start_place=:startplace,reach_place=:returnplace,seat_cost=:cost where vno=:vehiclenumber and s_date=:sd""",startplace=startplace,returnplace=returnplace,cost=cost,vehiclenumber=vehiclenumber,sd=date(sd))
                    connection.commit()
                    msg='vehicle updated successfully'
                    return render_template('managerhome.html',msg=msg)
                else:
                    msg='vehicle is not present in the database with this start date'
                    return render_template('managerupdate.html',msg=msg)

            elif psp:
                cursor.execute("""SELECT * FROM VEHICLEDETAILS WHERE VNO=:VNO AND START_PLACE=:PSP""",VNO=vehiclenumber,PSP=psp)
                connection.commit()
                account=cursor.fetchone()
                if account:
                    cursor.execute("""UPDATE vehicledetails SET start_place=:startplace,reach_place=:returnplace,seat_cost=:cost where vno=:vehiclenumber and start_place=:psp""",startplace=startplace,returnplace=returnplace,cost=cost,vehiclenumber=vehiclenumber,psp=psp)
                    connection.commit()
                    msg='vehicle updated successfully'
                    return render_template('managerhome.html',msg=msg)
                else:
                    msg='vehicle is not present in the database with this start place'
                    return render_template('managerupdate.html',msg=msg)
            else:
                msg="please fill startdate or present start date"
                return render_template('managerupdate.html',msg=msg)
            cursor.close()
            connection.close()
    else:
        return render_template('loginonly.html')
    return render_template('managerupdate.html',msg=msg)
@app.route('/vsdupdate',methods=['GET','POST'])
def vsdupdate():
    if session['manager']:
        if request.method=='POST' and 'vno' in request.form and 'bsd' in request.form and 'sd' in request.form:
            vno=request.form['vno']
            bsd=request.form['bsd']
            sd=request.form['sd']
            if not vno or not bsd or not sd:
                msg="please fill all fields"
                return render_template('vsdupdate.html',msg=msg)
            else:
                connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
                cursor =connection.cursor()
                cursor.execute("""SELECT vno FROM vehicledetails WHERE vno =:vehiclenumber and s_date=:sd""",vehiclenumber=vno,sd=date(bsd))
                connection.commit()
                account = cursor.fetchone()
                cursor.execute("""SELECT vno FROM vehicledetails WHERE vno =:vehiclenumber and s_date=:sd""",vehiclenumber=vno,sd=date(sd))
                connection.commit()
                x = cursor.fetchone()
                if account:
                    if x:
                        msg="vehicle with same details is already present"
                        return render_template('vsdupdate.html',msg=msg)
                    else:
                        cursor.execute("""update vehicledetails set s_date=:sd where vno=:vno and s_date=:bsd""",sd=date(sd),vno=vno,bsd=date(bsd))
                        connection.commit()
                        msg="succesfully updated"
                        return render_template('managerhome.html',msg=msg)
                else:
                    msg="vehicle with same date is not  present in the database"
                    return render_template('vsdupdate.html',msg=msg)
                cursor.close()
                connection.close()
    else:
        return render_template('loginonly.html')
    return render_template('vsdupdate.html')
@app.route('/addplace',methods=['GET','POST'])
def addplace():
    return render_template('manageraddplace.html')

@app.route('/addhotel',methods=['GET','POST'])
def addhotel():
    msg=''
    if(session['manager']):
        if request.method=='POST' and 'hotelname' in request.form and 'place' in request.form and 'address' in request.form and 'rating' in request.form and 'roomrent' in request.form and 'numberofrooms' in request.form:
            hotelname=request.form['hotelname']
            place=request.form['place']
            address=request.form['address']
            rating=request.form['rating']
            rr=request.form['roomrent']
            nor=request.form['numberofrooms']
            if not hotelname or not place or not address or not rating or not rr or not nor:
                msg="please fill all the details"
                return render_template('managerhoteladd.html',msg=msg)
            connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
            cursor =connection.cursor()
            cursor.execute("""SELECT * from hoteldetails where h_name=:name and place=:place""",name=hotelname,place=place)
            connection.commit()
            account=cursor.fetchone()
            if account:
                msg="hotel already exists"
                return render_template('managerhoteladd.html',msg=msg)
            else:
                sql="""INSERT INTO HOTELDETAILS(h_name,address,place,rating,roomrent,no_of_rooms) VALUES (:h_name,:address,:place,:rating,:roomrent,:no_of_rooms)"""
                cursor.execute(sql,[hotelname,address,place,rating,rr,nor])
                connection.commit()
                k1=int(nor)
                for x in range(1,k1+1):
                    for k3 in range(7):
                        sql="""INSERT INTO HOTELROOMS(h_name,place,room_no,status,s_day) VALUES(:k4,:k5,:k,:k2,:k3)"""
                        cursor.execute(sql,[hotelname,place,x,0,k3])
                        connection.commit()
                msg="hoteladded sucessfully"
                return render_template('managerhoteladd.html',msg=msg)
            cursor.close()
            connection.close()
    else:
        return render_template('loginonly.html')
    return render_template('managerhoteladd.html')
@app.route('/reset',methods=['GET','POST'])
def reset():
    if session['manager']:
        if request.method=='POST' and 'd0' in request.form and 'd1' in request.form and 'd2' in request.form and 'd3' in request.form and 'd4' in request.form and 'd5' in request.form and 'd6' in request.form:
            d0=request.form['d0']
            d1=request.form['d1']
            d2=request.form['d2']
            d3=request.form['d3']
            d4=request.form['d4']
            d5=request.form['d5']
            d6=request.form['d6']
            if not d1 or not d2 or not d3 or not d4 or not d5 or not d6:
                msg='fill all the dates'
                return render_template('reset.html',msg=msg)
            elif int(day(d0))!=0 or int(day(d1))!=1 or int(day(d2))!=2 or int(day(d3))!=3 or int(day(d4))!=4 or int(day(d5))!=5 or int(day(d6))!=6:
                msg=str(day(d0))+str(day(d1))+str(day(d2))+str(day(d3))+str(day(d4))+str(day(d5))+str(day(d6))
                return render_template('reset.html',msg=msg)
            else:
                count=0
                connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
                cursor =connection.cursor()
                cursor.execute("""SELECT S_DATE from vehicledetails""")
                connection.commit()
                x=cursor.fetchall()
                msg=''
                for k in x:
                    k=str(k)[2:-3]
                    p=dayfind(k)
                    p=int(p)
                    if p==0:
                        cursor.execute("""update vehicledetails set s_date=:s_date where s_date=:k""",s_date=date(d0),k=k)
                        connection.commit()
                        count=count+1
                    if p==1:
                        cursor.execute("""update vehicledetails set s_date=:s_date where s_date=:k""",s_date=date(d1),k=k)
                        connection.commit()
                        count=count+1
                    if p==2:
                        cursor.execute("""update vehicledetails set s_date=:s_date where s_date=:k""",s_date=date(d2),k=k)
                        connection.commit()
                        count=count+1
                    if p==3:
                        cursor.execute("""update vehicledetails set s_date=:s_date where s_date=:k""",s_date=date(d3),k=k)
                        connection.commit()
                        count=count+1
                    if p==4:
                        cursor.execute("""update vehicledetails set s_date=:s_date where s_date=:k""",s_date=date(d4),k=k)
                        connection.commit()
                        count=count+1
                    if p==5:
                        cursor.execute("""update vehicledetails set s_date=:s_date where s_date=:k""",s_date=date(d5),k=k)
                        connection.commit()
                        count=count+1
                    if p==6:
                        cursor.execute("""update vehicledetails set s_date=:s_date where s_date=:k""",s_date=date(d6),k=k)
                        connection.commit()
                        count=count+1
                    if count==7:
                        break
                cursor.execute("""update vehicledetails set booked_seats=:bk""",bk="0")
                connection.commit()
                cursor.execute("""update v_seats set s_status=:s""",s="0")
                connection.commit()
                cursor.execute("""update hotelrooms set status=:s""",s="0")
                connection.commit()
                msg="sucess"
                cursor.close()
                connection.close()
                return render_template('managerhome.html',msg=msg)
            return render_template('reset.html')
    else:
        return render_template('loginonly.html')
    return render_template('reset.html')



@app.route('/removehotel',methods=['GET','POST'])
def removehotel():
    if session['manager']:
        if request.method=='POST' and 'hotelname' in request.form and 'place' in request.form:
            hotel=request.form['hotelname']
            place=request.form['place']
            if not hotel or not place:
                msg="please fill out form"
                return render_template('removehotel.html',msg=msg)
            else:
                connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
                cursor =connection.cursor()
                cursor.execute("""SELECT * from hoteldetails where h_name=:hotel and place=:place""",hotel=hotel,place=place)
                connection.commit()
                acc=cursor.fetchone()
                if acc:
                    cursor.execute("""DELETE from hoteldetails where h_name=:hotel and place=:place""",hotel=hotel,place=place)
                    connection.commit()
                    msg="hotel deleted successfully"
                    return render_template('removehotel.html',msg=msg)
                else:
                    msg="hotel not present in database"
                    return render_template('removehotel.html',msg=msg)
                cursor.close()
                connection.close()
    else:
        return render_template('loginonly.html')
    return render_template('removehotel.html')
@app.route('/updatepackages',methods=['GET','POST'])
def updatepackages():
    return render_template('updatepackages.html')
@app.route('/profile',methods=['GET','POST'])
def profile():
    if session['loggedin']:
        email=session['EMAIL']
        connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
        cursor =connection.cursor()
        cursor.execute("""select * FROM customer where EMAIL=:email""",email=email)
        account=cursor.fetchone()
        cursor.close()
        connection.close()
        msg1=account[4]
        if msg1=="male":
            return render_template('profile.html',msg=account)
        else:
            return render_template('profile1.html',msg=account)
    else:
        return render_template('loginonly.html')
@app.route('/changepassword',methods=['GET','POST'])
def changepassword():
    msg=''
    if session['loggedin']:
        if request.method=='POST' and 'newpassword' in request.form and 'confirmpassword' in request.form and 'currentpassword':
          email=session['EMAIL']
          np=request.form['newpassword']
          cp=request.form['confirmpassword']
          cup=request.form['currentpassword']
          if not np or not cp or not cup:
              msg="enter all the fields"
              return render_template('changepassword.html',msg=msg)
          elif np!=cp:
              msg="enter same password both times"
              return render_template('changepassword.html',msg=msg)
          else:
              connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
              cursor =connection.cursor()
              cursor.execute("""SELECT C_PASS from customer where EMAIL=:email""",email=email)
              connection.commit()
              x=cursor.fetchone()
              if cup==str(x)[2:-3]:
                  cursor.execute("""update customer set c_pass=:np where email=:email """,np=np,email=email)
                  connection.commit()
                  msg="password sucessfully updated"
              else:
                  msg="current password is wrong"
              cursor.close()
              connection.close()
              return render_template('changepassword.html',msg=msg)
        else:
            return render_template('changepassword.html')
    else:
        return render_template('loginonly.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    session['loggedin']=False
    session['centry']=False
    session['cbook']=False
    session['cavailible']=False
    session['manager']=False
    session['forgotpassword']=False
    session['vc']=False
    session['bid2']=0
    return render_template('loginonly.html')
@app.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():
    if request.method=='POST' and 'email' in request.form:
        email=request.form['email']
        if not email:
            msg="please enter your email id"
            return render_template('forgotpassword.html',msg=msg)
        else:
              connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
              cursor =connection.cursor()
              cursor.execute("""SELECT EMAIL from customer where EMAIL=:email""",email=email)
              connection.commit()
              x=cursor.fetchone()
              if x:
                  session['forgotpassword']=True
                  S=10
                  ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
                  sql="""INSERT INTO FP(EMAIL,CODE) VALUES (:EMAIL,:CODE)"""
                  cursor.execute(sql,[str(x)[2:-3],ran])
                  connection.commit()
                  msg1="verification"
                  msg = Message(msg1,sender ='iconictravels6@gmail.com',recipients =[str(x)[2:-3]])
                  msg.body = 'this is the verification code to reset your account password: '+ran
                  mail.send(msg)
                  msg="enter code"
                  session['email']=x
                  return render_template('forgotpassword1.html',msg=msg)
              else:
                  msg="email you have enterd is incorrect recheck again"
                  return render_template('forgotpassword.html',msg=msg)
              cursor.close()
              connection.close()
    return render_template('forgotpassword.html')
@app.route('/forgotpassword1',methods=['GET','POST'])
def forgotpassword1():
    if session['forgotpassword']:
        if request.method=='POST' and 'verificationcode' in request.form:
            email=session['email']
            email=str(email)[2:-3]
            vc=request.form['verificationcode']
            if not vc:
                msg="please enter the code we have sent to your mail"
                return render_template('forgotpassword1.html',msg=msg)
            else:
                connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
                cursor =connection.cursor()
                cursor.execute("""SELECT code from FP where EMAIL=:email""",email=email)
                connection.commit()
                k=cursor.fetchall()
                for x in k:
                    if str(x)[2:-3]==vc:
                       cursor.execute("""DELETE FROM FP WHERE EMAIL=:EMAIL""",EMAIL=email)
                       connection.commit()
                       session['vc']=True
                       return render_template('forgotpassword2.html')
                cursor.close()
                connection.close()
                msg="verification code you have entered is incorrect"
                return render_template('forgotpassword1.html',msg=msg)
    else:
        return render_template('forgotpassword.html')
    return render_template('forgotpassword1.html')
@app.route('/forgotpassword2',methods=['GET','POST'])
def forgotpassword2():
    if session['forgotpassword']:
        if session['vc']:
            if request.method=='POST' and 'newpassword' in request.form and 'confirmpassword' in request.form:
                np=request.form['newpassword']
                cp=request.form['confirmpassword']
                if not np or not cp:
                    msg="enter new and current passwords"
                    return render_template('forgotpassword2.html',msg=msg)
                elif cp!=np:
                    msg="passwords doesn't match"
                    return render_template('forgotpassword2.html',msg=msg)
                else:
                    email=str(session['email'])[2:-3]
                    connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
                    cursor =connection.cursor()
                    cursor.execute("""update customer set c_pass=:np where EMAIL=:email""",np=np,email=email)
                    connection.commit()
                    session['forgotpassword']=False
                    session['vc']=False
                    cursor.close()
                    connection.close()
                    msg="password changed sucessfully"
                    return render_template('loginonly.html',msg=msg)
        else:
            return render_template('forgotpassword2.html')
    else:
        return render_template('loginonly.html')
    return render_template('forgotpassword2.html')

@app.route('/booking',methods=['GET','POST'])
def booking():
    msg=''
    if session['loggedin']:
        email=str(session['EMAIL'])
        y = datetime.datetime.now()
        y=y.strftime("%j")
        connection = cx_Oracle.connect('SYSTEM/Sreyas@2002@localhost')
        cursor =connection.cursor()
        cursor.execute("""SELECT * FROM TRAVEL_WEBSITE WHERE EMAIL=:email""",email=email)
        connection.commit()
        x=cursor.fetchall()
        count1=0
        count2=0
        for k in x:
            p=k[0]
            cursor.execute("""SELECT * FROM  C_bookings where c_no1 IS NULL""")
            connection.commit()
            h=cursor.fetchone()
            if h:
                cursor.execute("""DELETE FROM TRAVEL_WEBSITE WHERE booking_id=:bid""",bid=p)
                connection.commit()
        cursor.execute("""SELECT * FROM TRAVEL_WEBSITE WHERE EMAIL=:email""",email=email)
        connection.commit()
        x=cursor.fetchall()
        for k in x:
            p=k[2]
            p=p.strftime("%j")
            if int(p)>=int(y):
                count1=count1+1
            else:
                count2=count2+1
        current=[[] for i in range(count1)]
        prev=[[] for i in range(count2)]
        i=0
        j=0
        for k in x:
            p=k[2]
            p = p.strftime("%j")
            if int(p)>=int(y):
                msg=''
                msg1=''
                msg2=''
                cursor.execute("""SELECT * FROM TRAVEL_AGENCY WHERE booking_id=:bid""",bid=k[0])
                connection.commit()
                c=cursor.fetchone()
                cursor.execute("""SELECT * FROM hotel_site where booking_id=:bid""",bid=k[0])
                connection.commit()
                d=cursor.fetchone()
                cursor.execute("""SELECT * FROM hoteldetails WHERE h_name=:name and place=:place""",name=d[6],place=k[5])
                connection.commit()
                e=cursor.fetchone()
                cursor.execute("""SELECT * FROM C_BOOKINGS WHERE booking_id=:bid ORDER BY r_no""",bid=k[0])
                connection.commit()
                g=cursor.fetchall()
                for f in g:
                    if f[5]!=0:
                        msg=msg+str(f[4])+','+str(f[5])+','
                        msg1=msg1+str(f[6])+','+str(f[7])+','
                    else:
                        msg=msg+str(f[4])+','
                        msg1=msg1+str(f[6])+','
                    msg2=msg2+str(f[3])+','
                msg=msg[:-1]
                msg1=msg1[:-1]
                msg2=msg2[:-1]
                current[i]=[str(k[0])]
                current[i].append(str(k[4]))
                current[i].append(str(k[5]))
                current[i].append(str(k[3]))
                current[i].append(date(str(k[1])[:10]))
                current[i].append(date(str(k[2])[:10]))
                current[i].append(str(k[6]))
                current[i].append(str(c[0])+'('+str(k[7])+')')
                current[i].append(msg)
                current[i].append(str(c[1])+'('+str(k[8])+')')
                current[i].append(msg1)
                current[i].append(str(e[0]))
                current[i].append(msg2)
                current[i].append(str(e[1]))
                i=i+1
            else:
                msg=''
                msg1=''
                msg2=''
                cursor.execute("""SELECT * FROM TRAVEL_AGENCY WHERE booking_id=:bid""",bid=k[0])
                connection.commit()
                c=cursor.fetchone()
                cursor.execute("""SELECT * FROM hotel_site where booking_id=:bid""",bid=k[0])
                connection.commit()
                d=cursor.fetchone()
                cursor.execute("""SELECT * FROM hoteldetails WHERE h_name=:name and place=:place""",name=d[6],place=k[5])
                connection.commit()
                e=cursor.fetchone()
                cursor.execute("""SELECT * FROM C_BOOKINGS WHERE BOOKING_ID=:BID ORDER BY R_NO""",BID=k[0])
                connection.commit()
                g=cursor.fetchall()
                for f in g:
                    if f[5]!=0:
                        msg=msg+str(f[4])+','+str(f[5])+','
                        msg1=msg1+str(f[6])+','+str(f[7])+','
                    else:
                        msg=msg+str(f[4])+','
                        msg1=msg1+str(f[6])+','
                    msg2=msg2+str(f[3])+','
                msg=msg[:-1]
                msg1=msg1[:-1]
                msg2=msg2[:-1]
                prev[j]=[str(k[0])]
                prev[j].append(str(k[4]))
                prev[j].append(str(k[5]))
                prev[j].append(str(k[3]))
                prev[j].append(date(str(k[1])[:10]))
                prev[j].append(date(str(k[2])[:10]))
                prev[j].append(str(k[6]))
                prev[j].append(str(c[0])+'('+str(k[7])+')')
                prev[j].append(msg)
                prev[j].append(str(c[1])+'('+str(k[8])+')')
                prev[j].append(msg1)
                prev[j].append(str(e[0]))
                prev[j].append(msg2)
                prev[j].append(str(e[1]))
                j=j+1 
        cursor.close()
        connection.close()
        return render_template('mybookings.html',row=current,prev=prev)
    else:
        return render_template('loginonly.html')






