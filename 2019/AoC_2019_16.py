from tqdm import tqdm

def getFileLines(path):
	with open(path, "r") as file:
		return file.read().splitlines()

def partialSum(seq, start, bound):
	s = 0
	for i in range(start, bound):
		s += seq[i]
	return s

def nextSequence(seq):
	newSeq = []
	for rank in range(1, len(seq) + 1):
		start, s, m = rank - 1, 0, 1
		while start < len(seq):
			bound = min(start + rank, len(seq))
			s += m * partialSum(seq, start, bound)
			start = bound + rank
			m *= -1
		newSeq.append(abs(s) % 10)
	return newSeq

def runPhases(signalString, phasesNumber):
	seq = getSignal(signalString)
	for phase in tqdm(range(phasesNumber)):
		seq = nextSequence(seq)
	return formatAnswer(seq)

def getSignal(string):
	return list(map(int, list(string)))

def formatAnswer(seq):
	return ''.join(map(str, seq))


signalString = getFileLines('resources/input_16.txt')[0]
# print(signalString)

phasesNumber = 100
finalSeq = runPhases(signalString, phasesNumber)
print('\nAnswer 1: %s\n' % finalSeq[:8]) # 84487724

# ------------------------------------------
# Part 2:

# This works only because offset <= (len(seq) + 1) // 2
def runPhasesOffset(signalString, phasesNumber):
	offset = int(signalString[0:7])
	seq = getSignal(signalString[offset:]) # first values are not useful!
	for phase in tqdm(range(phasesNumber)):
		s = 0
		for i in range(len(seq)-1, -1, -1):
			s += seq[i]
			seq[i] = abs(s) % 10
	return formatAnswer(seq)

signalString = signalString * 10000

finalSeq = runPhasesOffset(signalString, phasesNumber)
print('\nAnswer 2: %s' % finalSeq[0:8]) # 84692524
