# upload PE file to VirusTotal
# then get info about the results
# of analysis, print if malicious
import os
import sys
import time
import json
import requests
import argparse
import hashlib

# for terminal colors
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    ENDC = '\033[0m'

# VirusTotal API key
VT_API_KEY = "425f8f84c850412868ad9be5f4f5d960e08b173f808565d0bc48808293e185b8  "

# VirusTotal API v3 URL
VT_API_URL = "https://www.virustotal.com/api/v3/"

# upload malicious file to VirusTotal and analyse
class VTScan:
    def __init__(self):
        self.headers = {
            "x-apikey" : VT_API_KEY,
            "User-Agent" : "vtscan v.1.0",
            "Accept-Encoding" : "gzip, deflate",
        }

    def upload(self, malware_path):
        print (Colors.BLUE + "upload file: " + malware_path + "..." + Colors.ENDC)
        self.malware_path = malware_path
        upload_url = VT_API_URL + "files"
        files = {"file" : (
            os.path.basename(malware_path),
            open(os.path.abspath(malware_path), "rb"))
        }
        print (Colors.YELLOW + "upload to " + upload_url + Colors.ENDC)
        res = requests.post(upload_url, headers = self.headers, files = files)
        if res.status_code == 200:
            result = res.json()
            self.file_id = result.get("data").get("id")
            print (Colors.YELLOW + self.file_id + Colors.ENDC)
            print (Colors.GREEN + "successfully upload PE file: OK" + Colors.ENDC)
        else:
            print (Colors.RED + "failed to upload PE file :(" + Colors.ENDC)
            print (Colors.RED + "status code: " + str(res.status_code) + Colors.ENDC)
            sys.exit()

    def analyse(self):
        print (Colors.BLUE + "get info about the results of analysis..." + Colors.ENDC)
        analysis_url = VT_API_URL + "analyses/" + self.file_id
        res = requests.get(analysis_url, headers = self.headers)
        if res.status_code == 200:
            result = res.json()
            status = result.get("data").get("attributes").get("status")
            if status == "completed":
                stats = result.get("data").get("attributes").get("stats")
                results = result.get("data").get("attributes").get("results")
                print (Colors.RED + "malicious: " + str(stats.get("malicious")) + Colors.ENDC)
                print (Colors.YELLOW + "undetected : " + str(stats.get("undetected")) + Colors.ENDC)
                print ()
                for k in results:
                    if results[k].get("category") == "malicious":
                        print ("==================================================")
                        print (Colors.GREEN + results[k].get("engine_name") + Colors.ENDC)
                        print ("version : " + results[k].get("engine_version"))
                        print ("category : " + results[k].get("category"))
                        print ("result : " + Colors.RED + results[k].get("result") + Colors.ENDC)
                        print ("method : " + results[k].get("method"))
                        print ("update : " + results[k].get("engine_update"))
                        print ("==================================================")
                        print ()
                print (Colors.GREEN + "successfully analyse: OK" + Colors.ENDC)
                sys.exit()
            elif status == "queued":
                print (Colors.BLUE + "status QUEUED..." + Colors.ENDC)
                with open(os.path.abspath(self.malware_path), "rb") as malware_path:
                    b = malware_path.read()
                    hashsum = hashlib.sha256(b).hexdigest()
                    self.info(hashsum)
        else:
            print (Colors.RED + "failed to get results of analysis :(" + Colors.ENDC)
            print (Colors.RED + "status code: " + str(res.status_code) + Colors.ENDC)
            sys.exit()

    def run(self, malware_path):
        self.upload(malware_path)
        self.analyse()

    def info(self, file_hash):
        print (Colors.BLUE + "get file info by ID: " + file_hash + Colors.ENDC)
        info_url = VT_API_URL + "files/" + file_hash
        res = requests.get(info_url, headers = self.headers)
        if res.status_code == 200:
            result = res.json()
            if result.get("data").get("attributes").get("last_analysis_results"):
                stats = result.get("data").get("attributes").get("last_analysis_stats")
                results = result.get("data").get("attributes").get("last_analysis_results")
                print (Colors.RED + "malicious: " + str(stats.get("malicious")) + Colors.ENDC)
                print (Colors.YELLOW + "undetected : " + str(stats.get("undetected")) + Colors.ENDC)
                print ()
                for k in results:
                    if results[k].get("category") == "malicious":
                        print ("==================================================")
                        print (Colors.GREEN + results[k].get("engine_name") + Colors.ENDC)
                        print ("version : " + results[k].get("engine_version"))
                        print ("category : " + results[k].get("category"))
                        print ("result : " + Colors.RED + results[k].get("result") + Colors.ENDC)
                        print ("method : " + results[k].get("method"))
                        print ("update : " + results[k].get("engine_update"))
                        print ("==================================================")
                        print ()
                print (Colors.GREEN + "successfully analyse: OK" + Colors.ENDC)
                sys.exit()
            else:
                print (Colors.BLUE + "failed to analyse :(..." + Colors.ENDC)

        else:
            print (Colors.RED + "failed to get information :(" + Colors.ENDC)
            print (Colors.RED + "status code: " + str(res.status_code) + Colors.ENDC)
            sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--mal', required = True, help = "PE file path for scanning")
    args = vars(parser.parse_args())
    vtscan = VTScan()
    vtscan.run(args["mal"])
