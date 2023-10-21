import networkx, typing
from durable_network_x import DurableNetworkX
from durable_network_x.storage_managers import StorageManager

class DurableDiGraph(DurableNetworkX):
    """
    DurableDiGraph is a specific implementation of DurableNetworkX that deals exclusively 
    with directed Graph objects from networkx.
    """

    def __init__(self, storage_manager: StorageManager):
        """
        Initialize a DurableDiGraph object.

        :param storage_manager: An instance of StorageManager to handle the storage operations.
        """
        super().__init__(storage_manager, graph_type = "DiGraph")
    
    def new(
        self, 
        instance_id: str, 
        network_x_graph_to_use: typing.Optional[networkx.DiGraph] = None
    ) -> 'DurableDiGraph':
        super().new(instance_id, network_x_graph_to_use)
        return self
    
    def use(self, instance_id: str) -> 'DurableDiGraph':
        super().use(instance_id)
        return self
    
    def save(self) -> 'DurableDiGraph':
        super().save()
        return self
    
    def delete(self) -> 'DurableDiGraph':
        super().delete()
        return self
    
    @property
    def graph(self) -> networkx.DiGraph:
        """
        The acutal DiGraph instance
        """
        return super().graph