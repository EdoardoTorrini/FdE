from threading import Thread
from datetime import datetime
import serial, os


class ReadSerial(Thread):
    
    def __init__(self, cFather, sName, sPort, nBdRate, nTimeOut, nByteSize,
                 nPar=serial.PARITY_NONE, nStopBit=serial.STOPBITS_ONE, bEnLog=False):

        super(ReadSerial, self).__init__()

        #   class father (caller)
        self.cFather = cFather
        #   attributo classe 'thread'
        self.name = sName
        #   true -> terminal thread
        self.bStopThread = False

        #   Pyserial attributes
        self.sPort = sPort
        self.nBdRate = nBdRate
        self.nTimeOut = nTimeOut
        self.nByteSize = nByteSize
        self.nPar = nPar
        self.nStopBit = nStopBit
        self.bEnLog = bEnLog

        # gestione per i log
        self.sPath = os.path.dirname(os.path.realpath(__file__))

        self.sErr = ""
        self.bAlive = False

        #   dichiarazione oggetto connessione seriale (None, verrà inizializzato)
        self.serPort = None
        self.connection()

    def run(self):

        print("Starting Thread:", self.name)
        sLog, sErr, data = "", "", ""

        if self.serPort.is_open:

            while 1:

                bErr = False

                try:
                    if self.bStopThread:
                        self.disconnect()
                        break

                    # leggo i dati dalla porta seriale e gli decodifico in latin1 - perché è scritto su internet
                    data = self.serPort.read(255).decode("latin1")

                    if data != "":

                        nPosEnd = data.find("\0")
                        sData = int(data[:nPosEnd].split("-")[0])

                        self.cFather.changeColor(sData)

                except Exception as sVal:
                    self.sErr = sVal
                    bErr = True

                    self.serPort.close()
                    self.connection()

                if bErr:
                    sErr = self.sErr

                sNow = datetime.now()
                sLog = "DATE:{}|PORT:{}|MESSAGE:{}|ERROR:{}\n".format(sNow.strftime("%d-%m-%Y %H:%M:%S"), self.sPort, data, sErr)
                self.log(sLog)

        else:
            self.connection()

    def log(self, sData):

        if sData != "" and self.bEnLog is True:
            if os.path.isdir(self.sPath):

                if os.path.exists(self.sPath + "\log.txt"):
                    if os.path.getsize(self.sPath + "\log.txt") > 10485760:
                        os.remove(self.sPath + "\log.txt")

                with open(self.sPath + "\log.txt", "a+") as file:
                    file.write(sData)

    def connection(self):

        #   Porta inizializzata
        if self.serPort is not None:

            #   Porta NON aperta
            if not self.serPort.is_open:

                #   oggetto serial definizione -> instaura connessione effettiva con l'STM
                try:
                    self.serPort = serial.Serial(
                        self.sPort, baudrate=self.nBdRate, timeout=self.nTimeOut, bytesize=self.nByteSize,
                        parity=self.nPar, stopbits=self.nStopBit
                    )

                except Exception as sVal:
                    self.sErr = sVal
                    self.connection()

            #   error raised in run() --> re-connection
            else:
                #   chiude
                self.serPort.close()
                #   riapre
                self.connection()

        #   Porta NON inizializzata --> inizializzare
        else:
            try:

                self.serPort = serial.Serial(
                    self.sPort, baudrate=self.nBdRate, timeout=self.nTimeOut, bytesize=self.nByteSize,
                    parity=self.nPar, stopbits=self.nStopBit
                )

            except Exception as sVal:

                self.sErr = sVal

    def disconnect(self):

        print("Ending Thread:", self.name)

        if self.serPort is not None:
            if self.serPort.is_open:
                self.serPort.close()

