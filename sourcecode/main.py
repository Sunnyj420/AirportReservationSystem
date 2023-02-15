# imported libraries
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors # For database interfaceing
import hashlib # For md5
import re # regex
import random
from datetime import date, datetime, timedelta
from time import strftime

# App initialization
app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config['SECRET_KEY'] = "sbdais83" # random
app.config['APP_HOST'] = "localhost"

# DB Information
app.config['DB_USER'] = "root"
app.config['DB_PASSWORD'] = ""
app.config['APP_DB'] = "airticket_reservation_system"
app.config['CHARSET'] = "utf8mb4"

conn = pymysql.connect(host=app.config['APP_HOST'],
                       user=app.config['DB_USER'],
                       password=app.config['DB_PASSWORD'],
                       db=app.config['APP_DB'],
                       charset=app.config['CHARSET'],
                       cursorclass=pymysql.cursors.DictCursor)

# Helper functions

def validateEmail(email):
  regex = r'\b[a-z0-9]+@[a-z]+\\b'
  return re.fullmatch(regex, email)

def hashPassword(password):
  output = hashlib.md5()
  output.update(password.encode())
  return output.hexdigest()

def validateAuthentication():
  if session.get("email"):  # email address
    return True
  else:                     # username
    return False

# Routes of Application Use Cases
@app.route('/')
def index():
  return render_template("index.html", name="Airline Ticket Reservation System")

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')

@app.route('/customerlogin')
def customerlogin():
  return render_template("customerlogin.html")

@app.route('/stafflogin')
def stafflogin():
  return render_template("stafflogin.html")

@app.route('/customerregister')
def customerregister():
	return render_template('customerregister.html')

@app.route('/staffregister')
def staffregister():
	return render_template('staffregister.html')

@app.route('/roundtripflights')
def roundtripflights():
	return render_template('roundtripflights.html')

@app.route('/onewayflights')
def onewayflights():
	return render_template('onewayflights.html')

@app.route('/flightstatus')
def flightstatus():
	return render_template('flightstatus.html')


#Authentication Methods of Application Use Cases

@app.route('/flightstatusAuth', methods=['GET', 'POST'])
def flightstatusAuth():
  airline = request.form['flightAirline']
  flight_number = request.form['flightNumber']
  departure_date = request.form['departureDate']
  arrival_date = request.form['flightArrivalDate']

  cursor = conn.cursor()

  query = 'SELECT * FROM flight WHERE airline = %s and flight_number = %s \
          and departure_date = %s and arrival_date = %s'
  cursor.execute(query, (airline, flight_number, departure_date, arrival_date))

  #stores the results in a variable
  data1 = cursor.fetchall()
  error = None

  if(data1):
		#If the previous query returns data, then user exists
    error = None
    cursor.close()
    return render_template('flightstatus.html', error = error, data = data1)
  else:
    error = "No matching flights found"
    return render_template('flightstatus.html', error = error)

# Customer Authentication
@app.route('/customerRegisterAuth', methods=['GET', 'POST'])
def customerRegisterAuth():
  #grabs information from the forms
  username = request.form['username']
  password = request.form['password']
  name = request.form['customerName']
  building_num = request.form['buildingNumber']
  street_name = request.form['streetName']
  city = request.form['cityName']
  state = request.form['stateName']
  phone_num = request.form['phoneNumber']
  passport_num = request.form['passportNumber']
  passport_exp = request.form['passportExpire']
  passport_country = request.form['passportCountry']
  birthday = request.form['birthday']

	#cursor used to send queries
  cursor = conn.cursor()

	#executes query
  query = 'SELECT * FROM Customer WHERE email = %s'
  cursor.execute(query, (username))

	#stores the results in a variable
  data = cursor.fetchone()
  error = None

  if(data):
		#If the previous query returns data, then user exists
    error = "This user already exists"
    return render_template('customerregister.html', error = error)

  else:
    ins = 'INSERT INTO Customer VALUES(%s, MD5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(ins, (username, password, name, building_num, street_name, city, \
                        state, phone_num, passport_num, passport_exp, passport_country, birthday))
    conn.commit()
    cursor.close()
    return render_template('index.html')

@app.route('/staffRegisterAuth', methods=['GET', 'POST'])
def staffRegisterAuth():
  #grabs information from the forms
  username = request.form['username']
  password = request.form['password']
  airline = request.form['airlineName']
  first_name = request.form['firstName']
  last_name = request.form['lastName']
  birthday = request.form['birthday']
  email = request.form['staffEmail']
  phone_num = request.form['phoneNumber']
  
	#cursor used to send queries
  cursor = conn.cursor()

	#executes query
  query = 'SELECT * FROM airline_staff WHERE username = %s'
  cursor.execute(query, (username))

	#stores the results in a variable
  data = cursor.fetchone()
  error = None

  if(data):
		#If the previous query returns data, then user exists
    error = "This user already exists"
    return render_template('staffregister.html', error = error)
  else:
    ins = 'INSERT INTO airline_staff VALUES(%s, %s, MD5(%s), %s, %s, %s)'
    ins2 = 'INSERT INTO airline_staff_email VALUES(%s, %s)'
    ins3 = 'INSERT INTO airline_staff_phone_number VALUES(%s, %s)'
    cursor.execute(ins, (username, airline, password, first_name, last_name, birthday))
    cursor.execute(ins2, (username, email))
    cursor.execute(ins3, (username, phone_num))
    conn.commit()
    cursor.close()
    return render_template('index.html')

@app.route('/customerLoginAuth', methods=['GET', 'POST'])
def customerLoginAuth():
  #grabs information from the forms
  username = request.form['email']
  password = request.form['password']

  #cursor used to send queries
  cursor = conn.cursor()

  #executes query
  query = 'SELECT * FROM Customer WHERE email = %s and pass_word = MD5(%s)'
  cursor.execute(query, (username, password))
  data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
  cursor.close()
  error = None
  if(data):
		#creates a session for the the user
		#session is a built in
    session['email'] = username
    return redirect(url_for('index'))
  else:
		#returns an error message to the html page
    error = 'Invalid login or username'
    return render_template('customerlogin.html', error=error)


# Airline Staff login
@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def staffLoginAuth():
  #grabs information from the forms
  username = request.form['username']
  password = request.form['password']

  #cursor used to send queries
  cursor = conn.cursor()

  #executes query
  query = 'SELECT * FROM airline_staff WHERE username = %s and pass_word = MD5(%s)'
  cursor = conn.cursor()
  cursor.execute(query, (username, password))
  data = cursor.fetchone()
  
	#use fetchall() if you are expecting more than 1 data row
  cursor.close()
  error = None
  if(data):
		#creates a session for the the user
		#session is a built in
    session['username'] = username
    return redirect(url_for('index'))
  else:
		#returns an error message to the html page
    error = 'Invalid login or username'
    return render_template('stafflogin.html', error=error)

@app.route('/roundtripflightsAuth', methods=['GET', 'POST'])
def roundtripflightsAuth():
   #grabs information from the forms
  departure_airport = request.form['departureAirport']
  arrival_airport = request.form['arrivalAirport']
  departure_date = request.form['departureDate']
  return_date = request.form['returnDate']

	#cursor used to send queries
  cursor1 = conn.cursor()
  cursor2 = conn.cursor()

	#executes query
  query1 = 'SELECT * FROM Flight WHERE \
          departure_airport = %s and arrival_airport = %s and departure_date = %s'
          
  cursor1.execute(query1, (departure_airport, arrival_airport, departure_date))

  query2 = 'SELECT * FROM Flight WHERE \
          departure_airport = %s and arrival_airport = %s and departure_date = %s' # we flip this
          
  cursor2.execute(query2, (arrival_airport, departure_airport, return_date))

	#stores the results in a variable
  data1 = cursor1.fetchall()
  data2 = cursor2.fetchall()
  #print(data)
  error = None

  if(data1 and data2):
    error = None
    cursor1.close()
    cursor2.close()
    return render_template('roundtripflights.html', error = error, data1 = data1, data2 = data2)

  else:
    error = "No matching flights found"
    return render_template('roundtripflights.html', error = error)


@app.route('/onewayflightsAuth', methods=['GET', 'POST'])
def onewayflightsAuth():
  #grabs information from the forms
  departure_airport = request.form['departureAirport']
  arrival_airport = request.form['arrivalAirport']
  departure_date = request.form['departureDate']

  #cursor used to send queries
  cursor = conn.cursor()

	#executes query

  query = 'SELECT * FROM Flight WHERE \
          departure_airport = %s and arrival_airport = %s and departure_date = %s'
          
  cursor.execute(query, (departure_airport, arrival_airport, departure_date))

	#stores the results in a variable
  data1 = cursor.fetchall()
  error = None

  if(data1):
    error = None
    cursor.close()
    return render_template('onewayflights.html', error = error, data = data1)

  else:
    error = "No matching flights found"
    return render_template('onewayflights.html', error = error)





# Routes of Customer Use Cases

@app.route('/purchaseOneWayTicket', methods=["GET", "POST"])
def purchaseOneWayTicket():
  return render_template("purchaseOneWayTicket.html")

@app.route('/purchaseRoundTripTicket', methods=["GET", "POST"])
def purchaseRoundTripTicket():
  return render_template("purchaseRoundTripTicket.html")

@app.route('/viewTickets')
def viewTickets():
    return render_template('viewTickets.html')

@app.route('/cancelFlight', methods=["GET", "POST"])
def cancelFlight():
    return render_template('cancelFlight.html')

@app.route('/giveRatings', methods=["GET", "POST"])
def giveRatings():
    return render_template('giveRatings.html')

@app.route('/trackSpending', methods=["GET", "POST"])
def trackSpending():
    return render_template('trackSpending.html')


# Authentication Methods of Customer Use Cases

@app.route('/purchaseOneWayTicketAuth', methods=["GET", "POST"])
def purchaseOneWayTicketAuth():
  airline = request.form['flightAirline']
  flight_number = request.form['flightNumber']
  departure_airport = request.form['departureAirport']
  arrival_airport = request.form['arrivalAirport']
  departure_date = request.form['departureDate']
  departure_time = request.form['departureTime']
  card_type = request.form['cardType']
  card_number = request.form['cardNumber']
  card_name = request.form['nameOnCard']
  card_expiration = request.form['cardExpiration']
  c_email = request.form['customerEmail']
  current_date = request.form['currentDate']
  current_time = request.form['currentTime']

  #cursor used to send queries
  cursor1 = conn.cursor()
  cursor2 = conn.cursor()
  cursor3 = conn.cursor()

	#executes query

  query1 = 'SELECT * FROM Flight WHERE airline = %s and flight_number = %s and departure_airport = %s \
          and arrival_airport = %s and departure_date = %s and departure_time = %s'
          
  cursor1.execute(query1, (airline, flight_number, departure_airport, arrival_airport, departure_date, departure_time))

	#stores the results in a variable
  data1 = cursor1.fetchone()

  if (not data1):
      error = "No matching flights found"
      return render_template("purchaseOneWayTicket.html", error = error)

  elif data1["seatCapacity"] == 0:
    error = "No more seats left on this flight"
    return render_template("purchaseOneWayTicket.html", error = error)

  else:
    num_seats = data1["seatCapacity"] - 1

    query3 = 'UPDATE Flight SET seatCapacity = %s WHERE airline = %s and flight_number = %s \
              and departure_date = %s and departure_time = %s'
           
    cursor3.execute(query3, (num_seats, data1['airline'], data1['flight_number'], \
                    data1['departure_date'], data1['departure_time']))
    
    t_id = random.randrange(0,10000)
    flight_number = data1['flight_number']
    base_price = data1['base_price']

    query2 = 'INSERT INTO Ticket VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            
    cursor2.execute(query2, (t_id, airline, flight_number, departure_date, departure_time, c_email, base_price, card_type,\
                            card_number, card_name, card_expiration, current_date, current_time))
                            
    error = None

    cursor1.close()
    cursor2.close()
    cursor3.close()
    return render_template("purchaseOneWayTicket.html")


@app.route('/purchaseRoundTripTicketAuth', methods=["GET", "POST"])
def purchaseRoundTripTicketAuth():
  airline = request.form['flightAirline']
  flight_number = request.form['flightNumber']
  departure_airport = request.form['departureAirport']
  arrival_airport = request.form['arrivalAirport']
  departure_date = request.form['departureDate']
  departure_time = request.form['departureTime']
  flight_number2 = request.form['flightNumber2']
  return_date = request.form['returnDate']
  return_time = request.form['returnTime']
  card_type = request.form['cardType']
  card_number = request.form['cardNumber']
  card_name = request.form['nameOnCard']
  card_expiration = request.form['cardExpiration']
  c_email = request.form['customerEmail']
  current_date = request.form['currentDate']
  current_time = request.form['currentTime']

  #cursor used to send queries
  cursor1 = conn.cursor()
  cursor2 = conn.cursor()
  cursor3 = conn.cursor()
  cursor4 = conn.cursor()
  cursor5 = conn.cursor()
  cursor6 = conn.cursor()

	#executes query

  query1 = 'SELECT * FROM Flight WHERE airline = %s and departure_airport = %s \
          and arrival_airport = %s and flight_number = %s and departure_date = %s and departure_time = %s'
          
  cursor1.execute(query1, (airline, departure_airport, arrival_airport, flight_number, departure_date, departure_time))

	#stores the results in a variable
  data1 = cursor1.fetchone()

  # flipping the arrival/departure airport for round trip
  query2 = 'SELECT * FROM Flight WHERE airline = %s and departure_airport = %s \
            and arrival_airport = %s and flight_number = %s and departure_date = %s and departure_time = %s' 
          
  cursor2.execute(query2, (airline, arrival_airport, departure_airport, flight_number2, return_date, return_time))

  data2 = cursor2.fetchone()

  if (not data1 and not data2):
    error = "No matching round trip tickets found"
    return render_template('purchaseRoundTripTicket.html', error = error)
  
  elif data1["seatCapacity"] == 0:
    error = "No more seats left on this departing flight"
    return render_template("purchaseRoundTripTicket.html", error = error)
  
  elif data2["seatCapacity"] == 0:
    error = "No more seats left on this returning flight"
    return render_template("purchaseRoundTripTicket.html", error = error)
  
  else:
    num_seats = data1["seatCapacity"] - 1

    query5 = 'UPDATE Flight SET seatCapacity = %s WHERE airline = %s and flight_number = %s \
              and departure_date = %s and departure_time = %s'
           
    cursor5.execute(query5, (num_seats, data1['airline'], data1['flight_number'], \
                    data1['departure_date'], data1['departure_time']))

    num_seats = data2["seatCapacity"] - 1

    query6 = 'UPDATE Flight SET seatCapacity = %s WHERE airline = %s and flight_number = %s \
              and departure_date = %s and departure_time = %s'
           
    cursor6.execute(query6, (num_seats, data2['airline'], data2['flight_number'], \
                    data2['departure_date'], data2['departure_time']))

    t_id = random.randrange(0,10000)
    base_price = data1['base_price']
    
    t_id2 = random.randrange(0,10000)
    base_price2 = data2['base_price']

    query3 = 'INSERT INTO Ticket VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            
    cursor3.execute(query3, (t_id2, airline, flight_number2, return_date, return_time, c_email, base_price2, card_type,\
                            card_number, card_name, card_expiration, current_date, current_time))

    query4 = 'INSERT INTO Ticket VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            
    cursor4.execute(query4, (t_id, airline, flight_number, departure_date, departure_time, c_email, base_price, card_type,\
                            card_number, card_name, card_expiration, current_date, current_time))
                            
    error = None

    cursor1.close()
    cursor2.close()
    cursor3.close()
    cursor4.close()
    cursor5.close()
    cursor6.close()
    return render_template("purchaseRoundTripTicket.html")

@app.route('/viewTicketsAuth', methods=["GET", "POST"])
def viewTicketsAuth():
  email = request.form['email']   
  cursor = conn.cursor()
  curr_date = date.today()
  curr_time = datetime.now().strftime('%H:%M:%S')

  query = 'SELECT * FROM Ticket WHERE IF (departure_date >= %s, 1 , departure_time >= %s) and c_email = %s'
  cursor.execute(query, (curr_date, curr_time, email))
  data1 = cursor.fetchall()

  if(data1):
    cursor.close()
    return render_template('viewTickets.html', data = data1)
  else:
    error = "No future flights"
    return render_template('viewTickets.html', error = error)


@app.route('/cancelFlightAuth', methods=["GET", "POST"])
def cancelFlightAuth():
  t_id = request.form['ticketID']

  cursor1 = conn.cursor()
  cursor2 = conn.cursor()
  cursor3 = conn.cursor()
  cursor4 = conn.cursor()
  cursor5 = conn.cursor()
  curr_date = date.today()

  query1 = 'SELECT * FROM Ticket WHERE t_id = %s'
  cursor1.execute(query1, t_id)
  data = cursor1.fetchone()

  airline = data['airline']
  flight_number = data['flight_number']
  departure_date = data['departure_date']
  departure_time = data['departure_time']
  
  if (not data):
    error = "Invalid Ticket ID"
    return render_template('cancelFlight.html', error = error)

  time_diff = (data['departure_date'] - curr_date).days

  query2 = 'SELECT * FROM Ticket WHERE (t_id = %s and %s >= 1)'
  cursor2.execute(query2, (t_id, time_diff))

  #stores the results in a variable
  data1 = cursor2.fetchall()
  error = None

  if(data1):
		#If the previous query returns data, then user exists
    error = None
    cursor1.close()
    cursor2.close()
    
    query4 = 'SELECT seatCapacity from Flight WHERE airline = %s and flight_number = %s and \
              departure_date = %s and departure_time = %s'
    cursor4.execute(query4, (airline, flight_number, departure_date, departure_time))
    data4 = cursor4.fetchone()
    num_seats = data4['seatCapacity'] + 1

    query5 = 'UPDATE Flight SET seatCapacity = %s WHERE airline = %s and flight_number = %s \
              and departure_date = %s and departure_time = %s'
           
    cursor5.execute(query5, (num_seats, airline, flight_number, \
                    departure_date, departure_time))

    query3 = 'DELETE FROM Ticket WHERE (t_id = %s and %s >= 1)'
    cursor3.execute(query3, (t_id, time_diff))
    cursor3.close()
    cursor4.close()
    cursor5.close()

    return render_template('cancelFlight.html', error = error)
    
  else:
    error = "Cannot cancel flight within 24 hours"
    return render_template('cancelFlight.html', error = error)

@app.route('/giveRatingsAuth', methods=["GET", "POST"])
def giveRatingsAuth():
  t_id = request.form['ticketID']
  email = request.form['customerEmail']
  rating = request.form['rating']
  comment = request.form['comments']
  cursor1 = conn.cursor()
  cursor2 = conn.cursor()
  cursor3 = conn.cursor()
  cursor4 = conn.cursor()
  curr_date = date.today()
  # curr_time = datetime.timestamp(datetime.now())

  query1 = 'SELECT * FROM Ticket WHERE t_id = %s'
  cursor1.execute(query1, (t_id))
  departure_info = cursor1.fetchone()
  flight_num = departure_info['flight_number']
  departure_date = departure_info['departure_date']
  departure_time = departure_info['departure_time']
  
  #Seeing if Ticket ID is valid
  if (not departure_info):
    error = "Invalid Ticket ID"
    return render_template('giveRatings.html', error = error)
  
  date_diff = departure_date - curr_date
  #time_diff = datetime.time(departure_time) - curr_time

  query2 = 'SELECT * FROM Ticket WHERE (t_id = %s and %s <= 0)'
  cursor2.execute(query2, (t_id, date_diff))
  data1 = cursor2.fetchone()

  error = None
  
  #Insert rating if flight time is valid
  if(data1):
		#If the previous query returns data, then user exists
    cursor1.close()
    cursor2.close()

    query3 = 'INSERT into Rates VALUES (%s, %s, %s, %s, %s, %s)'
    cursor3.execute(query3, (flight_num, departure_date, departure_time, email, rating, comment))
    cursor3.close()

    query4 = 'SELECT flight_number, rating, comments FROM Rates WHERE flight_number = %s \
              and departure_date = %s and departure_time = %s and email = %s' 
    cursor4.execute(query4, (flight_num, departure_date, departure_time, email))
    data2 = cursor4.fetchall()
    cursor4.close()

    return render_template('giveRatings.html', data = data2)
  else:
    error = "Cannot give a rating to this flight at this time"
    return render_template('giveRatings.html', error = error)

@app.route('/trackSpendingAuth', methods=["GET", "POST"])
def trackSpendingAuth():
  email = request.form['customerEmail']
  email2 = request.form['customerEmail2']
  startDate = request.form['startDate']
  endDate = request.form['endDate']
  current_date = date.today()

  cursor1 = conn.cursor()
  cursor2 = conn.cursor()
  cursor3 = conn.cursor()
  cursor4 = conn.cursor()
  
  query1 = 'SELECT t_id, sold_price FROM Ticket WHERE c_email = %s and (%s - curr_date) <= 4450'
  cursor1.execute(query1, (email, current_date))
  data1 = cursor1.fetchall()
  query3 = 'SELECT SUM(sold_price) as total_sum FROM Ticket WHERE c_email = %s and (%s - curr_date) <= 4450'
  cursor3.execute(query3, (email, current_date))
  data3 = cursor3.fetchall()
  cursor1.close()
  cursor3.close()
  
  if (data1 and data3):
    return render_template('trackSpending.html', data1 = data1, data3 = data3)
  
  
  if ((startDate and not endDate) or (endDate and not startDate)):
    error = "Invaild date range"
    return render_template('trackSpending.html', error = error)
    
  else:
    query2 = 'SELECT t_id, sold_price FROM Ticket WHERE c_email = %s and curr_date >= %s \
              and curr_date <= %s'
    cursor2.execute(query2, (email2, startDate, endDate))
    data2 = cursor2.fetchall()

    query4 = 'SELECT SUM(sold_price) as total_sum FROM Ticket WHERE c_email = %s and \
              (curr_date >= %s and curr_date <= %s)'
    cursor4.execute(query4, (email2, startDate, endDate))
    data4 = cursor4.fetchall()

    if (data2 and data4):
      return render_template('trackSpending.html', data2 = data2, data4 = data4)
      
    else:
      error = 'No flights purchased during this time period'
      return render_template('trackSpending.html', error = error)
    

  
  

# Routes of Airline Staff Use Cases

@app.route('/viewFlightsStaff', methods=["GET", "POST"])
def viewFlightsStaff():
  return render_template("viewFlightsStaff.html")

@app.route('/createFlight', methods=["GET", "POST"])
def createFlight():
  return render_template("createFlight.html")

@app.route('/changeStatus', methods=["GET", "POST"])
def changeStatus(): 
  return render_template("changeStatus.html")

@app.route('/createAirplane', methods=["GET", "POST"])
def createAirplane():
  return render_template("createAirplane.html")

@app.route('/createAirport', methods=["GET", "POST"])
def createAirport():
  return render_template("createAirport.html")

@app.route('/viewRatings', methods=["GET", "POST"])
def viewRatings():
  return render_template("viewRatings.html")

@app.route('/viewFrequentCustomer', methods=["GET", "POST"])
def viewFrequentCustomer():
  return render_template("viewFrequentCustomer.html")

@app.route('/viewReport', methods=["GET", "POST"])
def viewReport():
  return render_template("viewReport.html")

@app.route('/viewRevenue', methods=["GET", "POST"])
def viewRevenue():
  return render_template("viewRevenue.html")

@app.route('/addPhoneNumber', methods=["GET", "POST"])
def addPhoneNumber():
  return render_template("addPhoneNumber.html")
  
# Authentication Methods of Airline Staff Use Cases

@app.route('/viewFlightsStaffAuth', methods=["GET", "POST"])
def viewFlightsStaffAuth():
  airline = request.form['airline']
  airline2 = request.form['flightAirline']
  startDate = request.form['startDate']
  endDate = request.form['endDate']
  source_airport = request.form['sourceAirport']
  dest_airport = request.form['destinationAirport']
  flight_number = request.form['flightNumber']
  curr_date = date.today()
  
  cursor1 = conn.cursor()
  cursor2 = conn.cursor()
  cursor3 = conn.cursor()
  
  one_month_later = curr_date + timedelta(days=30)

  #Default 30 days
  query1 = 'SELECT * FROM Flight WHERE airline = %s and departure_date <= %s \
            and departure_date >= %s'
  cursor1.execute(query1, (airline, one_month_later, curr_date))
  data1 = cursor1.fetchall()

  if (airline):
    if (data1):
      error1 = None
      cursor1.close()
      return render_template('viewFlightsStaff.html', data1 = data1)

    else:
      error1 = "No flights found within the next 30 days"
      return render_template('viewFlightsStaff.html', error1 = error1)

  if (airline2):
    if ((startDate and not endDate) or (endDate and not startDate)):
      error1 = "Invaild date range"
      return render_template('viewFlightsStaff.html', error1 = error1)

    query2 = 'SELECT * FROM Flight WHERE airline = %s and departure_date <= %s \
              and departure_date >= %s and departure_airport = %s and arrival_airport = %s'
    cursor2.execute(query2, (airline2, endDate, startDate, source_airport, dest_airport))
    data2 = cursor2.fetchall()
    
    if (data2):
      error2 = None
      cursor2.close()
      return render_template('viewFlightsStaff.html', data2 = data2)

    else:
      error2 = "No flights found within the specified range"
      return render_template('viewFlightsStaff.html', error2 = error2)
  
  if (flight_number):
    query3 = 'SELECT c_email FROM Flight NATURAL JOIN Ticket WHERE flight_number = %s'
    cursor3.execute(query3, flight_number)
    data3 = cursor3.fetchall()

    if (data3):
      error3 = None
      cursor3.close()
      return render_template('viewFlightsStaff.html', data3 = data3)
    else:
      error3 = "Flight Not Found"
      return render_template('viewFlightsStaff.html', error3 = error3)

@app.route('/createFlightAuth', methods=["GET", "POST"])
def createFlightAuth():
  staff_airline = request.form['staffAirline']
  airline = request.form['airline']
  flight_number = request.form['flightNumber']
  departure_airport = request.form['departureAirport']
  departure_date = request.form['departureDate']
  departure_time = request.form['departureTime']
  arrival_airport = request.form['arrivalAirport']
  arrival_date = request.form['arrivalDate']
  arrival_time = request.form['arrivalTime']
  base_price = request.form['basePrice']
  airplane_id= request.form['airplane_ID']
  flight_status= request.form['flightStatus']

  error = None
  cursor = conn.cursor()

  if (staff_airline == airline):
    query = 'INSERT INTO Flight VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, (SELECT num_of_seats FROM Airplane WHERE airplane_id = %s))'
    cursor.execute(query, (airline, flight_number, departure_airport, departure_date, departure_time, arrival_airport, \
                          arrival_date, arrival_time, base_price, airplane_id, flight_status, airplane_id))
    cursor.close()
    return render_template("createFlight.html")
  else:
    error = "Unauthorized User: Cannot Add a Flight"
    return render_template("createFlight.html", error = error)

@app.route('/changeStatusAuth', methods=["GET", "POST"])
def changeStatusAuth():
  staff_airline = request.form['staffAirline']
  airline = request.form['airline']
  flight_number = request.form['flightNumber']
  departure_date = request.form['departureDate']
  departure_time = request.form['departureTime']
  flight_status= request.form['flightStatus']

  error = None
  cursor = conn.cursor()

  if (staff_airline == airline):
    query = 'UPDATE Flight SET flight_status = %s WHERE airline = %s and \
            flight_number = %s and departure_date = %s and departure_time = %s'
    cursor.execute(query, (flight_status, airline, flight_number, departure_date, departure_time))
    cursor.close()
    return render_template("changeStatus.html")
  else:
    error = "Unauthorized User: Cannot Change Flight Status"
    return render_template("changeStatus.html", error = error)

@app.route('/createAirplaneAuth', methods=["GET", "POST"])
def createAirplaneAuth():
  staff_airline = request.form['staffAirline']
  airline = request.form['airline']
  airplane_id = request.form['airplaneID']
  num_of_seats = request.form['numOfSeats']
  manufacturing_company = request.form['manufacturingCompany']
  age = request.form['age']
  
  cursor = conn.cursor()
  if (staff_airline == airline):
    query = 'INSERT INTO Airplane VALUES (%s, %s, %s, %s, %s)'
    cursor.execute(query, (airline, airplane_id, num_of_seats, manufacturing_company, age))
    cursor.close()
    return render_template("createAirplane.html")
  else:
    error = "Unauthorized User: Cannot Add a Airplane"
    return render_template("createAirplane.html", error = error)

@app.route('/createAirportAuth', methods=["GET", "POST"])
def createAirportAuth():
  name = request.form['nameAirport']
  city = request.form['cityAirport']
  country = request.form['countryAirport']
  type = request.form['typeAirport']

  cursor = conn.cursor()
  cursor2 = conn.cursor()

  query2 = 'SELECT * FROM Airport WHERE name = %s'  
  cursor2.execute(query2, (name))
  data = cursor2.fetchone()

  if(data):
    error = "Airport already exists"
    return render_template("createAirport.html", error = error)
  
  else:
    query = 'INSERT INTO Airport VALUES (%s, %s, %s, %s)'
    cursor.execute(query, (name, city, country, type))
    cursor.close()
    cursor2.close()
    return render_template("createAirport.html")

@app.route('/viewRatingAuth', methods=["GET", "POST"])
def viewRatingsAuth():
  flight_number = request.form['flightNumber']
  departure_date = request.form['departureDate']
  departure_time = request.form['departureTime']

  cursor1 = conn.cursor()
  cursor2 = conn.cursor()
  error = None

  query1 = 'SELECT email, rating, comments FROM Rates WHERE flight_number = %s and \
          departure_date = %s and departure_time = %s'
  cursor1.execute(query1, (flight_number, departure_date, departure_time))
  data1 = cursor1.fetchall()

  query2 = 'SELECT flight_number, AVG(rating) as avg_rating FROM Rates WHERE flight_number = %s and \
          departure_date = %s and departure_time = %s'
  cursor2.execute(query2, (flight_number, departure_date, departure_time))
  data2 = cursor2.fetchall()

  if (data1 and data2):
    cursor1.close()
    cursor2.close()
    return render_template('viewRatings.html', data1 = data1, data2 = data2)
  else:
    error = "Invalid flight number entered"
    return render_template('viewRatings.html', error = error)

@app.route('/viewFrequentCustomerAuth', methods=["GET", "POST"])
def viewFrequentCustomerAuth():
  airline = request.form['airline']
  airline2 = request.form['airline2']
  customer = request.form['customer']
  cursor1 = conn.cursor()
  cursor2 = conn.cursor()
  curr_date = datetime.today()
  past_year = datetime.today()-timedelta(days=365)
  error = None
  
  if (airline):

    query1 = 'SELECT a.* from (SELECT c_email, COUNT(c_email) as flight_occurance FROM ticket WHERE curr_date >= %s and curr_date <= %s and airline = %s GROUP BY c_email) a WHERE flight_occurance in (SELECT MAX(flight_occurance) FROM (SELECT c_email, COUNT(c_email) as flight_occurance FROM Ticket WHERE curr_date >= %s and curr_date <= %s and airline = %s GROUP BY c_email) a)'
    cursor1.execute(query1, (past_year, curr_date, airline, past_year, curr_date, airline))
    data1 = cursor1.fetchall()

    if (data1):
      cursor1.close()
      return render_template('viewFrequentCustomer.html', data1=data1)
    else:
      error = 'No purchased ticket from the past year'
      return render_template('viewFrequentCustomer.html', error=error)
  
  if (airline2):
    query2 = 'SELECT * FROM ticket WHERE c_email = %s and airline = %s'
    cursor2.execute(query2, (customer, airline2))

    data2 = cursor2.fetchall()
    
    if (data2):
      cursor2.close()
      return render_template('viewFrequentCustomer.html', data2=data2)
    else:
      error = 'Customer Not Found'
      return render_template('viewFrequentCustomer.html', error=error)

@app.route('/viewReportAuth', methods=["GET", "POST"])
def viewReportAuth():
  startDate = request.form['startDate']
  endDate = request.form['endDate']
  
  cursor1 = conn.cursor()
  cursor2 = conn.cursor()
  error=None

  query1 = 'SELECT COUNT(t_id) as num_tickets from Ticket WHERE curr_date >= %s \
            and curr_date <= %s'
  cursor1.execute(query1, (startDate, endDate))
  data1 = cursor1.fetchall()
  
  query2 = 'SELECT month(curr_date) AS month, COUNT(t_id) as num_ticket from Ticket WHERE curr_date >= %s \
            and curr_date <= %s GROUP BY month(curr_date)'
  cursor2.execute(query2, (startDate, endDate))
  data2 = cursor2.fetchall()


  if (data1 and data2):
    cursor1.close()
    cursor2.close()
    return render_template('viewReport.html', data1 = data1, data2 = data2)
  else:
    error = "Invalid range of dates entered"
    return render_template('viewReport.html', error=error)

@app.route('/viewRevenueAuth', methods=["GET", "POST"])
def viewRevenueAuth():
  curr_date = datetime.today()
  past_year = datetime.today()-timedelta(days=365)
  past_month = datetime.today()-timedelta(days=30)

  cursor1 = conn.cursor()
  cursor2 = conn.cursor()
  
  query1 = 'SELECT SUM(sold_price) as Total_Revenue_Past_Year \
            FROM Ticket WHERE curr_date >= %s and curr_date <= %s'

  cursor1.execute(query1, (past_year, curr_date))
  data1 = cursor1.fetchall()

  query2 = 'SELECT SUM(sold_price) as Total_Revenue_Past_Month \
            FROM Ticket WHERE curr_date >= %s and curr_date <= %s'\

  cursor2.execute(query2, (past_month, curr_date))
  data2 = cursor2.fetchall()

  if (data2):
    cursor1.close()
    cursor2.close()
    
    return render_template('viewRevenue.html', data1 = data1, data2 = data2)
  
  else:
    error = 'No tickets sold'
    return render_template('viewRevenue.html', error = error)

@app.route('/addPhoneNumberAuth', methods=["GET", "POST"])
def addPhoneNumberAuth():
  username = request.form['username']
  phone_num = request.form['phone_number']

  cursor1 = conn.cursor()
  cursor2 = conn.cursor()

  query1 = 'SELECT * from airline_staff_phone_number where phone_number = %s'
  cursor1.execute(query1, (phone_num))
  data1 = cursor1.fetchall()
  
  if (data1):
    error = 'This phone number already exists'
    return render_template('addPhoneNumber.html', error = error)
  else:
    query2 = 'INSERT INTO airline_staff_phone_number VALUES(%s, %s)'
    cursor2.execute(query2, (username, phone_num))
    return render_template('addPhoneNumber.html')
  

# 127.0.0.1 is the equivalent of localhost
# Port 3000 can be any port
if __name__ == "__main__":
  app.run("127.0.0.1", 3000, debug = True)