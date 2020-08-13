#
# this file displays a menu that allows to take control of the surveillance cam.
# the user may choose what actions should take place.
# the camera control code will be written to ommand.txt.
# There may also be the functionality of controlling camera movement - this code might be sent to motion.txt. 
#
# brainstorming 
#
#
#
# 1 - Start surveillance program
# 2 - Stop surveillance program
# 3 - Record video and send it to email address
# 4 - Take picture (still) and send it to email address
# 5 - ...
# 6 - ...
# 7 - ...
# 8 - ...
# 9 - ...
# 0 - Enter code manually (hit ENTER after typing code)
# q - Quit remote program
#
# according to keystroke: generate file "command.txt" and write the code into it.
#
#
#
# menu key 1 pressed
#
#
# echo "key 1 was pressed." >> ~/pi/APP__surveillance/testfile.txt
#
#
#

def menu():
	print("\nMake your choice, master: \n 1 - Start program \n 2 - Stop program \n 3 - Write text to testfile.txt \n")
	choice = input()

	if choice == "1":
		print("Program started!")
		menu()

	if choice == "2":
		print("Program stopped!")
		menu()

	if choice == "3":
		echo "this line was created via remote!" >> ./testfile.txt
menu()
