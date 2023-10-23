import numpy as np
import pandas as pd
import pulp as pl
from sklearn.preprocessing import MinMaxScaler
from sklearn_extra.cluster import KMedoids

from .representative_periods import RepresentativePeriods
from .utils import duration_function

def poncelet_method(temporal_data, N_RP, RP_length, N_bins=15, solver=None):
    """Find representative periods (RPs) and their weights using the Poncelet et al. (2017) method.

    Args:
        temporal_data (TemporalData): A TemporalData object containing the input data.
        N_RP (int): The number of representative periods to find.
        RP_length (int): The length of each representative period.
        N_bins (int, optional): The number of bins for duration curve discretization. Defaults to 15.
        solver (pulp solver, optional): The solver to use for optimization. Defaults to None. see : https://coin-or.github.io/pulp/guides/how_to_configure_solvers.html and https://coin-or.github.io/pulp/technical/solvers.html#module-pulp.apis 

    Returns:
        list: A list of RepresentativePeriods objects, each representing an RP with its weight.
    """
    # Get RP candidates (not normalized)
    Number_of_candidate_RP = temporal_data.data.shape[0] // RP_length
    P_candidates = {P_id: temporal_data.data.iloc[P_id * RP_length:(P_id + 1) * RP_length] for P_id in range(Number_of_candidate_RP)}

    # Set bins
    bins = np.arange(N_bins) / (N_bins - 1)

    # Set scalers
    scalers = {}
    for curve in temporal_data.curve_set():
        scaler = MinMaxScaler()
        scaler.fit(temporal_data.data[curve].to_numpy().reshape(-1, 1))
        scalers[curve] = scaler

    ## Set MILP model
    # Constants
    L = {}
    for curve in temporal_data.curve_set():
        DC = duration_function(scalers[curve].transform(temporal_data.data[curve].to_numpy().reshape(-1, 1)))
        for bin in bins:
            L[curve, bin] = DC(bin)
    A = {}
    for P_id in P_candidates:
        for curve in temporal_data.curve_set():
            DC = duration_function(scalers[curve].transform(P_candidates[P_id][curve].to_numpy().reshape(-1, 1)))
            for bin in bins:
                A[curve, bin, P_id] = DC(bin)

    # Variables
    U = {P_id: pl.LpVariable(f"U_{P_id}", cat="Binary") for P_id in P_candidates}
    W = {P_id: pl.LpVariable(f"W_{P_id}", cat="Continuous", lowBound=0) for P_id in P_candidates}
    errors = {(curve, bin): pl.LpVariable(f"error_{curve}-{bin}", cat="Continuous") for curve in temporal_data.curve_set() for bin in bins}

    # Constraints
    problem = pl.LpProblem("Poncelet_Method", pl.LpMinimize)
    problem += (
        pl.lpSum(U[P_id] for P_id in P_candidates) == N_RP,
        "Number_of_RP",
    )
    problem += (
        pl.lpSum(W[P_id] for P_id in P_candidates) == 1,
        "RP_weights",
    )

    for P_id in P_candidates:
        problem += (
            W[P_id] <= U[P_id],
            f"Weight_{P_id}_is_not_null_if_the_Period_{P_id}_is_selected",
        )

    for curve in temporal_data.curve_set():
        for bin in bins:
            problem += (
                errors[curve, bin] >= L[curve, bin] - pl.lpSum(W[P_id] * A[curve, bin, P_id] for P_id in P_candidates)
            )
            problem += (
                errors[curve, bin] >= pl.lpSum(W[P_id] * A[curve, bin, P_id] for P_id in P_candidates) - L[curve, bin]
            )

    # Objective
    problem += (
        pl.lpSum(errors[curve, bin] for curve in temporal_data.curve_set() for bin in bins),
        "Minimize global error",
    )

    problem.solve(solver)

    representative_periods = []
    for P_id in P_candidates:
        if U[P_id].varValue == 1:
            representative_periods.append(RepresentativePeriods(data=P_candidates[P_id], weight=W[P_id].varValue))
    return representative_periods

def random_method(temporal_data, N_RP, RP_length):
    """Generate representative periods (RPs) and their weights using random selection.

    Args:
        temporal_data (TemporalData): A TemporalData object containing the input data.
        N_RP (int): The number of representative periods to generate.
        RP_length (int): The length of each representative period.

    Returns:
        list: A list of RepresentativePeriods objects, each representing an RP with its weight.
    """
    # Get RP candidates (not normalized)
    Number_of_candidate_RP = temporal_data.data.shape[0] // RP_length
    P_candidates = {P_id: temporal_data.data.iloc[P_id * RP_length:(P_id + 1) * RP_length] for P_id in range(Number_of_candidate_RP)}

    # Randomly choose N_RP candidate periods
    P_id_choosen = np.random.choice(np.arange(Number_of_candidate_RP), size=N_RP, replace=False)

    # Generate random weights and normalize them
    weights = np.random.random(N_RP)
    weights = weights / weights.sum()

    # Create RepresentativePeriods objects for the chosen periods with their weights
    representative_periods = [RepresentativePeriods(data=P_candidates[P_id], weight=weights[i]) for i, P_id in enumerate(P_id_choosen)]

    return representative_periods

def kmedoids_method(temporal_data, N_RP, RP_length):
    """Generate representative periods (RPs) using the k-medoids clustering method. weights are calculated proportionnaly to the number of representatives in each cluster

    Args:
        temporal_data (TemporalData): A TemporalData object containing the input data.
        N_RP (int): The number of representative periods to generate.
        RP_length (int): The length of each representative period.

    Returns:
        list: A list of RepresentativePeriods objects, each representing an RP with its weight.
    """
    # Get RP candidates (not normalized)
    Number_of_candidate_RP = temporal_data.data.shape[0] // RP_length
    P_candidates = {P_id: temporal_data.data.iloc[P_id * RP_length:(P_id + 1) * RP_length] for P_id in range(Number_of_candidate_RP)}

    # Convert candidate data to a format suitable for k-medoids
    data = np.array([P_candidate.to_numpy().reshape((RP_length * temporal_data.data.shape[1]), order='F') for P_candidate in P_candidates.values()])

    # Apply k-medoids clustering
    kmedoids = KMedoids(metric="euclidean", n_clusters=N_RP)
    kmedoids.fit(data)

    # Count the number of data points in each cluster (representative period)
    number_by_cluster = {P_id: (kmedoids.predict(data) == k).sum() for k, P_id in enumerate(kmedoids.medoid_indices_)}

    # Calculate weights for each representative period
    weights = [number_by_cluster[P_id] / Number_of_candidate_RP for P_id in kmedoids.medoid_indices_]

    # Create RepresentativePeriods objects for the medoids with their weights
    representative_periods = [RepresentativePeriods(data=P_candidates[P_id], weight=weights[i]) for i, P_id in enumerate(kmedoids.medoid_indices_)]

    return representative_periods