var = ""
step = 0
while True:
	if step == 0:	
		print("Step:00")
		var = input("devam etmek istiyor musunuz? e/h : ")
		if(var == "h"):
			step = 0
		else:
			step = step + 1
	if step == 1:	
		print("Step:01")
		var = input("devam etmek istiyor musunuz? e/h")
		if(var == "h"):
			step = step - 1
		else:
			step = step + 1
	if step == 2:	
		print("Step:02")
		var = input("devam etmek istiyor musunuz? e/h")
		if(var == "h"):
			step = step - 1
		else:
			step = step + 1
	if step == 3:	
		print("Step:03")
		var = input("devam etmek istiyor musunuz? e/h")
		if(var == "h"):
			step = step - 1
		else:
			break

print("Program Bitti")