from subprocess import Popen, PIPE
#from list_rw_file2 import list_to_file

def crate_data_acquisition(IP_CRATE,POSITION_CRATE,POSITION_ADC,NUM_PONTS_CRATE,MAX_CONTAGEM_ADC):

    local = "cd CRATE_ACESSO/bpm-app/.halcs-libs/examples\n"
    comando = "./acq -b tcp://"+str(IP_CRATE)+":8978 -o "+str(POSITION_CRATE)+" -s "+str(POSITION_ADC)+" -c 0 -n "+str(NUM_PONTS_CRATE)

    command_stdout = Popen(local+comando,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
    command_stdout=command_stdout.splitlines()
    #print(command_stdout)
    #print(comando)  
    
    channel_1_num_array=[]
    channel_2_num_array=[]
    channel_3_num_array=[]
    channel_4_num_array=[]

    i=0
    for i in range (1, NUM_PONTS_CRATE+1):
        y=command_stdout[i].decode("utf-8")
        nums = [int(n) for n in y.split()]
        channel_1_num_array.append(nums[0])
        channel_2_num_array.append(nums[1])
        channel_3_num_array.append(nums[2])
        channel_4_num_array.append(nums[3])
        
    
    crate_data=[channel_1_num_array,channel_2_num_array,channel_3_num_array,channel_4_num_array]
    
    #Exporta os dados do crate para arquivo txt
    #list_to_file(0,channel_1_num_array,'/home/tadeu/Desktop/output.csv')
    #print("Exportou os dados do crate")
    
    channel_1_crate_to_volts=[]
    channel_2_crate_to_volts=[]
    channel_3_crate_to_volts=[]
    channel_4_crate_to_volts=[]
    
    i=0
    for i in range (0,NUM_PONTS_CRATE):
        channel_1_crate_to_volts.append(crate_data[0][i]/(MAX_CONTAGEM_ADC))
        channel_2_crate_to_volts.append(crate_data[1][i]/(MAX_CONTAGEM_ADC))
        channel_3_crate_to_volts.append(crate_data[2][i]/(MAX_CONTAGEM_ADC))
        channel_4_crate_to_volts.append(crate_data[3][i]/(MAX_CONTAGEM_ADC))
    
    volts_data=[channel_1_crate_to_volts,channel_2_crate_to_volts,channel_3_crate_to_volts,channel_4_crate_to_volts]
    
    return (crate_data,volts_data)