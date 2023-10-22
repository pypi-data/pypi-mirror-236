class ADPTWVertexData:
    """
    Data stored on vertices in an ADPTW problem setting.
    """

    def __init__(self, x: float, y: float, demand: float, earliest_time_of_arrival: float,
                 latest_time_of_arrival: float, service_time: float) -> ADPTWVertexData:
        """
        :param x: The x coordinate of the vertex.
        :param y: The y coordinate of the vertex.
        :param demand: The demand of the vertex. 0 for station and depot vertices.
        :param earliest_time_of_arrival: The earliest time at which service at the vertex can begin.
        :param latest_time_of_arrival: The latest time at which service at the vertex can begin.
        :param service_time: The time needed to serve the vertex.
        """
        ...


class ADPTWArcData:
    """
    Data stored on arcs in an ADPTW problem setting.
    """

    def __init__(self, distance: float, travel_time: float, consumption: float) -> ADPTWArcData:
        """
        :param distance: The distance between the two vertices connected by the arc.
        :param travel_time: The time it takes to travel between the two vertices connected by the arc.
        :param consumption: The time required to replenish the resource consumed when traveling between the two vertices connected by the arc.
        """
        ...


# adptw submodule
def create_adptw_vertex(vertex_id: int, str_id: str, is_facility: bool, is_depot: bool,
                        data: ADPTWVertexData) -> Vertex:
    """
    Creates a vertex for an ADPTW problem setting. Stores :param data directly as a native C++ object.

    .. warning::
        The data member of the created vertex is not accessible from python. Doing so will likely result in a crash.


    :param vertex_id: The unique identifier of the vertex.
    :param str_id: A human-readable string identifier for the vertex.
    :param is_facility: Whether the vertex is a replenishment facility.
    :param is_depot: Whether the vertex is a depot.
    :param data: The data to associate with this vertex.
    :return:
    """
    ...


def create_adptw_arc(data: ADPTWArcData) -> Arc:
    """
    Creates an arc for an ADPTW problem setting. Stores :param data directly as a native C++ object.

    .. warning::
        The data member of the created arc is not accessible from python. Doing so will likely result in a crash.

    :param data: The data to associate with this vertex
    :return:
    """
    ...


class ADPTWEvaluation(PyEvaluation):
    """
    Evaluation for ADPTW problems. Works only with arcs and vertices created using :ref:`create_adptw_arc` and :ref:`create_adptw_vertex`.
    Uses a set of penalty factors to penalize infeasible solutions.

    :var overload_penalty_factor: The penalty factor for overloading the vehicle.
    :var resource_penalty_factor: The penalty factor for consuming more resources than carried the vehicle.
    :var time_shift_penalty_factor: The penalty factor for time shifts.
    """

    overload_penalty_factor: float
    resource_penalty_factor: float
    time_shift_penalty_factor: float

    def __init__(self, vehicle_resource_capacity: float, vehicle_storage_capacity: float) -> None:
        """
        :param float vehicle_resource_capacity: The vehicle's battery capacity expressed in units of time, that is, the time it takes to fully replenish the resource of an empty vehicle.
        :param float vehicle_storage_capacity: The vehicle's storage capacity. Determines how much demand can be served in a single route.
        """
        ...


class ADPTWFacilityPlacementOptimizer:
    """
    ADPTW-specific detour insertion algorithm. Inserts visits to replenishment facilities at optimal locations into a route.
    """

    def __init__(self, instance: Instance, resource_capacity_time: float) -> None:
        """

        :param instance: The instance.
        :param resource_capacity_time: The vehicle's resource capacity expressed in units of time, that is, the time it takes to fully replenish the resource of an empty vehicle.
        """
        ...

    def optimize(self, route_vertex_ids: List[VertexID]) -> List[VertexID]:
        """
        Optimizes the route by inserting visits to replenishment facilities at optimal locations.
        :param route_vertex_ids: The vertex ids of the route to optimize.
        :return: The optimized route as a list of vertex ids.
        """
        ...
class RepairOperator:
    def __init__(self) -> None: ...

    def apply(self, evaluation: Evaluation, solution: Solution, removed_vertex_ids: List[VertexID]) -> None:
        """
        Apply this operator to the given solution. The solution is modified in-place.

        :param evaluation: The evaluation function to use.
        :param solution: The solution to apply the operator to.
        :param removed_vertex_ids: The IDs of the vertices that should be inserted into the solution.
        """
        ...

    def can_apply_to(self, solution: Solution) -> bool:
        """
        Check if this operator can be applied to the given solution.

        :param solution: The solution to check.
        """
        ...

    def name(self) -> str:
        """
        Get the name of this operator.
        """
        ...


class DestroyOperator:
    def __init__(self) -> None: ...

    def apply(self, evaluation: Evaluation, solution: Solution, number_of_vertices_to_remove: int) -> List[
        VertexID]:
        """
        Apply this operator to the given solution. The solution is modified in-place.

        :param evaluation: The evaluation function to use.
        :param solution: The solution to apply the operator to.
        :param number_of_vertices_to_remove: The number of vertices to remove from the solution.
        :return: A list containing the IDs of the vertices that were removed from the solution.
        """
        ...

    def can_apply_to(self, solution: Solution) -> bool:
        """
        Check if this operator can be applied to the given solution.

        :param solution: The solution to check.
        """
        ...

    def name(self) -> str:
        """
        Get the name of this operator.
        """
        ...


class AdaptiveLargeNeighborhood:
    """
    ALNS solver.
    Initially, all operators are assigned equal weights of 1. The weights are then adapted based on the performance of the
    operators in the last period. Upon requesting an update, the weights are recalculated as follows:

    .. math::

        w_{op, new} = \\alpha \\cdot \\frac{s_{op}}{\\max(1, n_{op})} + (1 - \\alpha) \\cdot w_{op, old}

    Where

    * :math:`w_{op, new}` is the updated weight of operator :math:`op`
    * :math:`\\alpha` is the smoothing factor, which determines the importance of an operator's historical performance
    * :math:`s_{op}` is the sum of scores achieved by operator :math:`op` in the last period
    * :math:`n_{op}` is the total number of solutions generated using operator :math:`op` in the last period
    * :math:`w_{op, old}` is the old weight of operator :math:`op`
    """

    def __init__(self, randgen: Random, smoothing_factor: float) -> None:
        """
        :param randgen: Random number generator.
        :param smoothing_factor: Smoothing factor for the adaptive weights. Determines the importance of the historical
        performance of the operators.
        """
        ...

    def adapt_operator_weights(self) -> None:
        """
        Calculate the new weights for the operators based on their respective performance in the last period.
        """
        ...

    def add_destroy_operator(self, destroy_operator: DestroyOperator) -> DestroyOperator:
        """
        Register a new destroy operator. The weight of this operator is initialized to the average weight of all other
        destroy operators.

        :param destroy_operator: The operator to add.
        """
        ...

    def add_repair_operator(self, repair_operator: RepairOperator) -> RepairOperator:
        """
        Register a new repair operator. The weight of this operator is initialized to the average weight of all other
        repair operators.

        :param repair_operator: The operator to add.
        """
        ...

    def collect_score(self, destroy_operator: DestroyOperator, repair_operator: RepairOperator,
                      score: float) -> None:
        """
        Collect the score achieved by a solution generated by the given destroy and repair operators.

        :param destroy_operator: The destroy operator used to generate the solution.
        :param repair_operator: The repair operator used to generate the solution.
        :param score: The score achieved by the solution.
        """
        ...

    def generate(self, evaluation: Evaluation, solution: Solution, number_of_vertices_to_remove: int) -> Tuple[
        DestroyOperator, RepairOperator]:
        """
        Generate a new solution by applying a destroy and repair operator selected based the on the operator weights.
        Modifies the solution in-place.

        :param evaluation: The evaluation function to use.
        :param solution: The solution to generate a new solution from.
        :param number_of_vertices_to_remove: The number of vertices to remove from the solution.
        :return: A tuple containing the destroy and repair operator used to generate the solution.
        """
        ...

    def remove_destroy_operator(self, destroy_operator: DestroyOperator) -> None:
        """
        Remove a destroy operator.

        :param destroy_operator: The operator to remove.
        """
        ...

    def remove_repair_operator(self, repair_operator: RepairOperator) -> None:
        """
        Remove a repair operator.

        :param repair_operator: The operator to remove.
        """
        ...

    def reset_operator_weights(self) -> None:
        """
        Reset the weights of all operators to 1.
        """
        ...

    @property
    def destroy_operators(self) -> Iterator:
        """
        Get an iterator over all registered destroy operators.
        """
        ...

    @property
    def repair_operators(self) -> Iterator:
        """
        Get an iterator over all registered repair operators.
        """
        ...
class _RandomRemovalOperator(DestroyOperator):
    """
    Removes random vertices from the solution. Note that the same vertex may apppear several times, i.e., if two
    visits to the same vertex are removed.
    """

    def __init__(self, random: Random) -> None:
        """
        :param Random random: The random number generator used.
        """


class _RandomInsertionOperator(RepairOperator):
    """
    Inserts vertices at random positions in the solution.
    """

    def __init__(self, random: Random) -> None:
        """
        :param random: The :py:class:`routingblocks.Random` instance to use.
        """
from typing import Any


class Arc:
    """
    A simple arc object that represents a connection between two vertices in a graph. The arc stores additional data
    transparent to the RoutingBlocks package. This data can be used to store additional information about the arc, such as
    distances, durations, or any other attributes relevant to the problem being modeled.
    """

    def __init__(self, data: Any) -> None:
        """
        :param data: Additional data associated with the arc.
        """
        ...

    @property
    def data(self) -> Any:
        """
        Retrieves the arc data.

        :return: The data associated with the arc.
        :rtype: Any
        """

    def __str__(self) -> str:
        """
        Generates a human-readable string representation of the arc.

        :return: A string representation of the arc.
        :rtype: str
        """
        ...
from typing import Any, List, Tuple, overload


class Evaluation:
    """
    The evaluation class implements problem-specific cost and move evaluation functions. It's design bases on the
    concepts introduced in :cite:t:`VidalCrainicEtAl2014`.
    Note that this class is an interface: it's not meant to be instantiated or used directly. Please use the concrete
    implementations of this interface and helper functions instead.
    """

    def __init__(self) -> None: ...

    def compute_cost(self, label: AnyForwardLabel) -> float:
        """
        Computes the cost of a given label.

        :param label: The label
        :return: The cost of the label
        :rtype: float
        """
        ...

    def evaluate(self, instance: Instance,
                 segments: List[List[Tuple[Vertex, AnyForwardLabel, AnyBackwardLabel]]]) -> float:
        """
        Evaluates the cost of the route given by concatenating the passed route sub-sequences. Each sub-sequences is
        guaranteed to have valid forward and backward labels.

        Corresponds to ``EVALN`` in :cite:t:`VidalCrainicEtAl2014`.

        :param instance: The instance
        :param segments: A list of route sub-sequences, each given as a list of tuples of (vertex, forward label, backward label)
        :return: The cost of the route
        :rtype: float
        """
        ...

    def create_backward_label(self, vertex: Vertex) -> AnyBackwardLabel:
        """
        Creates and initializes a backward label for the given vertex.

        Corresponds to ``INIT`` in :cite:t:`VidalCrainicEtAl2014`.

        :param vertex: The vertex representing singleton route [vertex]
        :return: The initialized backward label
        :rtype: AnyBackwardLabel
        """
        ...

    def create_forward_label(self, vertex: Vertex) -> AnyForwardLabel:
        """
        Creates and initializes a forward label for the given vertex.

        Corresponds to ``INIT`` in :cite:t:`VidalCrainicEtAl2014`.

        :param vertex: The vertex representing singleton route [vertex]
        :return: The initialized backward label
        :rtype: AnyBackwardLabel
        """
        ...

    def get_cost_components(self, label: AnyForwardLabel) -> List[float]:
        """
        Returns the cost components of a given label.

        :param label: The label
        :return: The cost components of the label
        :rtype: List[float]
        """
        ...

    def is_feasible(self, label: AnyForwardLabel) -> bool:
        """
        Checks whether a given label is feasible.

        :param label: The label
        :return: True if the label is feasible, False otherwise
        :rtype: bool
        """
        ...

    def propagate_forward(self, pred_label: AnyForwardLabel, pred_vertex: Vertex, vertex: Vertex,
                          arc: Arc) -> AnyForwardLabel:
        """
        Extends the partial route represented by the forward label of pred_vertex to the vertex.

        Corresponds to ``FORW([..., pred_vertex]⊕[vertex])`` in :cite:t:`VidalCrainicEtAl2014`.

        :param pred_label: The forward label of the predecessor vertex
        :param pred_vertex: The predecessor vertex
        :param vertex: The vertex
        :param arc: The arc connecting pred_vertex and vertex
        :return: The propagated forward label
        :rtype: AnyForwardLabel
        """
        ...

    def propagate_backward(self, succ_label: AnyBackwardLabel, succ_vertex: Vertex, vertex: Vertex,
                           arc: Arc) -> AnyBackwardLabel:
        """
        Extends the partial route represented by the backward label of succ_vertex to the vertex.

        Corresponds to ``BACK([vertex]⊕[succ_vertex, ...])`` in :cite:t:`VidalCrainicEtAl2014`.

        :param succ_label: The backward label of the successor vertex
        :param succ_vertex: The successor vertex
        :param vertex: The vertex
        :param arc: The arc connecting succ_vertex to vertex. Note that this corresponds to the reverse arc of the forward direction.
        :return: The propagated backward label
        :rtype: AnyBackwardLabel
        """
        ...


class PyEvaluation(Evaluation):
    """
    The PyEvaluation class implements the evaluation interface in pure Python. It's meant to be used as a base class
    for custom python-based evaluation classes.
    """
    ...


class PyConcatenationBasedEvaluation(Evaluation):
    def __init__(self) -> None: ...

    def concatenate(self, fwd: AnyForwardLabel, bwd: AnyBackwardLabel, vertex: Vertex) -> float:
        """
        Specialization of the general evaluation member of :ref:`PyEvaluation` for cases where two route subsequences can
        be concatenated efficiently. Classes who extend this class do not need to implement :ref:`PyEvaluation.evaluate`.

        The concatenation function works as follows:
        Assume that we have two route subsequences ``[v_1, ..., v_n]`` and ``[v_{n+1}, ..., v_m]``. The specialized evaluation
        function first propagates v_n to v_{n+1}, and the calls ``concatenate(fwd_{n+1}, bwd_{n+1}, v_{n+1})`` where ``fwd_{n+1}`` is the
        forward label of ``v_{n+1}`` and ``bwd_{n+1}`` is the backward label of ``v_{n+1}``.

        If the specialized evaluation function is called with several route sub-sequences
        ``[..., v_n], [v_n+1, ... v_{n+m}], [v_{n+m+1}, ...]`` then the first sequence is extended to v_{n+m} and the
        operation reduces to the first case:
        ``concatenate(fwd_{n+m+1}, bwd_{n+m+1}, v_{n+m+1})`` where ``fwd_{n+m+1}`` is the forward label of ``v_{n+m+1}`` and ``bwd_{n+m+1}`` is the backward label of ``v_{n+m+1}``.

        :param fwd: The forward label representing the route sub-sequence ``[v_1, ..., v_n, v_{n+1}]``
        :param bwd: The backward label representing the route sub-sequence ``[v_{n+1}, ..., v_m]``
        :param vertex: The vertex ``v_{n+1}``
        :return: The cost of the route ``[v_1, ..., v_n, v_{n+1}, ..., v_m]``
        :rtype: float
        """
        ...


@overload
def evaluate_insertion(evaluation: Evaluation, instance: Instance, route: Route, after_position: int,
                       vertex_id: VertexID) -> float:
    """
    Evaluates inserting a vertex into a route after the specified position.

    :param evaluation: The evaluation function
    :param instance: The instance
    :param route: The route
    :param after_position: The position after which the vertex is inserted
    :param vertex_id: The id of the vertex to insert
    :return: The cost of the route with the vertex inserted
    :rtype: float
    """
    ...


@overload
def evaluate_insertion(evaluation: Evaluation, instance: Instance, route: Route, after_position: int,
                       vertex: Vertex) -> float:
    """
    Evaluates inserting a vertex into a route after the specified position.

    :param evaluation: The evaluation function
    :param instance: The instance
    :param route: The route
    :param after_position: The position after which the vertex is inserted
    :param vertex: The vertex to insert
    :return: The cost of the route with the vertex inserted
    :rtype: float
    """
    ...


@overload
def evaluate_insertion(evaluation: Evaluation, instance: Instance, route: Route, after_position: int,
                       node: Node) -> float:
    """
    Evaluates inserting a node into a route after the specified position.

    :param evaluation: The evaluation function
    :param instance: The instance
    :param route: The route
    :param after_position: The position after which the vertex is inserted
    :param node: The node to insert
    :return: The cost of the route with the vertex inserted
    :rtype: float
    """
    ...


def evaluate_splice(evaluation: Evaluation, instance: Instance, route: Route, forward_segment_end_pos: int,
                    backward_segment_begin_pos: int) -> float:
    """
    Evaluates splicing two sub-sequences of a route together. The first sub-seuence ends (non-inclusive) at
    ``forward_segment_end_pos`` and the second sub-sequence starts (including) at ``backward_segment_begin_pos``.

    Example:
    Let ``route = [D, C1, C2, C3, C4, C5, C6, D]`` and ``forward_segment_end_pos = 2`` and ``backward_segment_begin_pos = 5``.
    Then the sub-sequences are ``[D, C1]`` and ``[C5, C6, D]``. The splice operation thus evaluates the cost of the route
    ``[D, C1, C5, C6, D]``.

    :param evaluation: The evaluation function
    :param instance: The instance
    :param route: The route
    :param forward_segment_end_pos: The end position of the first sub-sequence (non-inclusive)
    :param backward_segment_begin_pos: The start position of the second sub-sequence
    :return: The cost of the spliced route
    :rtype: float
    """
    ...
class Propagator:
    """
    The Propagator class implements problem-specific ordering, dominance, and propagation functions. It's design bases on the
    concepts introduced in :cite:t:`Irnich2008`.
    Note that this class is an interface: it's not meant to be instantiated or used directly. Please use the concrete
    implementations of this interface instead.
    """

    def __init__(self) -> None: ...

    def cheaper_than(self, label: Any, other_label: Any) -> bool:
        """
        Checks whether the label is cheaper than the other label, i.e., has lower cost.

        :param label: The (potentially) cheaper label.
        :param other_label: The (potentially) more expensive label.
        :return: True if the label is cheaper than the other label, False otherwise.
        """
        ...

    def create_root_label(self) -> Any:
        """
        Creates the initial label for the dynamic programming algorithm. Represents the state at the source node, i.e. the
        depot node.
        :return: The initial label.
        """
        ...

    def dominates(self, label: Any, other_label: Any) -> bool:
        """
        Checks whether the label dominates the other label.

        :param label: The (potentially) dominating label.
        :param other_label: The (potentially) dominated label.
        :return:
        """
        ...

    def extract_path(self, label: Any) -> List[VertexID]:
        """
        Extracts the path represented by label, converting it to a list of vertex IDs.

        :param label: The label that represents the path.
        :return: The list of vertex IDs visited on the path.
        """
        ...

    def is_final_label(self, label: Any) -> bool:
        """
        Checks whether the label is the final label, i.e. whether it represents a depot-depot path.
        :param label: The label to check.
        :return: True if the label is final, False otherwise.
        """
        ...

    def order_before(self, label: Any, other_label: Any) -> bool:
        """
        Whether the label should be ordered before the other label. This is used to determine the order in which labels are
        stored in the set of settled labels, which is important for dominance checks: the checks considers only labels that
        would be ordered before the label being checked.

        :param label: The (potentially) earlier label.
        :param other_label: The (potentially) later label.
        :return: True if the label should be ordered before the other label, False otherwise.
        """
        ...

    def prepare(self, route_vertex_ids: List[VertexID]) -> None:
        """
        Prepare the propagator before running the algorithm on the route represented by the given vertex IDs.
        :param route_vertex_ids: The vertex IDs of the route.
        """
        ...

    def propagate(self, label: Any, origin_vertex: Vertex, target_vertex: Vertex, arc: Arc) -> Optional[
        Any]:
        """
        Propagates the label to the target vertex, using the given arc. This creates a new label that represents the state
        at the target vertex. Return None if the resulting path would be infeasible.

        :param label: The label to propagate.
        :param origin_vertex: The origin vertex of the arc.
        :param target_vertex: The target vertex of the arc.
        :param arc: The arc to propagate the label along.
        :return: The propagated label, or None if the resulting path would be infeasible.
        """
        ...


class FacilityPlacementOptimizer:
    """
    Algorithm that inserts visits to replenishment facilities at optimal locations into a route.
    """

    def __init__(self, instance: Instance, propagator: Propagator) -> None:
        """

        :param instance: The instance.
        :param propagator: The propagator to use.
        """
        ...

    def optimize(self, route_vertex_ids: List[VertexID]) -> List[VertexID]:
        """
        Inserts visits to replenishment facilities at optimal locations into the route represented by the given vertex IDs.

        :param route_vertex_ids: The vertex IDs of the route.
        :return: The vertex IDs of the optimized route.
        """
        ...
class InsertionMove:
    vertex_id: VertexID
    after_node: NodeLocation
    delta_cost: float

    def __init__(self, vertex_id: VertexID, after_node_location: NodeLocation, delta_cost: float) -> None:
        """
        :param vertex_id: The vertex to be inserted.
        :param after_node: The node after which the vertex should be inserted.
        :param delta_cost: The change in cost incurred from inserting the vertex at the specified position.
        """
        ...

    def __eq__(self, other: InsertionMove) -> bool: ...


class InsertionCache:
    def __init__(self, instance: Instance) -> None: ...

    def clear(self) -> None: ...

    def get_best_insertions_for_vertex(self, vertex_id: VertexID) -> List[InsertionMove]: ...

    def invalidate_route(self, route: Route, route_index: int) -> None: ...

    def rebuild(self, evaluation: Evaluation, solution: Solution, vertex_ids: List[VertexID]) -> None: ...

    def stop_tracking(self, vertex_id: VertexID) -> None: ...

    def tracks_vertex(self, vertex_id: VertexID) -> bool: ...

    @property
    def moves_in_order(self) -> List[InsertionMove]: ...

    @property
    def tracked_vertices(self) -> List[VertexID]: ...
from typing import Iterator, overload, List


class Instance:
    """
    Represents an instance of a vehicle routing problem. The instance contains a collection of vertices (depot, stations,
    and customers), a matrix of arcs connecting the vertices, and a fleet size representing the number of vehicles available.
    Provides convenient methods to access and iterate through the various types of vertices.

    .. note::
        It is recommend to use the :ref:`InstanceBuilder <instance-builder>` to create instances.

    """

    @overload
    def __init__(self, depot: Vertex, stations: List[Vertex], customers: List[Vertex], arcs: List[List[Arc]],
                 fleet_size: int) -> None:
        """
        :param Vertex depot: The depot vertex
        :param List[Vertex] stations: A list of station vertices
        :param List[Vertex] customers: A list of customer vertices
        :param List[List[Arc]]] arcs: A matrix of Arc objects representing the connections between vertices
        :param int fleet_size: The number of vehicles in the fleet
        """
        ...

    @overload
    def __init__(self, vertices: List[Vertex], arcs: List[List[Arc]]) -> None:
        """
        :param List[Vertex] vertices: A list of vertices in the order depot, stations, customers
        :param List[List[Arc]] arcs: A list of lists of Arc objects representing the connections between vertices
        """
        ...

    @overload
    def __init__(self, vertices: List[Vertex], arcs: List[List[Arc]], fleet_size: int) -> None:
        """
        :param List[Vertex] vertices: A list of vertices in the order depot, stations, customers
        :param List[List[Arc]] arcs: A list of lists of Arc objects representing the connections between vertices
        :param int fleet_size: The number of vehicles in the fleet
        """
        ...

    @property
    def fleet_size(self) -> int:
        """
        Retrieves the number of vehicles available.

        :return: The fleet size.
        :rtype: int
        """
        ...

    @property
    def number_of_customers(self) -> int:
        """
        Retrieves the number of customers.

        :return: The number of customers.
        :rtype: int
        """
        ...

    @property
    def number_of_stations(self) -> int:
        """
        Retrieves the number of stations.

        :return: The number of stations.
        :rtype: int
        """
        ...

    @property
    def number_of_vertices(self) -> int:
        """
        Retrieves the number of vertices.

        :return: The number of vertices.
        :rtype: int
        """
        ...

    @property
    def depot(self) -> Vertex:
        """
        Retrieves the depot vertex.

        :return: The depot vertex.
        :rtype: Vertex
        """
        ...

    @property
    def vertices(self) -> Iterator[Vertex]:
        """
        Retrieves an iterator over the instance's vertices.

        :return: An iterator over the instance's vertices.
        :rtype: Iterator[Vertex]
        """
        ...

    @property
    def stations(self) -> Iterator[Vertex]:
        """
        Retrieves an iterator over the station vertices.

        :return: An iterator over the station vertices.
        :rtype: Iterator[Vertex]
        """
        ...

    @property
    def customers(self) -> Iterator[Vertex]:
        """
        Retrieves an iterator over the customer vertices.

        :return: An iterator over the customer vertices.
        :rtype: Iterator[Vertex]
        """
        ...

    def __len__(self) -> int:
        """
        Retrieves the number of vertices in the instance.

        :return: The number of vertices.
        :rtype: int
        """
        ...

    def __iter__(self) -> Iterator[Vertex]:
        """
        Retrieves an iterator over the vertices in the instance.

        :return: An iterator over the vertices.
        :rtype: Iterator[Vertex]
        """
        ...

    def get_vertex(self, id: int) -> Vertex:
        """
        Retrieves a vertex by its ID.

        :param int id: The ID of the desired vertex.
        :return: The vertex with the specified ID.
        :rtype: Vertex
        """
        ...

    def get_customer(self, customer_index: int) -> Vertex:
        """
        Retrieves the n-th customer vertex.

        :param int customer_index: The index of the desired customer vertex.
        :return: The customer vertex at the specified index.
        :rtype: Vertex
        """
        ...

    def get_station(self, station_index: int) -> Vertex:
        """
        Retrieves the n-th station vertex.

        :param int station_index: The index of the desired station vertex.
        :return: The station vertex at the specified index.
        :rtype: Vertex
        """
        ...

    def get_arc(self, source_vertex_id: int, target_vertex_id: int) -> Arc:
        """
        Retrieves the arc connecting two vertices, specified by their IDs.

        :param int source_vertex_id: The ID of the source vertex.
        :param int target_vertex_id: The ID of the target vertex.
        :return: The arc connecting the source and target vertices.
        :rtype: Arc
        """
        ...
from typing import Optional


class ArcSet:
    def __init__(self, number_of_vertices: int) -> None: ...

    def forbid_arc(self, origin_vertex_id: VertexID, target_vertex_id: VertexID) -> None: ...

    def include_arc(self, origin_vertex_id: VertexID, target_vertex_id: VertexID) -> None: ...

    def includes_arc(self, origin_vertex_id: VertexID, target_vertex_id: VertexID) -> bool: ...


class GeneratorArc:
    @overload
    def __init__(self, solution: Solution, origin_route_index: int, origin_node_position: int, target_route_index: int,
                 target_node_position: int) -> None: ...

    @overload
    def __init__(self, solution: Solution, origin_location: NodeLocation, target_location: NodeLocation) -> None: ...

    @property
    def origin_node(self) -> Node: ...

    @property
    def origin_route(self) -> Route: ...

    @property
    def target_node(self) -> Node: ...

    @property
    def target_route(self) -> Route: ...


class Move:
    """
    Interface for implementing custom moves.
    """

    def __init__(self) -> None: ...

    def apply(self, instance: Instance, solution: Solution) -> None:
        """
        Applies the move to the solution.

        :param Instance instance: The instance.
        :param Solution solution: The solution to be improved.
        :return:
        """
        ...

    def get_cost_delta(self, evaluation: Evaluation, instance: Instance, solution: Solution) -> float:
        """
        Returns the cost delta of the move according to the passed evaluation function.

        :param evaluation: The evaluation function to use.
        :param instance: The instance.
        :param solution: The solution.
        :return:
        """
        ...


class LocalSearchOperator:
    """
    Interface for implementing custom local search operators.
    """

    def __init__(self) -> None: ...

    def finalize_search(self) -> None:
        """
        Called after the search for improving moves has been completed.
        """
        ...

    def find_next_improving_move(self, evaluation: Evaluation, solution: Solution,
                                 last_evaluated_move: Optional[Move]) -> Optional[Move]:
        """
        Finds the next improving move. Returns None if no improving move is found.
        To avoid looping forever, this method should pick up the search where it left off, i.e., at last_evaluated_move.

        :param Evaluation evaluation: The evaluation function to use.
        :param Solution solution: The solution to be improved.
        :param Optional[Move] last_evaluated_move: The last move that was evaluated. Note that this corresponds to the last Move this operator returned. None if no move has been evaluated yet.
        :return: The next improving move. None if no improving move is found.
        :rtype: Optional[Move]
        """
        ...

    def prepare_search(self, solution: Solution) -> None:
        """
        Called before the search for improving moves is started.

        :param Solution solution: The solution to be improved.
        """
        ...


class PivotingRule:
    """
    Interface for implementing custom pivoting rules.
    """

    def __init__(self) -> None:
        ...

    def select_move(self, solution: Solution) -> Optional[Move]:
        """
        Return the move to be applied to the solution.Returns none if no move is found.

        :param Solution solution: The solution to be improved.
        :return: The move to be applied to the solution.
        :rtype: Optional[Move]
        """
        ...

    def continue_search(self, found_improving_move: Move, delta_cost: float, solution: Solution) -> bool:
        """
        Determine if the search should continue or terminate.

        :param Move found_improving_move: The move found to be improving.
        :param float delta_cost: The(exact) cost difference between the current solution and the solution after applying the move.
        :param Solution solution: The solution the move should be applied to.
        :return: True if the search should continue, False otherwise.
        """
        ...


class BestImprovementPivotingRule(PivotingRule):
    """
    The best improvement pivoting rule selects the best improving move found during the search for improving moves.
    It never terminates the search prematurely.
    """
    ...


class KBestImprovementPivotingRule(PivotingRule):
    """
    The k - best improvement pivoting rule selects best out of the first k improving moves found during the search
    for improving moves. It terminates the search as soon as the k - th improving move is found.

    """

    def __init__(self, k: int) -> None:
        """
        :param int k: The number of improving moves to consider.
        """
        ...


class FirstImprovementPivotingRule(PivotingRule):
    """
    The first improvement pivoting rule selects the first improving move found during the search for improving moves.
    It terminates the search as soon as the first improving move is found.
    """
    ...


class LocalSearch:
    """
    This class implements a customizable local search algorithm.
    """

    def __init__(self, instance: Instance, evaluation: Evaluation, exact_evaluation: Optional[Evaluation],
                 pivoting_rule: PivotingRule) -> None: ...

    def optimize(self, solution: Solution, operators: List[LocalSearchOperator]) -> None:
        """
        Searches the neighborhood of the solution for improving moves and applies them until no further improvement is possible.
        The neighborhood is defined by the passed operators. Modifies the passed solution in-place.

        :param Solution solution: The solution to be improved.
        :param List[LocalSearchOperator] operators: The operators to use for searching the neighborhood.
        :return:
        """
        ...


class QuadraticNeighborhoodIterator:

    def __init__(self) -> None: ...

    def iter_neighborhood(solution: Solution) -> Iterator: ...
class NIFTWVertexData:
    """
    Data stored on vertices in an NIFTW problem setting.
    """

    def __init__(self, x: float, y: float, demand: float, earliest_time_of_arrival: float,
                 latest_time_of_arrival: float, service_time: float) -> None:
        """
        :param x: The x coordinate of the vertex.
        :param y: The y coordinate of the vertex.
        :param demand: The demand of the vertex. 0 for station and depot vertices.
        :param earliest_time_of_arrival: The earliest time at which service at the vertex can begin.
        :param latest_time_of_arrival: The latest time at which service at the vertex can begin.
        :param service_time: The time needed to serve the vertex.
        """
        ...


class NIFTWArcData:
    """
    Data stored on arcs in an NIFTW problem setting.
    """

    def __init__(self, distance: float, travel_time: float, consumption: float) -> None:
        """
        :param distance: The distance between the two vertices connected by the arc.
        :param travel_time: The time it takes to travel between the two vertices connected by the arc.
        :param consumption: The time required to recharge the resources consumed when traveling between the two vertices connected by the arc.
        """
        ...


# niftw submodule
def create_niftw_vertex(vertex_id: int, str_id: str, is_station: bool, is_depot: bool, data: NIFTWVertexData) -> Vertex:
    """
    Creates a vertex for an NIFTW problem setting. Stores :param data directly as a native C++ object.

    .. warning::
        The data member of the created vertex is not accessible from python. Doing so will likely result in a crash.


    :param vertex_id: The unique identifier of the vertex.
    :param str_id: A human-readable string identifier for the vertex.
    :param is_station: Whether the vertex is a station.
    :param is_depot: Whether the vertex is a depot.
    :param data: The data to associate with this vertex.
    :return:
    """
    ...


def create_niftw_arc(data: NIFTWArcData) -> Arc:
    """
    Creates an arc for an NIFTW problem setting. Stores :param data directly as a native C++ object.

    .. warning::
        The data member of the created arc is not accessible from python. Doing so will likely result in a crash.

    :param data: The data to associate with this vertex
    :return:
    """
    ...


class NIFTWEvaluation(PyEvaluation):
    """
    Evaluation for NIFTW problems. Works only with arcs and vertices created using :ref:`create_niftw_arc` and :ref:`create_niftw_vertex`.
    Uses a set of penalty factors to penalize infeasible solutions.

    :var overload_penalty_factor: The penalty factor for overloading the vehicle.
    :var resource_penalty_factor: The penalty factor for consuming more resources than carried by the vehicle.
    :var time_shift_penalty_factor: The penalty factor for time shifts.
    """
    overload_penalty_factor: float
    resource_penalty_factor: float
    time_shift_penalty_factor: float

    def __init__(self, vehicle_resource_capacity: float, vehicle_storage_capacity: float,
                 replenishment_time: float) -> None:
        """
        :param vehicle_resource_capacity: The vehicle's battery capacity expressed in units of time, that is, the time it takes to fully recharge an empty battery.
        :param vehicle_storage_capacity: The vehicle's storage capacity. Determines how much demand can be served in a single route.
        :param replenishment_time: The time penalty incurred to replenish all the resources carried by the vehicle.
        """
        ...


class NIFTWFacilityPlacementOptimizer:
    """
    NIFTW-specific detour insertion algorithm. Inserts visits to replenishment facilities at optimal locations into a route.
    """

    def __init__(self, instance: Instance, battery_capacity_time: float,
                 replenishment_time: float) -> None:
        """

        :param instance: The instance to optimize.
        :param battery_capacity_time: The vehicle's resource capacity expressed in units of time, that is, the time it takes to fully recharge an empty battery.
        :param replenishment_time: The time penalty incurred to replenish all the resources carried by the vehicle.
        """
        ...

    def optimize(self, route_vertex_ids: List[VertexID]) -> List[VertexID]:
        """
        Optimizes the route by inserting visits to replenishment facilities at optimal locations.
        :param route_vertex_ids: The vertex ids of the route to optimize.
        :return: The optimized route as a list of vertex ids.
        """
        ...
class Node:
    """
    A node represents a visit to a vertex.
    It carries forward and backward labels that are used for cost calculation, constraint checking, and efficient move evaluation.
    The data itself is opaque to the node class, and is only used by the evaluation object.
    """

    def __init__(self, vertex: Vertex, fwd_label: AnyForwardLabel, bwd_label: AnyBackwardLabel) -> None:
        """
        :param Vertex vertex: The associated Vertex object.
        :param AnyForwardLabel fwd_label: The forward label for the node.
        :param AnyBackwardLabel bwd_label: The backward label for the node.
        """
        ...

    def cost(self, evaluation: Evaluation) -> float:
        """
        Computes the cost according to the forward label carried by the node using the given evaluation.
        See the documentation of the evaluation object for more information.

        :param Evaluation evaluation: The evaluation object for computing costs.
        :return: The cost.
        :rtype: float
        """
        ...

    def cost_components(self, evaluation: Evaluation) -> List[float]:
        """
        Computes the individual cost components according to the forward label carried by the node using the given evaluation.
        See the documentation of the evaluation object for more information.

        :param Evaluation evaluation: The evaluation object for computing cost components.
        :return: A list of cost components.
        :rtype: List[float]
        """
        ...

    def feasible(self, evaluation: Evaluation) -> bool:
        """
        Determines if the node is feasible based on the given evaluation.
        See the documentation of the evaluation object for more information.

        :param Evaluation evaluation: The evaluation object for checking feasibility.
        :return: True if the node is feasible, False otherwise.
        :rtype: bool
        """
        ...

    def update_backward(self, evaluation: Evaluation, predecessor: Node, arc: Arc) -> None:
        """
        Updates the backward label of the node based on the given evaluation, predecessor node, and arc.
        See the documentation of the evaluation object for more information.

        :param Evaluation evaluation: The evaluation object for updating the backward label.
        :param Node predecessor: The predecessor node in the solution space.
        :param Arc arc: The arc connecting the predecessor node to the current node.
        """
        ...

    def update_forward(self, evaluation: Evaluation, successor: Node, arc: Arc) -> None:
        """
        Updates the forward label of the node based on the given evaluation, successor node, and arc.
        See the documentation of the evaluation object for more information.

        :param Evaluation evaluation: The evaluation object for updating the forward label.
        :param Node successor: The successor node in the solution space.
        :param Arc arc: The arc connecting the current node to the successor node.
        """
        ...

    @property
    def backward_label(self) -> AnyBackwardLabel:
        """
        Retrieves the backward label of the node.

        :return: The backward label.
        :rtype: AnyBackwardLabel
        """
        ...

    @property
    def forward_label(self) -> AnyForwardLabel:
        """
        Retrieves the forward label of the node.

        :return: The forward label.
        :rtype: AnyForwardLabel
        """
        ...

    @property
    def vertex(self) -> Vertex:
        """
        Retrieves the vertex represented by this node.

        :return: The associated Vertex object.
        :rtype: Vertex
        """
        ...

    @property
    def vertex_id(self) -> int:
        """
        Shorthand to retrieve the unique id of the node's vertex.

        :return: The unique identifier of the associated vertex.
        :rtype: int
        """
        ...

    @property
    def vertex_strid(self) -> str:
        """
        Shorthand to retrieve the name of the node's vertex.

        :return: The name of the associated vertex.
        """
        ...
class NodeLocation:
    """
    A class representing the location of a node within a solution. Stores the route index and the position of the node within that route.
    """
    route: int
    position: int

    def __init__(self, route: int, position: int) -> None:
        """
        :param int route: The index of the route in which the node is located.
        :param int position: The position of the node within the route.
        """
        ...

    def __eq__(self, other: NodeLocation) -> bool: ...

    def __getitem__(self, i: int) -> int: ...

    def __len__(self) -> int: ...

    def __lt__(self, other: NodeLocation) -> bool: ...

    def __ne__(self, other: NodeLocation) -> bool: ...
class Random:
    @overload
    def __init__(self) -> None:
        """
        Initializes a new instance of the Random class without a seed.

        If no seed value is provided, it uses the current system time or another
        system-specific source of randomness to generate random numbers.
        """

    @overload
    def __init__(self, seed: int) -> None:
        """
        Initializes a new instance of the Random class with a provided seed.

        The seed is a number used to initialize the underlying pseudo-random
        number generator.

        :param int seed: The seed value for the random number generator. Providing the
                     same seed will generate the same sequence of random numbers.
        """

    def randint(self, min: int, max: int) -> int:
        """
        Returns a random integer from the specified range [min, max], including
        both endpoints.

        :param int min: The lower bound of the range.
        :param int max: The upper bound of the range.

        :return: A random integer value from the specified range [min, max].
        """

    def uniform(self, min: float, max: float) -> float:
        """
        Returns a random floating-point number between the specified min and max values,
        including min and potentially up to max.

        :param float min: The lower bound of the range.
        :param float max: The upper bound of the range.
        :return: A random floating-point number within the specified range [min, max).
        """
class RemovalMove:
    vertex_id: VertexID
    node_location: NodeLocation
    delta_cost: float

    def __init__(self, vertex_id: VertexID, node_location: NodeLocation, delta_cost: float) -> None:
        """
        :param vertex_id: The vertex ID of the node to be removed.
        :param node_location: The location of the node to be removed.
        :param delta_cost: The change in cost of the solution if the node is removed.
        """
        ...

    def __eq__(self, other: RemovalMove) -> bool: ...


class RemovalCache:
    def __init__(self, instance: Instance) -> None: ...

    def clear(self) -> None: ...

    def invalidate_route(self, route: Route, route_index: int) -> None: ...

    def rebuild(self, evaluation: Evaluation, solution: Solution) -> None: ...

    @property
    def moves_in_order(self) -> List[RemovalMove]: ...
from typing import Iterable, Tuple


class Route:
    """
    Routes represent a sequence of visits to vertices, represented by Node objects.
    A route starts and ends at the depot.
    The route class ensures that the information stored in each node's label is consistent with the forward and
    backward sequences.

    Example:
        Route [D, a, b, c, d, e, D], where capital D represents a visit to the depot. Then the route class ensures
        that the forward labels stored on node 'c' represent the sequence [D, a, b, c], that is, are calculated by propagating the forward label at D across arcs (D, a), (a, b), (b, c).
        Similarly, the backward labels stored on node 'c' represent the sequence [c, d, e, D].

    Routes behave like lists of nodes, that is, they can e.g. be indexed and iterated over.

    Routes carry a globally unique modification timestamp which can be used to efficiently test two routes for equality:
    On each modification of the route, the modification timestamp is incremented, while copying a route preserves it's timestamp.
    Hence, two routes with the same modification timestamp are guaranteed to be equal, although the converse does not necessarily apply.
    """

    def __init__(self, evaluation: Evaluation, instance: Instance) -> None:
        """
        The route constructor creates an empty route, that is, a route that contains only start and end depots.
        Refer to create_route for a method to create a route from a sequence of vertex ids.

        :param Evaluation evaluation: The Evaluation object used for cost and feasibility calculations.
        :param Instance instance: The Instance object representing the problem instance.
        """
        ...

    @property
    def cost(self) -> float:
        """
        Calculates the route's cost.

        :return: The cost of the route.
        :rtype: float
        """
        ...

    @property
    def cost_components(self) -> List[float]:
        """
        Calculates the route's cost components.

        :return: A list of cost components .
        :rtype: List[float]
        """
        ...

    @property
    def depot(self) -> Node:
        """
        Retrieves the depot node of the route.

        :return: The start depot node.
        :rtype: Node
        """
        ...

    @property
    def empty(self) -> bool:
        """
        Determines if the route is empty.

        :return: True if the route is empty, False otherwise.
        :rtype: bool
        """
        ...

    @property
    def end_depot(self) -> Node:
        """
        Retrieves the end depot node of the route.

        :return: The end depot node.
        :rtype: Node
        """
        ...

    @property
    def feasible(self) -> bool:
        """
        Determines if the route is feasible.

        :return: True if the route is feasible, False otherwise.
        :rtype: bool
        """
        ...

    @property
    def modification_timestamp(self) -> int:
        """
        Retrieves the modification timestamp of the route.

        :return: The modification timestamp.
        :rtype: int
        """
        ...

    def __iter__(self) -> Iterator:
        """
        Returns an iterator over the nodes in the route.

        :return: An iterator over the nodes in the route.
        :rtype: Iterator
        """
        ...

    def __len__(self) -> int:
        """
        Returns the number of nodes in the route, including the depot nodes.

        :return: The number of nodes in the route, including depot nodes.
        :rtype: int
        """
        ...

    def __eq__(self, arg0: Route) -> bool:
        """
        Compares this route to another route for equality.
        Note that this does not use the route's modification timestamp, but rather compares the nodes in the route.

        :param Route arg0: The route to compare with.
        :return: True if the routes are equal, False otherwise.
        :rtype: bool
        """
        ...

    def __ne__(self, arg0: Route) -> bool:
        """
        Compares this route to another route for inequality.
        Note that this does not use the route's modification timestamp, but rather compares the nodes in the route.

        :param Route arg0: The route to compare with.
        :return: True if the routes are not equal, False otherwise.
        :rtype: bool
        """
        ...

    def exchange_segments(self, segment_begin_position: int, segment_end_position: int,
                          other_segment_begin_position: int,
                          other_segment_end_position: int, other_route: Route) -> None:
        """
        Exchanges the segment [segment_begin_position, segment_end_position) of this route with the segment
        [other_segment_begin_position, other_segment_end_position) of the other route. The swapped segments do not
        include the respective segment end nodes. This method if well defined even if other_route is this route as
        long as the segments do not overlap.

        :param int segment_begin_position: The start position of the segment in this route.
        :param int segment_end_position: The end position of the segment in this route. Not included.
        :param int other_segment_begin_position: The start position of the segment in the other route.
        :param int other_segment_end_position: The end position of the segment in the other route. Not included.
        :param Route other_route: The other route to exchange segments with.
        """
        ...

    def insert_segment_after(self, position: int, node_segment: List[Node]) -> int:
        """
        Inserts a sequence of nodes after the given position in the route.

        :param int position: The position after which to insert the segment.
        :param List[Node] node_segment: The sequence of nodes to insert.
        :return: The new position after the insertion.
        :rtype: int
        """
        ...

    def insert_vertices_after(self, vertices: Iterable[Tuple[VertexID, int]]) -> None:
        """
        Inserts a batch of vertices at the given positions. This method is more efficient than calling insert_segment_after
        multiple times.


        :param Iterable vertices: The iterable containing tuples of vertices with the positions to insert after.
        """
        ...

    def remove_segment(self, begin_position: int, end_position: int) -> int:
        """
        Removes a segment of nodes from the route. Example:

        .. code-block:: python

            route = routingblocks.create_route(evaluation, instance, [D, C1, C2, C3, D])
            new_position_of_end_position = route.remove_segment(1, 3)
            print(route) # [D, C3, D]
            print(new_position_of_end_position) # 1

        :param int begin_position: The start position of the segment to remove.
        :param int end_position: The end position of the segment to remove. Not inclusive.
        :return: The new position of end_position after removal.
        :rtype: int
        """
        ...

    def remove_vertices(self, vertex_positions: List[int]) -> None:
        """
        Removes vertices at the specified positions from the route.

        :param List[int] vertex_positions: The list of vertex positions to remove.
        """
        ...

    def update(self) -> None:
        """
        Updates the route, recalculating the forward and backward labels, costs, and feasibility.
        """
        ...

    def __copy__(self) -> Route:
        """
        Creates a copy of the route. Copies Node objects and labels, but not the underlying Vertex and Instance objects.

        :return: A deep copy of the route.
        :rtype: Route
        """
        ...

    def copy(self) -> Route:
        """
        Creates a copy of the route. Copies Node objects and labels, but not the underlying Vertex and Instance objects.

        :return: A deep copy of the route.
        :rtype: Route
        """
        ...

    def __deepcopy__(self, memodict: Dict = None) -> Route:
        """
        Creates a copy of the route. Copies Node objects and labels, but not the underlying Vertex and Instance objects.
        Same as __copy__.

        :param Dict memodict: A dictionary for memoization (optional).
        :return: A deep copy of the route.
        :rtype: Route
        """
        ...

    def __getitem__(self, position: int) -> Node:
        """
        Retrieves the node at the specified position in the route.

        :param int position: The position of the node.
        :return: The node at the specified position.
        :rtype: Node
        """
        ...


def create_route(evaluation: Evaluation, instance: Instance, vertex_ids: List[int]) -> Route: ...
from typing import overload


class Solution:
    """
    The Solution class represents a solution to a VRP problem.
    It maintains a list of Route objects, providing methods for cost calculation, feasibility checking, route manipulation, and finding vertices.
    Solution objects behave like lists of routes, so you can iterate over them, index them, and get their length:

    .. code-block:: python

        solution = Solution(evaluation, instance, 5)

        for route in solution:
            print(route)

        print(solution[0])

        print(len(solution))

        del solution[0]

    Note that any operations that add routes implicitly copy the route objects. For example:

    .. code-block:: python

        solution = Solution(evaluation, instance, 0)
        route = create_route(evaluation, instance, [D, C1, D])
        solution.add_route(route)

        route.insert_vertex_after(1, C2)
        print(route) # [D, C1, C2, D]
        print(solution.routes[0]) # [D, C1, D]

    """

    @overload
    def __init__(self, evaluation: Evaluation, instance: Instance, number_of_routes: int) -> None:
        """
        Creates a new Solution object with the specified number of empty routes.

        :param Evaluation evaluation: The evaluation object for cost and feasibility calculations.
        :param Instance instance: The Instance object representing the problem instance.
        :param int number_of_routes: The number of empty routes the solution should contain.
        """
        ...

    @overload
    def __init__(self, evaluation: Evaluation, instance: Instance, routes: List[Route]) -> None:
        """
        Creates a new Solution object with the specified list of routes.

        :param Evaluation evaluation: The evaluation object for cost and feasibility calculations.
        :param Instance instance: The Instance object representing the problem instance.
        :param List[Route] routes: The list of routes to include in the solution.
        """
        ...

    def add_route(self, route: Optional[Route] = None) -> None:
        """
        Adds a new route to the solution. If no route is provided, an empty route will be added.

        :param Optional[Route] route: The route to add to the solution (optional).
        """
        ...

    @overload
    def exchange_segment(self, first_route: Route, first_route_begin_position: int, first_route_end_position: int,
                         second_route: Route, second_route_begin_position: int,
                         second_route_end_position: int) -> None:
        """
        Exchanges segments between two routes using Route objects.

        :param Route first_route: The first route in the exchange operation.
        :param int first_route_begin_position: The start position of the segment in the first route.
        :param int first_route_end_position: The end position of the segment in the first route.
        :param Route second_route: The second route in the exchange operation.
        :param int second_route_begin_position: The start position of the segment in the second route.
        :param int second_route_end_position: The end position of the segment in the second route.
        """
        ...

    @overload
    def exchange_segment(self, first_route_index: int, first_route_begin_position: int, first_route_end_position: int,
                         second_route_index: int, second_route_begin_position: int,
                         second_route_end_position: int) -> None:
        """
        Exchanges segments between two routes using their indices.

        :param int first_route_index: The index of the first route in the exchange operation.
        :param int first_route_begin_position: The start position of the segment in the first route.
        :param int first_route_end_position: The end position of the segment in the first route.
        :param int second_route_index: The index of the second route in the exchange operation.
        :param int second_route_begin_position: The start position of the segment in the second route.
        :param int second_route_end_position: The end position of the segment in the second route.
        """
        ...

    def find(self, vertex_id: int) -> List[NodeLocation]:
        """
        Finds the locations of a vertex in the solution.

        :param int vertex_id: The vertex ID to search for.
        :return: A list of NodeLocation objects representing the locations of the vertex in the solution.
        :rtype: List[NodeLocation]
        """
        ...

    def insert_vertex_after(self, after_location: NodeLocation, vertex_id: int) -> int:
        """
        Inserts a vertex after the specified location.

        :param NodeLocation after_location: The location after which to insert the vertex.
        :param int vertex_id: The vertex ID to insert.
        :return: The position of the newly inserted vertex.
        :rtype: int
        """
        ...

    def insert_vertices_after(self, vertex_ids_and_positions: Iterable[Tuple[VertexID, NodeLocation]]) -> None:
        """
        Inserts multiple vertices at the specified locations.

        :param Iterable[Tuple[VertexID, NodeLocation]] vertex_ids_and_positions: An iterable of tuples containing the vertex ID and the location after which to insert the vertex.
        """
        ...

    def lookup(self, location: NodeLocation) -> Node:
        """
        Retrieves the node at the specified location.

        :param NodeLocation location: The location of the node to retrieve.
        :return: The node at the specified location.
        :rtype: Node
        """
        ...

    def remove_route(self, route: Route) -> None:
        """
        Removes the specified route from the solution.

        :param Route route: The route to remove from the solution.
        """
        ...

    def remove_vertex(self, location: NodeLocation) -> None:
        """
        Removes the vertex at the specified location.

        :param NodeLocation location: The location of the vertex to remove.
        """
        ...

    def remove_vertices(self, locations: List[NodeLocation]) -> None:
        """
        Removes multiple vertices at the specified locations.
        This is more efficient than calling remove_vertex() multiple times.

        :param List[NodeLocation] locations: A list of locations of the vertices to remove.
        """
        ...

    def copy(self) -> Solution:
        """
        Creates a copy of the solution. This copies routes and nodes.

        :return: A copy of the solution.
        :rtype: Solution
        """
        ...

    def __copy__(self) -> Solution:
        """
        Creates a copy of the solution. This copies routes and nodes.

        :return: A copy of the solution.
        :rtype: Solution
        """
        ...

    def __deepcopy__(self, memodict: dict = {}) -> Solution:
        """
        Creates a copy of the solution. This copies routes and nodes.

        :param dict memodict: A memoization dictionary to store copies of objects (Optional).
        :return: A copy of the solution.
        :rtype: Solution
        """
        ...

    def __delitem__(self, route_index: int) -> None:
        """
        Removes the route at the specified index.

        :param int route_index: The index of the route to remove.
        """
        ...

    def __eq__(self, other: Solution) -> bool:
        """
        Determines if the solution is equal to another solution.

        :param Solution other: The other solution to compare.
        :return: True if the solutions are equal, False otherwise.
        :rtype: bool
        """
        ...

    def __getitem__(self, route_index: int) -> Route:
        """
        Retrieves the route at the specified index.

        :param int route_index: The index of the route to retrieve.
        :return: The route at the specified index.
        :rtype: Route
        """
        ...

    def __iter__(self) -> Iterator:
        """
        Returns an iterator over the routes in the solution.

        :return: An iterator over the routes.
        :rtype: Iterator
        """
        ...

    def __len__(self) -> int:
        """
        Returns the number of routes in the solution.

        :return: The number of routes in the solution.
        :rtype: int
        """
        ...

    def __ne__(self, other: Solution) -> bool:
        """
        Determines if the solution is not equal to another solution.

        :param Solution other: The other solution to compare.
        :return: True if the solutions are not equal, False otherwise.
        :rtype: bool
        """
        ...

    @property
    def cost(self) -> float:
        """
        Gets the total cost of the solution, i.e., the sum of costs of all routes.

        :return: The total cost of the solution.
        :rtype: float
        """
        ...

    @property
    def cost_components(self) -> List[float]:
        """
        Gets the cost components of the solution, i.e., the sum of costs components of all routes.

        :return: A list of cost components for the solution.
        :rtype: List[float]
        """
        ...

    @property
    def feasible(self) -> bool:
        """
        Determines if the solution is feasible.

        :return: True if the solution is feasible, False otherwise.
        :rtype: bool
        """
        ...

    @property
    def insertion_points(self) -> List[NodeLocation]:
        """
        Gets all possible insertion points in the solution. That is, for each route r, positions [0, len(r) - 2].

        :return: A list of NodeLocation objects representing the insertion points in the solution.
        :rtype: List[NodeLocation]
        """
        ...

    @property
    def non_depot_nodes(self) -> List[NodeLocation]:
        """
        Gets the non-depot nodes in the solution. Useful for removing nodes from the solution.

        :return: A list of NodeLocation objects representing the non-depot nodes in the solution.
        :rtype: List[NodeLocation]
        """
        ...

    @property
    def number_of_insertion_points(self) -> int:
        """
        Gets the number of insertion points in the solution.

        :return: The number of insertion points in the solution.
        :rtype: int
        """
        ...

    @property
    def number_of_non_depot_nodes(self) -> int:
        """
        Gets the number of non-depot nodes in the solution.

        :return: The number of non-depot nodes in the solution.
        :rtype: int
        """
        ...

    @property
    def routes(self) -> Iterator:
        """
        Returns an iterator over the routes in the solution.

        :return: An iterator over the routes.
        :rtype: Iterator
        """
        ...
from typing import Any

AnyForwardLabel = Any
AnyBackwardLabel = Any
VertexID = int
from typing import Any


class Vertex:
    """
    A simple vertex object that represents a location vehicles can visit. Vertices can be stations, depots or customers.
    Each vertex has a unique id and a human-readable string identifier. The vertex also stores additional data transparent
    to the RoutingBlocks package. This data can be used to store additional information about the vertex, such as time windows,
    demand, prizes, or any other attribute that is relevant to the problem.
    """
    vertex_id: int  # The unique identifier of the vertex.
    str_id: str
    is_station: bool
    is_depot: bool

    def __init__(self, vertex_id: int, str_id: str, is_station: bool, is_depot: bool, data: Any) -> None:
        """
        :param vertex_id: The unique identifier of the vertex.
        :param str_id: A human-readable string identifier for the vertex.
        :param is_station: Whether the vertex is a station.
        :param is_depot: Whether the vertex is a depot.
        :param data: Additional data associated with the vertex.
        """
        ...

    @property
    def is_customer(self) -> bool:
        """
        Determines if the vertex is a customer.

        :return: True if the vertex is a customer, False otherwise.
        :rtype: bool
        """
        ...

    @property
    def data(self) -> Any:
        """
        Retrieves the vertex data.

        :return: The data associated with the vertex.
        :rtype: Any
        """

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the vertex based on the arc's :ivar str_id.

        :return: A string representation of the vertex.
        :rtype: str
        """
        ...
