from flask import Flask, request,session, render_template,url_for,make_response
from flask import jsonify, request
from werkzeug.utils import redirect
#from flask_mysqldb import MySQL
import mysql.connector
import simplejson as json
from apscheduler.scheduler import Scheduler
from datetime import timedelta
import datetime as dt
from dateutil import parser


app = Flask(__name__)
app.secret_key = 'any random string'
cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()

mydb = mysql.connector.connect(
    host="parkwaydb.cvwsvf6gxkqf.us-east-2.rds.amazonaws.com",
    user="admin",
    passwd="admin123",
    database="parkwaydatabase"
    )

mycursor = mydb.cursor(buffered=True)


@app.route("/")
def index():
  return "Hello world"

@app.route('/success/<name>')
def success(name):
   if name == 'wrong':
       return jsonify(message='Invalid Username password'),400
   return jsonify(message=int(name)),200


@app.route('/register', methods=['POST'])
def register_page():
   data = request.json
   firstname = data['firstname']
   lastname = data['lastname']
   emailid = data['emailid']
   mobile = data['mobile']
   dob = data['dob']
   username = data['username']
   password = data['password']
   usertype = data['usertype']
   sql = '''INSERT INTO user (firstname,lastname,emailid,mobile,dob,username,password,usertype)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
   val = (firstname, lastname, emailid, mobile,  dob, username, password, usertype)
   mycursor.execute(sql, val)
   mydb.commit()
   uid=mycursor.lastrowid
   UserID_globals=uid
   return jsonify(message=uid),200


@app.route('/login', methods=['POST'])
def login():
   data = request.json
   user = data['username']
   password = data['password']
   mycursor.execute("Select userid,username,password from user where username = %s and password=%s", (user, password))
   mydb.commit()
   tabledata = mycursor.fetchone()
   session['userid']=tabledata[0]
   
   print(session['userid'])
   if tabledata:
       return redirect(url_for('success', name=tabledata[0]))
   else:
       return redirect(url_for('success', name="wrong"))

@app.route('/host_spot', methods=['POST'])
def host_spot():
   data=request.json
   HUserID = data['hid']
   P_City = data['pcity']
   SpotAddress = data['sAddress']
   P_State = data['pstate']
   P_Country= data['pcountry']
   P_Zipcode = data['pzcode']
   sql = '''INSERT INTO parking_spot (HUserID,P_City, SpotAddress, P_State,P_Country, P_Zipcode) VALUES (%s,%s,%s,%s,%s,%s)'''
   val = (HUserID, P_City, SpotAddress, P_State,P_Country, P_Zipcode)
   mycursor.execute(sql, val)
   sdid=mycursor.lastrowid
   session['sdid']=sdid
   mydb.commit()
   return jsonify(message=sdid),200


@app.route('/host_further', methods=['GET'])
def host_further():
  return jsonify(result=session['sdid'])


@app.route('/guest', methods=['POST'])
def guest_details():
   details = request.json
   guserid = details['gid']
   cardnumber = details['cnumber']
   expirydate = details['edate']
   lnum = details['iproof']
   sql = '''INSERT INTO guest (guserid, cardnumber, expirydate, LicenseNum)VALUES (%s,%s,%s,%s)'''
   val = (guserid,cardnumber, expirydate, lnum)
   mycursor.execute(sql,val)
   mydb.commit()
   return jsonify(message='success'),200


@app.route('/guest_vehicle', methods=['POST'])
def guest_vehicle():
   details = request.form
   GUserID= details['guid']
   VehicleNumber= details['vnumber']
   ModelName  = details['mname']
   cur = mysql.connection.cursor()
   sql = '''INSERT INTO guest_vehicle ( GUserID,VehicleNumber,ModelName) VALUES (%s,%s,%s)'''
   val = (GUserID,VehicleNumber,ModelName)
   mycursor.execute(sql, val)
   mydb.commit()
   return jsonify(message='success'),200

@app.route('/reservation', methods=['POST'])
def reservation():
   details = request.json
   GUserID= details['gid']
   SdID= details['sdid']
   ReservationStartDateTime= details['rsdatetime']
   ReservationEndDateTime= details['redatetime']
   TotalFee=details['tfee']
   ReservationStartDateTime1=parser.parse(ReservationStartDateTime)
   ReservationStartDateTime1=(ReservationStartDateTime1 - timedelta(minutes=5))
   ReservationEndDateTime1=parser.parse(ReservationEndDateTime)
   ReservationEndDateTime1=(ReservationEndDateTime1 - timedelta(minutes=5))
 
  

   sql = '''INSERT INTO reservation(GUserID, SdID, reservationstartdatetime, reservationenddatetime, TotalFee) VALUES (%s,%s,%s,%s,%s)'''
   val = (GUserID, SdID, ReservationStartDateTime1, ReservationEndDateTime1,TotalFee)
   mycursor.execute(sql, val)
   mydb.commit()
   return jsonify(message='success'),200


@app.route('/spot_description', methods=['POST'])
def spot_description():
   details = request.json
   SpotID = details['SpotID']
   SpotName = details['SpotName']
   ParkingFeePerHour = details['ParkingFeePerHour']
   sql = '''INSERT INTO spot_description (SpotID, SpotName, ParkingFeePerHour)VALUES (%s,%s,%s)'''
   val = (SpotID,SpotName, ParkingFeePerHour)
   mycursor.execute(sql,val)
   mydb.commit()
   return jsonify(message='success'),200


@app.route('/search', methods=['POST'])
def parking_spot():
   details=request.json
   uzipcode=details['P_Zipcode']
   ucity=details['P_City']
   availablestartdatetime= parser.parse(details['AvailStartDateTime'])
   availableenddatetime= parser.parse(details['AvailEndDateTime'])
   #availablestartdatetime=dt.datetime.strptime(details['AvailStartDateTime'], '%b, %d %Y %H:%M ')
   #availableenddatetime=dt.datetime.strptime(details['AvailEndDateTime'], '%b, %d %Y %H:%M ')
   sql='''Select p.SpotAddress, p.P_City, p.P_Zipcode, s.spotName, s.ParkingFeePerHour,(TIME_TO_SEC(timediff( %s,%s))*(s.parkingfeeperhour/3600))as total_fee,s.sdid
from parkwaydatabase.parking_spot p 
Inner join parkwaydatabase.spot_description s on p.SpotID=s.SpotID
Inner Join parkwaydatabase.spot_availability sa on s.SdID=sa.SdID
Where p.P_Zipcode= %s and (Timediff(%s,sa.AvailableStartDateTime)>=0 and timediff(sa.AvailableEndDateTime, %s)>=0) 
and s.SdID not in 
(select SdID from reservation r where
((timediff(%s,r.reservationstartdatetime)>=0 and timediff(r.reservationenddatetime,%s)>=0)
or (timediff(%s,r.reservationstartdatetime)>=0 and timediff(r.reservationenddatetime,%s)>=0)))

   '''
   val=(availableenddatetime,availablestartdatetime,uzipcode,availablestartdatetime,availableenddatetime,availablestartdatetime,availablestartdatetime,availableenddatetime,availableenddatetime)
   mycursor.execute(sql,val)
   mydb.commit()
   tabledata1 = mycursor.fetchall()
   if tabledata1:
      data1=[]
      #result={}
      i=0
      for j in tabledata1:
        result={}
        #str1='"{"'+'"SPotAddress":'+tabledata1[i][0]+',"P_City":'+tabledata1[i][1]+',"P_Zipcode":'+str(tabledata1[i][2])+',"spotName":'+tabledata1[i][3]+',"ParkingFeePerHour":'+str(tabledata1[i][4])+'"}"'
        result['SPotAddress']=j[0]
        result['P_City']=j[1]
        result['P_Zipcode']=j[2]
        result['spotName']=j[3]
        result['ParkingFeePerHour']=j[4]
        result['total_fee']=j[5]
        result['SdID']=j[6]
        #data1['results'+str(i)]=[result]'''
        data1.append(result)
        i+=1
        jsonData=json.dumps(data1)
      return redirect(url_for('success1', name=jsonData))
   else:
      return redirect(url_for('success1', name="wrong"))

@app.route('/success1/<name>')
def success1(name):
   dict={}
   if name == 'wrong':
       return jsonify(message='No data found'),400
   else:
       dict['result']=name
       return jsonify(dict),200


@app.route('/success2/<name>')
def success2(name):
   dict={}
   if name == 'wrong':
       return jsonify(message='No data found'),400
   else:
       return jsonify(result=name),200


# firstname, lastname, emailid, mobile, address and dob , username
@app.route('/profile_details/<uid>',methods=['GET'])
def profile_details(uid):

   sql="select concat(firstname, ' ', lastname) as uname, emailid, mobile as contact_number, Username from user where UserID= %s"
   val=(uid,)
   mycursor.execute(sql,val)
   tabledata1 = mycursor.fetchall()
   data=[]
   if tabledata1:
    tabledata = tabledata1[0]
    item = {
        'Name': tabledata[0],
        'EmailID': tabledata[1],
        'Contact_Number': tabledata[2],
        'Username': tabledata[3],
        }
    data.append(item)
    UserID_globals=uid
    print(UserID_globals)
    jsonData = json.dumps(data)
    return redirect(url_for('success2', name=jsonData))
   else:
    return redirect(url_for('success2', name="wrong"))

# spot
@app.route('/booking',methods=['POST'])
def booking():
	details=request.json
	jsonData=json.dumps([details])
	return details,200

def myconverter(o):
    if isinstance(o, dt.datetime):
        return o.__str__()


@app.route('/activity_host/<uid>', methods=['GET'])
def activity_host(uid):
  
  sql= "select s.spotname,r.reservationstartdatetime as reserved_from,r.reservationenddatetime as reserved_to, totalfee,p.SpotAddress, p.P_City from reservation r join spot_description s on s.sdid=r.sdid join parking_spot p on p.SpotID=s.SpotID where p.huserid= %s"

  val=(uid,)
  mycursor.execute(sql,val)
  data=mycursor.fetchall()
  if data:
     data1=[]
      #result={}
     i=0
     for j in data:

      result={}
        #str1='"{"'+'"SPotAddress":'+tabledata1[i][0]+',"P_City":'+tabledata1[i][1]+',"P_Zipcode":'+str(tabledata1[i][2])+',"spotName":'+tabledata1[i][3]+',"ParkingFeePerHour":'+str(tabledata1[i][4])+'"}"'
      result['SpotName']=j[0]
      result['reserved_from']=j[1]
      result['reserved_to']=j[2]
      result['totalfee']=j[3]
      result['SpotAddress']=j[4]
      result['P_City']=j[5]

        #data1['results'+str(i)]=[result]'''
      data1.append(result)
      i+=1
     jsonData=json.dumps(data1, default = myconverter)
     return redirect(url_for('success3', name=jsonData))
  else:
     return redirect(url_for('success3', name="wrong"))
@app.route('/activity_guest/<uid>', methods=['GET'])
def activity_guest(uid):

  sql= '''select s.spotname,r.reservationstartdatetime as reserved_from,r.reservationenddatetime as reserved_to, totalfee,p.SpotAddress, p.P_City 
          from reservation r join spot_description s on s.sdid=r.sdid 
          join parking_spot p on p.SpotID=s.SpotID
          where r.GUserID= %s'''

  val=(uid,)
  mycursor.execute(sql,val)
  data=mycursor.fetchall()
  if data:
     data1=[]
      #result={}
     i=0
     for j in data:

      result={}
        #str1='"{"'+'"SPotAddress":'+tabledata1[i][0]+',"P_City":'+tabledata1[i][1]+',"P_Zipcode":'+str(tabledata1[i][2])+',"spotName":'+tabledata1[i][3]+',"ParkingFeePerHour":'+str(tabledata1[i][4])+'"}"'
      result['SpotName']=j[0]
      result['reserved_from']=j[1]
      result['reserved_to']=j[2]
      result['totalfee']=j[3]
      result['SpotAddress']=j[4]
      result['P_City']=j[5]
        #data1['results'+str(i)]=[result]'''
      data1.append(result)
      i+=1
     #print(session['userid'])
     jsonData=json.dumps(data1,default = myconverter)
     return redirect(url_for('success3', name=jsonData))
  else:
      return redirect(url_for('success3', name="wrong"))

@app.route('/sessions')
def sessions():
  uid=session['userid']
  return jsonify(userid=uid),200


@app.route('/success3/<name>')
def success3(name):
   dict={}
   if name == 'wrong':
       return jsonify(message='No data found'),400
   else:
       dict['result']=name
       return jsonify(dict),200


@app.route('/spot_availability', methods=['POST'])
def spot_availability():
   details = request.json
   SdID= details['Sdid']
   AvailableStartDateTime= details['AvailableStartDateTime']
   AvailableEndDateTime= details['AvailableEndDateTime']
   AvailableStartDateTime1=parser.parse(AvailableStartDateTime)
   AvailableEndDateTime1=parser.parse(AvailableEndDateTime)
   sql = '''INSERT INTO spot_availability(SdID, AvailableStartDateTime, AvailableEndDateTime) VALUES (%s,%s,%s)'''
   val = (SdID, AvailableStartDateTime1, AvailableEndDateTime1)
   mycursor.execute(sql, val)
   mydb.commit()
   return jsonify(message='success'),200

@app.route('/host_home/<hid>', methods=['GET'])
def host_home(hid):
  
  sql= '''SELECT  s.SdID,s.SpotName, p.SpotAddress, p.P_City, s.ParkingFeePerHour FROM spot_description s join parking_spot p on p.spotid=s.spotid 
          where p.huserid= %s '''

  val=(hid,)
  mycursor.execute(sql,val)
  data=mycursor.fetchall()
  if data:
     data1=[]
      #result={}
     i=0
     for j in data:

      result={}
        #str1='"{"'+'"SPotAddress":'+tabledata1[i][0]+',"P_City":'+tabledata1[i][1]+',"P_Zipcode":'+str(tabledata1[i][2])+',"spotName":'+tabledata1[i][3]+',"ParkingFeePerHour":'+str(tabledata1[i][4])+'"}"'
      result['SdID']=j[0]
      result['SpotName']=j[1]
      result['SpotAddress']=j[2]
      result['P_City']=j[3]
      result['parkingfeeperhour']=j[4]
      
      

        #data1['results'+str(i)]=[result]'''
      data1.append(result)
      i+=1
     jsonData=json.dumps(data1, default = myconverter)
     return redirect(url_for('success3', name=jsonData))
  else:
     return redirect(url_for('success3', name="wrong"))

@app.route('/view_availabilty', methods=['POST'])
def view_availabilty():
  
  details=request.json
  SdID=details['SdID']

  sql= '''select s.SpotName, sa.AvailableStartDateTime, sa.AvailableEndDateTime from spot_availability sa join spot_description s on s.SdID=sa.SdID 
where sa.SdID= %s '''

  val=(SdID,)
  mycursor.execute(sql,val)
  data=mycursor.fetchall()
  if data:
     data1=[]
      #result={}
     i=0
     for j in data:

      result={}
        #str1='"{"'+'"SPotAddress":'+tabledata1[i][0]+',"P_City":'+tabledata1[i][1]+',"P_Zipcode":'+str(tabledata1[i][2])+',"spotName":'+tabledata1[i][3]+',"ParkingFeePerHour":'+str(tabledata1[i][4])+'"}"'
      result['SpotName']=j[0]
      result['AvailableStartDateTime']=j[1]
      result['AvailableEndDateTime']=j[2]      
      

        #data1['results'+str(i)]=[result]'''
      data1.append(result)
      i+=1
     jsonData=json.dumps(data1, default = myconverter)
     return redirect(url_for('success3', name=jsonData))
  else:
     return redirect(url_for('success3', name="wrong"))

if __name__== '__main__':
  app.run()