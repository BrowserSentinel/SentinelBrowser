import re
import os 
import time
from mitmproxy import http
from mitmproxy.options import Options
from bs4 import BeautifulSoup

# Get current directory 
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build full path to blocklist file
blocklist_file = os.path.join(current_dir, "blocklist.txt")

with open(blocklist_file) as f:
    blocklist = [line.strip() for line in f]

    print(f"""
 
███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗       █████╗ ██████╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║      ██╔══██╗██╔══██╗██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║█████╗███████║██║  ██║██████╔╝██║     ██║   ██║██║     █████╔╝ █████╗  ██████╔╝
╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║╚════╝██╔══██║██║  ██║██╔══██╗██║     ██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗ ██║  ██║██████╔╝██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
       made by https://github.com/Rud3p    
""")
time.sleep(3)    
print("Server running...")
print("")
time.sleep(1) 
print("How to set the Adblocker up ?")
time.sleep(2)
print("")
print("Go to your settings in Windows and search for the Proxy Settings")
time.sleep(2)
print("")
print("You must set the IP to 127.0.0.1 and the Port to 8080")
time.sleep(2)
print("")
print("Now you are connected to the locally running proxy Server that blocks ADs")
time.sleep(10)

class Addon:
    def __init__(self):
        self.num_blocked = 0

    def response(self, flow: http.HTTPFlow):
        if self.check_blocklist(flow, blocklist):
            flow.response.content = self.remove_ads(flow.response.content, blocklist)
            self.num_blocked += 1

    def check_blocklist(self, flow, blocklist):
        if "text/html" in flow.response.headers["Content-Type"]:
            for domain in blocklist:
                if domain in flow.response.content:
                    return True
        return False

    def remove_ads(self, content, blocklist):
        soup = BeautifulSoup(content, "html.parser")
        for tag in soup.find_all(src=blocklist):
            tag.decompose()
        return str(soup).encode()

    def done(self):
        print(f"Blocked {self.num_blocked} ads")
        
options = Options(listen_host='127.0.0.1', listen_port=8080)

addons = [
    Addon()
]
