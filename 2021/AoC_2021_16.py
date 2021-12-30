def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

def charToHexVal(char):
	idx = ord(char)
	if idx in range(48, 58):
		return idx - 48
	return idx - 55

def toBinary(val):
	l = []
	while val != 0:
		l.append(val % 2)
		val = val // 2
	while l == [] or len(l) % 4 != 0: # appendng trailing zeros
		l.append(0)
	l.reverse()
	return l

def toDecimal(bitList):
	s, m = 0, 1
	for i in range(len(bitList)-1, -1, -1):
		s += bitList[i] * m
		m *= 2
	return s

def buildHexaList(string):
	hexaList = []
	for char in string:
		if char != '\n':
			hexaList.extend(toBinary(charToHexVal(char)))
	return hexaList

def parse(hexaList, k=0, sumVersions=0):
	print('\n->', hexaList, '\n')
	if len(hexaList) < 11: # 11: smallest possible packet
		print('Packet too small, stopping:', hexaList)
		return 0, []
	values = []
	version = toDecimal(hexaList[:3])
	typeID = toDecimal(hexaList[3:6])
	sumVersions += version
	print('version:', version)
	print('typeID:', typeID)
	if typeID == 4: # literal value
		print('literal value')
		bitList = []
		for i in range(6, len(hexaList), 5):
			bitList.extend(hexaList[i+1:i+5])
			if hexaList[i] == 0: # trailing zeros remain
				break
		value = toDecimal(bitList)
		print('value:', value)
		start = i + 5
		if k == 0: # removing trailing zeros!
			while start % 4 != 0:
				print('trailing zero')
				start += 1
		values.append(value)
		packetsSumVersions, packetsValues = parse(hexaList[start:], k+1)
		values.extend(packetsValues)
	else: # operator
		print('operator')
		lengthTypeID = hexaList[6]
		print('lengthTypeID:', lengthTypeID)
		if lengthTypeID == 0: # total length mode
			print('total length mode')
			totalBitsLength = toDecimal(hexaList[7:22])
			print('totalBitsLength:', totalBitsLength)
			packetsSumVersions, packetsValues = parse(hexaList[22:22+totalBitsLength], k+1)
			sumVersions += packetsSumVersions
			values.append(applyOperator(typeID, packetsValues))
			packetsSumVersions, packetsValues = parse(hexaList[22+totalBitsLength:], k+1)
			values.extend(packetsValues)
		else: # packets number mode
			print('packets number mode')
			packetsNumber = toDecimal(hexaList[7:18])
			print('packetsNumber:', packetsNumber)
			packetsSumVersions, packetsValues = parse(hexaList[18:], k+1)
			values.append(applyOperator(typeID, packetsValues[:packetsNumber]))
			values.extend(packetsValues[packetsNumber:])
	sumVersions += packetsSumVersions
	return sumVersions, values

def applyOperator(typeID, values):
	if typeID == 0:
		return sum(values)
	elif typeID == 1:
		m = 1
		for val in values:
			m *= val
		return m
	elif typeID == 2:
		return min(values)
	elif typeID == 3:
		return max(values)
	elif len(values) != 2:
		print('Invalid length:', len(values))
		exit()
	elif typeID == 5:
		return int(values[0] > values[1])
	elif typeID == 6:
		return int(values[0] < values[1])
	elif typeID == 7:
		return int(values[0] == values[1])
	else:
		print('Insupported typeID:', typeID)
		exit()


# inputData = 'D2FE28'
# inputData = '38006F45291200'
# inputData = 'EE00D40C823060'
# inputData = '8A004A801A8002F478' # versions sum: 16
# inputData = '9C0141080250320F1802104A08' # produces 1, because 1 + 3 = 2 * 2.

inputData = getFileContent('resources/input_16.txt')

print('\ninputData:', inputData)

hexaList = buildHexaList(inputData)
# print(hexaList)

results = parse(hexaList)
print('\n\nResult 1:', results[0]) # 949

# ------------------------------------------
# Part 2:

print('\nResult 2:', results[1][0]) # 1114600142730
