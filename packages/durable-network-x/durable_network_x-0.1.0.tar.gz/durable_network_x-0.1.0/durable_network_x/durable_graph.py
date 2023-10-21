import networkx, typing
from durable_network_x import DurableNetworkX
from durable_network_x.storage_managers import StorageManager

class DurableGraph(DurableNetworkX):
    """
    DurableGraph is a specific implementation of DurableNetworkX that deals exclusively 
    with undirected Graph objects from networkx.
    """

    def __init__(self, storage_manager: StorageManager):
        """
        Initialize a DurableGraph object.

        :param storage_manager: An instance of StorageManager to handle the storage operations.
        """
        super().__init__(storage_manager, graph_type = "Graph")
    
    def new(
        self, 
        instance_id: str, 
        network_x_graph_to_use: typing.Optional[networkx.Graph] = None
    ) -> 'DurableGraph':
        super().new(instance_id, network_x_graph_to_use)
        return self
    
    def use(self, instance_id: str) -> 'DurableGraph':
        super().use(instance_id)
        return self
    
    def save(self) -> 'DurableGraph':
        super().save()
        return self
    
    def delete(self) -> 'DurableGraph':
        super().delete()
        return self
    
    @property
    def graph(self) -> networkx.Graph:
        """
        The acutal Graph instance
        """
        return super().graph