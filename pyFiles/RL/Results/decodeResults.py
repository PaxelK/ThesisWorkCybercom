import statistics

a=[4,612.0,0.10941332652510048,2,444.0,0.0854225,3,393.0,0.07877214603492869,1,199.0,0.036280499999999986,2,422.0,0.07841380069071294,1,244.0,0.0398395,1,226.0,0.0447022,2,398.0,0.0772123,1,166.0,0.02943679999999999,2,411.0,0.0722944664218718,]

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