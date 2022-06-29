# Code Challenge - Shortest Paths on OpenStreetMap
Developed by Baturalp Arisoy, 29.06.2022, Munich

I am excited to share my results of the coding challenge with you. Please find notes and explanations of code blocks & algorithm below.

Note 1: Due to the limitation of the PC's CPU power, a much more narrow BBOX is tested during the develop process. However, the current parameter of the OSM access code is set as the original BBOX, stated by the challenge menu documentation. Both BBOXs can be found in the "Setting all variables" section of the code.

Note 2: The code is scriptted with object-oriented programming logic, therefore multiple classes can be found. Each class (except Queue) represents one of three different parts of the task; data preparation, shortest path algorithm Two-Q implementation and visualization. Furthermore, methods in the classes can be initiated with given parameters. By the design, the code first contains all the classes and their method

Note 3: Code comments

- Folders:
  - Codes:
    - WCS connection (R code)
    - NutriB2 with ArcPy (Python code)
  - Vector data:
    - Necessary dataset to run codes
    - Information is given as text in the codes
