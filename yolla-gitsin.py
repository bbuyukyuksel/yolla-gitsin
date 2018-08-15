#!/usr/bin/python
# -*- coding: utf-8 -*-
#link : http://pythondialog.sourceforge.net/doc/widgets.html
import os,time,pwd
import locale
from dialog import Dialog
from subprocess import Popen,PIPE

#Config Settings
mypath = "/opt/"
locale.setlocale(locale.LC_ALL, '')

text_port = "22"
text_host = "cyamaneren@10.150.20.74"
text_pass = "1"
text_host_dir="cyamaneren@10.150.20.74:/home/cyamaneren/."

d = Dialog(dialog="dialog")
d.set_background_title("Yolla Gitsin Moruq")

d.msgbox("Hoş Geldiniz!\n\nLütfen dosyaların taşınmasını istediğiniz bilgisayarda openssh-server uygulamasının kurulu olduğundan emin olun.",width=40,height=12)

code = d.yesno("SSH Key üretilsin mi?")
if code == d.OK :
    print("İşlem bitene kadar <enter> 'a basınız.")
    os.popen("rm -rf ~/.ssh")
    output = Popen(['ssh-keygen', '-t', 'rsa'], stdout=PIPE, stdin=PIPE)
    output.stdin.write("\n\n\n".encode())
    output.stdin.close()
    output.wait()
    d.infobox("SSH KEY'ler oluşturuldu.", width=0, height=0, title="Başarılı")
    time.sleep(2)
    d.infobox("Public ID karşı pc'ye kopyalanıcak")
    
    
    isDone = 'renamed'
    while isDone == 'renamed':
        isDone, tag, text = d.inputmenu("Bağlanılacak bilgisayarın bilgilerini giriniz",height=18, menu_height=16, choices=[("Port",text_port),("Host",text_host),("Host_Direction",text_host_dir),("Password",text_pass)])
        if(isDone == 'renamed'):
            if(tag == 'Port'):
                text_port = text
            elif tag == "Password":
                text_pass = text
            elif tag == "Host":
                text_host = text
            elif tag == "Host_Direction":
                text_host_dir = text    
    output2 = Popen(['sshpass -p "{}" ssh-copy-id -o StrictHostKeyChecking=no -p {} {} '.format(text_pass, text_port, text_host)], stdout=PIPE, stdin=PIPE,shell=True)
    
    output2.stdin.close()
    output2.wait()	
    #d.infobox("SSH KEY'ler aktarıldı.", width=0, height=0, title="Başarılı")
    time.sleep(2)
    
else:
    d.infobox("SSH KEY üretilmeden devam ediliyor.",width=40,height=3)
    time.sleep(2)
    

#SCP'yi kodla
isDone = "cancel"
while not(isDone == 'ok'):
    isDone, path = d.dselect("/home/" + pwd.getpwuid(os.getuid())[0] +"/")

onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
onlyfiles_len = len(onlyfiles)
info4files = []
for i in range(onlyfiles_len):
	info4files.append((onlyfiles[i],"",False))
print(info4files)

name,send_files = d.checklist("Gönderilecek dosyaları seç", height=20, choices=info4files)
print(os.path.join(path,send_files[0]))
print("scp -P {} {} {}".format(text_port,os.path.join(path,send_files[0]),text_host_dir))
output3= Popen(["scp -P {} {} {}".format(text_port,os.path.join(path,send_files[0]),text_host_dir)],stdin=PIPE,stdout=PIPE,shell=True)
print(output3.stdout.read().decode("utf-8"))
output3.wait()

print("\nPORT : ", text_port)
print("HOST : ", text_host)


