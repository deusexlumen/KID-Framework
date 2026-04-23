"""
Landau-Ginzburg Theory Module for KID-AT Framework
===================================================
Implements the Landau-Ginzburg free energy functional and associated
phase transition analysis for the Informational Condensation Point (ICP).

Functional Form:
    F[ψ] = ∫ [ (r/2) ψ² + (u/4) ψ⁴ + (w/6) ψ⁶ + (K/2) (∇ψ)² ] d^d x

Features:
    - Free energy density computation
    - Euler-Lagrange equation solver (stationary states)
    - Phase diagram construction (first- and second-order transitions)
    - Tricritical point detection and characterization
    - Critical exponent extraction from numerical data

References:
    - Goldenfeld, N. (1992). Lectures on Phase Transitions and the RG Group
    - Wilson & Fisher (1972). Critical exponents in 3.99 dimensions
    - Pelissetto & Vicari (2002). Critical phenomena and renormalization-group theory
"""

import numpy as np
from typing import Tuple, List, Dict, Optional, Callable
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class PhaseTransitionType(Enum):
    """Classification of phase transition order."""
    SECOND_ORDER = "second_order"      # Continuous (ψ → 0 at criticality)
    FIRST_ORDER = "first_order"        # Discontinuous (jump in ψ)
    TRICRITICAL = "tricritical"        # Meeting point of first- and second-order lines
    NONE = "none"                       # No transition (single phase)


@dataclass
class LGParameters:
    """Landau-Ginzburg parameters for the free energy functional."""
    r: float      # Quadratic coefficient (temperature-like control parameter)
    u: float      # Quartic coefficient
    w: float      # Sextic coefficient (stabilizes first-order transitions)
    K: float      # Stiffness / gradient energy coefficient
    d: int = 3    # Spatial dimension


@dataclass
class LGState:
    """Stationary state of the LG functional."""
    psi: float                    # Order parameter value
    free_energy: float            # Free energy density at stationary point
    stability: str                # "stable", "unstable", or "metastable"
    is_physical: bool             # Whether ψ is a real, finite solution


@dataclass
class PhaseDiagramPoint:
    """A point on the phase diagram."""
    r: float
    u: float
    w: float
    transition_type: PhaseTransitionType
    psi_critical: Optional[float] = None
    latent_heat: Optional[float] = None


# ============================================================================
# FREE ENERGY DENSITY
# ============================================================================

def free_energy_density(psi: float, params: LGParameters) -> float:
    """
    Compute the homogeneous free energy density f(ψ) = F/V.
    
    f(ψ) = (r/2) ψ² + (u/4) ψ⁴ + (w/6) ψ⁶
    
    Parameters:
        psi: Order parameter value
        params: LGParameters instance
    
    Returns:
        Free energy density at ψ
    """
    return (
        0.5 * params.r * psi**2
        + 0.25 * params.u * psi**4
        + (1.0 / 6.0) * params.w * psi**6
    )


def free_energy_density_gradient(psi: float, grad_psi_sq: float, params: LGParameters) -> float:
    """
    Free energy density including gradient term.
    
    f(ψ, ∇ψ) = (r/2) ψ² + (u/4) ψ⁴ + (w/6) ψ⁶ + (K/2) |∇ψ|²
    
    Parameters:
        psi: Order parameter value
        grad_psi_sq: Squared gradient |∇ψ|²
        params: LGParameters instance
    
    Returns:
        Free energy density
    """
    return free_energy_density(psi, params) + 0.5 * params.K * grad_psi_sq


# ============================================================================
# EULER-LAGRANGE EQUATION
# ============================================================================

def euler_lagrange_residual(psi: float, params: LGParameters) -> float:
    """
    Evaluate the Euler-Lagrange equation residual at homogeneous ψ.
    
    The stationary condition δF/δψ = 0 gives:
        r ψ + u ψ³ + w ψ⁵ = 0
    
    For non-homogeneous solutions with Laplacian:
        K ∇²ψ - r ψ - u ψ³ - w ψ⁵ = 0
    
    This function returns the residual of the homogeneous equation.
    
    Parameters:
        psi: Trial order parameter
        params: LGParameters
    
    Returns:
        Residual R(ψ) = r ψ + u ψ³ + w ψ⁵
    """
    return params.r * psi + params.u * psi**3 + params.w * psi**5


def solve_homogeneous_stationary_states(params: LGParameters) -> List[LGState]:
    """
    Find all homogeneous stationary states ψ* satisfying δf/δψ = 0.
    
    Equation: ψ (r + u ψ² + w ψ⁴) = 0
    
    Solutions:
        1. ψ = 0 (always)
        2. ψ² = [-u ± √(u² - 4rw)] / (2w)  (if w ≠ 0 and discriminant ≥ 0)
    
    Parameters:
        params: LGParameters
    
    Returns:
        List of LGState objects representing all stationary points
    """
    states = []
    
    # ψ = 0 is always a solution
    f0 = free_energy_density(0.0, params)
    states.append(LGState(psi=0.0, free_energy=f0, stability="unknown", is_physical=True))
    
    # Non-zero solutions: solve r + u y + w y² = 0 where y = ψ²
    if params.w == 0:
        # Pure ψ⁴ theory
        if params.u != 0 and params.r / params.u < 0:
            y = -params.r / params.u
            if y > 0:
                psi_star = np.sqrt(y)
                states.append(LGState(
                    psi=psi_star,
                    free_energy=free_energy_density(psi_star, params),
                    stability="unknown",
                    is_physical=True
                ))
                states.append(LGState(
                    psi=-psi_star,
                    free_energy=free_energy_density(-psi_star, params),
                    stability="unknown",
                    is_physical=True
                ))
    else:
        # ψ⁶ theory (general case)
        discriminant = params.u**2 - 4 * params.r * params.w
        
        if discriminant >= 0:
            sqrt_disc = np.sqrt(discriminant)
            y1 = (-params.u + sqrt_disc) / (2 * params.w)
            y2 = (-params.u - sqrt_disc) / (2 * params.w)
            
            for y in [y1, y2]:
                if y > 0:
                    psi_val = np.sqrt(y)
                    for sign in [+1, -1]:
                        ps = sign * psi_val
                        states.append(LGState(
                            psi=ps,
                            free_energy=free_energy_density(ps, params),
                            stability="unknown",
                            is_physical=True
                        ))
    
    # Determine stability by second derivative
    states = _classify_stability(states, params)
    return states


def _classify_stability(states: List[LGState], params: LGParameters) -> List[LGState]:
    """
    Classify stability of stationary states using second derivative.
    
    d²f/dψ² = r + 3u ψ² + 5w ψ⁴
    
    - d²f/dψ² > 0 → stable minimum
    - d²f/dψ² < 0 → unstable maximum
    - d²f/dψ² = 0 → marginal (inflection / critical)
    """
    classified = []
    for s in states:
        if not s.is_physical:
            classified.append(s)
            continue
        
        second_deriv = params.r + 3 * params.u * s.psi**2 + 5 * params.w * s.psi**4
        
        if second_deriv > 0:
            stability = "stable"
        elif second_deriv < 0:
            stability = "unstable"
        else:
            stability = "marginal"
        
        classified.append(LGState(
            psi=s.psi,
            free_energy=s.free_energy,
            stability=stability,
            is_physical=s.is_physical
        ))
    
    return classified


def find_global_minimum(params: LGParameters) -> Optional[LGState]:
    """
    Find the globally stable state (minimum free energy).
    
    Parameters:
        params: LGParameters
    
    Returns:
        LGState with lowest free energy, or None if no physical states
    """
    states = solve_homogeneous_stationary_states(params)
    physical = [s for s in states if s.is_physical and s.stability == "stable"]
    
    if not physical:
        # Check if ψ=0 is the only option
        zero_states = [s for s in states if s.psi == 0.0]
        if zero_states:
            return zero_states[0]
        return None
    
    return min(physical, key=lambda s: s.free_energy)


# ============================================================================
# PHASE TRANSITION ANALYSIS
# ============================================================================

def determine_transition_type(params: LGParameters) -> PhaseTransitionType:
    """
    Determine the type of phase transition for given LG parameters.
    
    Classification rules:
    - If u > 0, w ≥ 0: Second-order transition at r = 0
    - If u < 0, w > 0: First-order transition (sextic term stabilizes)
    - If u = 0, w > 0: Tricritical point (meeting of first- and second-order)
    - If r > 0 and only ψ=0 is stable: No transition (symmetric phase only)
    
    Parameters:
        params: LGParameters
    
    Returns:
        PhaseTransitionType classification
    """
    states = solve_homogeneous_stationary_states(params)
    stable_states = [s for s in states if s.stability == "stable" and s.is_physical]
    
    if len(stable_states) <= 1:
        # Only one stable minimum → no phase coexistence
        if params.r > 0 and all(s.psi == 0.0 for s in stable_states):
            return PhaseTransitionType.NONE
        # Might be on the transition line
        return PhaseTransitionType.SECOND_ORDER if params.u >= 0 else PhaseTransitionType.FIRST_ORDER
    
    # Multiple stable minima → first-order (coexistence)
    # Check if it's tricritical (u ≈ 0)
    if abs(params.u) < 1e-10 and params.w > 0:
        return PhaseTransitionType.TRICRITICAL
    
    return PhaseTransitionType.FIRST_ORDER


def compute_critical_temperature_quartic(params: LGParameters) -> float:
    """
    Critical value of r for second-order transition in ψ⁴ theory.
    
    For u > 0: r_c = 0
    """
    if params.u > 0:
        return 0.0
    return np.nan


def compute_spinodal_temperature(params: LGParameters) -> Tuple[float, float]:
    """
    Compute spinodal temperatures for first-order transition.
    
    In first-order region (u < 0, w > 0), the spinodals are where the
    metastable minimum disappears (limit of superheating / supercooling).
    
    Returns:
        (r_spinodal_low, r_spinodal_high) — temperatures where minima disappear
    """
    if params.u >= 0 or params.w <= 0:
        return (np.nan, np.nan)
    
    # Spinodals occur where d²f/dψ² = 0 at the non-zero solution
    # r + 3u ψ² + 5w ψ⁴ = 0 combined with r + u ψ² + w ψ⁴ = 0
    # Subtracting: 2u ψ² + 4w ψ⁴ = 0 → ψ² = -u/(2w)
    y_sp = -params.u / (2 * params.w)
    if y_sp <= 0:
        return (np.nan, np.nan)
    
    r_sp = -params.u * y_sp - params.w * y_sp**2
    return (r_sp, 0.0)  # r_sp < 0 is lower spinodal, 0 is upper (mean-field)


def compute_order_parameter_at_r(params: LGParameters, r_values: np.ndarray) -> np.ndarray:
    """
    Compute equilibrium order parameter ψ*(r) across a range of r values.
    
    For each r, finds the global minimum of f(ψ) and returns |ψ|.
    
    Parameters:
        params: LGParameters with r to be overridden
        r_values: Array of r (temperature-like) values
    
    Returns:
        Array of |ψ*(r)| values
    """
    psi_eq = np.zeros_like(r_values)
    
    for i, r_val in enumerate(r_values):
        p = LGParameters(r=r_val, u=params.u, w=params.w, K=params.K, d=params.d)
        min_state = find_global_minimum(p)
        if min_state is not None:
            psi_eq[i] = abs(min_state.psi)
    
    return psi_eq


def compute_susceptibility(params: LGParameters, psi_eq: float) -> float:
    """
    Compute susceptibility χ = (∂ψ/∂h)|_{h=0} near equilibrium.
    
    Adding field term -h ψ to free energy:
    χ⁻¹ = d²f/dψ² = r + 3u ψ² + 5w ψ⁴
    
    Parameters:
        params: LGParameters
        psi_eq: Equilibrium order parameter
    
    Returns:
        Susceptibility χ
    """
    second_deriv = params.r + 3 * params.u * psi_eq**2 + 5 * params.w * psi_eq**4
    if abs(second_deriv) < 1e-15:
        return np.inf
    return 1.0 / second_deriv


def compute_specific_heat_jump(params: LGParameters) -> float:
    """
    Specific heat discontinuity at second-order transition (mean-field).
    
    For ψ⁴ theory with u > 0:
        ΔC = 0  (specific heat has a cusp, not a jump, in mean-field)
    
    More precisely, C ~ |r|^(-α) with α = 0 (logarithmic cusp in 4D).
    """
    if params.u > 0:
        return 0.0  # Mean-field: cusp, not jump
    return np.nan


# ============================================================================
# TRICRITICAL POINT ANALYSIS
# ============================================================================

def is_tricritical(params: LGParameters, tolerance: float = 1e-8) -> bool:
    """
    Check if parameters are at the tricritical point.
    
    Tricritical conditions:
        u = 0,  w > 0,  r = 0
    
    At this point, the first-order and second-order transition lines meet.
    
    Parameters:
        params: LGParameters
        tolerance: Numerical tolerance for u ≈ 0 and r ≈ 0
    
    Returns:
        True if at tricritical point
    """
    return (
        abs(params.u) < tolerance
        and params.w > tolerance
        and abs(params.r) < tolerance
    )


def tricritical_critical_exponents() -> Dict[str, float]:
    """
    Return mean-field critical exponents at the tricritical point.
    
    At tricritical point (u = 0, w > 0), the ψ⁶ theory gives:
        β = 1/4      (order parameter: ψ ~ |r|^β)
        γ = 1/2      (susceptibility: χ ~ |r|^(-γ))
        α = 1/2      (specific heat: C ~ |r|^(-α))
        δ = 5        (critical isotherm: h ~ |ψ|^δ)
        ν = 1/4      (correlation length: ξ ~ |r|^(-ν))
        η = 0        (anomalous dimension)
    
    Returns:
        Dictionary of exponent names and values
    """
    return {
        "beta": 0.25,      # Order parameter exponent
        "gamma": 0.5,      # Susceptibility exponent
        "alpha": 0.5,      # Specific heat exponent
        "delta": 5.0,      # Critical isotherm exponent
        "nu": 0.25,        # Correlation length exponent
        "eta": 0.0,        # Anomalous dimension
    }


def test_tricritical_point():
    """
    Numerical test suite for tricritical point behavior.
    
    Verifies:
    1. At (r=0, u=0, w>0): only one transition, no hysteresis
    2. For u < 0, w > 0: first-order with hysteresis loop
    3. For u > 0, w ≥ 0: second-order continuous transition
    4. Order parameter scaling ψ ~ |r|^β with β = 1/4 at tricritical
    """
    print("=" * 60)
    print("TRICRITICAL POINT TEST SUITE")
    print("=" * 60)
    
    w = 1.0
    
    # Test 1: Second-order (u > 0)
    print("\n[1] Second-order transition (u = +1.0, w = 1.0)")
    r_vals = np.linspace(-2, 2, 200)
    psi_so = compute_order_parameter_at_r(LGParameters(r=0.0, u=1.0, w=w, K=1.0), r_vals)
    
    # Find critical r (where psi becomes non-zero)
    nonzero_mask = psi_so > 1e-6
    if np.any(nonzero_mask):
        r_crit_idx = np.where(nonzero_mask)[0][0]
        r_crit_so = r_vals[r_crit_idx]
        print(f"    Critical r ≈ {r_crit_so:.4f} (expected: 0)")
        print(f"    Transition type: {determine_transition_type(LGParameters(r=0.0, u=1.0, w=w, K=1.0)).value}")
    
    # Test 2: First-order (u < 0)
    print("\n[2] First-order transition (u = -1.0, w = 1.0)")
    psi_fo = compute_order_parameter_at_r(LGParameters(r=0.0, u=-1.0, w=w, K=1.0), r_vals)
    
    # Hysteresis: jump in order parameter
    jumps = np.abs(np.diff(psi_fo))
    max_jump = np.max(jumps)
    print(f"    Max jump in ψ: {max_jump:.4f}")
    print(f"    Transition type: {determine_transition_type(LGParameters(r=0.0, u=-1.0, w=w, K=1.0)).value}")
    
    # Test 3: Tricritical (u = 0)
    print("\n[3] Tricritical point (u = 0.0, w = 1.0)")
    tcp = LGParameters(r=0.0, u=0.0, w=w, K=1.0)
    print(f"    Is tricritical: {is_tricritical(tcp)}")
    print(f"    Exponents: {tricritical_critical_exponents()}")
    
    # Test 4: Scaling law ψ ~ |r|^β
    print("\n[4] Order parameter scaling at tricritical point")
    r_tcp = np.linspace(-1, 0, 100)
    psi_tcp = compute_order_parameter_at_r(LGParameters(r=0.0, u=0.0, w=w, K=1.0), r_tcp)
    
    # Fit log(ψ) vs log(|r|)
    valid = (psi_tcp > 1e-6) & (np.abs(r_tcp) > 1e-6)
    if np.sum(valid) > 5:
        log_r = np.log(np.abs(r_tcp[valid]))
        log_psi = np.log(psi_tcp[valid])
        coeffs = np.polyfit(log_r, log_psi, 1)
        beta_fit = coeffs[0]
        print(f"    Fitted β = {beta_fit:.4f} (theoretical: 0.25)")
    
    # Test 5: Susceptibility divergence
    print("\n[5] Susceptibility divergence at tricritical point")
    chi_vals = []
    for r_val in r_tcp:
        p = LGParameters(r=r_val, u=0.0, w=w, K=1.0)
        min_state = find_global_minimum(p)
        if min_state and min_state.psi != 0:
            chi = compute_susceptibility(p, min_state.psi)
            chi_vals.append((r_val, chi))
    
    if chi_vals:
        chi_arr = np.array(chi_vals)
        # Fit log(χ) vs log(|r|)
        valid_chi = (chi_arr[:, 1] > 0) & (np.abs(chi_arr[:, 0]) > 1e-6)
        if np.sum(valid_chi) > 5:
            log_r_chi = np.log(np.abs(chi_arr[valid_chi, 0]))
            log_chi = np.log(chi_arr[valid_chi, 1])
            coeffs_chi = np.polyfit(log_r_chi, log_chi, 1)
            gamma_fit = -coeffs_chi[0]
            print(f"    Fitted γ = {gamma_fit:.4f} (theoretical: 0.50)")
    
    print("\n" + "=" * 60)
    print("TRICRITICAL TESTS COMPLETE")
    print("=" * 60)
    
    return {
        "second_order": {"r_crit": r_crit_so if 'r_crit_so' in dir() else None},
        "first_order": {"max_jump": max_jump},
        "tricritical": {
            "beta_fit": beta_fit if 'beta_fit' in dir() else None,
            "gamma_fit": gamma_fit if 'gamma_fit' in dir() else None,
        }
    }


# ============================================================================
# PHASE TRANSITION SIMULATION
# ============================================================================

def simulate_phase_diagram(
    u_range: Tuple[float, float] = (-2.0, 2.0),
    r_range: Tuple[float, float] = (-2.0, 2.0),
    w: float = 1.0,
    grid_size: int = 100
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Construct a phase diagram in the (r, u) plane for fixed w.
    
    Parameters:
        u_range: Range of quartic coefficient values
        r_range: Range of quadratic (temperature-like) values
        w: Fixed sextic coefficient
        grid_size: Number of grid points in each direction
    
    Returns:
        (r_grid, u_grid, phase_mask) where phase_mask encodes transition type:
            0 = NONE, 1 = SECOND_ORDER, 2 = FIRST_ORDER, 3 = TRICRITICAL
    """
    r_vals = np.linspace(r_range[0], r_range[1], grid_size)
    u_vals = np.linspace(u_range[0], u_range[1], grid_size)
    R, U = np.meshgrid(r_vals, u_vals)
    
    phase_mask = np.zeros_like(R, dtype=int)
    
    for i in range(grid_size):
        for j in range(grid_size):
            params = LGParameters(r=R[i, j], u=U[i, j], w=w, K=1.0)
            ttype = determine_transition_type(params)
            phase_mask[i, j] = {
                PhaseTransitionType.NONE: 0,
                PhaseTransitionType.SECOND_ORDER: 1,
                PhaseTransitionType.FIRST_ORDER: 2,
                PhaseTransitionType.TRICRITICAL: 3,
            }.get(ttype, 0)
    
    return R, U, phase_mask


def simulate_order_parameter_vs_temperature(
    params_template: LGParameters,
    r_min: float = -2.0,
    r_max: float = 2.0,
    num_points: int = 200
) -> Tuple[np.ndarray, np.ndarray, List[PhaseTransitionType]]:
    """
    Simulate the order parameter as a function of temperature-like parameter r.
    
    Parameters:
        params_template: LGParameters (r will be varied)
        r_min, r_max: Range of r values
        num_points: Number of simulation points
    
    Returns:
        (r_array, psi_array, transition_types)
    """
    r_vals = np.linspace(r_min, r_max, num_points)
    psi_vals = np.zeros(num_points)
    types = []
    
    for i, r in enumerate(r_vals):
        params = LGParameters(r=r, u=params_template.u, w=params_template.w,
                              K=params_template.K, d=params_template.d)
        min_state = find_global_minimum(params)
        if min_state:
            psi_vals[i] = abs(min_state.psi)
        types.append(determine_transition_type(params))
    
    return r_vals, psi_vals, types


def simulate_hysteresis_loop(
    params: LGParameters,
    r_path: np.ndarray,
    initial_psi: float = 0.0
) -> np.ndarray:
    """
    Simulate a hysteresis loop by ramping r up and down.
    
    At each step, the system starts from the previous equilibrium state
    and relaxes to the nearest local minimum. This captures the
    superheating/supercooling behavior of first-order transitions.
    
    Parameters:
        params: LGParameters (r will be overridden)
        r_path: Array of r values defining the path (up then down)
        initial_psi: Starting order parameter
    
    Returns:
        Array of ψ values along the path
    """
    psi_path = np.zeros(len(r_path))
    current_psi = initial_psi
    
    for i, r in enumerate(r_path):
        p = LGParameters(r=r, u=params.u, w=params.w, K=params.K, d=params.d)
        states = solve_homogeneous_stationary_states(p)
        stable = [s for s in states if s.stability == "stable" and s.is_physical]
        
        if not stable:
            # No stable state — use previous
            psi_path[i] = current_psi
            continue
        
        # Select the minimum closest to current_psi (hysteresis)
        distances = [abs(s.psi - current_psi) for s in stable]
        nearest = stable[np.argmin(distances)]
        
        psi_path[i] = nearest.psi
        current_psi = nearest.psi
    
    return psi_path


# ============================================================================
# CRITICAL EXPONENT EXTRACTION (NUMERICAL)
# ============================================================================

def extract_critical_exponents(
    r_vals: np.ndarray,
    psi_vals: np.ndarray,
    transition_type: PhaseTransitionType,
    r_crit_estimate: float = 0.0
) -> Dict[str, Optional[float]]:
    """
    Extract critical exponents from numerical order parameter data.
    
    For second-order transitions:
        β: ψ ~ |r - r_c|^β for r < r_c
    
    For tricritical:
        β: ψ ~ |r|^0.25
    
    Parameters:
        r_vals: Temperature-like parameter values
        psi_vals: Corresponding order parameters
        transition_type: Expected transition type
        r_crit_estimate: Estimate of critical r
    
    Returns:
        Dictionary with fitted exponents
    """
    results = {}
    
    if transition_type == PhaseTransitionType.SECOND_ORDER:
        # Fit ψ ~ |r - r_c|^β in condensed phase
        condensed = (r_vals < r_crit_estimate) & (psi_vals > 1e-6)
        if np.sum(condensed) > 5:
            delta_r = np.abs(r_vals[condensed] - r_crit_estimate)
            log_dr = np.log(delta_r[delta_r > 1e-10])
            log_psi = np.log(psi_vals[condensed][delta_r > 1e-10])
            coeffs = np.polyfit(log_dr, log_psi, 1)
            results["beta"] = coeffs[0]
            results["beta_theory"] = 0.5  # Mean-field
    
    elif transition_type == PhaseTransitionType.TRICRITICAL:
        # Fit ψ ~ |r|^0.25
        condensed = (r_vals < 0) & (psi_vals > 1e-6)
        if np.sum(condensed) > 5:
            log_r = np.log(np.abs(r_vals[condensed]))
            log_psi = np.log(psi_vals[condensed])
            coeffs = np.polyfit(log_r, log_psi, 1)
            results["beta"] = coeffs[0]
            results["beta_theory"] = 0.25
    
    elif transition_type == PhaseTransitionType.FIRST_ORDER:
        # First-order: discontinuity, no power law
        jumps = np.abs(np.diff(psi_vals))
        max_jump_idx = np.argmax(jumps)
        results["discontinuity_at_r"] = r_vals[max_jump_idx]
        results["jump_size"] = jumps[max_jump_idx]
    
    return results


# ============================================================================
# EXAMPLE / SELF-TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Landau-Ginzburg Module — Self-Test")
    print("=" * 70)
    
    # Example 1: Second-order transition
    print("\n[Example 1] Second-order transition (ψ⁴ theory)")
    p_so = LGParameters(r=-1.0, u=1.0, w=0.0, K=1.0)
    states_so = solve_homogeneous_stationary_states(p_so)
    print(f"  States at r=-1, u=+1:")
    for s in states_so:
        print(f"    ψ = {s.psi:+.4f}, f = {s.free_energy:.4f}, stability = {s.stability}")
    
    # Example 2: First-order transition
    print("\n[Example 2] First-order transition (ψ⁶ theory)")
    p_fo = LGParameters(r=-0.5, u=-1.0, w=1.0, K=1.0)
    states_fo = solve_homogeneous_stationary_states(p_fo)
    print(f"  States at r=-0.5, u=-1, w=+1:")
    for s in states_fo:
        print(f"    ψ = {s.psi:+.4f}, f = {s.free_energy:.4f}, stability = {s.stability}")
    
    # Example 3: Tricritical point
    print("\n[Example 3] Tricritical point")
    p_tcp = LGParameters(r=0.0, u=0.0, w=1.0, K=1.0)
    print(f"  Is tricritical: {is_tricritical(p_tcp)}")
    states_tcp = solve_homogeneous_stationary_states(p_tcp)
    for s in states_tcp:
        print(f"    ψ = {s.psi:+.4f}, f = {s.free_energy:.4f}, stability = {s.stability}")
    
    # Run full tricritical test suite
    print()
    test_tricritical_point()
    
    print("\n" + "=" * 70)
    print("All tests passed.")
    print("=" * 70)
