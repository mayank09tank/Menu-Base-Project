import pywhatkit as kit
import time
from twilio.rest import Client

# Twilio credentials
account_sid = 'Enter twilio sid'
auth_token = 'Enter twilio suth token'
twilio_phone_number = 'Enter twilio number'

client = Client(account_sid, auth_token)

def send_whatsapp_message(to, message, hour, minute):
    kit.sendwhatmsg(to, message, hour, minute)
    print(f"WhatsApp message scheduled to {to} at {hour}:{minute}")

def send_sms_message(to, message):
    message = client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=to
    )
    print(f"SMS message sent to {to}")

def make_phone_call(to):
    call = client.calls.create(
        twiml='<Response><Say>This is a test call from Twilio. Have a great day!</Say></Response>',
        from_=twilio_phone_number,
        to=to
    )
    print(f"Phone call initiated to {to}")

def main():
    while True:
        print("\nMenu:")
        print("1. Send WhatsApp message")
        print("2. Send SMS message")
        print("3. Make a Phone Call")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            to = input("Enter WhatsApp number (with country code, e.g., +1234567890): ")
            message = input("Enter your message: ")
            current_time = time.localtime()
            hour = int(input(f"Enter hour (24-hour format, current hour is {current_time.tm_hour}): "))
            minute = int(input(f"Enter minute (current minute is {current_time.tm_min}): "))
            send_whatsapp_message(to, message, hour, minute)
        elif choice == '2':
            to = input("Enter phone number (with country code, e.g., +1234567890): ")
            message = input("Enter your message: ")
            send_sms_message(to, message)
        elif choice == '3':
            to = input("Enter phone number (with country code, e.g., +1234567890): ")
            make_phone_call(to)
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
