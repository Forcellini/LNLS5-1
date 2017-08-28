def list_to_file_aux(self, data, filename):
    length=len(data)
    file = open(str(filename), "w")
    for i in range (0,length):
        str1 = ''.join(str(data[i]))
        file.write(str1+"\n")
    file.close()

    '''def list_to_file(self, data, filename):
    length=len(data)
    file = open(str(filename), "w")
    for i in range (0,length):
        str1 = ''.join(str(data[i]))
        str1=str1.replace("]], ","");
        str1=str1.replace("[","");
        str1=str1.replace("]","");
        str1=str1.replace(",","");
        str1=str1.replace(")","");
        str1=str1.replace("(","");
        str1=str1.replace("'","");
        str1=str1.replace("\n"," ");
        file.write(str1+"\n")
    file.close()'''

