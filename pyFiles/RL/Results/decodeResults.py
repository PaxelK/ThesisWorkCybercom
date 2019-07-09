import statistics

a = [1227,232998.0,43.75726220000102,639,121304.0,21.450398100000044,1084,205892.0,37.975007200000626,1158,219861.0,37.98235020000062,1162,220635.0,40.83622010000079,873,165788.0,29.7202129000003,1135,215605.0,40.055393600000585,942,178866.0,32.11251020000032,527,100006.0,17.648483099999996,893,169447.0,31.45061260000037,]
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