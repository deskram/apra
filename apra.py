# """
#  ______   _______  _______  _        _______  _______  _______ 
# (  __  \ (  ____ \(  ____ \| \    /\(  ____ )(  ___  )(  ___  )
# | (  \  )| (    \/| (    \/|  \  / /| (    )|| (   ) || () () |
# | |   ) || (__    | (_____ |  (_/ / | (____)|| (___) || || || |
# | |   | ||  __)   (_____  )|   _ (  |     __)|  ___  || |(_)| |
# | |   ) || (            ) ||  ( \ \ | (\ (   | (   ) || |   | |===>("Ali")
# | (__/  )| (____/\/\____) ||  /  \ \| ) \ \__| )   ( || )   ( |
# (______/ (_______/\_______)|_/    \/|/   \__/|/     \||/     \|
# """         ___                  

import requests ,shutil,os
from termcolor import colored
import OpenSSL.crypto,pyfiglet
from requests.exceptions import HTTPError, MissingSchema, InvalidSchema, ConnectionError
from time import sleep

logo = pyfiglet.figlet_format('Apra Injection')
print(colored(logo,color="blue"))

print('[+] Type yes to continue ... ')
ent = input('').lower()
if ent == "yes":        
    sleep(2)
    print('[+] Running ..')
    def handle_response(resp):
        if resp.status_code == 200:
            return resp.content
        else:
            pass
    
    def get_data(url):
        traf = {
            "http": "http://127.0.0.1:8080",
            "https": "https://127.0.0.1:8080"
        }
        try:
            resp = requests.get(url, proxies=traf)
            return handle_response(resp)
        except (HTTPError, MissingSchema, InvalidSchema, ConnectionError):
            return "Request failed"
    
    def save_data(data, filename):
        with open(filename, 'wb') as file:
                file.write(data)
    
    data = get_data('http://burp/cert')
    derfile,pemfile = 'deskram.der','deskram.pem'

    if "Request failed" not in str(data):
        save_data(data, derfile)
        print('[+] Complete Download')
        sleep(1.5)
        if not derfile.endswith('.der') or not os.path.exists(derfile):
            print("[-] Please provide a valid .der file.")
        elif not pemfile.endswith('.pem') or not pemfile:
            print("[-] Please provide a valid .pem file.")
        print('[+] Complete Convert')
        def convert_der_to_pem(der_file,pem_file):
            with open(der_file,'rb') as file:
                der_data = file.read()
                cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1,der_data)
                pem_data = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM,cert)
                with open (pem_file, 'wb') as pem_out:
                    pem_out.write(pem_data)
                return pem_out
        
        convert_der_to_pem(derfile,pemfile)
        def get_subject_hash(cert_file):
            with open(cert_file, 'rb') as file:
                cert_data = file.read()
                cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_data)
                subject_hash = hex(cert.subject_name_hash())[2:]
                return subject_hash
            
        subject_hash = get_subject_hash(pemfile)
        shutil.copy(pemfile,f'{subject_hash}.0')

    elif "Request failed" in data:
        print("[-] Burp Suite Connection Interceptor Closed .")
    else:print("[-] Something wrong")
else:
    print('[-] Program stoping') 
