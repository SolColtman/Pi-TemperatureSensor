from guizero import App, MenuBar, Text, PushButton
import os
import time
import glob
import backend

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir='/sys/bus/w1/devices/'
device_folder=glob.glob(base_dir+'28*')[0]
device_file=device_folder+'/w1_slave'

def read_temp_raw():
    f=open(device_file, 'r')
    lines=f.readlines()
    f.close()
    return lines

def read_temp():
    lines=read_temp_raw()
    while lines[0].strip()[-3:]!='YES':
        time.sleep(0.2)
        lines=read_temp_raw()
    equals_pos=lines[1].find('t=')
    if equals_pos!=-1:
        temp_string=lines[1][equals_pos+2:]
        temp_c=float(temp_string)/1000.0
        temp_f=temp_c*9.0/5.0+32.0
        file=open("data.txt", "w")
        file.write(str(temp_c))
        file.close()
        return temp_c, temp_f

def file_function():
    app.destroy()

def refresh():
    read_temp()
    text.clear()
    file=open("data.txt", "r")
    f=str(file.readline())
    text.append(f+" °C")
    file.close()
    text2.clear()
    text2.append("Last updated at "+str(time.asctime( time.localtime(time.time()) ))[11:19])
    if float(f)>25 and float(f)<29:
        text3.clear()
        text3.append("Room is slightly too hot")
        text3.text_color=("orange")
    elif float(f)>29:
        text3.clear()
        text3.append("Room is way too hot")
        text3.text_color=("red")
    elif float(f)>20 and float(f)<32:
        text3.clear()
        text3.append("Room is perfect")
    else:
        text3.clear()
        text3.append("Room is too cold")
        text3.text_color=("blue")


app=App(title="Room Temperature", width=350, height=220, layout='auto')
menu=MenuBar(app, toplevel=["..."],options=[[["Exit Application", file_function]]])
text1=Text(app, text="Current Room Temperature")
text=Text(app, text="--°C", size=30)
text3=Text(app, text="--", size=10)
button=PushButton(app, text="Refresh", width=30, height=4, command=refresh)
text2=Text(app, text="")
app.display()
