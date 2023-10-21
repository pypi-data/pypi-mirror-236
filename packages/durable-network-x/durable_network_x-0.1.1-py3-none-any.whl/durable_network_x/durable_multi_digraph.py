import networkx, typing
from durable_network_x import DurableNetworkX
from durable_network_x.storage_managers import StorageManager

class DurableMultiGraph(DurableNetworkX):
    """
    DurableMultiGraph is a specific implementation of DurableNetworkX that deals exclusively 
    with MultiGraph objects from networkx.
    """

    def __init__(self, storage_manager: StorageManager):
        """
        Initialize a DurableDiGraph object.

        :param storage_manager: An instance of StorageManager to handle the storage operations.
        """
        super().__init__(storage_manager, graph_type = "MultiGraph")
    
    def new(
        self, 
        instance_id: str, 
        network_x_graph_to_use: typing.Optional[networkx.MultiGraph] = None
    ) -> 'DurableMultiGraph':
        super().new(instance_id, network_x_graph_to_use)
        return self
    
    def use(self, instance_id: str) -> 'DurableMultiGraph':
        super().use(instance_id)
        return self
    
    def save(self) -> 'DurableMultiGraph':
        super().save()
        return self
    
    def delete(self) -> 'DurableMultiGraph':
        super().delete()
        return self
    
    @property
    def graph(self) -> networkx.MultiGraph:
        """
        The acutal MultiGraph instance
        """
        return super().graph