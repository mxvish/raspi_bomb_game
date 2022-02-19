import wiringpi as pi
from so1602 import so1602

#Setting 7seg display in i2c#flag
i2c = pi.I2C()
seg = i2c.setup(0x71)#setup a device address
so1602_addr = 0x3c
so1602 = so1602( i2c, so1602_addr )

### 7seg function ###
def seg_reset():
    #Clear & display colon#
    i2c.write(seg, 0x76)
    i2c.write(seg, 0x77)
    i2c.write(seg, 0b00010000)

def seg_display(raw):
    #convert 10-decimal -> 60-decimal
    minute = raw//60
    second = raw%60

    #cutting each digit
    minute10 = minute//10
    minute1 = minute%10
    second10 = second//10
    second1 = second%10

    i2c.write(seg, 0x79)
    i2c.write(seg, 0x00)
    #display number#
    i2c.write(seg, minute10)
    i2c.write(seg, minute1)
    i2c.write(seg, second10)
    i2c.write(seg, second1)

def chara_display(line1,line2):
    so1602.move_home( i2c )
    so1602.set_cursol( i2c, 0 )
    so1602.set_blink( i2c, 0 )

    so1602.clear(i2c)
    so1602.move( i2c, 0, 0 )
    so1602.write( i2c, line1 )
    so1602.move( i2c, 0, 1 )
    so1602.write( i2c, line2 )

def chara_display_nihongo(line1,line2):
    so1602.move_home( i2c )
    so1602.set_cursol( i2c, 0 )
    so1602.set_blink( i2c, 0 )

    so1602.clear(i2c)
    so1602.move( i2c, 0, 0 )
    so1602.write_nihongo( i2c, line1 )
    so1602.move( i2c, 0, 1 )
    so1602.write_nihongo( i2c, line2 )
