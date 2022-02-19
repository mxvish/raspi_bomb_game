import ezSet
import func_bomb as fb
import subprocess as sp
import tkinter as tk
import wiringpi as pi
import random, time

### Frame function ###
def timer():
    timenum = int(init_time.get())
    if timenum > 0 and flag.val("timer_stop") == False:
        f.after(1000, timer)
        timenum -= 1
        buzzer()
        fb.seg_display(timenum)
        init_time.set(str(timenum))
    elif timenum <= 0:
        sce.now_scene("failed")

def button_start_clicked():
    flag.fal("timer_stop")
    sce.now_scene("locked")
    button_start['state'] = tk.DISABLED
    timer()

def button_stop_clicked():
    flag.tru("timer_stop")
    button_start['state'] = tk.NORMAL

def button_miss_herasu(num):
    if num > 0:
        num -= 1
        flag.set("miss_count",num)
        change_miss_lamps(num)

#################### Scene function
def scene_locked():
    fb.chara_display("Bomb Locked","")
    print("<message> scene locked now")

def scene_select():
    fb.chara_display("Next","")
    print("<message> choose setting")

def scene_nazo1():
    fb.chara_display("security mode","is activated...")
    time.sleep(2)
    print("<message> nazo1")
    fb.chara_display("To get driverKey","please operate")
    f.after(2000,nazo1_main)

def scene_nazo3():
    led_gre2.high()
    flag.tru("timer_stop")
    fb.chara_display("=== CLEAR!! ===","")
    time.sleep(1)
    print("<message> nazo3")

    buzzer_ex(0.05,10)
    fb.chara_display_nihongo("=== CLEAR!! ===","   ...し゛ゃないよ")
    flag.fal("timer_stop")
    time.sleep(2)
    fb.chara_display_nihongo("せいかい の こーと゛きって ね","ねたは゛れ した よね? ^o^")

def scene_failed():
    fb.chara_display("== EXPLODED!! ==","")
    button_stop_clicked()
    sp.call("mpg321 bomb1.mp3",shell=True)

def scene_clear():
    fb.chara_display("=== CLEAR!! ===","")
    sp.call("mpg321 announcement.mp3",shell=True)
    button_stop_clicked()

###################physical-button functioon
def dont_perm():
    fb.chara_display("You do not have","permission!!")
    f.after(3000,scene_select)

def deka_check_rising():
    if flag.val("deka_led") == False:
        flag.tru("deka_led")
        deka_check_led()

def deka_check_led():
    if flag.val("deka_led") == True:
        led_gre2.high()
        f.after(500,led_gre2.low)
        f.after(1000,deka_check_led)

def deka_check_false(args):
    flag.fal("deka_led")
    miss()

def deka_check_true(args):
    flag.fal("deka_led")
    sce.now_scene("nazo3")

def push_Button_check():
    f.after (100, push_Button_check)
    for i in range(len(PIN_list)):
        PIN_list[i].check_state()

def count(num):
    timenum = int(init_time.get())
    timenum += num
    init_time.set(str(timenum))

def buzzer():
    buzzer_PIN.high()
    f.after(100,buzzer_PIN.low)

def buzzer_ex(tim,ite):
    for i in range(ite):
        buzzer_PIN.high()
        time.sleep(tim)
        buzzer_PIN.low()
        time.sleep(tim)

#################### Nazo function
def random_pick(k):
    ns = []
    while len(ns) < k:
        n = random.randint(1,4)
        if not n in ns:
            ns.append(n)
    return ns

def nazo1_main():
    stage = flag.val("nazo1_stage")
    iro_list = ["green", "blue", "red", "orange"]

    code = random.randint(1,4)
    disp_num = random_pick(4)
    line1 = " step:" + str(stage) + " code:" + str(code)
    answer = ""

    if stage == 1:
        line2 = "1    2    3    4"
        fb.chara_display(line1,line2)
        answer = iro_list[code-1]

    elif stage == 2:
        line2 = str(disp_num[0]) +"    "+ str(disp_num[1])+"    "+ str(disp_num[2]) +"    "+ str(disp_num[3])
        fb.chara_display(line1,line2)
        index = disp_num.index(2)
        if index % 2 == 0:
            answer = iro_list[index+1]
        else:
            answer = iro_list[index-1]

    flag.set("nazo1_precode",code)
    flag.set("nazo1_answer",answer)

def nazo1_try(color):
    flag.set("nazo1_stage3",False)
    if color == flag.val("nazo1_answer"):
        sp.call("mpg321 correct1.mp3",shell=True)
        stage = flag.val("nazo1_stage")
        stage += 1
        flag.set("nazo1_stage",stage)

        if stage > 2:
            sce.now_scene("nazo3")
        else:
            nazo1_main()
    else:
        miss()
        nazo1_main()

def nazo1_stage3_try():
    if flag.val("nazo1_stage3") == True:
        miss()
        flag.set("nazo1_stage",1)
        flag.set("nazo1_stage3",False)
        nazo1_main()

def miss(*args):
    m = flag.val("miss_count")
    m += 1
    flag.set("miss_count",m)
    sp.call("mpg321 incorrect1.mp3",shell=True)
    print("<message> missed!")
    change_miss_lamps(m)

def change_miss_lamps(m):
    rightRedLED.high()
    centerRedLED.high()
    leftRedLED.high()
    if m == 4:
        sce.now_scene("failed")
    if m < 1:
        rightRedLED.low()
    if m < 2:
        centerRedLED.low()
    if m < 3:
        leftRedLED.low()

#####################Main Function#
#Flag Initialize#
flag = ezSet.class_flag()
flag_args = {"mode":0, "timer_stop": False, "push_check": True, "buzzer_ex":0, "miss_count":0, "nazo1_stage":1, "nazo1_precode":0, "nazo1_answer":0, "nazo1_stage3":False, "deka_led":False}
for x,y in flag_args.items():
    flag.set(x,y)

#Generating Window
fb.seg_reset()
f = tk.Tk()
la=tk.Label(f,text="=== timer ==")
la.grid(column=0,row=1)

#timer and buttons
init_time = tk.StringVar()
init_time.set("900")
entry = tk.Entry(f, textvariable = init_time)
entry.grid(column=0,row=2)
button_start = tk.Button(f, text = 'START', command = button_start_clicked)
button_start.grid(column=1,row=2)

button_stop = tk.Button(f, text = "STOP", command = button_stop_clicked)
button_stop.grid(column=2,row=2)

button_herasu = tk.Button(f, text = "herasu", command = lambda:button_miss_herasu(flag.val("miss_count")))
button_herasu.grid(column=1,row=3)

button_discount = tk.Button(f, text = "discount10", command = lambda:count(-10))
button_discount.grid(column=1,row=4)

button_count = tk.Button(f, text = "count20", command = lambda:count(20))
button_count.grid(column=2,row=4)

button_susumu = tk.Button(f, text = "susumu", command = lambda:sce.now_scene("nazo3"))
button_susumu.grid(column=2,row=3)

#Scene Setting#
sce = ezSet.scene("locked", "select", "nazo1", "nazo3", "clear", "failed")
scene_args = {scene_locked:"locked", scene_select:"select", scene_nazo1:"nazo1", scene_nazo3:"nazo3", scene_failed:"failed", scene_clear:"clear"}
for x,y in scene_args.items():
    sce.scene_func(x,y)

#Setting switch in GPIO#
pi.wiringPiSetupGpio()
led_gre1 = ezSet.GPIO_output(5,pi.LOW)
led_gre2 = ezSet.GPIO_output(6,pi.LOW)
rightRedLED = ezSet.GPIO_output(13,pi.LOW)
centerRedLED = ezSet.GPIO_output(19,pi.LOW)
leftRedLED = ezSet.GPIO_output(26,pi.LOW)
buzzer_PIN = ezSet.GPIO_output(21,pi.LOW)

sw_red = ezSet.GPIO_input(14, pi.LOW, sce,"DOWN")
sw_ora = ezSet.GPIO_input(15, pi.LOW, sce,"DOWN")
sw_gre = ezSet.GPIO_input(18, pi.LOW, sce,"DOWN")
sw_blu = ezSet.GPIO_input(23, pi.LOW, sce,"DOWN")
wi_ok = ezSet.GPIO_input(16, pi.HIGH, sce,"DOWN")
wi_ng = ezSet.GPIO_input(20, pi.HIGH, sce,"DOWN")
PIN_list = [sw_red,sw_ora,sw_gre,sw_blu,wi_ok,wi_ng]

#adding functions to pins
sw_red.func_set("locked", "Long_ex", sce.now_scene, ("select"), push_time=2, ex_func = miss)

color_pins = [sw_red, sw_ora, sw_gre, sw_blu]
select_funcs = [dont_perm, sce.now_scene, dont_perm, dont_perm]
select_func_args = ["", "nazo1", "", ""]
nazo1_try_args = ["red", "orange", "green", "blue"]

for x in range(len(color_pins)):
    color_pins[x].func_set("select", "Normal", select_funcs[x], select_func_args[x])
    color_pins[x].func_set("nazo1", "Normal", nazo1_try, nazo1_try_args[x])

wi_pins = [wi_ok, wi_ng]
wi_args = ["locked", "select", "nazo1"]
for pin in wi_pins:
    for arg in wi_args:
        pin.func_set(arg, "Normal", sce.now_scene, "failed")

wi_ok.func_set("nazo3", "Normal", sce.now_scene, "clear")
wi_ng.func_set("nazo3", "Normal", sce.now_scene, "failed")

fb.chara_display("setting up now", "...")
push_Button_check()
f.mainloop()
