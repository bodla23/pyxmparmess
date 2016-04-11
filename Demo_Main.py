#===========================================================#
#                                                           #
#               Demo Main file 07-04-16                     #
#               Simon Goodwin                               #
#                                                           #
#===========================================================#
from Demo_Classes import *
import myDictionary             #required for relaod
from myDictionary import *


#===========================================================#
#                                                           #
#          MAIN() - test list provided for example          #
#          this was an input from text file in reality      #
#                                                           #
#===========================================================#
if __name__ == '__main__':

    #This contains list of example command messages
    test_list = ['get_Product_name','set_Ringtone','state_changed']  
   
    menu = raw_input('do you want to update the myDictionary file from xml y/n: ')
    if menu.lower().strip()== 'y':

        #this should be moved to class
        print "current myDictionary as follows"
        for k,v in myDictionary.MsgTypeDict.iteritems():
            print k,hex(v)

        #this is for updating the dictionary lookup file from the xml input - used to demo parser in Basic_Classes.py
        try:
            xmlParse =  myParsers()
            xmlParse.parse_xml()
            reload(myDictionary)
        except:
            ReportException("problem with xmlparser")


        #this should be moved to class
        print "updated myDictionary as follows"
        for k,v in myDictionary.MsgTypeDict.iteritems():
            print k,hex(v)

       
    #setup list class for contructed messages
    try:
        myMSG_LIST = MESSAGE_LIST_CLASS()
    except:
        ReportException("problem creating message list")

    #This section contructs our messages and adds to message list
    for testName in test_list:
        #is our command get / set / state ?
        if 'get' in testName or 'state' in testName:
            payload = ''
        else:
            payload = '0xCAFEFEED'      #this is just an example payload

        #construct our message
        try:
            FullMSG = MSG_CLASS(testName,payload)
        except:
            ReportException("problem with cresting Container")
 
        #add our message to parsed message list for Tx
        try:
            myMSG_LIST.add_message(FullMSG)
        except:
            ReportException("problem with adding to message list")

    #print it out for demo
    try:

        myMSG_LIST.print_msg_list()
        print "\nEnd of Demo"
    except:
        ReportException("problem with output")

