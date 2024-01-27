# OAuth Device Code Phishing Attack

![Project Logo](https://i.postimg.cc/FR1B22ys/16769a86-59c4-42fc-8d9f-4c4841f57549.jpg)

## Table of Contents
- [Introduction](#introduction)
- [Usage](#usage)
  - [Help Options](#help-options)
  - [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

OAuth Device Code Phishing Attack is a Python script designed for educational purposes to demonstrate a phishing technique using OAuth device code authentication against Office 365. This project aims to raise awareness about the potential risks associated with social engineering attacks.

## Usage

### Help Options
To run the script, use the following command-line options:

```bash
python3 OAuth_Phishing.py [-h] [-m] [-s Sender_email] [-p Sender_password] [-r Recipient_email] [-n Recipient_name]

    -h, --help: Show this help message and exit.
    -m, --mail: Send a phishing email to the victim.
    -s Sender_email, --sender Sender_email: Sender's email address.
    -p Sender_password, --passwd Sender_password: Sender's email password. If you are using Gmail, please provide an 'app password' instead.
    -r Recipient_email, --receiver Recipient_email: Recipient's email address.
    -n Recipient_name, --name Recipient_name: Recipient's name.
```

### Deployment

1. Clone the repository:

```bash
git clone https://github.com/Vishal-Raj007/OAuth-Device-Code-Phishing.git 
cd OAuth-Device-Code-Phishing
```
2. Install dependencies:
```
pip3 install -r requirements.txt
```
3. Run the script:
```bash
python3 OAuth_Phishing.py
```

## Contributing
Contributions are welcome! If you find any issues or want to enhance the project, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any questions or suggestions, feel free to reach out:

    Author: Vishal Raj
    Email: vishalraj.infosecpro@gmail.com
