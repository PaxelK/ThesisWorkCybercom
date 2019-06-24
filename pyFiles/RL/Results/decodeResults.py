import statistics

a = [8341,593362.0,3978,341828.0,7933,382332.0,11631,568916.0,5965,459553.0,12971,472697.0,3802,359181.0,9015,331908.0,2686,294525.0,4834,358957.0,13877,606126.0,4923,406434.0,6216,491029.0,9354,491518.0,9654,390517.0,9513,343184.0,11937,529598.0,8315,459968.0,8974,565095.0,5662,480311.0]
meanRounds = a[0::2]
meanPackets = a[1::2]


meanRounds =  statistics.mean(meanRounds)
meanPackets = statistics.mean(meanPackets)

print(f"Mean Rounds: {meanRounds}")
print(f"Mean Packets: {meanPackets}")