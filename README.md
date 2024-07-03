
# ComplexSocialOpinion

The source code was intially written in Python 2.7, and has been slightly modified for python3. Pygame and Numpy are required to run the code.  Some output data are post-processed or plotted with matplotlib.  A simple user interface is under development by using Tkinter.  In the latest version flow fields are calculated by using a flow solver.  

### How-To: 
python ui.py --> user interface (GUI) --> select input files --> visulize geometry settings --> start simulation

(1) When tkinter window (GUI) is activated, please select the input files for simulation.  Choose csv file for agent input data.  Users can optionally use fds file to create the compartment geometry, and the agent features must be described in csv file.  If fds file is omitted, the compartment geometry should be described in csv file.  Please take a look at the user guide and examples for details.  

(2) When pygame screen is activated, press certain keys to adjust the display features:  
Use pageup/pagedown keys to zoom in/zoom out the entities.  
Use space key to pause the simulation.  
Use direction keys to move the entities vertically or horizonally in screen.  

(3) There are currently several examples in the repo.  Users can learn from the examples on how to write a simple csv files.  If you have any question about how to create a complex example, please feel free to contact me or raise a question by using issue trackers.  

The program mainly consists of four components: User Interface, Simulation Core, Data Tool, Visualization Tool.  

**User Interface**: The user interface is written in tkinter in ui.py.  Users run ui.py to enable a graphic user interface (GUI) where one selects the input files, initialize compartment geometry, and configure or start a simulation.  Currently there is a simple version of GUI and it needs to be improved in several aspects.  If you find any problems when using the user interface, please send me a message or start an issue here.  

**Simulation Core**: The multi-agent simulation is implemented in simulation.py.  The component is packed in a class called simulation class, and it computes interaction of four types of entities: agents, walls, doors and outlets.  This agent-based model is an extension of the traditional social force model by Helbing, Farkas, Vicsek and Molnár.  The model aims at investigating protypes of pedestrian behavior in crowd evacuation.  

**Data Tool**: This component is included in data.py, which reads in data from input files and write data to output files.  In the latest version the agent data must be included in a csv file.  The compartment geometry (i.e., walls, doors and exits) is either read from the csv file or fds file (FDS+Evac input file).  Please refer to examples for details on specification of agents, walls, doors and outlets.  

**Visualization Tool**:  The visulization component is packed in draw_func.py and pygame (SDL for Python) is used to visualize the simulation result.  We have developed a simple data tool such that users can first run the simulation and get the output data, and then visualize the output data for further analysis.  

### Acknowledgments
I would like to express my sincere gratitude to Dr. Peter Luh for his helpful comments on my earlier work in University of Connecticut. I am also thankful to Timo Korhonen for helpful discussion in his wonderful simulation work of FDS+Evac.  I highly appreciates the research program funded by NSF Grant # CMMI-1000495.  

### Collaborators are needed and your ideas are much valued!  

If you are a student or researcher who want to use this python package to test your own model or algorithm, please feel free to contact me by email or issue trackers, and I am glad to guide you to use this package!  

So if you are interested in this project and would like to contribute your ideas, please feel free to start an issue to propose your ideas!  Collaborations are much welcome and comments are appreciated!  There are several things to do to improve the source code and document.  For example, the user interface (GUI) is to be improved, but I do not have much time to do that.  If you are good at developing user interface, please feel free to contribute and I will give you credits in the manual or in our papers.  Please refer to the issue "To-do list" for details.  

Open discussion is much encouraged about the model and algorithm!  
