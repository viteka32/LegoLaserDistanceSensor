from utime import sleep_ms
import LPF2
from machine import I2C,Pin
import machine
from VL53L1X import VL53L1X

def ledCallback(timerInfo):
      if not lpf2.connected:
           led.toggle()
      print(value)
      
value = 0
 
led = Pin(17, mode=Pin.OUT)
led.on()
ledTimer = machine.Timer(-1, period=500, callback=ledCallback )

# Name, Format [# datasets, type, figures, decimals], 
# raw [min,max], Percent [min,max], SI [min,max], Symbol, functionMap [type, ?], view
mode0 = ['DISTANCE',[1,LPF2.DATA16,3,0],[0,900],[0,100],[0,900],'RAW',[LPF2.ABSOLUTE,0],True]
modes = [mode0]

txpin=20
rxpin=21   

pin1 = Pin(rxpin, mode=Pin.OUT)
pin1.on()
pin0 = Pin(txpin, mode=Pin.OUT)
pin0.off()

lpf2 = LPF2.LPF2(1, txpin,rxpin, modes, LPF2.SPIKE_Ultrasonic, timer = -1, freq = 50)    # SPIKE
#lpf2 = LPF2.LPF2(1, txpin,rxpin, modes, LPF2.Ev3_Utrasonic, timer = -1, freq = 50)    # EV3

lpf2.initialize()

# set laser xshut to value 1
pin_xShut = Pin(4, mode=Pin.OUT)
pin_xShut.on()
# set laser int to input
pin_int = Pin(6, mode=Pin.IN)
i2c = I2C(1, scl=Pin(11), sda=Pin(10), freq=100000)
print("Laser address:")
print(i2c.scan())
distanceSensor = VL53L1X(i2c)

# Loop
while True:
     try:
          if not lpf2.connected:
               lpf2.sendTimer.deinit()
               sleep_ms(200)
               lpf2.initialize()
               value = 0
          else:
               led.on()
               value = int(distanceSensor.read() / 10);
               lpf2.load_payload('Int16',[value])
               sleep_ms(20)
     except:
          lpf2.close() # clean up
          raise