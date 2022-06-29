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
### Libraries:
 - deque from collections: build-in used for the operations ıf low and high FIFO queues
 - osmnx: third party used to extract and download OSM elements (graph) with the selected BBOX
 - a) pandas & b) geopandas: third parties used to a) read and slice (data analysis) of datasets, b) read and extract coordinates of geometry attributes
 - shapely: third party used to perform simple geo-processes such as "Select by Location between two features"
 - contextily & matplotlib: third parties, both used to design and plot the geo-features on a cartographic map



### Class OSM:
 - Setting up instances:
   - The user should define the parent directory first to save the Geopackage
   - BBOX coordinates should have been set as, maxx, minx, ymax, ymin
 - get_data() method in the class downloads graph of the pedestrian walking network
 - The graph is downloaded as GeoPackage since, Geopackage is an optimized and interoperable format to store geo-datasets
 - Downloaded GeoPackage contains two classes; nodes(points) and edges(polyLines)
  
    
      
### Class Queue:
 - Each method of the class is called to the following class twoQ
 - Class confirms a FIFO (First in First out) queue (Pallottino offers that both Qs should be FIFO queues)
   - enqueue() adds a new element to queue from the tail
   - dequeue() removes an existing element from the head of the queue
   - isEmpty() and length() are used to check while loop continuity and assess a range of a for loop respectively



### Class twoQ:
- algorithm()
  - Third-party libraries are never used for the construction of the algorithm but for other purposes
  - Algorithm consists of 3 main parts according to Pallottino; initialization, extract and scanning operation
  - Setting up instances:
    - graph: Gets directory of graph, specified with Class OSM
    - index numbers of source and destination nodes [if OID in QGIS or ArcGIS starts from 1, the index of first element will be 0 (i = OID-1)]
    - result: function/method two_q(graph, source, target) -> route
  - Reads nodes and edges
  - Define label, state, parent information as LISTS
  - INITIALIZATION of the the queues, all candidate nodes are stored in both of the queues, conforming FIFO rule
    - Assign, label = inf, state = unreached, parent = none to all candidate nodes with a loop
    - Assign, label = 0, state = in-queue, parent = -1 to source node (Parent index have to be integer because it will point out the child node index but -1 cant be a parent index of any node, so it will stop the routeList iteration later on)
    - WHILE loop
     - Extraction and Scanning operations will be inside the loop
     - Loop stops when only both high and low queues are emptied out by the extraction operation
    - Extraction operation; remove first element of high queues unless high queue is empty, then removal from low queue
    - Scanning operation
     - Select all candidate edges of the current node by the intersection operation
     - Select all nodes that are connected to selected edges + remove current node to get rid of the redundancy
     - Select single edge in a loop and get its length from its attribute table
     - Perform labeling for each j node that are connected to i node; add node J to either low or high queue depending on the state
    - Label node i = Scanned
    - Go back to While loop
     - Check if both of queues are empty, if not, continue
     - Loop starts from graph.node[0] and iterates until graph.node[last_index], once the last index is obtained, the loop starts from the first graph.node[0] once again
     - Once the two-Q is over, the remaining of the code extracts list of path from destination to source node e.g. 
routeList = [index[destination], index[parent[destination], index[parent[parent[destination]], ............, index[source]]
     - pathNodes = Above code block also slides node features, resulting in obtaining only nodes that are relevant to route between source and destination nodes
     - Return both routeList and pathNodes
    
- description()
  - Method can be called to solely obtain simple printed text of route description
 e.g. Start from index[sourceNode], go to index[node], ..., you have arrived the destination index[destinationNode]
 

   
### Class getMap:
- visualization()
 - Read nodes and edges
 - Slice edges and nodes to obtain only relevant edges and nodes of the routh
  - return objects of method algorithm() of class twoQ are called (routeList and pathNodes)
 - CRS transformation of the sliced dataframes to default CRS of OSM basemap
 - Setting parameters for plot such as line tickness, alpha, label properties
 - OSM DE basemap is added
 - Calling function results in map of route between source and destination node over OSM basemap in German



### Setting all variables (instances)
- This part can be done by following instance descriptions of above classes
