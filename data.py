import sqlite3

db_path:('/home/beyondvelocity/beyondvelocity161/bv.db')

# Connect to a database
def connect_db(path):
    conn = sqlite3.connect(path)
    # Converts tuples into dictionary
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())

# Insert New Account Data to DB
def insert_account(account_data):
    conn, cur = connect_db('db_path')
    query = 'INSERT INTO accounts (email, password, type) VALUES (?,?,?)'
    values = (account_data['email'],
              account_data['password'],
              account_data['type'])
    cur.execute(query, values)
    conn.commit()
    conn.close()

# Checks if login credentials exist in the Database
def login_account(email, password):
    conn, cur = connect_db('db_path')
    query = 'SELECT *  FROM accounts WHERE email=? AND password=?'
    result = cur.execute(query, (email, password))
    row = cur.fetchone()
    conn.close()
    if row:
        return row
    else:
        return False

# Checks if provided email is in the database
def check_dupe(email):
    conn, cur = connect_db('db_path')
    query = 'SELECT *  FROM accounts WHERE email=?'
    result = cur.execute(query, (email,))
    row = cur.fetchone()
    conn.close()
    if row:
        return False
    else:
        return True

# Input an application based on the email
def check_application(email):
    conn, cur = connect_db('db_path')
    query = 'SELECT *  FROM applications WHERE email=?'
    results = cur.execute(query, (email,)).fetchone()
    conn.close()
    if results:
        return results
    else:
        return False

# Input an application based on the id
def read_app_by_id(appid):
    conn, cur = connect_db('db_path')
    query = 'SELECT * FROM applications WHERE id=?'
    results = cur.execute(query, (appid,)).fetchone()
    conn.close()
    return results

# Insert New Application Data to Database
def insert_application(app_data):
    conn, cur = connect_db('db_path')
    query = 'INSERT INTO applications (firstname, lastname, sex, civil, birthdate, birthplace, age, citizenship, religion, mobile, street1, street2, city, state, country, url, apptype, advocacy, email) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    values = (app_data['firstname'],
              app_data['lastname'],
              app_data['sex'],
              app_data['civil'],
              app_data['birthdate'],
              app_data['birthplace'],
              app_data['age'],
              app_data['citizenship'],
              app_data['religion'],
              app_data['mobile'],
              app_data['street1'],
              app_data['street2'],
              app_data['city'],
              app_data['state'],
              app_data['country'],
              app_data['url'],
              app_data['apptype'],
              app_data['advocacy'],
              app_data['email']
              )
    cur.execute(query,values)
    conn.commit()
    conn.close()

# all applications data
def retreive_masterlist():
    conn, cur = connect_db('db_path')
    query = 'SELECT * FROM applications'
    results = cur.execute(query).fetchall()
    conn.close()
    return results

# Delete an application
def delete_application(email):
    conn, cur = connect_db('db_path')
    query = 'DELETE FROM applications WHERE email=?'
    cur.execute(query, (email,))
    conn.commit()
    conn.close()

# Update application data
def update_application(app_data):
    conn, cur = connect_db('db_path')
    query = 'UPDATE applications SET firstname=?, lastname=?, sex=?, civil=?, birthdate=?, birthplace=?, age=?, citizenship=?, religion=?,  mobile=?, street1=?, street2=?, city=?, state=?, country=?, url=?, apptype=?, advocacy=?, WHERE email=?'
    values = (app_data['firstname'],
              app_data['lastname'],
              app_data['sex'],
              app_data['civil'],
              app_data['birthdate'],
              app_data['birthplace'],
              app_data['age'],
              app_data['citizenship'],
              app_data['religion'],
              app_data['mobile'],
              app_data['street1'],
              app_data['street2'],
              app_data['city'],
              app_data['state'],
              app_data['country'],
              app_data['url'],
              app_data['apptype'],
              app_data['advocacy'],
              app_data['email']
              )
    cur.execute(query, values)
    conn.commit()
    conn.close()

# Match searches based on query
def field_search(field, search):
    conn, cur = connect_db('db_path')
    if field == 'firstname':
        query = 'SELECT * FROM applications WHERE firstname=?'
    elif field == 'lastname':
        query = 'SELECT * FROM applications WHERE lastname=?'
    elif field == 'sex':
        query = 'SELECT * FROM applications WHERE sex=?'
    elif field == 'civil':
        query = 'SELECT * FROM applications WHERE civil=?'
    elif field == 'birthdate':
        query = 'SELECT * FROM applications WHERE birthdate=?'
    elif field == 'birthplace':
        query = 'SELECT * FROM applications WHERE birthplace=?'
    elif field == 'age':
        query = 'SELECT * FROM applications WHERE age=?'
    elif field == 'citizenship':
        query = 'SELECT * FROM applications WHERE citizenship=?'
    elif field == 'religion':
        query = 'SELECT * FROM applications WHERE religion=?'
    elif field == 'mobile':
        query = 'SELECT * FROM applications WHERE mobile=?'
    elif field == 'city':
        query = 'SELECT * FROM applications WHERE city=?'
    elif field == 'state':
        query = 'SELECT * FROM applications WHERE state=?'
    elif field == 'country':
        query = 'SELECT * FROM applications WHERE country=?'
    elif field == 'apptype':
        query = 'SELECT * FROM applications WHERE apptype=?'
    elif field == 'advocacy':
        query = 'SELECT * FROM applications WHERE advocacy=?'
    elif field == 'email':
        query = 'SELECT * FROM applications WHERE email=?'
    results = cur.execute(query, (search,)).fetchall()
    conn.close()
    if results:
        return results
    else:
        return False
