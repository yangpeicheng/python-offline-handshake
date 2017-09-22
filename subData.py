import csv


def extract(m):
    start=85
    end=229
    new = m.split('.')[0] + "t.csv"
    output=open(new,'w',newline="")
    write=csv.writer(output)
    with open(m) as f:
        reader=csv.reader(f)
        index=0
        for line in reader:
            index+=1
            if index>start and index<end:
                write.writerow(line)

extract("E:\\SensorData\\pcatest\\masterlocal-9.csv")
extract("E:\\SensorData\\pcatest\\slavelocal-9.csv")


