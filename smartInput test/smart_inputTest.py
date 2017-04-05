



if __name__ == "__main__":
    
    import smartinput as si
    
    
    #commandHistory = ['you are nice', 'that is wonderful', 'yeah indeed']
    
    file = "histroyFiles/test/history.pickle"    
    
    smart_input = si.SmartInput(commandHistoryFilePath = file) #commandHistory)
    
    input = smart_input("Type something here?:")
    
    print "You wrote: {}".format(input)
    