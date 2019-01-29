import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import hashlib

sentinel = True
continue_reading = True


def end_read(signal=None, frame=None):
    global sentinel
    global continue_reading
    print ("ending read.")
    sentinel = False
    continue_reading = False
    GPIO.cleanup()

# This call the function with the cached uid as parametter and reduce the loop_counter.
# If loop_counter is 0, the loop will stop
def when_uid_cached(function, hashed_uid, loop_counter):
    if function:
	function(hashed_uid)
    if loop_counter >= 0:
	loop_counter -= 1
    return loop_counter == 0


def start_loop(function=None, loop_counter=0):
    global sentinel
    global continue_reading
    print("Reader working ...")
    signal.signal(signal.SIGINT, end_read)
    while sentinel:
	time.sleep(1)
        continue_reading = True
        MIFAREReader = MFRC522.MFRC522()
        while continue_reading:
            (detected,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            (status,uid) = MIFAREReader.MFRC522_Anticoll()
            if detected == MIFAREReader.MI_OK:
                print("Card detected")
            if status == MIFAREReader.MI_OK:
		string_uid = ''
                for e in uid:
		    string_uid += str(e)
		hashed_uid = hashlib.sha256(string_uid).hexdigest()
		print("hashed uid -> " + hashed_uid)
		continue_reading = False
		if when_uid_cached(function, hashed_uid, loop_counter):
		    end_read()


if __name__ == '__main__':
    start_loop()
