# Code Challenge - Shortest Paths on OpenStreetMap
Developed by Baturalp Arisoy, 29.06.2022, Munich <br />
ReadMe is written in GitHub as a markdown file

I am excited to share my results of the coding challenge with you. Please find the notes and explanations of the code blocks & algorithm below.

## Notes
Note 1: Due to the limitation of the PC's CPU power, a much more narrow BBOX is tested during the develop process. However, the current parameter of the OSM access code is set to the original BBOX, stated by the challenge menu documentation. Both BBOXs can be found in the "Setting all variables" section of the code.

Note 2: The code is scriptted with object-oriented programming logic, therefore multiple classes can be found. Each class (except Queue) represents one of three different parts of the task; data preparation, shortest path algorithm Two-Q implementation and visualization. Furthermore, methods in the classes can be initiated with given parameters. By the design, the code first contains all the classes and their methods consecutively and instance set-up at the end.

Note 3: The detailed explanation of code blocks can be found below, however the code itself gives explanations with several comment lines.

Note 4: The only part of the code that doesn't functioning 100% as intended is the Two-Q algorithm itself. Due to some reasons, both low and high queues are emptied out before the completion of labeling some of the candidate nodes permentantly. Even though all nodes are "SCANNED", some of the nodes will not be labeled, therefore cannot be inilialization parameters as source or destination nodes. However, all the permenantly labeled nodes give excellent routing results, as well as their path visualization in the cartographic map.


## Code Design
- Libraries:
  - deque from collections: build-in used for the operations ıf low and high FIFO queues
  - osmnx: third party used to extract and download OSM elements(graph) with the selected BBOX
  - a) pandas & b) geopandas: third parties used to a) read and slice (data analysis) of datasets, b) read and extract coordinates of geometry attributes
  - shapely: third party used to perform simple geo-processes such as "Select by Location between two features"
  - contextily & matplotlib: third parties, both used to design and plot the geo-features on a cartographic map



- Class OSM:
  - Setting up instances:
    - The user should define the parent directory first to save the Geopackage
    - BBOX coordinates should have been set as, maxx, minx, ymax, ymin
  - get_data() method in the class downloads graph of the pedestrian walking network.
  - The graph is downloaded as GeoPackage since, Geopackage is an optimized and interoperable format to store geo-datasets.
  - Downloaded GeoPackage contains two classes; nodes(points) and edges(polyLines)
  
    
      
- Class Queue:
  - Each method of the class is called to the following class twoQ
  - Class confirms a FIFO (First in First out)
    - enqueue() adds a new element to queue from the tail
    - dequeue() removes an existing element from the head of the queue
    - isEmpty() and length() are used to check while loop continuity and assess a range of a for loop respectively



- Class twoQ:
  - Setting up instances:
    - The user should define the parent directory first to save the Geopackage
    - BBOX coordinates should have been set as, maxx, minx, ymax, ymin
   
   
   
   
   
