from p5250_ovako.p3270 import P3270Client


class P5250Client():
    def __init__(self, luName=None, hostName='localhost', hostPort='23', modelName='3279-2',
                 verifyCert='yes', enableTLS='no', codePage='cp037', path=None, timeoutInSec=20):
        self.luName = luName
        self.hostName = hostName
        self.hostPort = hostPort
        self.modelName = modelName
        self.verifyCert = verifyCert
        self.enableTLS = enableTLS
        self.timeout = timeoutInSec
        self.path = path
        self.codePage = codePage

        self.p3270 = P3270Client(luName=self.luName, hostName=self.hostName, hostPort=self.hostPort,
                                 modelName=self.modelName, verifyCert=self.verifyCert, enableTLS=self.enableTLS,
                                 codePage=self.codePage, path=self.path, timeoutInSec=self.timeout)

    def connect(self):
        """ Connect to the host
        """
        return self.p3270.connect()

    def disconnect(self):
        """ Disconnect from host
        """
        return self.p3270.disconnect()

    def endSession(self):
        """ End the emulator script
        """
        return self.p3270.endSession()

    def sendEnter(self):
        """ Send Enter to host
        """
        return self.p3270.sendEnter()

    def sendBackTab(self):
        """ Send back tab (to go to the beginning previous field).
        """
        return self.p3270.sendBackTab()

    def sendTab(self):
        """ Send tab key (to go to the beginning of the next field).
        """
        return self.p3270.sendTab()

    def sendBackSpace(self):
        """ Send ASCII BS or move cursor to the left
        """
        return self.p3270.sendBackSpace()

    def delChar(self):
        """ Delete character under cursor
        """
        return self.p3270.delChar()

    def delField(self):
        """ Delete entire field.
        """
        return self.p3270.delField()

    def eraseChar(self):
        """ Erase previous character (or send ASCII BS).
        """
        return self.p3270.eraseChar()

    def moveCursorDown(self):
        """ Move cursor Down.
        """
        return self.p3270.moveCursorDown()

    def moveCursorUp(self):
        """ Move cursor Up.
        """
        return self.p3270.moveCursorUp()

    def moveCursorLeft(self):
        """ Move cursor left.
        """
        return self.p3270.moveCursorLeft()

    def moveCursorRight(self):
        """ Move cursor right.
        """
        return self.p3270.moveCursorRight()

    def moveTo(self, row, col):
        """ Move cursor to the position specified by (row,col) pair.
        """
        return self.p3270.moveTo(row=row, col=col)

    def moveToFirstInputField(self):
        """ Move cursor to the first input field.
        """
        return self.p3270.moveToFirstInputField()

    def sendText(self, text):
        """ Send text to host.
        """
        return self.p3270.sendText(text)

    def saveScreen(self, fileName='screen', dataType='html'):
        """ Save the current screen in the form of an HTML file.
        """
        return self.p3270.saveScreen(fileName=fileName, dataType=dataType)

    def getScreen(self):
        """ Get the content of the current screen as string
        """
        return self.p3270.getScreen()

    def printScreen(self):
        """ Print the current screen to stdout
        """
        return self.p3270.printScreen()

    def isConnected(self):
        """ Get the connection status.
            returns 'True' if connected, 'False' otherwise
        """
        return self.p3270.isConnected()

    def readTextAtPosition(self, row, col, length):
        """ Reads text at a row,col position and returns it
        """
        return self.p3270.readTextAtPosition(row=row, col=col, length=length)

    def readTextArea(self, row, col, rows, cols):
        """ Reads a textarea at a row,col position going down a number of rows and reading a number of cols
        """
        return self.p3270.readTextArea(row=row, col=col, rows=rows, cols=cols)

    def foundTextAtPosition(self, row, col, sent_text):
        return self.p3270.foundTextAtPosition(row=row, col=col, sent_text=sent_text)

    def trySendTextToField(self, text, row, col) -> bool:
        return self.p3270.trySendTextToField(text=text, row=row, col=col)

    def waitForField(self):
        return self.p3270.waitForField()

    def rollUp(self):
        return self.p3270.sendPF(8)

    def rollDown(self):
        return self.p3270.sendPF(7)

    def errorReset(self):
        return self.p3270.sendPF(10)

    def sendF(self, n):
        if 0 < n < 13:
            self.p3270.sendPA(1)
            return self.p3270.sendPF(n)
        elif 12 < n < 25:
            return self.p3270.sendPF(n)
        else:
            raise Exception("Only F1 to F24 is allowed")

    def connectAndLogin(self, user, pw):
        """ Connect to the host and login to base home screen
        """
        self.p3270.connect()
        self.sendText(user)
        self.sendTab()
        self.sendText(pw)
        for i in range(3):
            self.sendEnter()

        if self.readTextAtPosition(1, 2, 9) != 'MNS010/B4':
            return False
        else:
            return True

    def Logout(self):
        """Back out of all programs before logging out
        """
        while not self.readTextAtPosition(8, 25, 30) == 'Du är på väg att avsluta MOVEX':
            beforescreen = self.getScreen()
            self.sendF(3)
            if beforescreen == self.getScreen():
                beforescreen = self.getScreen()
                self.sendF(12)
                if beforescreen == self.getScreen():
                    return False
        self.sendEnter()
        self.disconnect()
        self.endSession()
        #print(f'{self.connection_name} disconnectad och avslutad')
        return True

    def RunProgram(self, Program):
        """Backs out of program and enters the new program automatically
        """
        while not self.readTextAtPosition(8, 25, 30) == 'Du är på väg att avsluta MOVEX':
            beforescreen = self.getScreen()
            self.sendF(3)
            if beforescreen == self.getScreen():
                beforescreen = self.getScreen()
                self.sendF(12)
                if beforescreen == self.getScreen():
                    return False

        self.sendF(3)
        self.trySendTextToField(Program, 20, 7)

        if not self.readTextAtPosition(1, 2, len(Program)) == Program:
            return False
        else:
            return True

    def GoHome(self):
        """Useless?? I'ma just gonna make it anyways
        """
        while not self.readTextAtPosition(8, 25, 30) == 'Du är på väg att avsluta MOVEX':
            beforescreen = self.getScreen()
            self.sendF(3)
            if beforescreen == self.getScreen():
                beforescreen = self.getScreen()
                self.sendF(12)
                if beforescreen == self.getScreen():
                    return False
        self.sendF(3)
        return True