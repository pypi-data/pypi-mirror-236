import networkx, typing
from durable_network_x import DurableNetworkX
from durable_network_x.storage_managers import StorageManager

class DurableMultiDiGraph(DurableNetworkX):
    """
    DurableMultiDiGraph is a specific implementation of DurableNetworkX that deals exclusively 
    with MultiDiGraph objects from networkx.
    """

    def __init__(self, storage_manager: StorageManager):
        """
        Initialize a DurableDiGraph object.

        :param storage_manager: An instance of StorageManager to handle the storage operations.
        """
        super().__init__(storage_manager, graph_type = "MultiDiGraph")
    
    def new(
        self, 
        instance_id: str, 
        network_x_graph_to_use: typing.Optional[networkx.MultiDiGraph] = None
    ) -> 'DurableMultiDiGraph':
        super().new(instance_id, network_x_graph_to_use)
        return self
    
    def use(self, instance_id: str) -> 'DurableMultiDiGraph':
        super().use(instance_id)
        return self
    
    def save(self) -> 'DurableMultiDiGraph':
        super().save()
        return self
    
    def delete(self) -> 'DurableMultiDiGraph':
        super().delete()
        return self
    
    @property
    def graph(self) -> networkx.MultiDiGraph:
        """
        The acutal MultiDiGraph instance
        """
        return super().graph