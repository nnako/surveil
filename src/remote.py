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
# 9 - Status (e.g. recording mode, temperature, cpu and mem data)
# 0 - Enter code manually (hit ENTER after typing code)
# q - Quit remote program
#
# according to keystroke / input: generate file "command.txt" and write the code into it.
#
loop = True
while loop:

	def menu():
		print("\nMake your choice:")
		print("1 - Start program (Fake)")
		print("2 - Stop program (Fake)")
		print("3 - Quit surveillance")
		print("4 - do something")
		print("5 - do something")
		print("6 - do something")
		print("7 - do something")
		print("8 - do something")
		print("9 - do something")
		print("0 - do something\n")
		print("Q - Quit this program\n")


		choice = str(input())

		if choice == "1":
			print("Surveillance started!")
			menu()

		if choice == "2":
			print("Surveillance stopped!")
			menu()

		if choice == "3":
			f = io.open("./command.txt","w")	# open command.txt file
			f.write(u'quit')					# write code to command.txt

		if choice == "q":
			print("Program stopped!")
			loop = False

	#
	# when 'q' is pressed an erro occurs. NameError: name 'q' is not defined
	# is it recommended to close the command.txt file after writing?
	#

	menu()
print("Program stopped, really!")
