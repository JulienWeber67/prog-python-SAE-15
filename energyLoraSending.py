"""
    File : assess-sending-energy-lora.py
    Author : Sébastien Bindel
    email : sebastien.bindel@uha.fr
"""
import machine
import os
from network import LoRa
import socket
import pycom
import utime
import time
import ubinascii

# determine the maximal data size
def ComputeMaxDataSize(sprfa,bw):
    max_size = 0
    if bw == 125:
        if sprfa == 7 :
            max_size = 222
        elif sprfa == 8 :
            max_size = 222
        elif sprfa == 9 :
            max_size = 115
        elif sprfa == 10 :
            max_size = 51
        elif sprfa == 11 :
            max_size = 51
        elif sprfa == 12 :
            max_size = 51
    elif bw == 250 :
        if sprfa == 7 :
            max_size = 222
    return max_size

# create a message with the selected length
def create_mess(ln):
    mess = ubinascii.unhexlify(b'ff')
    return mess*ln

def StartLoRaTransmission (bwd, sprfa, cr, dbg):
    # declare variable
    display = "TIteration;TBlock;TMessGen;TMessSend;TDisplay;TOA;Essai;TxPower;SF;Bandwidth;CodingRate;Taille\n"
    info = ""
    infoLog = ""
    mess = ""
    data_max_size=0

    """ time variables related to time capture """
    begin_it = None
    time_blocking = None
    mess_generated_time = None
    send_mess = None

    """ variables related to the lora configuration """
    preamble_length=8

    """ Variables à modifier """
    taille=0
    data_max_size = ComputeMaxDataSize(sprfa,bwd)

    # Configure LED color (BLUE=LoRA)
    if bool(dbg) :
        print("LED is ON")
        pycom.heartbeat(False)
        pycom.rgbled(0x00007f)

    #Configure LORA connection
    lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

    if bwd == 125 :
        if cr == "4_8":
            lora.init(region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=sprfa, preamble=preamble_length, coding_rate=LoRa.CODING_4_8)
        elif cr == "4_7":
            lora.init(region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=sprfa, preamble=preamble_length, coding_rate=LoRa.CODING_4_7)
        elif cr == "4_6":
            lora.init(region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=sprfa, preamble=preamble_length, coding_rate=LoRa.CODING_4_6)
        elif cr == "4_5":
            lora.init(region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=sprfa, preamble=preamble_length, coding_rate=LoRa.CODING_4_5)
    elif bwd == 250 :
        if sprfa == 7 :
            if cr == "4_8":
                lora.init(region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ, sf=sprfa, preamble=preamble_length, coding_rate=LoRa.CODING_4_8)
            elif cr == "4_7":
                    lora.init(region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ, sf=sprfa, preamble=preamble_length, coding_rate=LoRa.CODING_4_7)
            elif cr == "4_6":
                    lora.init(region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ, sf=sprfa, preamble=preamble_length, coding_rate=LoRa.CODING_4_6)
            elif cr == "4_5":
                    lora.init(region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ, sf=sprfa, preamble=preamble_length, coding_rate=LoRa.CODING_4_5)

    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    #avoid overflow
    if taille > data_max_size:
        taille = data_max_size

    #Send Info
    while taille <= data_max_size:
        """ Begin Iteration """

        """ Block socket """
        s.setblocking(True)

        """ Generate message """
        print("data generation")
        mess = create_mess(taille) # generate message

        """ Send Mess """
        print("sending data")
        result = s.send(mess)
        print("end sending")

        if bool(dbg) :
            """ Catch sending info """
            info="TOA:"+str(lora.stats().tx_time_on_air)
            info+=",Essai:"+str(lora.stats().tx_trials)
            info+=",SF:"+str(lora.stats().sftx)
            info+=",BW:"+str(bwd)
            info+=",CR:"+str(cr)
            info+=",Taille:"+str(result)+"/"+str(data_max_size)+"\n"
            print(info)
        taille+=1
