def enob(sinad_media,sinad_media_matlab,utilizarMatlab_check):

    enob_ch=[]  
    enob_ch_matlab=[]  
    i=0

    for i in range (0,4):
        enob_ch.append((sinad_media[i]-1.76)/6.02)
        if(utilizarMatlab_check==True):
            enob_ch_matlab.append((sinad_media_matlab[i]-1.76)/6.02)
        else:
            enob_ch_matlab.append('-inf')
    return(enob_ch,enob_ch_matlab)