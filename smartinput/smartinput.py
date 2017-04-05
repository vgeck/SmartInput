#!/usr/bin/env python
# encoding: utf-8


__all__ = ["smart_input"]

import sys,StringIO,string,os
import copy

try:
    import cpickle as pickle
except:
    import pickle as pickle

# copy of namespace
namespace = vars().copy()


class SmartInput(object):
    """
    
    """
    def __init__(self, commandHistory = None, commandHistoryFilePath = None, fullOutput = False):
        """
        
        commandHistory
        commandHistoryPath
        commandHistoryFileName
        fullOutput
        
        """
        
        self.maxHistoryNumber = 250
        
        self.commandHistory = []
        if commandHistoryFilePath != None:
            self.commandHistoryFilePath = commandHistoryFilePath
            self.commandHistory = self.load_history()
        
        if commandHistory != None:
            fullOutput = True
            self.commandHistory.extend(commandHistory)
        
        # created chached history
        self.cachedHistory = copy.copy(self.commandHistory)
        self.cachedHistory.append("") # append an entry for the current line
            
        self.fullOutput = fullOutput
            
    def load_history(self):
        """
        
        """
        commandHistory = []
        # check if file exist if not create it
        if not os.path.isfile(self.commandHistoryFilePath):
            if '/' in self.commandHistoryFilePath:
                directories = '/'.join(self.commandHistoryFilePath.split('/')[0:-1])
                print directories
                if not os.path.isdir(directories):
                    os.makedirs(directories)  
            # create the file
            file = open(self.commandHistoryFilePath,'w')
            file.close()     
        else: 
            # try to open and check if it is pickable
            try:
                file = open(self.commandHistoryFilePath,'r')
                commandHistory = pickle.load(file)
                file.close()
            except EOFError:
                commandHistory = []
         
        # crop if it has more than maxHistoryNumber entries
        if len(commandHistory) > self.maxHistoryNumber:
            commandHistory = commandHistory[len(commandHistory)-self.maxHistoryNumber:]
        # return commpandHistory of file or empty list        
        return commandHistory
        
        
    def save_history(self):
        """
        
        """
        if os.path.isfile(self.commandHistoryFilePath):
            file = open(self.commandHistoryFilePath,'w')
            pickle.dump(self.commandHistory,file)
            file.close()
            
    def set_max_history_entries(self, maxHistoryNumber):
        """
        
        """
        
        self.maxHistoryNumber = maxHistoryNumber
            
    def smart_input(self, prompt):
        """
        
        """    
        
        # tab completion namespace from history
        autocompnamespace = list(set([word for word in ' '.join(self.cachedHistory).split(' ') if len(word)>3 ]))
                    
        # get handel on stdout
        stdout = sys.stdout
        #Choose a file-like object to write to
        outputBuffer = StringIO.StringIO() 
        sys.stdout = outputBuffer
        
        # write the prompt
        stdout.write(prompt + " ")
        
        line = ""
        
        # counter for the history
        historyPosition = len(self.cachedHistory)-1
        # counter for position in line
        curserPosition = 0
                
               
        captureInput = True
        while captureInput == True:
            char = getchar()
                        
            # line feed
            if char in "\r\n":
                stdout.write("\n")
                captureInput = False
            # ctrl-D
            elif char == "\x04":
                stdout.write("\nKeyboardInterupt\n")
                sys.exit(0)
            # backspace
            elif char == "\x7f":
                # only if character present
                if len(line) > 0:
                    
                    if curserPosition == len(line):
                        # remove one
                        line = line[:-1]
                        # subtract, replace with space, subtract again
                        stdout.write("\b \b")
                        curserPosition -= 1
                    else:
                        stdout.write("\b \b")
                        stdout.write(line[curserPosition::])
                        stdout.write(' ')
                        nBackspacing = len(line[curserPosition::])+1
                        stdout.write(''.join(['\b' for b in xrange(nBackspacing)]))
                        line = line[:curserPosition-1] + line[curserPosition:]
                        curserPosition -= 1
                        
            # Arrow keys
            elif char == "\x1b":
    
                direction = sys.stdin.read(2)
                
                # left
                if direction == "[D":
                    if curserPosition > 0:
                        stdout.write("\b")
                        curserPosition -= 1
                
                # right
                elif direction == "[C":
                    if curserPosition < len(line):
                        if len(line) != 0:
                            stdout.write(line[curserPosition])
                            curserPosition += 1
                
                # \t == tab
                # \f == jump one line down
                # \a == replace character under the curser
                # \v == jump one line down
                # \r == jump to start of line
                # \i == jump to start of line
                # \x == escape
                
                # up
                elif direction == "[A":
                    
                    # overwrite current line with cached history line
                    self.cachedHistory[historyPosition] = line
                    
                    if historyPosition != 0:
                        historyPosition -= 1
                    
                    while curserPosition < len(line):
                        stdout.write(line[curserPosition])
                        curserPosition += 1                       
                    stdout.write("\b \b"*len(line))
                    
                    stdout.write(self.cachedHistory[historyPosition])
                    line = self.cachedHistory[historyPosition]
                    curserPosition = len(line)
    
                # down
                elif direction == "[B":
     
                    # overwrite current line with cached history line
                    self.cachedHistory[historyPosition] = line
                    
                    if historyPosition < len(self.cachedHistory)-1:
                        historyPosition += 1
                                       
                    while curserPosition < len(line):
                        stdout.write(line[curserPosition])
                        curserPosition += 1             
                    stdout.write("\b \b"*len(line))
                    
                    stdout.write(self.cachedHistory[historyPosition])
                    line = self.cachedHistory[historyPosition]
                    curserPosition = len(line)
#             
            # trigger tab
            elif char == "\t":
                # check if at the last position
                if curserPosition == len(line):
                    # find position where the word ends
                    i = -1
                    while -i<len(line) and line[i] in string.letters + string.digits:
                        i -= 1
                    if line[i] == " ":
                        i +=1
                    
                    out = []
                    for key in autocompnamespace:
                        if line[i:] == key[:-i]:
                            out.append(key)
                    
                    # name completion if unique
                    if len(out) == 1:
                        line += out[0][-i:]
                        stdout.write(out[0][-i:])
                        curserPosition += len(out[0][-i:])
         
                    # list options if not unique
                    elif len(out) > 1:
                        out = "  ".join(out)
                        stdout.write("\n  " + out + "\n")
                        stdout.write(prompt + " " + line)        
                    
            
            # add char to line
            else:
                if curserPosition == len(line):   
                    stdout.write(char)
                    line += char
                    curserPosition += 1 
                # TODO change this so we aclually add characters to the string!!
                elif curserPosition == 0:
                    line = char + line
                    stdout.write(line)
                    curserPosition += 1 
                    nBackspacing = len(line)-1
                    stdout.write(''.join(['\b' for b in xrange(nBackspacing)]))
                else:
                    
                    line = line[0:curserPosition] + char + line[curserPosition:]
                    
                    stdout.write(line[curserPosition:])
                    
                    nBackspacing = len(line[curserPosition:])-1
                    stdout.write(''.join(['\b' for b in xrange(nBackspacing)]))
                    curserPosition += 1 
        
        # reset stdout to stdout
        sys.stdout = stdout
        outputBuffer.close()
        
        
        # add line to history
        self.commandHistory.append(line)
        # save history
        self.save_history()
        
        if self.fullOutput == False:
            return line
        else:
            return line, self.commandHistory

    def __call__(self, prompt):
        return self.smart_input(prompt)

def getchar():
    '''
    Function to get the entered character for Unix systems
    '''
    import tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


if __name__ == "__main__":
    import doctest
    doctest.testmod()