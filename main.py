"""
scripts to collect information about Japan's stock buyback announcement from the website and create a daily automated email of all stock buyback announcements for the day.
"""
import asyncio
from playwright.async_api import async_playwright
import smtplib
from email.mime.text import MIMEText
from datetime import date

# Set up email parameters
sender_email = "sender@example.com"
receiver_email = "receiver@example.com"
smtp_server = "smtp.example.com"
smtp_port = 587
smtp_username = "username"
smtp_password = "password"

# Set up today's date
today = date.today().strftime("%B %d, %Y")

async def main():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)

        # Create page context
        page = await browser.new_context()

        # Navigate to webpage
        await page.goto("https://tradingeconomics.com/japan/stock-market")
        #await page.get_by_text("https://tradingeconomics.com/japan/stock-market").click()

        # Find buyback announcements
        buybacks = await page.querySelectorAll(".calendar-event-row.buybacks")

        # Create message body
        message_body = f"Stock buyback announcements for {today}:\n\n"
        for buyback in buybacks:
            title = await buyback.querySelector(".calendar-event-title")
            time = await buyback.querySelector(".calendar-event-time")
            message_body += f"{await time.innerText()}: {await title.innerText()}\n"

        # Close browser
        await browser.close()

        # Create email message
        message = MIMEText(message_body)
        message["Subject"] = f"Stock buyback announcements for {today}"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Set up email server and send message
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("Email sent successfully!")

# Run the asyncio event loop
asyncio.get_event_loop().run_until_complete(main())