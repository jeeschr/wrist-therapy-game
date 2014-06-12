#
# GUI through wxPython allows user to play exercise test game
# Serial is polled to read load sensor value and control servomotor accordingly
# NOTE: serial is currently set as serial.Serial('/dev/cu.usbmodem1421', 115200, timeout=1)
#


import time
import serial
import struct
import wx


class windowClassInner(wx.Frame):

	def __init__(self, parent, id):
		wx.Frame.__init__(self, parent, id, 'Exercise Test', size=(600, 600))

		panel=wx.Panel(self, -1)

		#add pic
		imageFile = "/Users/m/Desktop/project/Untitled.png"
		image = wx.Image( imageFile, wx.BITMAP_TYPE_ANY)
		imageBitmap = wx.StaticBitmap(panel, wx.ID_ANY, wx.BitmapFromImage(image))

		sizer = wx.BoxSizer(wx.VERTICAL)
		
		instructions = wx.StaticText(panel, -1, 'Press button to start exercise test')

		self.Bind(wx.EVT_CLOSE, self.closewindow)

		button1 = wx.Button(panel, label="Begin", pos=(270, 150), size=(60, 60))
		self.Bind(wx.EVT_BUTTON, self.onbutton, button1)
		text = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.text=text

		sizer.Add(instructions, 1, wx.ALIGN_CENTER_HORIZONTAL)
	 	sizer.Add(imageBitmap, 1, wx.ALIGN_CENTER_HORIZONTAL)
		sizer.Add(button1, 1,  wx.ALIGN_CENTER_HORIZONTAL)
		sizer.Add(text, 1, wx.EXPAND|wx.ALL, 10)

		panel.SetSizer(sizer)

	def textoutput(self, text):
		self.text.AppendText(text)

	def onbutton(self, event):
		ser.flush()
		self.textoutput('\nTake your hand off the device, and allow it to start in the upward position.\n')
		# wx.Yield()
		# time.sleep(2)
		currentangle = 2130
		ser.write(struct.pack('I', int(currentangle)))
		# self.textoutput('SENDING' + str(currentangle) +' TO THE DEVICE')
		wx.Yield()

		endtime = time.time() + 0.5
		while(time.time() < endtime):
			ser.readline()

		self.textoutput('\nCalibrating... Do NOT touch the device!')
		wx.Yield()

		endtime = time.time() + 0.5
		while(time.time() < endtime):
			ser.readline()

		endtime = time.time() + 5
		rollingavg = 0
		valuescount = 0
		uselesscount = 0
		# ser.flush()
		while(time.time() < endtime):
			
			line = ser.readline()
			data = [float(val) for val in line.split()]
			line = data[0]
			currentangle = data[1]
		# 	#line = 12
			print line, currentangle
			if(uselesscount > 20):
				rollingavg = rollingavg + line
				valuescount = valuescount + 1
			uselesscount = uselesscount + 1
		rollingavg = rollingavg/valuescount
		print rollingavg
		wx.Yield()

		endtime = time.time() + 0.5
		while(time.time() < endtime):
			ser.readline()

		self.textoutput('\n\nCalibration complete. You may now use the device. Press gently and slowly increase pressure until the device reacts. Bring the platform to the horizontal point.')
		wx.Yield()
		

		# ser.flush()
		while(currentangle > 1450):
			
			line = ser.readline()
			data = [float(val) for val in line.split()]
			line = data[0]
			currentangle = data[1]
			#line = 23
			print line, currentangle
			if(line > rollingavg + 20):
				ser.write(struct.pack('I', int(currentangle-5)))
				#print 'SENDING ', currentangle-20, ' TO THE DEVICE'
		wx.Yield()

		endtime = time.time() + 0.5
		while(time.time() < endtime):
			ser.readline()

		self.textoutput('\n\nGood! Now relieve pressure on the device, but keep your hand on it. It will slowly return to it\'s starting position.')
		wx.Yield()
		# ser.flush()
		while(currentangle < 2140):
			
			line = ser.readline()
			data = [float(val) for val in line.split()]
			line = data[0]
			currentangle = data[1]
			#line = 16
			print line, currentangle
			if(line < rollingavg+15):
				ser.write(struct.pack('I', int(currentangle+5)))
				#print 'SENDING ', currentangle+20, ' TO THE DEVICE'
		wx.Yield()

		endtime = time.time() + 0.5
		while(time.time() < endtime):
			ser.readline()

		self.textoutput('\n\nGood! Now apply more pressure and bring it all the way down. Full flexion!')
		wx.Yield()

		# ser.flush()
		while(currentangle > 960):
			
			line = ser.readline()
			data = [float(val) for val in line.split()]
			line = data[0]
			currentangle = data[1]
			#line = 23
			print line, currentangle
			if(line > rollingavg + 20):
				ser.write(struct.pack('I', int(currentangle-5)))
				#print 'SENDING ', currentangle-20, ' TO THE DEVICE'
		wx.Yield()

		endtime = time.time() + 0.5
		while(time.time() < endtime):
			ser.readline()

		self.textoutput('\n\nGood! Now relieve pressure on the device, but keep your hand on it. It will slowly return to it\'s starting position.')
		wx.Yield()
		# ser.flush()
		while(currentangle < 2140):
			
			line = ser.readline()
			data = [float(val) for val in line.split()]
			line = data[0]
			currentangle = data[1]
			#line = 16
			print line, currentangle
			if(line < rollingavg+15):
				ser.write(struct.pack('I', int(currentangle+5)))
				#print 'SENDING ', currentangle+20, ' TO THE DEVICE'
		wx.Yield()

		endtime = time.time() + 0.5
		while(time.time() < endtime):
			ser.readline()

		self.textoutput('\n\nGood job! The exercise test is complete!')
	 	wx.Yield()


	def closebutton(self, event):
		ser.close()
		self.Close(True)

	def closewindow(self, event):
		self.Destroy()


class windowClass(wx.Frame):

	def __init__(self, parent, id):
		wx.Frame.__init__(self, parent, id, 'Welcome')

		panel=wx.Panel(self)

		sizerA = wx.BoxSizer(wx.VERTICAL)

		welcomeText = wx.StaticText(panel, -1, 'Select from the options below:')

		sizerA.Add(welcomeText, wx.EXPAND, wx.ALIGN_CENTER_HORIZONTAL)

		self.Bind(wx.EVT_CLOSE, self.closewindow)

		button1 = wx.Button(panel, label="Play")
		self.Bind(wx.EVT_BUTTON, self.playbutton, button1)

		sizerA.Add(button1, wx.EXPAND, wx.ALIGN_CENTER_HORIZONTAL)

		button=wx.Button(panel, label="Exit")
		self.Bind(wx.EVT_BUTTON, self.closebutton, button)

		sizerA.Add(button, wx.EXPAND, wx.ALIGN_CENTER_HORIZONTAL)

		panel.SetSizer(sizerA)

	def closebutton(self, event):
		self.Close(True)

	def closewindow(self, event):
		self.Destroy()

	def playbutton(self, event):

		frame = windowClassInner(parent=None, id=-1)	

		frame.Show()
		

####################

ser = serial.Serial('/dev/cu.usbmodem1421', 115200, timeout=1)
ser.readline()

def main():

	app = wx.App()

	frame = windowClass(parent=None, id=-1)	

	frame.Show()

	app.MainLoop()

if __name__ == "__main__":
	main()
