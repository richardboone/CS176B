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
	drop_setting = int(sys.argv[1])
	inname = sys.argv[2]
	outname = sys.argv[3]

# inname = "doors.au"


packet_sizes = [100, 200, 400, 600, 800, 1000, 1200, 1500]
loss_rates = [0.005, 0.01, 0.02, 0.04, 0.08, 0.12, 0.16, 0.25, 0.36, 0.49, 0.64]


#packet settings
packet_size = 300     #bytes
loss_rate = 0.01
# drop_setting = ADD_ZEROES
zero_bytes = bytes([0x00]*1000)
# print(zero_bytes)
outdata = bytes()
finoutdata = bytes()
print("dropsetting:", drop_setting)
if (drop_setting != 4):
	infile = sunau.open(inname, 'r')
	print(outname)
	outfile = sunau.open(outname, 'w')

	channels, sampwidth, framerate, nframes,comptype, compname = infile.getparams()

	print("input file", inname, "with", channels, "channels,", sampwidth, "sample width, and a framerate of", framerate)
	print("file is", nframes, "frames (", nframes/(framerate*channels), "seconds)", "long with", comptype, "comptype and", compname, "compname")



	outfile.setnchannels(channels)
	outfile.setsampwidth(sampwidth)
	outfile.setframerate(framerate)
	outfile.setnframes(nframes)
	for i in range(0, nframes, packet_size):
		packet = infile.readframes(packet_size)
		someval = random.random()
		if(i%1000000 ==0):
			print(i)
			# outfile.setnframes(i)
			# outfile.writeframes(outdata)
			finoutdata += outdata
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
	outfile.writeframes(finoutdata)
	infile.close()
	outfile.close()
else: 
	print("hit else")
	for loss in loss_rates:
		for psize in packet_sizes:
			for drop_setting in [0, 1, 2]:
				infile = sunau.open(inname, 'r')
				outname = inname.split('.')[0] + '_output_' + 'loss' + str(int(loss*1000)) + 'psize' + str(psize) + 'dropset' + str(drop_setting) + '.au'
				print(outname)
				outfile = sunau.open(outname, 'w')
				channels, sampwidth, framerate, nframes,comptype, compname = infile.getparams()
				outfile.setnchannels(channels)
				outfile.setsampwidth(sampwidth)
				outfile.setframerate(framerate)
				outfile.setnframes(nframes)
				outdata = bytes()
				finoutdata = bytes()
				for i in range(0, nframes, psize):
					packet = infile.readframes(psize)
					someval = random.random()
					if(i%1000000 ==0):
						print(i)
						# outfile.setnframes(i)
						# outfile.writeframes(outdata)
						finoutdata += outdata
						outdata = bytes()
					if (someval > loss):
						outdata += packet
						prev_packet = packet
					else:
						if(drop_setting == ADD_ZEROES):
							outdata += zero_bytes
						elif(drop_setting == DUP_SAMPLE):
							outdata += bytes(prev_packet[len(prev_packet)-1] * psize)
							prev_packet = prev_packet
						elif(drop_setting == DUP_PACKET):
							outdata += prev_packet
							prev_packet = prev_packet
				outfile.writeframes(finoutdata)
				outfile.close()
				infile.close()


