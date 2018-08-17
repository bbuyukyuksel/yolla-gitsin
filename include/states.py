#!/usr/bin/python3
import os,time,pwd,sys
import locale
from dialog import Dialog 
from subprocess import Popen,PIPE
import json

class CONTROLLER:
	def isDictSame(x,y):
		size = len(y)
		for i in y:
			if i == x:
				return True
		return False

class STATES:
	#Current State
	current_state = 0
	def __init__(self):
		#State : 0
		locale.setlocale(locale.LC_ALL, '')
		self.text_port = "2222"
		self.text_host = "pardus@10.150.17.180"
		self.text_pass = "1"
		self.text_host_dir="pardus@10.150.17.180:/home/pardus/Masaüstü/."
		self.path = "/home/" + pwd.getpwuid(os.getuid())[0] +"/Masaüstü/"
		self.d = Dialog(dialog="dialog")
		self.d.set_background_title("Yolla Gitsin Moruq")
		self.current_state = 1
	
		
	def state_info(self):
		#State : 01
		self.d.msgbox("Hoş Geldiniz!\n\nLütfen dosyaların taşınmasını istediğiniz bilgisayarda openssh-server uygulamasının kurulu olduğundan emin olun.",width=40,height=12)
		self.current_state = 2
	
	def state_02(self):
		#STATE 2
		#Config Setting to Connect PC
		isDone, tag, text = self.d.inputmenu("Bağlanılacak bilgisayarın bilgilerini giriniz",height=18, menu_height=16, choices=[("Port",self.text_port),("Host",self.text_host),("Host_Direction",self.text_host_dir),("Password",self.text_pass)])
		if(isDone == 'renamed'):
			if(tag == 'Port'):
				self.text_port = text
			elif tag == "Password":
				self.text_pass = text
			elif tag == "Host":
				self.text_host = text
			elif tag == "Host_Direction":
				self.text_host_dir = text 
		elif(isDone == 'accepted'):
			self.current_state += 1
		else:
			self.current_state -= 1
	
	def state_03(self):
		#State : 03
		code = self.d.yesno("SSH Key üretilsin mi?")
		if(code == self.d.OK):
			self.current_state = 4
		#7. State'e dallan
		else:
			self.current_state = 7 
	def state_04(self):
		#State : 04
		#SSH-KEYGEN
		os.popen("rm -rf ~/.ssh")
		output = Popen(['ssh-keygen', '-t', 'rsa'], stdout=PIPE, stdin=PIPE)
		output.stdin.write("\n\n\n".encode())
		output.stdin.close()
		output.wait()
		self.d.infobox("SSH KEY'ler oluşturuldu.", width=0, height=0, title="Başarılı")
		time.sleep(2)
		self.current_state = 5
	
	def state_05(self):
		#State : 05
		#ALERT : SSH-KEY Karşı Bilgisayar Kopyalanıcak
		self.d.infobox("Public KEY karşı pc'ye kopyalanıcak")
		time.sleep(1)	
		self.current_state = 6
	
	def state_06(self):
		#State : 06
		#SSH-COPY-ID
		output2 = Popen(['sshpass -p "{}" ssh-copy-id -o StrictHostKeyChecking=no -p {} {} '.format(self.text_pass, self.text_port, self.text_host)], stdout=PIPE, stdin=PIPE,shell=True)
		output2.stdin.close()
		output2.wait()	
		self.d.infobox("SSH KEY'ler aktarıldı.", width=0, height=0, title="Başarılı")
		time.sleep(1)
		self.current_state = 8
	
	def state_07(self):
		#State : 07
		#SSH-KEYGEN ÜRETİLMEDEN çalıştırma   
		self.d.infobox("SSH KEY üretilmeden devam ediliyor.",width=40,height=3)
		time.sleep(2)
		self.current_state = 8
	
	def state_08(self):
		#State : 08
		isDone, temp_path = self.d.dselect(self.path)
		if not(temp_path == ""):
			self.path = temp_path
		if isDone == 'ok':
			self.current_state = 9
		else:
			self.current_state = 2
	
	def state_09(self):
		#State : 09
		onlyfiles = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path,f))]
		onlyfiles_len = len(onlyfiles)
		info4files = []
		
		for i in range(onlyfiles_len):
			info4files.append((onlyfiles[i],"",False))
		
		code,send_files = self.d.checklist("Gönderilecek dosyaları seç", height=20, choices=info4files)
		if code == 'cancel':
			self.current_state = 8
		elif code == 'ok':
			send_files_len = len(send_files)
			if(send_files_len == 0):
				self.d.infobox("Dosya Seçilmedi")
				time.sleep(2)
			else:
				for i in range(send_files_len):
					output3= Popen(['sshpass -p "{}" scp -P {} {} {}'.format(self.text_pass, self.text_port,os.path.join(self.path,send_files[i]),self.text_host_dir)],stdin=PIPE,stdout=PIPE,shell=True)
					output3.stdin.close()
					out = output3.stdout.read().decode("utf-8")
					self.d.infobox(text = out)
					output3.wait()
			self.current_state = 10
		
	def state_repeat(self):
		#State : 10
		code = self.d.yesno("Dosya Yollamaya devam etmek ister misiniz?",yes_label = "Yes Baba",no_label="No Baba")
		if(code == 'ok'):
			self.current_state = 8
		else:
			self.current_state = 11
			
	def state_final(self):
		#State : 11
		self.d.infobox("Çıkıyor Moruq")
		time.sleep(2)
	def state_login(self):
		#2
		code = self.d.yesno("Eski oturumlarla devam et",yes_label = "Yes Baba",no_label="No Baba")
		if code =="ok":
			self.current_state = 21
		else:
			self.current_state = 22
	def state_login_read(self):
		# state 2.1 = 21
		try:
			_choices = []
			with open("Conf/conf.json","r") as f:
				conf = json.load(f)
				for i in range(len(conf["user"])):
					_str = "{}".format(conf["user"][i]["host"])
					_choices.append((str(i),_str,False))
				code,tag = self.d.radiolist("kullanıcı ekranı",height=15,choices=_choices)
				if code == "ok":
					self.text_port = conf["user"][int(tag)]["port"]
					self.text_host = conf["user"][int(tag)]["host"]
					self.text_pass = conf["user"][int(tag)]["pass"]
					self.text_host_dir = conf["user"][int(tag)]["host_dir"]
					self.current_state = 3
				else:
					self.current_state = 2
		except (FileNotFoundError):
			self.d.infobox("Eski Oturum Bulunumadı!")
			time.sleep(2)
			self.current_state = 2
	def state_login_create(self):
		#State : 2.2 - 22
		isDone, tag, text = self.d.inputmenu("Bağlanılacak bilgisayarın bilgilerini giriniz",height=18, menu_height=16, choices=[("Port",self.text_port),("Host",self.text_host),("Host_Direction",self.text_host_dir),("Password",self.text_pass)])
		if(isDone == 'renamed'):
			if(tag == 'Port'):
				self.text_port = text
			elif tag == "Password":
				self.text_pass = text
			elif tag == "Host":
				self.text_host = text
			elif tag == "Host_Direction":
				self.text_host_dir = text 
		elif(isDone == 'accepted'):
			conf = {}
			append_data = {"port":self.text_port,"host":self.text_host,"pass":self.text_pass,"host_dir":self.text_host_dir}
			isSameData = False
			try:
				#Eğer dosya oluşturulduysa
				with open("Conf/conf.json","r") as f:
					conf = json.load(f)
					isSameData = CONTROLLER.isDictSame(append_data,conf["user"])	
			except:
				conf = {"user":[]}
				os.mkdir("Conf")
			finally:
				if not(isSameData):
					with open("Conf/conf.json","w") as f:	
						conf["user"].append(append_data)
						json.dump(conf,f,indent=4)
						self.current_state = 3
				else:
					self.d.infobox("Daha önceden kaydedilmiş içerik.")
					time.sleep(2)
					self.current_state = 2
		else : 
			self.current_state = 2

def Yolla_Gitsin_begin():
	states = STATES()
	while True:
		if(states.current_state == 0):
			states.__init__()
		if(states.current_state == 1):
			states.state_info()
		if(states.current_state == 2):
			states.state_login()
		if(states.current_state == 21):
			states.state_login_read()
		if(states.current_state == 22):
			states.state_login_create()
		if(states.current_state == 3):
			states.state_03()
		if(states.current_state == 4):
			states.state_04()
		if(states.current_state == 5):
			states.state_05()
		if(states.current_state == 6):
			states.state_06()
		if(states.current_state == 7):
			states.state_07()
		if(states.current_state == 8):
			states.state_08()
		if(states.current_state == 9):
			states.state_09()	
		if(states.current_state == 10):
			states.state_repeat()
		if(states.current_state == 11):
			states.state_final()		
			exit()
			#states.state_final()
