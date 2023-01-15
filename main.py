import gsmmodem
import mysql.connector

# Connect to the GSM modem
modem = gsmmodem.GsmModem('/dev/ttyUSB0')
modem.connect()

# Connect to the MySQL database
conn = mysql.connector.connect(user='root', password='', host='localhost', database='sms_enabler')
cursor = conn.cursor()

# Create the table to store the messages
cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                  (id INT AUTO_INCREMENT, sender VARCHAR(255), message TEXT, PRIMARY KEY (id))''')

# Wait for an incoming SMS message
message = modem.waitForSms(10)

# Extract the sender and message text
sender = message.number
text = message.text

# Insert the message into the database
cursor.execute("INSERT INTO messages (sender, message) VALUES (%s, %s)", (sender, text))
conn.commit()

# Close the connections
modem.close()
cursor.close()
conn.close()