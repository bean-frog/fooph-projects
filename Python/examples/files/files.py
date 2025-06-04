import subprocess

#num emails
emails = subprocess.run("cat mail.txt | grep 'From:' | wc -l", shell=True, capture_output=True)
print(f"num of emails: {eval(emails.stdout)}")

#num berkeley emails
berkeley_emails = subprocess.run("cat mail.txt | grep 'From:' | grep 'berkeley.edu' | wc -l", shell=True, capture_output=True)
print(f"num of berkeley emails: {eval(berkeley_emails.stdout)}")
