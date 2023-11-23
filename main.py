import requests
import time
from bs4 import BeautifulSoup as BS
import os
import smtplib
from email.message import EmailMessage


#a function to equire the change percentage from the yahoo finance page
def extract_the_change():
    #def the link to the microsoft stock in yahoo finance
    url = 'https://finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch'

    response = requests.get(url)

    # Parse the HTML content
    soup = BS(response.content, 'html.parser')
    return soup.find('fin-streamer', {'data-field': 'preMarketChangePercent'})

#a function to get the float out of a string
def get_float(num):
    res = ""
    for n in num:
        if(n.isdigit() or n == '.'):
            res = res + n
    return float(res)

#a function to send an email to user
def send_message(change):
    
    email_address = "Test@gmail.com"
    email_password = '*******'

    # create email

    msg = EmailMessage()
    msg['Subject'] = "Stock Update!"
    msg['From'] = email_address
    msg['To'] = "reciever@gmail.com"
    msg.set_content("There has been a change of " + change + "% in the microsoft stock!")

    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


change_element = extract_the_change() 
last_change = change_element.text.strip() if change_element else 'N/A'



#loop forever and get the change and check if the change was great enough to notify user
while(True):
    time.sleep(1)
    change_element = extract_the_change() 
    new_change = change_element.text.strip() if change_element else 'N/A'

    if(abs(get_float(last_change) - get_float(new_change)) > 0.01):
        send_message(str(abs(get_float(last_change) - get_float(new_change))))

    last_change = new_change
