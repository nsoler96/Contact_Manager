import pandas as pd
import datetime
import smtplib
import os

current_path = os.getcwd()
print(current_path)

# Change working directory (optional)
os.chdir(current_path)

# Input your Gmail credentials
GMAIL_ID = input("Enter your email: ")
GMAIL_PSWD = input("Enter password for your email mentioned above: ")

def sendEmail(to, sub, msg):
    print(f"Email to {to} sent: \nSubject: {sub} ,\nMessage: {msg}")
    # Create SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()  # Start TLS encryption
    s.login(GMAIL_ID, GMAIL_PSWD)
    s.sendmail(GMAIL_ID, to, f"Subject: {sub}\n\n{msg}")
    s.quit()

if __name__ == "__main__":
    # Load the friends' data from the Excel file
    df = pd.read_excel("data.xlsx")
    today = datetime.datetime.now().strftime("%d-%m")
    yearNow = datetime.datetime.now().strftime("%Y")

    writeInd = []
    for index, item in df.iterrows():
        bday = item['Birthday']
        bday = datetime.datetime.strptime(bday, "%d-%m-%Y")
        bday = bday.strftime("%d-%m")
        if today == bday and yearNow not in str(item['LastWishedYear']):
            sendEmail(item['Email'], "Happy Birthday", item['Dialogue'])
            writeInd.append(index)

    if writeInd:
        for i in writeInd:
            oldYear = df.loc[i, 'LastWishedYear']
            df.loc[i, 'LastWishedYear'] = str(oldYear) + ", " + str(yearNow)

    df.to_excel('data.xlsx', index=False)
