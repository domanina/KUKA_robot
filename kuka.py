import tarfile
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import shutil

tar = tarfile.open("kuka_robot.log.tar.gz")
tar.extractall(path="./temp")

timeData = []
globalStatesData = []
statesData = []
targetsData = []
deltasData = []

with open("./temp/kuka_robot.log", "r") as kukaLog:
    for i, line in enumerate(kukaLog):
        if line.find("state.ts") != -1:
            params = line.split(";")

            currentTime = datetime.strptime(params[0], "%Y-%m-%d %H:%M:%S.%f")
            timeData.append(currentTime)

            currentGlobalState = int(params[5].split("=")[1])
            globalStatesData.append(currentGlobalState)
            currentStates = [float(parameter.split("= ")[1]) for parameter in params[6:12]]
            statesData.append(currentStates)
            currentTargets = [float(parameter.split("= ")[1]) for parameter in params[12:]]
            targetsData.append(currentTargets)
            currentDeltas = [currentStates[y] - currentTargets[y] for y in range(6)]
            deltasData.append(currentDeltas)
        else:
            continue

# удаление временной папки
#try:
#    shutil.rmtree("./temp")
#except OSError as e:
#    print("Error: %s - %s." % (e.filename, e.strerror))

#Для графика начинаю считать время с нуля (первое время в логе ставлю стартом)
startMoment = timeData[0]
timeDataInSec = [(times - startMoment).total_seconds() for times in timeData]

for i in range(6):
    fig = plt.figure(figsize=(13, 7))
    fig.suptitle("Joint A{}".format(i+1))
    js = fig.add_subplot(311)
    js.set_xlabel("Time, sec")
    js.set_ylabel("Angle, rad")
    js.plot(timeDataInSec, [joint[i] for joint in statesData], color="b")

    js = fig.add_subplot(312)
    js.set_xlabel("Time, sec")
    js.set_ylabel("Angle, rad")
    js.plot(timeDataInSec, [joint[i] for joint in targetsData], color="r")

    jd = fig.add_subplot(313)
    jd.set_xlabel("Time, sec")
    jd.set_ylabel("Diff: state - target, rad")
    jd.plot(timeDataInSec, [joint[i] for joint in deltasData], color="g")
    plt.show() # вывод сразу на экран, а не в файл
    #plt.savefig('Joint A{}.png'.format(i+1))


