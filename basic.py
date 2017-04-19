import serial
import math
import matplotlib.pyplot as plt

"""
ser = serial.Serial(
    port='COM3', \
    baudrate=9600, \
    parity=serial.PARITY_NONE, \
    stopbits=serial.STOPBITS_ONE, \
    bytesize=serial.EIGHTBITS, \
    )

print("connected to: " + ser.portstr)
"""
area = 0
perimeter = 0
i = 0

left, width = .25, .5
bottom, height = .5, .5
right = left + width
top = bottom + height

fig = plt.figure()
fig.suptitle('Wall Scanner 1.6', fontsize=14, fontweight='bold' )

ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.85)
ax.set_title('The Shape')

ax.set_xlabel('centimeters')
ax.set_ylabel('centimeters')

data1 = open("data1.txt", "w")
data2 = open("data2.txt", "w")
while True:

    #-------------Get input from the sensor-----------------------
    #s = ser.readline()

    test = ("b'1000,%d\r\n" %i)
    s = test
    r_str, degree_str = (str(s).replace("\\", "").replace("rn", "").replace("b", "").replace("'", "").split(','))

    if r_str == "off" or degree_str == "off":
        print("off mode\n")
        continue
    r = int(r_str)/10
    degree = int(degree_str)/10

    i=i+14

    #--------------Writing data to text file-----------------------
    if float(degree) < 360 or i < 258:
        x = round(float(r)*math.cos(math.pi/180*(degree)),1)
        y = round(float(r)*math.sin(math.pi/180*(degree)),1)
        data1.write("%s %s %.1f\n" %(x, y, degree))
        print("1st: r = %.1f cm  degree = %.1f || x = %.3f y = %.3f" % (r, degree, x, y))
        if float(degree) >= 359:
            print(float(degree))
            data1.close()
    elif float(degree) <= 721:
        if float(degree) <= 359.8:
            continue
        degree2 = 361-degree
        x = round(float(r)*math.cos(math.pi/180*(degree2)),3)
        y = round(float(r)*math.sin(math.pi/180*(degree2)),3)
        degree_ini = degree2 + 360
        data2.write("%s %s %.1f\n" % (x, y, degree_ini))
        print("2nd: r = %.1f cm  degree = %.1f || x = %.3f y = %.3f" % (r, degree_ini, x, y))
    if float(degree) >= 720:
            data2.close()
            break
    #-----------------------------------------------------------------

#ser.close()

#-------------Data convertion-------------------
data1 = open("data1.txt", "r")
data2 = open("data2.txt", "r")
data3 = open("data3.txt", "w")
for line in reversed(data2.readlines()):
    x2, y2, d2 = line.rstrip().split(" ")
    x1, y1, d1 = data1.readline().split(" ")
    if(float(d1) == float(d2)):
        x_f = 0.5*(float(x1) + float(x2))
        y_f = 0.5*(float(y1) + float(y2))
        data3.write("%.3f %.3f\n" % (x_f, y_f))
    else:
        continue

data1.close()
data2.close()
data3.close()

#----------------Drawing a graph and Calculating the Area&Perimeter----
data3 = open("data3.txt", "r")
i = 0

x1=y1=x0=y0=0
for line in data3.readlines():

    x_text, y_text = line.split(" ")
    x = float(x_text)
    y = float(y_text)

    plt.plot(x, y, '.r-')

    if int(i) > 0:
        area += math.fabs(x1*y - y1*x)
        perimeter += math.sqrt((y-y1)*(y-y1)+(x-x1)*(x-x1))

    x1 = x
    y1 = y

    if int(i) == 0:
        x0 = x
        y0 = y
        i = 1

area += math.fabs(x1*y0 - y1*x0)
perimeter += math.sqrt((y0-y1)*(y0-y1)+(x0-x1)*(x0-x1))
print("--------------        Complete        --------------\n\n")

data3.close()
finalArea = (round(0.5*area, 3))
finalPerimeter = (round(perimeter, 3))

textArea = 'Area         = %.3f $cm^2$' % (finalArea)
textPerimeter = 'Perimeter = %.3f cm' % (finalPerimeter)

#----------------Show the graph----------------------
ax.text(0.5*(left+right), 0.4*(bottom+top), textArea,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=10,
        transform=ax.transAxes)

ax.text(0.5*(left+right), 0.3*(bottom+top), textPerimeter,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=10,
        transform=ax.transAxes)

plt.grid()
plt.axis('scaled')
plt.show()