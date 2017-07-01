import Tkinter
import socket
import sys
from visual import *
import math
import time
import thread
import os
import signal


################################UI Section########################################

#s = socket.socket()         # Create a socket object
host = "10.42.0.1" # Get local machine name
port = 12345                # Reserve a port for your service.
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((host, port))


# s.bind((host, port))        # Bind to the port
# s.listen(5)                 # Now wait for client connection.
# c, addr = s.accept()     # Establish connection with client.
UDP_IP = "" #socket.gethostname() # Get local machine name
UDP_PORT = 12345                # Reserve a port for your service.

s = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
s.bind(("", UDP_PORT))
data,addr = s.recvfrom(1024)


SimState  = None
###########################Modes label functions############################
def ModesRealTime():
	selection = "You selected Real Time" #+ str(var.get())
	label.config(text = selection)
	for child in SpTasks.winfo_children():
		child.configure(state='disable')
	for child in ConLbl.winfo_children():
		child.configure(state='disable')
	SendButton.config(state="disable")
	StopButton.config(state="normal")
	# c, addr = s.accept()     # Establish connection with client.
	#c.send("RealTime")
	s.sendto("RealTime",addr)

def ModesSim():
	global addr
	global SimState
	SimState = "continue"
	#print data,addr
	selection = "You selected Simulation" #+ str(var.get())
	label.config(text = selection)
	for child in SpTasks.winfo_children():
		child.configure(state='disable')
	for child in ConLbl.winfo_children():
		child.configure(state='disable')
	SendButton.config(state="disable")
	StopButton.config(state="normal")
	# c, addr = s.accept()     # Establish connection with client.
	#c.send("Simulation")
	s.sendto("Simulation", addr)
	time_diff = 0.01
	########################################
	scene.title ='Robotic Arm'
	scene.exit = False

	g = 9.8
	M1 = 2.0
	M2 = 1.0
	d = 0.05 # thickness of each bar
	gap = 2.*d # distance between two parts of upper, U-shaped assembly
	L1 = 0.5 # physical length of upper assembly; distance between axles
	L1display = L1+d # show upper assembly a bit longer than physical, to overlap axle
	L2 = 1.0 # physical length of lower bar
	L2display = L2+d/2. # show lower bar a bit longer than physical, to overlap axle
	L3display = .3

	hpedestal = 1.3*(L1+L2) # height of pedestal
	wpedestal = 0.1 # width of pedestal
	tbase = 0.05 # thickness of base
	wbase = 8.*gap # width of base
	offset = 2.*gap # from center of pedestal to center of U-shaped upper assembly
	top = vector(0,0,0) # top of inner bar of U-shaped upper assembly
	scene.center = top-vector(0,(L1+L2)/2.,0)

	theta1 = 1.3*pi/2. # initial upper angle (from vertical)
	theta1dot = 0 # initial rate of change of theta1
	theta2 = 0 # initial lower angle (from vertical)
	theta2dot = 0 # initial rate of change of theta2

	top = vector(0,0,0) # top of inner bar of U-shaped upper assembly
	pedestal = box(pos=top-vector(0,hpedestal/2.,offset),
	                 height=1.1*hpedestal, length=wpedestal, width=wpedestal,
	                 color=(0.4,0.4,0.5))

	frame1 = frame(pos=top)
	bar1 = box(frame=frame1, pos=(L1display/2.-d/2.,0,-(gap+d)/2.), size=(L1display,d,d), color=color.red)
	frame1.axis = (0,-1,0)

	frame2 = frame(pos=frame1.axis*L1)
	bar2 = box(frame=frame2, pos=(L2display/2.-d/2.,0,0), size=(L2display,d,d), color=color.green)
	frame2.axis = (0,-1,0)
	frame2.pos = top+frame1.axis*L1

	frame3 = frame(pos = frame2.axis*L2)
	bar3 = box(frame=frame3, pos=(L3display/2.-d/2.,0,0), size=(L3display,d,d), color=color.yellow)
	frame3.axis = (0,-1,0)
	frame3.pos = top+frame1.axis*L1 +frame2.axis*L2

	scene.autoscale = 0


	#####################################################################################



	if True:
	   #c, addr = s.accept()     # Establish connection with client.
		#print 'Got connection from', addr
		try:
			############ 1 ###################
			print "1"
			#ss1 = c.recv(sys.getsizeof(float))
			data,addr = s.recvfrom(1024)
			ss1 = data.strip()
			ss1 = ss1[2:11]
			print ss1 , type(ss1)
			previous_x = float(ss1)

			############## 2 ##################
			print "2"
			#ss2 = c.recv(sys.getsizeof(float))
			data,addr = s.recvfrom(1024)
			ss2 = data.strip()
			ss2 = ss2[2:11]
			previous_x2 = float(ss2)
			############### 3 ##################
			print "3"
			#ss3 = c.recv(sys.getsizeof(float))
			data,addr = s.recvfrom(1024)
			ss3 = data.strip()
			ss3 = ss3[2:11]
			previous_x3 = float(ss3)
			print "4"
			#ssy3 = c.recv(sys.getsizeof(float))
			data,addr = s.recvfrom(1024)
			ssy3 = data.strip()
			ssy3 = ssy3[2:11]
			previous_y3 = float(ss2)
			print "before send"
			#c.send(SimState.encode())
			print SimState
			s.sendto(SimState.encode(), addr)

			while True:
				################### 1 #######################
				#s1 = c.recv(sys.getsizeof(float))
				data,addr = s.recvfrom(1024)
				s1 = data.strip()
				if s1[:2]=="x1":
				  s1 = s1[2:11]
				else:
				  s1 = previous_x
				  #tmp = c.recv(sys.getsizeof(float))

				delta_x = float(s1)

				frame1.rotate(axis=(0,0,1), angle=delta_x -previous_x )
				frame2.pos = top+frame1.axis*L1

				previous_x = delta_x

				################## 2 ############################

				#s2 = c.recv(sys.getsizeof(float))
				data,addr = s.recvfrom(1024)
				s2 = data.strip()
				if s2[:2]=="x2":
				  s2 = s2[2:11]
				else:
				  s2 = previous_x2
				  #tmp = c.recv(sys.getsizeof(float))
				delta_x2 = float(s2)

				frame2.rotate(axis=(0,0,1), angle=delta_x2 -previous_x2 )
				frame3.pos = top+frame1.axis*L1+frame2.axis*L2 +(0,0,L3display/2)
				previous_x2 = delta_x2

				##################### 3 #############################
				#s3 = c.recv(sys.getsizeof(float))
				data,addr = s.recvfrom(1024)
				s3 = data.strip()
				if s3[:2]=="x3":
				  s3 = s3[2:11]
				else:
				  s3 = previous_x3
				  #tmp = c.recv(sys.getsizeof(float))
				delta_x3 = float(s3)

				#s4 = c.recv(sys.getsizeof(float))
				data,addr = s.recvfrom(1024)
				s4 = data.strip()
				if s4[:2]=="y3":
				  s4 = s4[2:11]
				else:
				  s4 = previous_y3
				  #tmp = c.recv(sys.getsizeof(float))
				delta_y3 = float(s4)

				frame3.rotate(angle=(delta_x3-previous_x3), axis=vector(1,0,0))
				frame3.rotate(angle=(delta_y3-previous_y3), axis=vector(0,0,1))

				previous_x3 = delta_x3
				previous_y3 = delta_y3
				print "before send"
				#c.send(SimState.encode())
				print SimState
				s.sendto(SimState.encode(), addr)
				if SimState == "StopSim":
					#s.close()
					break
				print "after send"


		except KeyboardInterrupt:
			print "close"
			#s.close()
			#c.close()                # Close the connection

def ModesSpsTasks():
	selection = "You selected Gestures" #+ str(var.get())
	label.config(text = selection)
	for child in SpTasks.winfo_children():
		child.configure(state='normal')
	for child in ConLbl.winfo_children():
		child.configure(state='disable')
	SendButton.config(state="disable")
	StopButton.config(state="disable")
	# c, addr = s.accept()     # Establish connection with client.
	#c.send("Tasks")
	s.sendto("Tasks", addr)

def ModesControlMotors():
	for child in ConLbl.winfo_children():
		child.configure(state='normal')
	for child in SpTasks.winfo_children():
		child.configure(state='disable')
	SendButton.config(state="normal")
	StopButton.config(state="disable")
	pass

#######################Tasks label functions################################
def TasksOrPos():
	selection = "You selected Original position"# + str(var.get())
	label.config(text = selection)
	#c, addr = s.accept()     # Establish connection with client.
	#c.send("OriPos")
	s.sendto("OriPos", addr)

def TasksNinDeg():
	selection = "You selected Ninteen Degree" #+ str(var.get())
	label.config(text = selection)
	#c, addr = s.accept()     # Establish connection with client.
	#c.send("NinDegree")
	s.sendto("NinDegree", addr)

def TasksGripperMoving():
	selection = "You selected Gripper Moving" #+ str(var.get())
	label.config(text = selection)
	#c, addr = s.accept()     # Establish connection with client.
	#c.send("GripperMoving")
	s.sendto("GripperMoving", addr)


def QuitButtonHandle():
	selection = "Good bye" #+ str(var.get())
	label.config(text = selection)
	# c, addr = s.accept()     # Establish connection with client.
	#c.send("Exit")
	s.sendto("Exit", addr)
	#c.close()
	s.close()
	root.quit()
	os.kill(os.getpid(), signal.SIGTERM)
	pass
def ModesSimThread():
	global thr1
	thr1 = thread.start_new_thread(ModesSim, ())
	pass
def StopButtonHandle():
	selection = "Stopped" #+ str(var.get())
	label.config(text = selection)
	global SimState
	SimState = "StopSim"
	#cleanup_stop_thread()
	pass
def SendButtonHandle():
	s2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	print var3.get()+str(ValueSlider.get())
	s.sendto(str(var3.get())+str(ValueSlider.get()), ("192.168.43.161", 5001))
	pass

###############################root window setup##########################
root = Tkinter.Tk()
root.geometry("500x500")
root.wm_title("Robot Control")

###########################Variables to control radio buttons###################
var = Tkinter.IntVar()
var2 = Tkinter.IntVar()
var3 = Tkinter.StringVar()
var4 = Tkinter.IntVar()
var3.set("x0")

##############################Group Boxs###############################################
ModesGrpBox = Tkinter.LabelFrame(root, text="Modes")
SpTasks = Tkinter.LabelFrame(root, text="Tasks")
ConLbl = Tkinter.LabelFrame(root, text="Control")


##################################Modes Radio Buttons################################################
RT = Tkinter.Radiobutton(ModesGrpBox, text="Real Time", variable=var, value=1,command=ModesRealTime)
RT.pack()

Sim = Tkinter.Radiobutton(ModesGrpBox, text="Simulation", variable=var, value=2,command=ModesSimThread)
Sim.pack( anchor = Tkinter.W)

SpecTasks = Tkinter.Radiobutton(ModesGrpBox, text="Specific Tasks", variable=var, value=3,command=ModesSpsTasks)
SpecTasks.pack( anchor = Tkinter.W )

ControlMotors = Tkinter.Radiobutton(ModesGrpBox, text="Control Motors", variable=var, value=4,command=ModesControlMotors)
ControlMotors.pack( anchor = Tkinter.W )

########################################Tasks Radio Buttons#################################################
OriPos = Tkinter.Radiobutton(SpTasks, text="Original Position", variable=var2, value=1,command=TasksOrPos)
OriPos.pack()

NinDegree = Tkinter.Radiobutton(SpTasks, text="90 Degree", variable=var2, value=3,command=TasksNinDeg)
NinDegree.pack( anchor = Tkinter.W)

GripMove = Tkinter.Radiobutton(SpTasks, text="Gripper Moving", variable=var2, value=2,command=TasksGripperMoving)
GripMove.pack( anchor = Tkinter.W )

##############################Servos Radio Buttons##########################
BaseBut = Tkinter.Radiobutton(ConLbl, text="Base", variable=var3, value="x0")
BaseBut.pack()

ShoulderBut = Tkinter.Radiobutton(ConLbl, text="Shoulder", variable=var3, value="x1")
ShoulderBut.pack()

ElbowBut = Tkinter.Radiobutton(ConLbl, text="Elbow", variable=var3, value="x2")
ElbowBut.pack()

RestRotBut = Tkinter.Radiobutton(ConLbl, text="Rest Rotation", variable=var3, value="x3")
RestRotBut.pack()

RestLinBut = Tkinter.Radiobutton(ConLbl, text="Rest Linear", variable=var3, value="y3")
RestLinBut.pack()

ValueSlider = Tkinter.Scale(ConLbl, from_=-120, to=90,resolution=1, orient=Tkinter.HORIZONTAL)
ValueSlider.pack()


####################################Buttons##############################
SendButton = Tkinter.Button(root, text ="Send", command = SendButtonHandle)
StopButton = Tkinter.Button(root, text ="Stop", command = StopButtonHandle)
QuitButton = Tkinter.Button(root, text ="Quit", command = QuitButtonHandle)


###########################Disable Tasks And Control by Default#########################
for child in SpTasks.winfo_children():
    child.configure(state='disable')

for child in ConLbl.winfo_children():
    child.configure(state='disable')

SendButton.config(state="disable")
StopButton.config(state="disable")
################################Packing######################################
label = Tkinter.Label(root)
ModesGrpBox.pack( expand="yes")
SpTasks.pack( expand="yes")
ConLbl.pack( expand="yes")
label.pack()
SendButton.pack()
StopButton.pack()
QuitButton.pack()
root.mainloop()



