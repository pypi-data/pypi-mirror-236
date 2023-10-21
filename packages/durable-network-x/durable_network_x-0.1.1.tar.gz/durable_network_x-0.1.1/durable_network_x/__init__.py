import networkx, typing
from durable_network_x.storage_managers import StorageManager

class DurableNetworkX:
    """A durable graph class that integrates with networkx for graph operations and persists the graph data."""

    __graph_type_mapping = {
        "Graph": networkx.Graph,
        "DiGraph": networkx.DiGraph,
        "MultiDiGraph": networkx.MultiDiGraph,
        "MultiGraph": networkx.MultiGraph
    }
    __graph: typing.Union[
        networkx.Graph, 
        networkx.DiGraph, 
        networkx.MultiDiGraph, 
        networkx.MultiGraph,
        None
    ] = None
    __allowed_networkx_graph_types: list[str] = list(__graph_type_mapping.keys())
    __networkx_graph_type: str = "Graph"
    __instance_id: typing.Optional[str] = None
    __instance_storage_path: typing.Optional[str] = None

    def __init__(
        self,
        storage_manager: StorageManager,
        graph_type: str = "Graph"
    ):
        """
        Initialize a DurableGraph object.

        :param storage_manager: An instance of StorageManager to handle the storage operations.
        :param graph_type: A string representing the type of graph. Default is "Graph".
        :raises AssertionError: If the provided graph_type is not allowed.
        """
        assert graph_type in self.__allowed_networkx_graph_types, \
            f"The graph_type (given: {graph_type}) MUST be equal to one of {', '.join(self.__allowed_networkx_graph_types)}"
        self.__storage_manager: StorageManager = storage_manager
        self.__networkx_graph_type = graph_type

    def __get_graph_constructor(self) -> typing.Callable:
        """
        Return the constructor of the specified graph type.
        
        :raises TypeError: If the graph_type is not recognized.
        """
        constructor = self.__graph_type_mapping.get(self.__networkx_graph_type)
        if not constructor:
            raise TypeError(
                f"The graph_type (given: {self.__networkx_graph_type}) MUST be equal to one of {', '.join(self.__allowed_networkx_graph_types)}"
            )
        return constructor
        
    def __verify_graph_type(self):
        """
        Check if the current graph instance matches the expected graph type.
        
        :raises TypeError: If the current graph type doesn't match the expected one.
        """
        if self.__graph is None:
            return
        required_graph_type = self.__graph_type_mapping.get(self.__networkx_graph_type)
        if not required_graph_type:
            raise TypeError(
                f"The graph_type (given: {self.__networkx_graph_type}) MUST be equal to one of {', '.join(self.__allowed_networkx_graph_types)}"
            )
        if not isinstance(self.__graph, required_graph_type):
            type_of_instance = str(type(self.__graph))
            raise TypeError((f"Graph type mismatch. The defined graph_type in constructor"
                             f" is `{self.__networkx_graph_type}` while the actual graph type"
                             f" is {type_of_instance}. Either correct the graph_type in"
                             " constructor or `delete` this instance and create a `new` one."))
        
    def __instance_id_to_storage_path(self, instance_id: str) -> str:
        """Convert an instance ID to its storage path."""
        return f"{instance_id}.graphml"
    
    def allowed_graph_types(self) -> list[str]:
        return self.__allowed_networkx_graph_types
    
    def save(self) -> 'DurableNetworkX':
        """
        Save the current graph to the storage.
        
        :raises NotImplementedError: If instance_id or instance_storage_path is missing.
        """
        if not (self.__instance_id and self.__instance_storage_path):
            raise NotImplementedError(f"No instance_id found. Create a `new` instance or `use` an instance before saving it")
        linefeed = chr(10)
        graphml = linefeed.join(networkx.generate_graphml(self.__graph))
        self.__storage_manager.write(graphml, self.__instance_storage_path)
        return self

    def new(
            self, 
            instance_id: str, 
            network_x_graph_to_use: typing.Union[
                networkx.Graph, 
                networkx.DiGraph, 
                networkx.MultiDiGraph, 
                networkx.MultiGraph,
                None
            ] = None
        ) -> 'DurableNetworkX':
        """
        Create a new graph instance.

        :param instance_id: A unique identifier for the graph instance.
        :param network_x_graph_to_use: An optional networkx graph instance. If not provided,
                                    a new graph of the type specified during class instantiation 
                                    will be created. If provided, it must match the graph type 
                                    specified during class instantiation.
        :returns: The current DurableNetworkX instance.
        :raises FileExistsError: If an instance with the given ID already exists.
        :raises TypeError: If the provided or generated graph does not match the expected type.
        """
        self.__instance_id = instance_id
        self.__instance_storage_path = self.__instance_id_to_storage_path(self.__instance_id)
        
        if self.__storage_manager.exists(self.__instance_storage_path):
            raise FileExistsError((f"An instance with id={self.__instance_id} already exists."
                                   " Cannot create a new one. Either `use` the existing instance"
                                   " or `delete` it first"))
        if network_x_graph_to_use is None:
            self.__graph = self.__get_graph_constructor()()
        else:
            self.__graph = network_x_graph_to_use
        self.__verify_graph_type()
        self.save()
        return self
    
    def use(self, instance_id: str) -> 'DurableNetworkX':
        """
        Use an existing graph instance.

        :param instance_id: A unique identifier for the graph instance.
        :raises FileNotFoundError: If no instance with the given ID exists.
        """
        self.__instance_id = instance_id
        self.__instance_storage_path = self.__instance_id_to_storage_path(self.__instance_id)
        
        if not self.__storage_manager.exists(self.__instance_storage_path):
            raise FileNotFoundError(f"An instance with id={self.__instance_id} does not exist. Create a `new` instance first.")
        
        graphml: typing.Optional[str] = self.__storage_manager.read(self.__instance_storage_path)
        if graphml:
            self.__graph = networkx.parse_graphml(graphml)
            self.__verify_graph_type()
        else:
            raise FileNotFoundError(f"Instance (id='{self.__instance_id}') not found.")
        return self

    def delete(self) -> 'DurableNetworkX':
        try:
            self.__storage_manager.delete(self.__instance_storage_path)
        except FileNotFoundError as e:
            print(f"[Warning] {str(e)}")
            
        del self.__graph
        self.__graph = None
        return self

    @property
    def graph(self) -> typing.Union[networkx.Graph, networkx.DiGraph, networkx.MultiDiGraph, networkx.MultiGraph, None]:
        """Returns the graph instance. The actual type of the graph returned 
        will match the type specified during class instantiation.

        Returns:
            networkx.Graph|networkx.DiGraph|networkx.MultiDiGraph|networkx.MultiGraph|None: The graph instance.
        """
        return self.__graph

    def exists_in_storage(self, instance_id: str) -> bool:
        "Check if the graph instance defined by instance_id exists in storage."
        return self.__storage_manager.exists(self.__instance_id_to_storage_path(instance_id))
    
    

