import time
import gsmmodem
import mysql.connector

# Connect to the GSM modem
modem = gsmmodem.GsmModem('/dev/ttyUSB2')
modem.connect()

# Connect to the MySQL database
conn = mysql.connector.connect(user='root', password='', host='localhost', database='sms_enabler')
cursor = conn.cursor()

# Create the table to store the messages
cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                  (id INT AUTO_INCREMENT, sender VARCHAR(255), message TEXT, PRIMARY KEY (id))''')

# Initialize an empty list to store incoming SMS messages
messages = []


# Define a function to handle incoming SMS messages
def handleSms(sms):
    print(sms)
    messages.append(sms)


# Register the function to handle incoming SMS messages
modem.smsReceivedCallback = handleSms

# Wait for 10 seconds for an incoming SMS message
time.sleep(10)

# Check if any SMS messages were received
if messages:
    for message in messages:
        print(message)
        # Extract the sender and message text
        sender = message.number
        text = message.text

        # Insert the message into the database
        cursor.execute("INSERT INTO messages (sender, message) VALUES (%s, %s)", (sender, text))
        conn.commit()
else:
    print("No SMS messages received.")

# Close the connections
modem.close()
cursor.close()
conn.close()

# # Wait for an incoming SMS message
# message = modem.waitForSms(10)
# message = modem.listStoredSms()

# for m in message:
#     # Print the message
#     if m.number == "Super Deal":
#         print(m.text)
#         cursor.execute("INSERT INTO messages (sender, message) VALUES (%s, %s)", (m.number, m.text))

#     # Send the message to the database
#     # cursor.execute('''INSERT INTO messages (sender, message) VALUES (%s, %s)''', (m[0], m[1]))
#         conn.commit()
# conn.close()
