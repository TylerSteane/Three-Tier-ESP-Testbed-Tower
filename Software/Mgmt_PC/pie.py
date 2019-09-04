# |**********************************************************************;
# * Project           : Dynamic HTML Log Dashboard.
# *
# * Program name      : pie.py
# *
# * Author            : Tyler Steane
# *
# * Date created      : 20-02-2019
# *
# * Purpose           : Generates a PNG Image of a Pie chart for to input values.
# *                     It returns the filename. This script is used in genLog.py.
# *
# * Dependencies      :  Matplotlib.
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision
# * 20-02-2019  T Steane     1      Initial implementation.
# *
# |**********************************************************************;

import matplotlib.pyplot as plt

# Function called with value for Sucess and Fails as well as the desired filename without file extention.
def PiePlot( Sucess, Fail, filename ):

    #label for slices
    labels = 'Sucess','Fail'
    #slice values
    status = [Sucess, Fail]
    explode = (0, 0.1)  # explode out one slice
    colors = ['#99ff99', '#ff9999'] # green and red also used in tables.

    #create figure
    fig1, ax1 = plt.subplots()

    #plot PieChart
    ax1.pie(status,colors= colors, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    filename +='.png'
    #save image to file with minimised padding.
    fig1.savefig( filename ,bbox_inches='tight', dpi = 80)

    #return filename as string.
    return filename
