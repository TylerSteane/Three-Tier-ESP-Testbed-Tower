# |**********************************************************************;
# * Project           : Dynamic HTML Log Dashboard.
# *
# * Program name      : genLog.py
# *
# * Author            : Tyler Steane
# *
# * Date created      : 20-02-2019
# *
# * Purpose           : Format log data from managment PC into a HTML Dashboard.
# *                     This scritp supports the server scripts used for the ESP
# *                     Programming towersself.
# *
# * Dependencies      : yattag Library and the Pieplot script (requires
# *                     Matplotlib).
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision
# * 20-02-2019  T Steane     1      Initial implementation using hardcoded dictioary to simulate data.
# * 01-07-2019  T Steane     2      Added Log file read and formatting into dictioary.
# *
# |**********************************************************************;

import glob, os, sys
from yattag import Doc, indent
from pie import PiePlot

def compileLog(folder):
    log = {} # Log data dicitioary
    #sys.path(folder)
    for file in glob.glob(folder+"Tower*.*"): #read all Tower log files, ignore other log files.
        f = open(file, 'r')# read files a line at a time
        Tower_results= {} #sub dictioary for each tower

        for  line in f:
            content = [x.strip() for x in line.split(',')] # split each line at commas
            device = "ESP-%02d"% (int(content[0])+1) # nicer device names
            Tower_results[device] = content[1:5] #first element becomes dictioary key other elements are the value
            log[file.split('\\')[1].split('_')[0]] = Tower_results

# Sample Log data for testing.
# log = {
#     "Tower 1" :{
#         "ESP-01" : ("blink.bin", 1, "19-02-2019 08:32:55", "Complete"),
#         "ESP-02" : ("blink.bin", 1, "19-02-2019 08:33:55", "Complete"),
#         "ESP-03" : ("flash.bin", 0, "19-02-2019 08:34:55", "Could not find the file C:\ code\ falsh.bin - Programming was aborted."),
#         "ESP-04" : ("blink.bin", 1, "19-02-2019 08:38:55", "Complete")
#     },
#     "Tower 2" :{
#         "ESP1" : ("blink.bin", 1, "19-02-2019 08:32:55", "Complete"),
#         "ESP3" : ("flash.bin", 0, "19-02-2019 08:34:55", "Could not find the file C:\ code\ falsh.bin - Programming was aborted."),
#         "ESP4" : ("blink.bin", 1, "19-02-2019 08:38:55", "Complete")
#     },
#     "Tower 3" :{
#         "ESP1" : ("blink.bin", 1, "19-02-2019 08:32:55", "Complete"),
#         "ESP2" : ("blink.bin", 1, "19-02-2019 08:33:55", "Complete"),
#         "ESP3" : ("flash.bin", 0, "19-02-2019 08:34:55", "Could not find the file C:\ code\ falsh.bin - Programming was aborted."),
#         "ESP4" : ("blink.bin", 1, "19-02-2019 08:38:55", "Complete"),
#         "ESP2" : ("blink.bin", 1, "19-02-2019 08:33:55", "Complete"),
#     },
#     "Tower 4" :{
#         "ESP1" : ("blink.bin", 1, "19-02-2019 08:32:55", "Complete"),
#         "ESP2" : ("blink.bin", 1, "19-02-2019 08:33:55", "Complete"),
#         "ESP3" : ("flash.bin", 0, "19-02-2019 08:34:55", "Could not find the file C:\ code\ falsh.bin - Programming was aborted."),
#         "ESP4" : ("blink.bin", 1, "19-02-2019 08:38:55", "Complete")
#     },
#     "Tower 5" :{
#         "ESP1" : ("blink.bin", 1, "19-02-2019 08:32:55", "Complete"),
#         "ESP2" : ("blink.bin", 1, "19-02-2019 08:33:55", "Complete"),
#         "ESP3" : ("flash.bin", 0, "19-02-2019 08:34:55", "Could not find the file C:\ code\ falsh.bin - Programming was aborted."),
#         "ESP4" : ("blink.bin", 1, "19-02-2019 08:38:55", "Complete")
#     },
# }

    #status-  Count up key status values
    No_Towers = 0;
    No_ESPs = 0
    No_Sucess = 0;
    No_Fail = 0;

    for tower,devices in log.items():
        No_Towers += 1
        for device, data in devices.items():
            No_ESPs += 1
            if int(data[1]):
                No_Sucess += 1
            else:
                No_Fail += 1

    # creat/edit Html file and open for editing as "Log"
    logpage= open("log.html","w+")

    # call function to draw Pie Chart for the given Success fail ration. And store the filename.
    PieChart = PiePlot(No_Sucess, No_Fail, 'pie')

    # create a Doc object to handel HTML.
    doc, tag, text = Doc().tagtext()

    # write string as is. Start HTML Doc.
    doc.asis('<!DOCTYPE html>')

    # HTML Header
    with tag('head'):
        # for debug refresh page ever few seconds.
        doc.asis('<meta http-equiv="refresh" content="5" />')
        # link CSS file for padding and styles.
        doc.stag('link', rel="stylesheet", href="css/custom.css")


        # Use HTML with tag and specify content with text()
    with tag('h1'):
        text('Programming Status Log')

    #write as is, start table with boarder set.
    with tag('table', border="3", klass="main_table"):
        with tag('tr'):
            with tag('td'):
                text('No. Towers')
            with tag('td', align='center'):
                text(No_Towers)
            with tag('td', rowspan='4'):
                doc.stag('img', src='./'+PieChart)

        with tag('tr'):
            with tag('td'):
                text('No. ESPs')
            with tag('td', align='center'):
                text(No_ESPs)
        with tag('tr'):
            with tag('td'):
                text('No. of Sucessful')
            with tag('td', align='center'):
                text(No_Sucess)
        with tag('tr'):
            with tag('td'):
                text('No. failed')
            with tag('td', align='center'):
                text(No_Fail)

    ## Tables for each tower giving status of each espself.
    for tower,devices in log.items():
        # table heading
        with tag('h2'):
            text(tower,' :')
        # table header
        with tag('table', border="1", klass="detail_table"):
            with tag('tr'):
                with tag('th'):
                    text('Device')
                with tag('th'):
                    text('img')
                with tag('th'):
                    text('Status')
                with tag('th'):
                    text('Time Stamp')
                with tag('th'):
                    text('Message')

            # row for each device
            for device, data in devices.items():
                # convert Success fail bools to text and class identifier.
                if int(data[1]):
                    classval = "success"
                    status   = "Success"
                else:
                    classval = "fail"
                    status   = "Fail"
                    #Write HTML for table rows.
                with tag('tr', klass = classval):
                    with tag('td'):
                        with tag('h2'):
                            text(device)
                    with tag('td'):
                        with tag('h2'):
                            text(data[0])
                    with tag('td'):
                        with tag('h2'):
                            text(status)
                    with tag('td'):
                        with tag('h2'):
                            text(data[2])
                    with tag('td'):
                        with tag('h3'):
                            text(data[3])

    #end HTML file
    doc.asis('</HTML>')
    #write Doc to file with indentaion so that HTML is easier to read.
    logpage.write(indent(doc.getvalue()))
