#===========================================================#
#                                                           #
#               Demo_Classes file 07-04-16                  #
#               Simon Goodwin                               #
#                                                           #
#   All Classes defined here - most cut down for example    #
#                                                           #
#===========================================================#
import os, time
import xml.etree.ElementTree as ET


#exception report traceback
def ReportException(ErrorString):
    import traceback
    print "Error is ",ErrorString
    traceback.print_exc()

#user defined imports
try:
    import myDictionary
    from myDictionary import *
    #from Error_Report import *
except:
    ReportException("User defined import error")


#=======================================================================#
#                                                                       #
#   This is basic message list  - keeps list of messages created        #
#                                                                       #
#=======================================================================#
class MESSAGE_LIST_CLASS():
    def __init__(self):
        self.current_session_msg_list = []
    def add_message(self,newMsg):
        self.current_session_msg_list.append(newMsg)
    def print_msg_list(self):
        i=0
        print "\nMessage List is as follows"
        for msg in self.current_session_msg_list:
            i+=1
            print "MSG " + str(i)  + " : " + msg.completeMsg


#===================================================#
#                                                   #
#       MESSAGE CONTAINER  - header + command       #
#                                                   #
#===================================================#
class MSG_CLASS():
    def __init__(self,cmdName,cmdParams):
        #these variables are headers and are hardcoded here for example and to reduce size of code 
        self.address = '0x1234'
        self.msgType = '0xAB'       
        self.packetType = '0xCD'
        self.msg_hdr = (self.msgType[2:] + self.address[2:] + self.packetType[2:])

        #now get command and payload
        if isinstance(cmdParams, str):
            self.PAYLOAD = COMMAND_CLASS(cmdName,cmdParams)
        else:
            ReportException("Incorrect Type - please ensure you are using a Hex string")
        self.completeMsg = self.msg_hdr + self.PAYLOAD.cmd

        #create bytearray for transport
        self.getByteArray()
    def getByteArray(self):
        hex_data = (self.completeMsg).decode("hex")
        self.MsgInBytes = bytearray(hex_data)



#===================================================#
#                                                   #
#       COMMAND CLASS  - command type and payload   #
#                                                   #
#===================================================#
class COMMAND_CLASS():
    def __init__(self,cmdName,cmdParams):
        self.cmdID = None

        try:
            self.cmdPayload = cmdParams
            self.cmdID = self.find_key(myDictionary.MsgTypeDict, cmdName)
        except:
            ReportException("failed to find command hex")

        #check to see if we have payload or is this an 'empty' get command
        try:
            self.cmd = (self.cmdID[2:].zfill(4) + self.cmdPayload[2:])
        except:
            self.cmd = self.cmdID[2:].zfill(4)

    def find_key(self,dic, cmdName):
        for key,value in dic.iteritems():
            if key == cmdName:
                return hex(value)
    
             
  

#===============================================================================#   
#                                                                               #
#   this class updates the dictionary.py file in line with the XML registry     #
#                                                                               #
#===============================================================================#
class myParsers():
    def __init__(self):
        self.newDict = {}

    def parse_xml(self):
        print "\nParsing xml file and update myDictionary.py file....."
        curr_dict_file = open('myDictionary.py', 'r')
        temp_file = open('TEMP_myDictionary.py', 'w+')
        with open('example_registry.xml') as f:                                      
            try:
                tree = ET.parse(f)
            except:
                ReportException("error parsing file")

        #parse xml into temp dictionary file
        temp_file.write("MsgTypeDict = {\n\t\t")                             
        for node in tree.iter():

            if (node.tag == "setting"):
                myStr = str('get ' + node.get('name'))
                myStr = str(myStr.replace(" ","_"))
                self.newDict[myStr] = node.get('id')
 
            elif node.tag == "command":
                if "Set" in node.get('name'):
                    node_name = node.get('name')
                    node_name = node_name[4:]
                else:
                    node_name = node.get('name')

                myStr = str('set_' + node_name)
                myStr = str(myStr.replace(" ","_"))
                self.newDict[myStr] = node.get('id')
     
            elif node.tag=="event": 
                myStr = str(node.get('name')) 
                myStr = str(myStr.replace(" ","_"))
                self.newDict[myStr] = node.get('id')
            else:
                pass  
           
        #rewrite new values to tempFile 
        for key, value in self.newDict.iteritems():
            temp = [key,value]
            temp_file.write("'" + key + "'" + ':' + value + ',\n\t\t')      
        temp_file.seek(-5,2)
        temp_file.write("}\n\n")

        #read previous file and add non-changing elements back to new file
        previous_version = curr_dict_file.read()                            
        index_after_xml = previous_version.find("PKT_STRUCTURE")
        temp_file.write(previous_version[index_after_xml:])
        temp_file.close()
        curr_dict_file.close()
    
        #rename temp dict to dict file
        os.remove("myDictionary.py")                                          
        os.rename(temp_file.name,"myDictionary.py")
        print "completed..myDictionary has been updated\n"