FS Pro x Blender Rocket Visualizer

By Mark Brunson
April 2023

Dependencies
  math, os, csv, bpy(blender)

Requires blender, 'decision_fitness.csv', and 'components.csv'

There is a TON of room for improvement, bit it gets the job done. Good enough.

              ,  ,
             / \/ \,'| _
            ,'    '  ,' |,|
           ,'           ' |,'|
          ,'                 ;'| _
         ,'                    '' |
        ,'                        ;-,
       (___                        /
     ,'    `.  ___               ,'
    :       ,`'   `-.           /
    |-._ o /         \         /
   (    `-(           )       /
  ,'`.     \      o  /      ,'
 /    `     `.     ,'      /
(             `"""'       /
 `._                     /
    `--.______        '"`.
       \__,__,`---._   '`;
            ))`-^--')`,-'
          ,',_____,'  |
          \_          `).
  		   `.      _,'  `
            /`-._,-'      \

Instructions for drawing rockets onto blender enviornments:

	1. Add 'compnents.csv' and 'decision_fitness.csv' to current folder
	2. Reverse csv lists using Matlab function CSVReverser.m
		- Matlab runtimes are available online (https://www.mathworks.com/help/matlab/matlab_external/call-matlab-functions-from-python.html). CSVReverser(filename) and CSVTrimmer(filename, rows) both have file outputs. Leave header rows for both.
		- If testing, trim the lists with CSVTrimmer.m first, then reverse. Test with 200-500 rows (about rows/5 prints). Always trim 'components.csv' with rows*13. Then change the Rocket_Visualizer.py script componentsFile and decisionFile vars to 'reversed_trimmed_'filename.
	3. Add the reversed files to the folder.
	4. Open a clean blender file and open the python file in the text editor.
	5. Delete ALL objects.
	6. Run the python script.
	7. After completing, quit the blender file, it has already saved and quitting will help it run faster. 
	8. Everything here is just like normal, objects are only modified and not deleted. Build the stage, apply shaders, add lights, and camera, then export the video like normal. 

This is meant to allow shader application and building after the keystones for the rocket are added. Building a stage beforehand is possible but make sure there are no objects named 'cube', 'cylinder', or 'cone' (or any '.001' etc.) in the upper right corner. With less powerful computers, it is possible to initilize the rocket beforehand, apply shaders, and build the stage. Just split the file in half before the for loop, apply shaders and build the stage around the cylinder reference. 