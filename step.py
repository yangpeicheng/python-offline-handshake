import subprocess
import time

#os.popen("adb forward tcp:4444 localabstract:/adb-hub")
#os.popen("adb connect 127.0.0.1:4444")
subprocess.call("adb forward tcp:4444 localabstract:/adb-hub")
subprocess.check_call("adb connect 127.0.0.1:4444")
time.sleep(2)
output=subprocess.check_output("adb devices")
print(output)
subprocess.check_call("adb -s 127.0.0.1:4444 pull /storage/emulated/0/data E:\SensorData")
'''pipe=subprocess.Popen("adb -s 127.0.0.1:4444 shell",stdin=subprocess.PIPE, stdout=subprocess.PIPE)
cmds=[
    "rm -r /storage/emulated/0/data",
    "exit",
]
code=pipe.communicate("\n".join(cmds) + "\n")'''
time.sleep(2)
subprocess.check_call("adb disconnect 127.0.0.1:4444")
#subprocess.Popen("adb disconnect 127.0.0.1:4444")
#os.popen("adb -s 127.0.0.1:4444 shell")
#output=os.popen("ls")
