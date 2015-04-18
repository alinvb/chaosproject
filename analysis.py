# chaosproject
Project to analyze chaotic motion in salsa dance movements 
from pylab import *
from matplotlib.pyplot import *
from scipy.fftpack import fft, fftfreq
from numpy import *
import os
import argparse
import subprocess

p = argparse.ArgumentParser(description = " The files with the position vs time information")

p.add_argument("files", metavar='DIR', nargs='+')
args = p.parse_args()
subfile_list = args.files

for file in subfile_list:
    data = loadtxt(str(file), unpack = True, skiprows = 8)
    file_name = file.split('.')
    time = data[0]
    coord = data[1:]
    i = 1
    for coordinate in coord:
        y = coordinate
        N = y.size
        yfft = fft.fft(y, N)
        yfft = abs(yfft)/N
        freq = 60.0
        freqs = fft.fftfreq(N, 1./freq)
        freqs = freqs[:floor(N/2)]
        yfft = yfft[:floor(N/2)]
        plot(time, coordinate)
        xlabel("time(s)")
        ylabel("position(mm)")
	savefig(str(i) + file_name[0] +"time.png")
        clf()
        plot(freqs,abs(log(yfft)))
        xlabel("frequency(Hz)")
        ylabel("log(power)")
        savefig(str(i) + file_name[0] + "fft.png")
	clf()
        filename = str(i) + file_name[0] + "position.txt"
        outfile = open(str(i) + file_name[0] + "position.txt", 'w')
        for value in coordinate:
            outfile.write(str(value))
            outfile.write("\n")
        outfile.close()

        
        s = "./minfo -b 6 -t 200"
        s = s.split()
        newfile = str(i) + file_name[0] + ".mi"

        cmd = cmd = s + [str(filename), ">", "/Users/aliyababul/desktop/timeser" + newfile]
        with open(str(newfile), 'w') as f:
            subprocess.call(cmd, stdout=f)
        information = loadtxt(newfile ,delimiter=' ',unpack= True)
        inf = information[1]
        delaytime = information[0]
        plot(delaytime, inf)
        ylabel("information(bits)")
        xlabel("delay time(s)")
	savefig(str(i) + file_name[0] +"information.png")
        clf()
        i = i + 1



    x = array(data[1])
    y = array(data[2])
    z = array(data[3])


    vel_x  = np.empty(len(x))
    vel_y = np.empty(len(y))
    vel_z = np.empty(len(z))
    vel_x.fill(0.0)
    vel_z.fill(0.0)
    vel_y.fill(0.0)
        
    vel_x[0] = x[0]/time[1]
    vel_y[0] = y[0]/time[1]
    vel_z[0] = z[0]/time[1]
        
    j = 1
    i = 1
    xyz = open("xyz" + file_name[0] + ".txt", 'w')
    xyz.write(str(x[0]) + "  " + str(y[0]) + "    " + str(z[0]))
    xyz.write("\n")
    #calculate velocity
    while j < len(time):
        vel_x[j] = (x[j]- x[j-1])/(time[j]- time[j-1])
            
        vel_y[j] = (y[j]- y[j-1])/(time[j]- time[j-1])
            
        vel_z[j] = (z[j]- z[j-1])/(time[j]- time[j-1])
        xyz.write(str(x[j]) + "  " + str(y[j]) + "    " + str(z[j]))
        xyz.write("\n")
        
        j = j + 1
    
    xyz.close()


    vel_x = array(vel_x)
    vel_y = array(vel_y)
    vel_z = array(vel_z)

#v_total = (vel_x**2 + vel_y**2 + vel_z**2)**(0.5)
#position_total = (x**2 + y**2 + z**2)

    plot(x, vel_x)
    savefig(file_name[0] + "phasespace_x.png")
    xlabel("position(mm)")
    ylabel("velocity(mm/s)")
    clf()
    plot(y, vel_y)
    xlabel("position(mm)")
    ylabel("velocity(mm/s)")
    savefig(file_name[0] + "phasespace_y.png")
    clf()
    plot(z, vel_z)
    xlabel("position(mm)")
    ylabel("velocity(mm/s)")
    savefig(file_name[0] + "phasespace_z.png")
    clf() 







