import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time

# Function to get stock news from a website
def get_stock_news():
    urls = [
        "https://in.finance.yahoo.com",
        "https://www.moneycontrol.com",
        "https://economictimes.indiatimes.com"
    ]
    news_data = []
    
    # Scraping each URL
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example for scraping headlines (this will vary based on the site)
        headlines = soup.find_all('h3', class_='Mb(5px)')  # Adjust based on the site layout
        for headline in headlines:
            news_data.append(headline.get_text())
    
    return "\n".join(news_data)

# Function to send the email
def send_email(news_content):
    from_email = "raul.ranar@gmail.com"
    to_email = "raul.ranar@gmail.com"
    password = "$@ndesh@1"  # Use an app-specific password if using Gmail or similar
    
    subject = "Stock News for Today"
    body = f"Here are the latest stock updates for India:\n\n{news_content}"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # Setting up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)  # For Gmail, use 587
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

# Function to be run daily
def daily_task():
    news_content = get_stock_news()
    send_email(news_content)

# Scheduling the task to run at 7 AM every day
schedule.every().day.at("07:00").do(daily_task)

# Keeping the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # wait for 1 minute
