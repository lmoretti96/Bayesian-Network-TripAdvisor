library(igraph)

node <- data.frame(name=c("fantastic","good","old","Service","Cleanliness",
                          "Overall","great","Value","bad","Rooms","small",
                          "Location"))

relations <- data.frame(from=c("fantastic","fantastic","fantastic","fantastic","fantastic","fantastic","fantastic","fantastic","fantastic","fantastic","fantastic","good","good","good","good","good","good","good","good","good","good","old","old","old","old","old","old","old","old","old","Service","Service","Service","Service","Service","Service","Service","Service","Cleanliness","Cleanliness","Cleanliness","Cleanliness","Cleanliness","Cleanliness","Cleanliness","Overall","Overall","Overall","Overall","Overall","Overall","great","great","great","great","great","Value","Value","Value","Value","bad","bad","bad","Rooms","Rooms","small"),
                        
                        to=c("good","old","Service","Cleanliness","Overall","great","Value","bad","Rooms","small","Location","old","Service","Cleanliness","Overall","great","Value","bad","Rooms","small","Location","Service","Cleanliness","Overall","great","Value","bad","Rooms","small","Location","Cleanliness","Overall","great","Value","bad","Rooms","small","Location","Overall","great","Value","bad","Rooms","small","Location","great","Value","bad","Rooms","small","Location","Value","bad","Rooms","small","Location","bad","Rooms","small","Location","Rooms","small","Location","small","Location","Location"))

g <- graph.data.frame(relations, directed=TRUE, vertices=node)
plot(g, vertex.label = V(g)$name)

