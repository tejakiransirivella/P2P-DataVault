import time
from datetime import datetime
from data_node import data_node
from node import node

# data_node = data_node(5)
# data_node.append(node("1.2.3.4",8080,1))
# time.sleep(3)
# data_node.append(node("1.2.3.5",8080,2))
#
# print(data_node)

node = node("1.2.3.4",8080,1)
print(node)