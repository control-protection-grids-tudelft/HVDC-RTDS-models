from selenium import webdriver
import winsound
import socket
import time
from selenium.webdriver.common.keys import Keys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


plotting = True

def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)

def on_launch(min_x, max_x, seen=True, figure=None, ax=None, ax1=None, ax2=None, ax3=None ):
    # Set up plot
    if not seen:
        figure, ((ax, ax1), (ax2, ax3)) = plt.subplots(2,2,figsize=(8, 10), layout="constrained")
    #subplot 1
    lines, = ax.plot([], [], 'o-', c='blue')
    ax.set_title('Active power at CSA2 ')
    ax.set_ylabel('Active Power (MW)')
    ax.set_xlabel('Time (s)')
    # subplot 2
    lines1, = ax1.plot([], [], 'o-', c='green')
    ax1.set_title('Wind speed near CSA2 ')
    ax1.set_ylabel('Wind Speed (m/s)')
    ax1.set_xlabel('Time (s)')

    lines2, = ax2.plot([], [], 'x-', c='blue')
    ax2.set_title('Active power at CSA3 ')
    ax2.set_ylabel('Active Power (MW)')
    ax2.set_xlabel('Time (s)')

    lines3, = ax3.plot([], [], 'x-', c='green')
    ax3.set_title('Wind speed near CSA3 ')
    ax3.set_ylabel('Wind Speed (m/s)')
    ax3.set_xlabel('Time (s)')

    move_figure(figure, 3015, 0)
    # Autoscale on unknown axis and known lims on the other
    ax.set_autoscaley_on(True)
    ax.set_xlim(min_x, max_x)
    ax1.set_autoscaley_on(True)
    ax1.set_xlim(min_x, max_x)
    ax2.set_autoscaley_on(True)
    ax2.set_xlim(min_x, max_x)
    ax3.set_autoscaley_on(True)
    ax3.set_xlim(min_x, max_x)
    # Other stuff
    if not seen:
        ax.grid()
        ax1.grid()
        ax2.grid()
        ax3.grid()
    return figure, ax, ax1, ax2, ax3, lines, lines1, lines2, lines3


def on_running(xdata, ydata, ydata1, ydata2, ydata3, figure, ax, ax1, ax2, ax3, lines, lines1, lines2, lines3 , min_x=-1, max_x=-1):
    # Update data (with the new _and_ the old points)
    lines.set_data(xdata, ydata)
    # Need both of these in order to rescale
    ax.relim()
    ax.autoscale_view()
    if min_x != -1:
        ax.set_xlim(min_x, max_x)
    # We need to draw *and* flush

    # Update data (with the new _and_ the old points)
    lines1.set_data(xdata, ydata1)
    # Need both of these in order to rescale
    ax1.relim()
    ax1.autoscale_view()
    if min_x != -1:
        ax1.set_xlim(min_x, max_x)

    # Update data (with the new _and_ the old points)
    lines2.set_data(xdata, ydata2)
    # Need both of these in order to rescale
    ax2.relim()
    ax2.autoscale_view()
    if min_x != -1:
        ax2.set_xlim(min_x, max_x)

    # Update data (with the new _and_ the old points)
    lines3.set_data(xdata, ydata3)
    # Need both of these in order to rescale
    ax3.relim()
    ax3.autoscale_view()
    if min_x != -1:
        ax3.set_xlim(min_x, max_x)

    # We need to draw *and* flush
    figure.canvas.draw()
    figure.canvas.flush_events()
    return figure, ax, ax1, ax2, ax3, lines, lines1, lines2, lines3

browser1 = webdriver.Chrome(r"C:\New folder\chromedriver_win32 (1)\chromedriver.exe") # Added path of chrome driver.
browser1.set_window_size(500, 800)
browser1.set_window_position(2000, 0)
browser2 = webdriver.Chrome(r"C:\New folder\chromedriver_win32 (1)\chromedriver.exe") # Added path of chrome driver.
browser2.set_window_size(500, 800)
browser2.set_window_position(2510, 0)
browser1.get("https://weatherfile.com/location?loc_id=GBR00129")  # opening website
browser2.get("https://weatherfile.com/location?loc_id=GBR00020")  # opening website
browser2.refresh()
browser2.refresh()
time.sleep(0.5)
temp_status1 = "None"
temp_status2 = 'None'
try:
    item_status1= browser1.find_element_by_xpath("//*[@id='meter_wind_avg']").text
    temp_status1 = item_status1
except:
    print(f"Shetland Islands is crushed proceeding with previous values {temp_status1}")
    item_status1 = temp_status1

item_status1 = ''.join([n for n in item_status1 if n.isdigit()])

try:
    item_status2= browser2.find_element_by_xpath("//*[@id='meter_wind_avg']").text
    temp_status2 = item_status2
except:
    print(f"Orkney Islands is crushed proceeding with previous values {temp_status1}")
    item_status2 = temp_status2

item_status2 = ''.join([m for m in item_status2 if m.isdigit()])


TCP_IP = '127.0.0.1'
TCP_PORT = 4575
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

if plotting:
    t = 0
    plt.ion()
    min_t = 0
    max_t = 10
    figure, ax, ax1, ax2, ax3, lines, lines1, lines2, lines3 = on_launch(min_t, max_t, seen=False)
    xdata = []
    ydata = []
    ydata1 = []
    ydata2 = []
    ydata3 = []

while(item_status1):
    print(f"Wind speed at Shetland Islands is {item_status1} m/s")
    print(f"Wind speed at Orkney Islands is {item_status2} m/s")
    #x = int(item_status,base = 10)*2

    x1 = int(item_status1,base = 10)
    x1 = x1
    try:
        message = str('SetSlider "Subsystem #1 : CTLs : Inputs : WT1WindSPD" = %f;' %x1)
        s.send(message.encode("utf-8"))
        s.send('SUSPEND 0.1;'.encode("utf-8"))
        s.send('temp_float = MeterCapture("WF1PGfilt");'.encode("utf-8"))
        s.send('sprintf(temp_string, "WF1PGfilt = %f END", temp_float);'.encode("utf-8"))
        s.send('ListenOnPortHandshake(temp_string);'.encode("utf-8"))
        tokenstring = s.recv(BUFFER_SIZE)
        tokenstring = str(tokenstring).split("= ")[1].split(" END")[0]
    except:
        message = str('SetSlider "Subsystem #1 : CTLs : Inputs : WT1WindSPD" = %f;' %x1)
        s.send(message.encode("utf-8"))
        s.send('SUSPEND 0.1;'.encode("utf-8"))
        s.send('temp_float = MeterCapture("WF1PGfilt");'.encode("utf-8"))
        s.send('sprintf(temp_string, "WF1PGfilt = %f END", temp_float);'.encode("utf-8"))
        s.send('ListenOnPortHandshake(temp_string);'.encode("utf-8"))
        tokenstring = s.recv(BUFFER_SIZE)
        tokenstring = str(tokenstring).split("= ")[1].split(" END")[0]

    print(f"Injected Active power at CSA2 is {tokenstring} MW")
    browser1.refresh()
    browser1.refresh()
    time.sleep(0.1)

    try:
        item_status1 = browser1.find_element_by_xpath("//*[@id='meter_wind_avg']").text
        temp_status1 = item_status1
    except:
        print(f"Shetland Islands is crushed proceeding with previous values {temp_status1}")
        item_status1 = temp_status1

    item_status1 = ''.join([n for n in item_status1 if n.isdigit()])

    y = int(item_status2,base = 10)
    y = y
    try:
        message1 = str('SetSlider "Subsystem #1 : CTLs : Inputs : WT12WindSPD" = %f;' %y)
        s.send(message1.encode("utf-8"))
        s.send('SUSPEND 0.1;'.encode("utf-8"))
        s.send('temp_float1 = MeterCapture("WF12PGfilt");'.encode("utf-8"))
        s.send('sprintf(temp_string1, "WF12PGfilt = %f END", temp_float1);'.encode("utf-8"))
        s.send('ListenOnPortHandshake(temp_string1);'.encode("utf-8"))
        tokenstring1 = s.recv(BUFFER_SIZE)
        tokenstring1 = str(tokenstring1).split("= ")[1].split(" END")[0]
    except:
        message1 = str('SetSlider "Subsystem #1 : CTLs : Inputs : WT12WindSPD" = %f;' %y)
        s.send(message1.encode("utf-8"))
        s.send('SUSPEND 0.1;'.encode("utf-8"))
        s.send('temp_float1 = MeterCapture("WF12PGfilt");'.encode("utf-8"))
        s.send('sprintf(temp_string1, "WF12PGfilt = %f END", temp_float1);'.encode("utf-8"))
        s.send('ListenOnPortHandshake(temp_string1);'.encode("utf-8"))
        tokenstring1 = s.recv(BUFFER_SIZE)
        tokenstring1 = str(tokenstring1).split("= ")[1].split(" END")[0]

    print(f"Injected Active power at CSA3 is: {tokenstring1} MW")
    browser2.refresh()
    browser2.refresh()
    time.sleep(0.1)
    try:
        item_status2 = browser2.find_element_by_xpath("//*[@id='meter_wind_avg']").text
        temp_status2 = item_status2
    except:
        print(f"Orkney Islands is crushed proceeding with previous values {temp_status2}")
        item_status2 = temp_status2
    item_status2 = ''.join([m for m in item_status2 if m.isdigit()])

    if plotting:
        xdata.append(t)
        ydata.append(float(tokenstring))
        ydata1.append(float(x1))
        ydata2.append(float(tokenstring1))
        ydata3.append(float(y))

        t = t + 1
        if t>=max_t:
            figure, ax, ax1, ax2, ax3, lines, lines1, lines2, lines3 = on_running(xdata, ydata, ydata1, ydata2, ydata3, figure, ax, ax1, ax2, ax3, lines, lines1, lines2, lines3, min_x=t-max_t, max_x=t+1)
        else:
            figure, ax, ax1, ax2, ax3, lines, lines1, lines2, lines3 = on_running(xdata, ydata, ydata1, ydata2, ydata3, figure, ax, ax1, ax2, ax3, lines, lines1, lines2, lines3)
