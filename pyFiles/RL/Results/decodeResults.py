import statistics

a = [2197,300209.0,99.99999999999955,3196,386271.0,99.99999999999912,3658,441576.0,99.99999999999967,3500,442810.0,99.99999999999932,3374,409185.0,99.99999999999955,3793,456350.0,99.99999999999906,3130,428366.0,99.99999999999963,4481,512071.0,99.99999999999987,2531,341156.0,99.99999999999955,3725,442382.0,99.9999999999995,]
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