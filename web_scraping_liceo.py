import requests
from bs4 import BeautifulSoup
import smtplib, ssl
import time

#setup mail:
port = 465 #per SSL
password = 'password_account_mailbot'
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("mail_bot", password)

sender_email = "mail_bot"
receiver = "mail_ricevente"

#indirizzo url
url = "https://www.liceogallarate.edu.it/circolari/"

#invio una HTTP request all'url della pagina
#come risposta ottengo il contenuto HTML di questa.
page = requests.get(url)

#controllo 200=OK ; 404 = Not Found
if page.status_code == 200:
    print('OK')
elif page.status_code  == 404:
    print('404 Error! Not Found')

#creazione dizionario circolari
d = {}

#lettura file e scrittura dizionario
hand= open("Circolari.txt")
for line in hand:
    pos = line.find('http')
    d[line[:pos-1]] = line[pos:]
    
#apertura file/database
file = open("Circolari.txt", "a")

#inizio web scraping    
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id = "post-7385")#cerco id con tutte le circolari

circolari = results.find('div', class_ = "post-content entry-content")
circ_elems = circolari.find_all('a', href=True)
for circ_elem in circ_elems:
    if circ_elem.text.strip() not in d:
        d[circ_elem.text.strip()] = circ_elem['href']
        print("circolare nuova")
        #mandare mail notifica alla persona
        message = circ_elem.text.strip() + "\n" + circ_elem['href']
        server.sendmail(sender_email, receiver, message)
        #scrittura su file
        file.write(circ_elem.text.strip())
        file.write(" ")
        file.write(circ_elem['href'])
        file.write("\n")

file.close()
time.sleep(10800)
#print(d)
