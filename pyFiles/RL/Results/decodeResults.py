import statistics

a= [82,15589.0,2.836261299999998,61,11664.0,2.0675134999999987,66,12626.0,2.255070199999999,71,13733.0,2.6111554999999997,68,13046.0,2.505087799999999,71,13553.0,2.4996553999999978,41,7763.0,2.275476,57,10910.0,2.237700700000001,68,12963.0,2.417946099999998,74,14138.0,2.739277000000001,]

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