import sunau
import random
import sys

ADD_ZEROES = 0
DUP_SAMPLE = 1
DUP_PACKET = 2

if (len(sys.argv) != 4):
	print("command should be: python transmision_imitation.py <decode_style> <input_file> <output_file>")
	exit();
else:
	drop_setting = sys.argv[1]
	inname = sys.argv[2]
	outname = sys.argv[3]

# inname = "doors.au"
infile = sunau.open(inname, 'r')
# outname = inname.split('.')[0] + '_output.au'
print(outname)
outfile = sunau.open(outname, 'w')

channels, sampwidth, framerate, nframes,comptype, compname = infile.getparams()

print("input file", inname, "with", channels, "channels,", sampwidth, "sample width, and a framerate of", framerate)
print("file is", nframes, "frames (", nframes/(framerate*channels), "seconds)", "long with", comptype, "comptype and", compname, "compname")



outfile.setnchannels(channels)
outfile.setsampwidth(sampwidth)
outfile.setframerate(framerate)
outfile.setnframes(nframes)



#packet settings
packet_size = 100     #bytes
loss_rate = 0.05
drop_setting = ADD_ZEROES
zero_bytes = bytes([0x00]*1000)
# print(zero_bytes)
outdata = bytes()

for i in range(0, nframes, packet_size):
	packet = infile.readframes(packet_size)
	someval = random.random()
	if(i%1000000 ==0):
		print(i)
		# outfile.setnframes(i)
		outfile.writeframes(outdata)
		outdata = bytes()
	if (someval > loss_rate):
		outdata += packet
		prev_packet = packet
	else:
		if(drop_setting == ADD_ZEROES):
			outdata += zero_bytes
		elif(drop_setting == DUP_SAMPLE):
			outdata += bytes(prev_packet[packet_size-1] * packet_size)
			prev_packet = prev_packet
		elif(drop_setting == DUP_PACKET):
			outdata += prev_packet
			prev_packet = prev_packet
# outfile.setnframes(nframes)
outfile.writeframes(outdata)
	

	
infile.close()
outfile.close()