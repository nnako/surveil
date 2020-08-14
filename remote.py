import io

#
# this file displays a menu that allows to take control of the surveillance cam.
# the user may choose what actions should take place.
# the camera control code will be written to ommand.txt.
# There may also be the functionality of controlling camera movement - this code might be sent to motion.txt. 

#
# brainstorming of possible functionality
#

# 1 - Start surveillance program
# 2 - Stop surveillance program
# 3 - Record video and send it to email address
# 4 - Take picture (still) and send it to email address
# 5 - ...
# 6 - ...
# 7 - ...
# 8 - ...
# 9 - Status (e.g. recording mode)
# 0 - Enter code manually (hit ENTER after typing code)
# q - Quit remote program
#
# according to keystroke / input: generate file "command.txt" and write the code into it.
#

def menu():
	print("\nMake your choice: \n 1 - Start program \n 2 - Stop program \n 3 - Write text to command.txt \n")
	choice = str(input())

	if choice == "1":
		print("Program started!")
		menu()

	if choice == "2":
		print("Program stopped!")
		menu()


	if choice == "3":
		f = io.open("./command.txt","w")
		f.write(u'This line was written from remote.py\n')
		
# At the moment the code above this line causes a syntax error. When typed directly in the terminal, it works!
# (It then creates a text line in the testfile.)
		
menu()
