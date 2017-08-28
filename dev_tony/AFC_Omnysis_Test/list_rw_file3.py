def list_to_file(self, data, filename):
    length=len(data)
    file = open(str(filename), "w")
    for i in range (0,length):
        str1 = ''.join(str(data[i]))
        file.write(str1+"\n")
    file.close()