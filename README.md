# global-clinic-2020

This document outlines the user manual for the HMC Optimization software. You can download this entire repository as a .zip folder to a preferred location on your computer.

Begin in the folder containing the executable file and several folders of supporting files. You should only work in these folders if you are altering the software. Otherwise, all you need to do is open the executable file. 

#insert pic 

Note that when opening the "main.exe" for the first time, your computer may open a “Windows protected your PC” dialog. 

* If only opening the software once, you can click “Run Anyway” to open the software. If that is not an option, click “More Info” and then “Run Anyway” to continue. 

* To prevent this dialog from opening repeated times, you will need to add an exclusion to Windows Security by following the steps at the following link, <https://support.microsoft.com/en-us/help/4028485/windows-10-add-an-exclusion-to-windows-security>. 
Note that these steps are specific to Windows 10, so use whichever steps are appropriate for your operating system.


For a recorded walk-through of these steps, refer the video at this link: <https://youtu.be/4X3S24hETXM>

A blank terminal window pops up when the software opens. The terminal is not necessary, but closing this window also closes the software, so either minimize it or just leave it on the screen.

The software opens with a splash page which contains a "Help" and "Continue" button. 

#insert pic 

Clicking the "Help" button open the "Help" window, which is accessible from each of the windows in the software. This window contains a brief how-to, a detailed explanation for the data input and results windows, and our project motivation. 

#insert pic

Clicking "Done" exits this window, and clicking "Continue" from the splash page opens the data input window. This window opens with a blank .csv file template, which is formatted in the appropriate way for the optimization solver. This template can be populated either in the software itself or by opening the .csv file in an external editor. You should be sure to edit a copy of the template file, since the software will always open with the template. This file can be located anywhere on your computer. Clicking "Import" open a file dialog for the user to select a .csv file to open in the table. If a non-.csv file is selected, an Error window will open asking the user to select a different file or cancel. Once a .csv file is imported, if you want to make an alternate copy, click "Export" to save a copy of the currently shown table in a new .csv file. 

#insert pics

In order to populate the template, you should understand what data is needed in each column.
1. Column 1 assigns a number to each process. This is just for referencing purposes.
2. Column 2 has the process name.
3. Column 3 has the cycle time of the process. This is the time it takes for a single operator to complete the task for one unit.
4. Column 4 indicates whether the process is automated or done manually.
5. Column 5 is the capacity of the automated processes. For example, if there are only four computers available for a process, 4 would be the capacity for the process.
6. Column 6 is the immediate predecessor of the process, denoted using the numbers from Column 1. The numbers listed here indicate that those processes must be completed before the current process can begin. In a serial process flow, this is just the number of the process before it.
7. Column 7 is the length in meters of the space needed for one operator to complete each process. For an automated job, this is for one computer. For a manual job, this is the lateral space needed for one human to do the task.
8. Column 8 is the width in meters of the space needed for one operator to complete each process. It is measured in the same way described for Column 7 but is the depth of the space needed.
9. Column 9 is where we begin overall production line parameters that are not linked to any particular process. This column contains the takt time in seconds. Takt time is the rate at which a product needs to be completed in order to meet customer demand.
10. Column 10, like Column 9, is also an overall parameter, which means it only needs to be entered once. This column contains the human capacity defined as the maximum number of human operators that can be assigned to a single station. This is an optional parameter, but it gives the user the flexibility to indicate at what point a station becomes too crowded.


Once the desired data is uploaded, click "Results". This opens a warning page to ensure that changes in the table are saved to a .csv file. If you have made changes to the table in the software, click "Save and Continue", which will open a new file dialog to save the table to a .csv file. If you have not made any changes, click "Continue without Saving" to start the optimization.
#insert pic

Once the software has found an optimal process distribution to minimize the number of operators, the data window will close and the results window will open. Looking at the results window, the top panel contains the process distribution results, broken down by station, and the bottom panel contains a corresponding linear layout. The result data shows which tasks are located at each station, along with the number of operators of each type needed to complete those tasks at that station. Note that there is a computer operator column for each type of automated process in our input data.
#insert pic

To save the results data, click “save .csv results”. Note that the software automatically saves the output results in a pLineOpt.csv, but using the save button allows you to name and save it anywhere on your computer. To save the layout, click “save .png layout”. To go back to the data window, click “Go Back”. To exit the software, click “Exit”. Since the "Go Back" and "Exit" buttons will close the results window, a warning message appears to confirm that you want it to close. 

For further detail on the functionality of the software, consult Section 6.1 in our Final Report 
#insert link to google drive
