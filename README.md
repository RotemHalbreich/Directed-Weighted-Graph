# *Ex3:*
----------------------------------------------------------------------------------------------------------
# *Object Oriented Programming project in Python - Ariel University*
----------------------------------------------------------------------------------------------------------
## :bar_chart: *Based on "Graph Theory" subject, dealing with directed weighted graph*
### *Implementation of the following classes:*
- *[Node()](https://github.com/shakedaviad55/Ex3/wiki/Node-Class) - represents the vertices of the graph*
- *[DiGraph()](https://github.com/shakedaviad55/Ex3/wiki/DiGraph-Class) - represents a directed weighted graph*
- *[GraphAlgo()](https://github.com/shakedaviad55/Ex3/wiki/GraphAlgo-Class) - represents the directed weighted graph's algorithms*

----------------------------------------------------------------------------------------------------------
## :question: *The purpose of the project:*
- *Convert project Ex2 (part 1) from Java to Python.* 
- *Compare between our Java's and Python's running time.*
- *Compare between our code and [NetworkX's](https://networkx.org/documentation/stable/tutorial.html) code.*

### *The comparison is for methods:*

*Function* | *Explanation*
------------------------------------------------------|----------------------------------------------------
 :small_red_triangle_down:*`shortest_path()`* | *Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm. Adds to every vertex, the previous vertex which the vertex "came from". Finally, sends to help function seek_path() which returns a Tuple of the distance and the list of the vertices creating route.*
 :small_red_triangle_down:*`connected_component()`* | *Finds the Strongly Connected Component (SCC) which node id1 is a part of. Help function sub_graph(), returns the reversed graph of all the vertices we can get to from vertex id1 and the list of all these vertices using DFS algorithm. Then, help function direction() returns the list of all vertices which we got to from the reverse graph using DFS algorithm. Finally, help function union(), unites both lists nd returns the Strongly Connected Component (SCC).*
 :small_red_triangle_down:*`connected_components()`* | *Finds all the Strongly Connected Components (SCC) in the graph, passes through every vertex and sends it to the function connected_component() as long as the vertex is unvisited yet.*

----------------------------------------------------------------------------------------------------------
### :pencil: *Authors of this project:*
| *Rotem Halbreich  -  GitHub: https://github.com/RotemHalbreich* | *Shaked Aviad  -  GitHub: https://github.com/shakedaviad55* |
------------------------------------------------------|----------------------------------------------------
----------------------------------------------------------------------------------------------------------
### :white_check_mark: *Initialize the project:*
*Clone the project using the Command Line by typing the command:*

`git clone https://github.com/shakedaviad55/Ex3.git`

----------------------------------------------------------------------------------------------------------
## :camera: *[matplotlib](https://matplotlib.org/) - Example for data A5 graph from Json format:*
![A5](https://user-images.githubusercontent.com/66558110/104127304-16daaa00-536a-11eb-8676-76ed0a17373d.png)

----------------------------------------------------------------------------------------------------------

## :books: *External sources:*
  *Subject:* | *Link:*
------------------------------------------------------|----------------------------------------------------
*The definition of a graph:* | *https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)* 
*Directed Graph:* | *https://en.wikipedia.org/wiki/Directed_graph*
*Dijkstra's Algorithm:* | *https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm*
*Depth-First Search (DFS) Algorithm:* | *https://en.wikipedia.org/wiki/Depth-first_search*
*Strongly Connected Component (SCC):* | *https://en.wikipedia.org/wiki/Strongly_connected_component*
*Matplotlib:* | *https://matplotlib.org/*
*NetworkX:* | *https://networkx.org/*

----------------------------------------------------------------------------------------------------------
  *Dijkstra's Algorithm:* | *DFS Algorithm:*
------------------------------------------------------|----------------------------------------------------
 ![Dijkstra's algorithm](https://upload.wikimedia.org/wikipedia/commons/5/57/Dijkstra_Animation.gif)|![DFS](https://miro.medium.com/max/1280/0*miG6xdyYzdvrB67S.gif)

----------------------------------------------------------------------------------------------------------
## :book: *Wiki:*
*Please be sure to check out our [Wiki](https://github.com/shakedaviad55/Ex3/wiki) for more information about the project!*

----------------------------------------------------------------------------------------------------------
### *Enjoy, and please share!* :smile:
