import statistics

a = [22,4080.0,1.6245023999999992,27,5116.0,2.135632100000001,17,3169.0,1.4807209999999993,37,6893.0,2.579833299999999,30,5616.0,2.1950239,27,5055.0,2.1003627999999996,26,4802.0,2.093892899999999,23,4381.0,1.7064711999999997,21,3956.0,1.6813514999999994,23,4289.0,1.9395910999999992,]

meanRounds = a[0::3]
meanPackets = a[1::3]
meanEnergy = a[2::3]

print(f"Rounds: {meanRounds}")
print(f"Packets: {meanPackets}")
print(f"Energy: {meanEnergy} \n")

meanRounds =  statistics.mean(meanRounds)
meanPackets = statistics.mean(meanPackets)
meanEnergy =statistics.mean(meanEnergy)

print(f"Mean Rounds: {meanRounds}")
print(f"Mean Packets: {meanPackets}")
print(f"Mean Energy: {meanEnergy}")