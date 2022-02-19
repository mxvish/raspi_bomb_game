import wiringpi as pi

class GPIO_input():
    def __init__(self, PIN_number, default_state,scene_name,res = 0):
        self.PIN = PIN_number
        self.default_state = default_state
        self.push_check = 0
        self.push_check_ex = 0
        self.scene_name = scene_name
        self.now = scene_name.now_scene_get()
        pi.pinMode(self.PIN, pi.INPUT)

        if default_state != pi.HIGH and default_state != pi.LOW:
           print("GPIO_input(PIN:%s) is wrong" % self.PIN)

        if res == "UP":
            pi.pullUpDnControl(self.PIN, pi.PUD_UP)
        elif res == "DOWN":
            pi.pullUpDnControl(self.PIN, pi.PUD_DOWN)

        self.mode_dic = {}
        self.func_dic = {}
        self.args_dic = {}
        self.opti1_dic = {}
        self.opti2_dic = {}
        self.opti3_dic = {}

    def func_set(self, sce, mode, func, func_args ="", push_time = None, ex_func = None,rising_func = None ):
        self.mode_dic[sce] = mode
        self.func_dic[sce] = func
        self.args_dic[sce]= (func_args)

        if mode == "Long" and push_time != None:
            self.opti1_dic[sce] = push_time
        elif mode == "Long" and push_time == None:
            print("LONG func set(PIN:%s) is wrong" % self.PIN)

        if mode == "Long_ex" and push_time != None and ex_func != None:
            self.opti1_dic[sce] = push_time
            self.opti2_dic[sce] = ex_func
            self.opti3_dic[sce] = rising_func
        elif mode == "Long_ex" and (push_time == None or ex_func == None):
            print("LONG_ex func set(PIN:%s) is wrong" % self.PIN)

    def check_state(self):

        if self.now != self.scene_name.now_scene_get():
            self.clear_flag()
            self.now = self.scene_name.now_scene_get()

        mode = self.mode_dic.get(self.now)
        func = self.func_dic.get(self.now)
        args = self.args_dic.get(self.now)
        opti1 = self.opti1_dic.get(self.now)
        opti2 = self.opti2_dic.get(self.now)
        opti3 = self.opti3_dic.get(self.now)

        if mode == "Normal":
            self.normal_check(func, args)
        elif mode == "Long":
            self.long_check(func, opti1 ,args)
        elif mode == "Long_ex":
            self.long_ex_check(func, opti1 ,opti2, opti3, args)
        elif mode == "No_touch":
            self.no_touch_check()
        elif mode == "rise_and_fall":
            self.rise_and_fall_check(func, args)

    def normal_check(self,func, args):
        state = pi.digitalRead(self.PIN)
        if state != self.default_state:
            if self.push_check == 0:
                self.handler(func, args)
            self.push_check = 1
        else:
            self.push_check = 0

    def long_check(self,func, push_time, args):
        state = pi.digitalRead(self.PIN)
        if state != self.default_state:
            if self.push_check >= push_time:
                self.handler(func, args)
                self.push_check = 0
            elif self.push_check < push_time:
                self.push_check += 0.1
                print(self.push_check)
        else:
            self.push_check = 0

    def long_ex_check(self,func, push_time,ex_func,rising_func, args):
        state = pi.digitalRead(self.PIN)
        if state != self.default_state:
            if rising_func != None and self.push_check == 0:
                self.handler(rising_func, "")
            self.push_check += 0.1
            self.push_check_ex = 1
            print(self.push_check)
        else:
            if self.push_check_ex == 1:

                if self.push_check > (push_time -1) and self.push_check < (push_time +1):
                    self.handler(func, args)
                else:
                    self.handler(ex_func, args)
                self.push_check = 0
                self.push_check_ex = 0

    def rise_and_fall_check(self,func, args):
        state = pi.digitalRead(self.PIN)
        if self.push_check_ex == 0:
            self.push_check = state
            self.push_check_ex = 1

        if self.push_check_ex != 0 and state != self.push_check:
            self.handler(func,args)
            if self.push_check == pi.HIGH:
                self.push_check = pi.LOW
            elif self.push_check == pi.LOW:
                self.push_check = pi.HIGH

    def handler(self, func, args):
        if type(args) == tuple:
            func(*args)
        elif args == "":
            func()
        else:
            func(args)

    def clear_flag(self):
        self.push_check = 0
        self.push_check_ex = 0

class GPIO_output():
    def __init__(self, PIN_number, default_state):
        self.PIN = PIN_number
        self.default_state = default_state
        pi.pinMode(self.PIN, pi.OUTPUT)

        if default_state == pi.HIGH or default_state == pi.LOW:
            pi.digitalWrite(self.PIN, default_state)
        else:
           print("GPIO_output(PIN:%s) was wrong" % self.PIN)

    def high(self):
        pi.digitalWrite(self.PIN, pi.HIGH)

    def low(self):
        pi.digitalWrite(self.PIN, pi.LOW)

class class_flag():
    def __init__(self):
        self.dic = {}

    def set(self, key, item):
        self.dic[key] = item

    def tru(self, key):
        if type(self.dic[key]) == bool:
            self.dic[key] = True
        else:
            print("%s is not boolean" % key)

    def fal(self, key):
        if type(self.dic[key]) == bool:
            self.dic[key] = False
        else:
            print("%s is not boolean" % key)

    def val(self, key):
        return self.dic[key]

class scene():
    def __init__(self,*args):
        self.name_list = [*args]
        self.func_dic = {}
        self.now_scene(self.name_list[0])

    def now_scene(self, nex):
        self.now_sce = nex
        self.scene_func_monitor()

    def now_scene_get(self):
        return self.now_sce

    def scene_func(self, func, nex):
        self.func_dic[nex] = func

    def scene_func_monitor(self):
        if self.now_sce in self.func_dic:
            self.func_dic[self.now_sce]()
