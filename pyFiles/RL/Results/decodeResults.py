import statistics

a =[71,13652.0,2.5118605999999972,58,11002.0,2.2352497999999983,73,14033.0,2.488763899999999,71,13615.0,2.5935568999999976,68,12899.0,2.443512799999998,76,14455.0,2.7151884999999987,66,12512.0,2.376595999999999,61,11645.0,2.5828834,33,6315.0,1.5445771000000001,42,7834.0,1.6736417000000001,]

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