from AoC_2019_09 import *

def queueOutputs(nextPaquetsQueue, outputs, NATlastPacket, earlyStopping):
	for i in range(0, len(outputs), 3):
		address, x, y = outputs[i], outputs[i+1], outputs[i+2]
		if address in nextPaquetsQueue:
			nextPaquetsQueue[address].append([x, y])
		else:
			# print('Received a packet for unknown address %d:' % address, (x, y), '\n')
			if address == 255:
				if earlyStopping or NATlastPacket == [x, y]:
					print('Result:', y, '\n')
					return -1
				NATlastPacket[0] = x
				NATlastPacket[1] = y
	return outputs != []

def isNetworkIdle(paquetsQueue, computers):
	nothingReceived, computersNotSending = True, True
	for idx in paquetsQueue:
		if paquetsQueue[idx] != []:
			nothingReceived = False
			break
	for idx in computers:
		if computers[idx][2] == 1:
			computersNotSending = False
			break
	return nothingReceived and computersNotSending

def dispatchPackets(computers, paquetsQueue, earlyStopping=False):
	NATlastPacket = [0, 0]
	while True:
		if isNetworkIdle(paquetsQueue, computers):
			# print('Network is idle! Sending NAT last packet to address 0:', NATlastPacket, '\n')
			paquetsQueue[0].append(NATlastPacket[:])
		# print('Paquets queue:', paquetsQueue, '\n')
		for idx in paquetsQueue:
			if paquetsQueue[idx] == []:
				paquetsQueue[idx] = [[-1]]
			packet = paquetsQueue[idx][0]
			paquetsQueue[idx] = paquetsQueue[idx][1:]
			# Note: programs here are always waiting for inputs:
			outputs, newProg, currPos = run(computers[idx][0], packet, start=computers[idx][1])
			sending = queueOutputs(paquetsQueue, outputs, NATlastPacket, earlyStopping)
			computers[idx] = [newProg, currPos, sending] # changing internal states
			if sending == -1:
				return


inputFile = 'resources/input_23.txt'
stringInput = getFileLines(inputFile)[0]
# print(stringInput, '\n')
program = getInput(stringInput)
program += [0] * 1000

poolSize = 50
computers = { idx : [program, 0, 1] for idx in range(poolSize) }
paquetsQueue = { idx : [[idx]] for idx in computers }

dispatchPackets(computers.copy(), paquetsQueue.copy(), earlyStopping=True) # result: 21160

# ------------------------------------------
# Part 2:

dispatchPackets(computers.copy(), paquetsQueue.copy(), earlyStopping=False) # result: 14327
