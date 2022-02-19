import time
import unicodedata

class so1602:
    def __init__(self, i2c, ad ):
        self.ad = ad
        self.cursol = 1
        self.blink = 1
        self.display = 1
        self.x = 0
        self.y = 0

        self.so = i2c.setup( self.ad )

        time.sleep(0.1)
        i2c.writeReg8( self.so, 0x00, 0x01 )
        time.sleep(0.20)
        i2c.writeReg8( self.so, 0x00, 0x02 )
        time.sleep(0.02)
        i2c.writeReg8( self.so, 0x00, 0x0f )
        time.sleep(0.02)
        i2c.writeReg8( self.so, 0x00, 0x06 )
        time.sleep(0.02)
        i2c.writeReg8( self.so, 0x00, 0x01 )
        time.sleep(0.02)

    def clear(self, i2c):
        i2c.writeReg8( self.so, 0x00, 0x01)
        time.sleep(0.1)

    def set_display(self, i2c):
        buf = 0x08 + 0x04 * self.display + 0x02 * self.cursol + self.blink
        i2c.writeReg8( self.so, 0x00, buf)
        time.sleep(0.1)

    def set_cursol(self, i2c, buf):
        if buf != 0:
            buf = 1
        self.cursol = buf
        self.set_display( i2c )

    def set_blink(self, i2c,buf):
        if buf != 0:
            buf = 1
        self.blink = buf
        self.set_display(i2c)

    def move_home(self, i2c):
        self.x = 0
        self.y = 0
        i2c.writeReg8( self.so, 0x00, 0x01 )
        time.sleep(0.1)

    def move(self, i2c, mx, my):
        self.x = mx
        self.y = my
        if self.x < 0:
            self.x=0
        if self.x > 0x0f:
            self.x=0x0f
        if self.y < 0:
            self.y=0
        if self.y > 1:
            self.y=1
        oy = self.y * 0x20
        out = self.x + oy + 0x80
        i2c.writeReg8( self.so, 0x00, out )
        time.sleep( 0.1 )

    def write(self, i2c, buf):
        length = len(buf)
        i = 0
        while i < length:
            if self.x > 0x0f:
                if self.y == 0:
                    self.move( 0x00, 0x01 )
                else:
                    break
            out = ord( buf[i] )
            i2c.writeReg8( self.so, 0x40, out)

            self.x = self.x + 1
            i = i + 1

    def write_nihongo(self, i2c, buf):
        gozyuu = "をぁぃぅぇぉゃゅょっーあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわん゛゜"
        gozyuu_list = list(gozyuu)
        length = len(buf)

        i = 0
        while i < length:
            if self.x > 0x0f:
                if self.y == 0:
                    self.move( 0x00, 0x01 )
                else:
                    break
            if self.is_japanese(buf[i]) == True:
                for m in range(len(gozyuu_list)):
                    if buf[i] == gozyuu_list[m]:
                        out = 0xa6 + m
            else:
                out = ord( buf[i] )
            i2c.writeReg8( self.so, 0x40, out)

            self.x = self.x + 1
            i = i + 1

    def is_japanese(self,string):
        for ch in string:
            name = unicodedata.name(ch)
            if "HIRAGANA" in name:
                return True
        return False
