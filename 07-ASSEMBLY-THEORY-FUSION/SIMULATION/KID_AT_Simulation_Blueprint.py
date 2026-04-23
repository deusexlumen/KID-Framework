#!/usr/bin/env python3
"""
KID-AT Unified Framework: Simulation Blueprints
================================================
Implements two concrete simulation designs for falsifiable hypotheses:
  H1: Graph-based Assembly Space Exploration (Phase Transitions)
  H2: Entropy-Export Optimization Dynamics (Critical Self-Organization)

References:
  - Sharma et al. (2023) Nature: Assembly theory explains and quantifies selection
  - Chen & Prokopenko (2025): SOC from information-theoretic utility
  - Cronin et al. (2024): Experimental measurement of assembly indices

Document: KID-AT-MAS-2026-PHASE-A
"""

import numpy as np
import networkx as nx
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Callable, Optional
from dataclasses import dataclass
from enum import Enum
import matplotlib.pyplot as plt
from scipy import stats
from scipy.signal import find_peaks


# ============================================================================
# TOAST EFFICIENCY
# ============================================================================

def compute_toast_efficiency(c_parameter: float) -> float:
    """
    Compute the TOAST efficiency η_toast(C).
    
    The TOAST heuristic efficiency is maximized at C = 1 (critical point)
    and falls off symmetrically for C < 1 and C > 1.
    
    Formula: η_toast(C) = 4C / (1 + C)^2
    
    Properties:
    - η_toast(0) = 0
    - η_toast(1) = 1  (maximum)
    - η_toast(C) → 0 as C → ∞
    - Symmetry: η_toast(C) = η_toast(1/C)
    """
    return 4.0 * c_parameter / (1.0 + c_parameter) ** 2


# ============================================================================
# UTILITY CLASSES AND DATA STRUCTURES
# ============================================================================

class PhaseLevel(Enum):
    """Emergence levels as defined in the unified framework."""
    PHYSICAL = 1       # AI_min = 1
    CHEMICAL = 2       # AI_min = 10
    BIOLOGICAL = 3     # AI_min = 100
    NEURAL = 4         # AI_min = 1000
    CONSCIOUSNESS = 5  # AI_min = 10000
    COLLECTIVE = 6     # AI_min = 100000


@dataclass
class AssemblyObject:
    """Represents an object in assembly space."""
    id: int
    ai: int  # Assembly index (minimum path length)
    kolmogorov_estimate: float  # Upper bound on K(x)
    parents: Tuple[int, ...]  # Parent object IDs
    mass: float  # "Mass" of the object (for copy number dynamics)
    
    def __hash__(self):
        return self.id


@dataclass
class SimulationState:
    """Snapshot of simulation state at time t."""
    t: int
    copy_numbers: Dict[int, int]  # object_id -> copy count
    kid_k: float  # Kolmogorov KID
    c_parameter: float  # C = KID_K / KID_K_crit
    mean_ai: float
    max_ai: int
    ai_distribution: Dict[int, int]  # AI value -> count of objects
    entropy_production: float
    eta_toast: float = 0.0  # Toast efficiency


# ============================================================================
# HYPOTHESIS 1: GRAPH-BASED ASSEMBLY SPACE EXPLORATION
# ============================================================================

class AssemblyPhaseTransitionSimulator:
    """
    Simulates a directed acyclic graph (DAG) assembly space with selection.
    
    Tests Hypothesis 1: Phase transitions occur at predicted AI thresholds
    when selection parameter alpha < 1 and tau_d ≈ tau_p.
    
    Algorithm (from synthesis document):
      1. Initialize root vertices with copy numbers N_0
      2. At each timestep:
         a. Discovery step (prob 1/tau_d): combine objects to discover new ones
         b. Production step (prob 1/tau_p): increment copy numbers
         c. Compute KID_K(t) and AI distribution
      3. Detect phase transitions in dKID_K/dt
    """
    
    # Emergence thresholds from unified framework (6 levels)
    AI_THRESHOLDS = {
        PhaseLevel.PHYSICAL: 1,
        PhaseLevel.CHEMICAL: 10,
        PhaseLevel.BIOLOGICAL: 100,
        PhaseLevel.NEURAL: 1000,
        PhaseLevel.CONSCIOUSNESS: 10000,
        PhaseLevel.COLLECTIVE: 100000,
    }
    
    def __init__(
        self,
        graph: nx.DiGraph,
        alpha: float = 0.5,          # Selection parameter [0, 1]
        tau_d: float = 10.0,         # Discovery timescale
        tau_p: float = 10.0,         # Production timescale
        N0: int = 10000,             # Initial copy number
        V_eff: float = 100.0,        # Effective interaction volume
        tau_form: float = 1.0,       # Formation timescale
        K_ref: float = 1.0,          # Reference complexity (dimensionless)
        kid_crit: float = 1.0,       # Critical KID threshold
        seed: int = 42
    ):
        self.graph = graph
        self.alpha = alpha
        self.tau_d = tau_d
        self.tau_p = tau_p
        self.N0 = N0
        self.V_eff = V_eff
        self.tau_form = tau_form
        self.K_ref = K_ref
        self.KID_K_crit = kid_crit
        self.rng = np.random.default_rng(seed)
        
        # Extract graph structure
        self._initialize_from_graph()
        
        # Simulation history
        self.history: List[SimulationState] = []
        self.transitions_detected: List[Tuple[int, PhaseLevel]] = []
        
    def _initialize_from_graph(self):
        """Extract assembly objects and their properties from the graph."""
        self.objects: Dict[int, AssemblyObject] = {}
        
        # Root nodes (no predecessors)
        roots = [n for n in self.graph.nodes() if self.graph.in_degree(n) == 0]
        
        for node in self.graph.nodes():
            # Assembly index = shortest path from any root
            if node in roots:
                ai = 0
            else:
                ai = min(
                    nx.shortest_path_length(self.graph, source=r, target=node)
                    for r in roots if nx.has_path(self.graph, r, node)
                )
            
            # Estimate Kolmogorov complexity as AI * log(num_operations)
            # This is the upper bound from Theorem 4.1
            parents = tuple(self.graph.predecessors(node))
            k_est = ai * np.log2(max(self.graph.out_degree(p) for p in parents) + 1) if parents else 1.0
            
            self.objects[node] = AssemblyObject(
                id=node,
                ai=ai,
                kolmogorov_estimate=k_est,
                parents=parents if parents else tuple(roots),
                mass=self.graph.nodes[node].get('mass', 1.0)
            )
        
        self.root_ids = set(roots)
        self.copy_numbers: Dict[int, int] = {n: 0 for n in self.graph.nodes()}
        for r in roots:
            self.copy_numbers[r] = self.N0
            
    def _discovery_step(self):
        """Attempt to discover a new object by combining existing ones."""
        # Available objects (those with copy number > 0)
        available = [obj_id for obj_id, count in self.copy_numbers.items() if count > 0]
        if len(available) < 2:
            return
        
        # Selection-weighted sampling: prefer higher copy number objects
        # with exponent alpha (alpha=1: random; alpha<1: selects high-copy)
        weights = np.array([self.copy_numbers[o]**(1 - self.alpha) for o in available])
        weights = weights / weights.sum()
        
        obj1_id = self.rng.choice(available, p=weights)
        
        # Second object: preferentially combine with objects that can create new discoveries
        candidates = []
        for o2_id in available:
            if o2_id == obj1_id and self.copy_numbers[o2_id] < 2:
                continue
            # Check if combining obj1 + obj2 creates any new object
            for successor in self.graph.successors(obj1_id):
                preds = set(self.graph.predecessors(successor))
                if o2_id in preds or (len(preds) == 1 and obj1_id in preds):
                    candidates.append(o2_id)
                    break
        
        if not candidates:
            return
            
        obj2_id = self.rng.choice(candidates)
        
        # Discover what this combination creates
        for successor in self.graph.successors(obj1_id):
            preds = list(self.graph.predecessors(successor))
            if obj1_id in preds and (obj2_id in preds or len(preds) == 1):
                if self.copy_numbers[successor] == 0:
                    # New discovery! Award initial copies
                    self.copy_numbers[successor] = max(1, int(self.N0 * 0.01))
                    break
    
    def _production_step(self):
        """Increment copy numbers of existing objects."""
        available = [obj_id for obj_id, count in self.copy_numbers.items() if count > 0]
        if not available:
            return
        
        # Preferentially reproduce objects with higher assembly index
        # (selected objects have "purpose" in the assembly space)
        weights = np.array([
            self.objects[o].ai + 1.0 for o in available
        ])
        weights = weights / weights.sum()
        
        obj_id = self.rng.choice(available, p=weights)
        self.copy_numbers[obj_id] += 1
    
    def _compute_kid_k(self) -> float:
        """Compute Kolmogorov KID at current state."""
        total = 0.0
        for obj_id, count in self.copy_numbers.items():
            if count > 0:
                obj = self.objects[obj_id]
                total += obj.kolmogorov_estimate * count
        
        # KID_K = sum(K(x) * n(x)) / (V_eff * tau_form * K_ref)
        kid_k = total / (self.V_eff * self.tau_form * self.K_ref)
        return kid_k
    
    def _record_state(self, t: int):
        """Record current simulation state."""
        kid_k = self._compute_kid_k()
        
        # AI distribution
        ai_dist = Counter()
        for obj_id, count in self.copy_numbers.items():
            if count > 0:
                ai_dist[self.objects[obj_id].ai] += count
        
        total_copies = sum(ai_dist.values())
        mean_ai = sum(ai * count for ai, count in ai_dist.items()) / total_copies if total_copies > 0 else 0
        max_ai = max((self.objects[o].ai for o, c in self.copy_numbers.items() if c > 0), default=0)
        
        state = SimulationState(
            t=t,
            copy_numbers=dict(self.copy_numbers),
            kid_k=kid_k,
            c_parameter=kid_k / self.KID_K_crit,
            mean_ai=mean_ai,
            max_ai=max_ai,
            ai_distribution=dict(ai_dist),
            entropy_production=0.0,  # Would be computed from detailed balance
            eta_toast=compute_toast_efficiency(kid_k / self.KID_K_crit)
        )
        self.history.append(state)
    
    def run(self, T_max: int = 100000, record_interval: int = 100):
        """
        Run the assembly space simulation.
        
        Parameters:
            T_max: Maximum simulation timesteps
            record_interval: Record state every N steps
        """
        self._record_state(0)
        
        for t in range(1, T_max + 1):
            # Discovery step
            if self.rng.random() < 1.0 / self.tau_d:
                self._discovery_step()
            
            # Production step
            if self.rng.random() < 1.0 / self.tau_p:
                self._production_step()
            
            if t % record_interval == 0:
                self._record_state(t)
        
        return self.history
    
    def detect_phase_transitions(self) -> List[Tuple[int, PhaseLevel]]:
        """
        Detect phase transitions from KID_K trajectory.
        Returns list of (timestep, predicted_level) tuples.
        """
        if len(self.history) < 10:
            return []
        
        times = np.array([s.t for s in self.history])
        kid_values = np.array([s.kid_k for s in self.history])
        max_ai_values = np.array([s.max_ai for s in self.history])
        
        # Compute dKID_K/dt
        dt = times[1:] - times[:-1]
        d_kid = np.diff(kid_values) / dt
        
        # Find peaks in derivative (discontinuities = transitions)
        peaks, properties = find_peaks(np.abs(d_kid), height=np.std(d_kid), distance=5)
        
        transitions = []
        for peak_idx in peaks:
            t_transition = times[peak_idx]
            ai_at_transition = max_ai_values[peak_idx]
            
            # Determine level — find highest threshold that ai_at_transition meets or exceeds
            level = PhaseLevel.PHYSICAL
            for pl, threshold in self.AI_THRESHOLDS.items():
                if ai_at_transition >= threshold:
                    level = pl
            
            if level != PhaseLevel.PHYSICAL:
                transitions.append((int(t_transition), level))
        
        self.transitions_detected = transitions
        return transitions
    
    def compute_success_criteria(self) -> Dict[str, bool]:
        """
        Evaluate success criteria for Hypothesis 1.
        """
        if not self.history:
            return {"ran": False}
        
        criteria = {}
        
        # Criterion 1: KID_K increases over time (condensation)
        kid_values = [s.kid_k for s in self.history]
        criteria["kid_increases"] = kid_values[-1] > kid_values[0]
        
        # Criterion 2: Mean AI increases (complexity growth)
        mean_ai_values = [s.mean_ai for s in self.history]
        criteria["ai_increases"] = mean_ai_values[-1] > mean_ai_values[0]
        
        # Criterion 3: Transitions detected at predicted thresholds
        transitions = self.detect_phase_transitions()
        criteria["transitions_detected"] = len(transitions) > 0
        
        # Criterion 4: In Toast-optimal regime (tau_d ≈ tau_p)
        criteria["toast_optimal"] = 0.5 <= self.tau_d / self.tau_p <= 2.0
        
        # Criterion 5: Toast efficiency is non-negligible at some point
        if self.history:
            eta_toast_values = [compute_toast_efficiency(s.c_parameter) for s in self.history]
            criteria["toast_efficiency_max"] = max(eta_toast_values) > 0.5
        else:
            criteria["toast_efficiency_max"] = False
        
        # Criterion 6: Selection matters (alpha < 1)
        criteria["selection_active"] = self.alpha < 1.0
        
        criteria["all_pass"] = all(criteria.values())
        return criteria


# ============================================================================
# HYPOTHESIS 2: ENTROPY-EXPORT OPTIMIZATION DYNAMICS
# ============================================================================

class EntropyExportOptimizer:
    """
    Simulates agents optimizing predictive information (empowerment)
    in an Ising-like perception-action loop.
    
    Tests Hypothesis 2: Systems self-organize to C ≈ 1 where
    thermodynamic efficiency η_thermo is maximized.
    
    Based on Chen & Prokopenko (2025): interpreting Ising model
    as perception-action loop with empowerment optimization.
    """
    
    def __init__(
        self,
        N: int = 100,               # Number of agents
        T: float = 2.0,             # Temperature (in units of J/k_B)
        J: float = 1.0,             # Coupling strength
        learning_rate: float = 0.01, # Empowerment gradient ascent rate
        V_eff: float = 100.0,       # Effective interaction volume
        tau_form: float = 1.0,      # Formation timescale
        K_ref: float = 1.0,         # Reference complexity
        kid_crit: float = 1.0,      # Critical KID
        seed: int = 42
    ):
        self.N = N
        self.T = T
        self.J = J
        self.learning_rate = learning_rate
        self.V_eff = V_eff
        self.tau_form = tau_form
        self.K_ref = K_ref
        self.KID_K_crit = kid_crit
        self.rng = np.random.default_rng(seed)
        
        # State: N agents with spins {-1, +1}
        self.spins = self.rng.choice([-1, 1], size=N)
        
        # Each agent has a "policy" — probability of flipping given neighbor state
        # Simplified: each agent tracks a bias parameter
        self.policies = self.rng.normal(0, 0.1, size=N)
        
        # History
        self.history: List[Dict] = []
        
    def _local_field(self, i: int) -> float:
        """Compute local magnetic field at site i."""
        neighbors = [(i-1) % self.N, (i+1) % self.N]  # 1D ring
        return self.J * sum(self.spins[j] for j in neighbors)
    
    def _energy(self) -> float:
        """Total energy of Ising configuration."""
        E = 0.0
        for i in range(self.N):
            E -= self.spins[i] * self._local_field(i) / 2  # divide by 2 to avoid double counting
        return E
    
    def _glauber_step(self):
        """One step of Glauber dynamics at temperature T."""
        for i in range(self.N):
            h = self._local_field(i)
            # Glauber transition probability
            p_flip = 1.0 / (1.0 + np.exp(2 * h / self.T))
            
            # Active inference modification: policy influences flip probability
            policy_effect = np.tanh(self.policies[i] * h)
            p_flip = np.clip(p_flip + self.learning_rate * policy_effect, 0.01, 0.99)
            
            if self.rng.random() < p_flip:
                self.spins[i] *= -1
    
    def _compute_predictive_information(self, num_samples: int = 100) -> float:
        """
        Compute I(S_{t+1}; S_t) via sampling.
        Simplified: use correlation between current and next state.
        """
        current = self.spins.copy()
        
        # Estimate transition probabilities by sampling
        next_samples = []
        for _ in range(num_samples):
            s = current.copy()
            for i in range(self.N):
                h = self.J * (s[(i-1)%self.N] + s[(i+1)%self.N])
                p_flip = 1.0 / (1.0 + np.exp(2 * h / self.T))
                s_p = self.policies[i] * self.learning_rate
                p_flip = np.clip(p_flip + s_p * h, 0.01, 0.99)
                if self.rng.random() < p_flip:
                    s[i] *= -1
            next_samples.append(s.copy())
        
        # I_predict ≈ mutual information between current and expected next
        # Simplified: use average agreement
        avg_next = np.mean(next_samples, axis=0)
        predictability = np.mean((avg_next * current + 1) / 2)
        
        # Binary entropy of predictability
        if predictability <= 0 or predictability >= 1:
            return 0.0
        H_cond = -(predictability * np.log2(predictability) + 
                   (1 - predictability) * np.log2(1 - predictability))
        
        return self.N * (1.0 - H_cond)  # Approximate predictive info
    
    def _update_policies(self):
        """Gradient ascent on empowerment (predictive information)."""
        # Simple gradient estimate: perturb policies, measure change
        base_info = self._compute_predictive_information(num_samples=50)
        
        for i in range(self.N):
            self.policies[i] += 0.01
            new_info = self._compute_predictive_information(num_samples=20)
            grad = (new_info - base_info) / 0.01
            self.policies[i] -= 0.01
            
            # Gradient ascent
            self.policies[i] += self.learning_rate * grad
            self.policies[i] = np.clip(self.policies[i], -2.0, 2.0)
    
    def _compute_kid_k(self, I_predict: float) -> float:
        """Compute KID_K from predictive information."""
        return I_predict / (self.V_eff * self.tau_form * self.K_ref)
    
    def _record_state(self, t: int, I_predict: float, W_cost: float):
        """Record simulation state."""
        kid_k = self._compute_kid_k(I_predict)
        c_param = kid_k / self.KID_K_crit
        
        # Compute magnetization (order parameter)
        M = np.abs(np.mean(self.spins))
        
        # Correlation length estimate
        correlations = []
        for d in range(1, self.N // 4):
            corr = np.mean(self.spins * np.roll(self.spins, d))
            correlations.append(corr)
        xi = sum(corr > 0.1 for corr in correlations) if correlations else 0
        
        # Compute TOAST efficiency
        eta_toast = compute_toast_efficiency(c_param)
        
        state = {
            't': t,
            'kid_k': kid_k,
            'c_parameter': c_param,
            'I_predict': I_predict,
            'W_cost': W_cost,
            'eta_thermo': I_predict / W_cost if W_cost > 0 else 0,
            'eta_toast': eta_toast,
            'magnetization': M,
            'correlation_length': xi,
            'energy': self._energy(),
        }
        self.history.append(state)
    
    def run(self, T_max: int = 100000, record_interval: int = 100):
        """Run the entropy-export optimization simulation."""
        # Initial measurement
        I_pred = self._compute_predictive_information(num_samples=50)
        E0 = self._energy()
        self._record_state(0, I_pred, 0.1)
        
        for t in range(1, T_max + 1):
            # Update policies (empowerment optimization)
            if t % 10 == 0:
                self._update_policies()
            
            # Glauber dynamics step
            E_before = self._energy()
            self._glauber_step()
            E_after = self._energy()
            
            # Compute observables
            if t % record_interval == 0:
                I_pred = self._compute_predictive_information(num_samples=100)
                W_cost = abs(E_after - E_before) + 0.01  # Avoid division by zero
                self._record_state(t, I_pred, W_cost)
        
        return self.history
    
    def compute_success_criteria(self) -> Dict[str, bool]:
        """Evaluate success criteria for Hypothesis 2."""
        if not self.history:
            return {"ran": False}
        
        c_values = np.array([s['c_parameter'] for s in self.history])
        eta_values = np.array([s['eta_thermo'] for s in self.history])
        xi_values = np.array([s['correlation_length'] for s in self.history])
        
        criteria = {}
        
        # Criterion 1: System approaches C ≈ 1
        final_c = c_values[-1]
        criteria["approaches_critical"] = 0.5 <= final_c <= 2.0
        
        # Criterion 2: eta_thermo is substantial
        criteria["eta_positive"] = np.max(eta_values) > 0.1
        
        # Criterion 3: Correlation length grows (critical behavior)
        criteria["correlation_grows"] = xi_values[-1] > xi_values[0]
        
        # Criterion 4: System exhibits non-trivial dynamics
        criteria["nontrivial_dynamics"] = np.std(c_values) > 0.01
        
        # Criterion 5: C stays bounded (doesn't diverge)
        criteria["c_bounded"] = np.max(c_values) < 10.0
        
        # Criterion 6: TOAST efficiency is maximized near C ≈ 1
        eta_toast_values = np.array([s['eta_toast'] for s in self.history])
        criteria["toast_peak_near_critical"] = np.max(eta_toast_values) > 0.8
        
        criteria["all_pass"] = all(criteria.values())
        return criteria


# ============================================================================
# VISUALIZATION AND ANALYSIS
# ============================================================================

def plot_h1_results(simulator: AssemblyPhaseTransitionSimulator, 
                    title: str = "H1: Assembly Phase Transitions"):
    """Plot results from Hypothesis 1 simulation."""
    if not simulator.history:
        print("No history to plot")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    times = [s.t for s in simulator.history]
    kid_values = [s.kid_k for s in simulator.history]
    c_values = [s.c_parameter for s in simulator.history]
    mean_ai = [s.mean_ai for s in simulator.history]
    max_ai = [s.max_ai for s in simulator.history]
    
    # Plot 1: KID_K over time
    axes[0, 0].plot(times, kid_values, 'b-', linewidth=1.5)
    axes[0, 0].axhline(y=simulator.KID_K_crit, color='r', linestyle='--', 
                       label=f'KID_K_crit = {simulator.KID_K_crit}')
    axes[0, 0].set_xlabel('Time')
    axes[0, 0].set_ylabel('KID_K')
    axes[0, 0].set_title('Kolmogorov KID over Time')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: C parameter
    axes[0, 1].plot(times, c_values, 'g-', linewidth=1.5)
    axes[0, 1].axhline(y=1.0, color='r', linestyle='--', label='C = 1 (critical)')
    axes[0, 1].set_xlabel('Time')
    axes[0, 1].set_ylabel('C = KID_K / KID_K_crit')
    axes[0, 1].set_title('Condensation Parameter')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Mean and Max AI
    axes[1, 0].plot(times, mean_ai, 'b-', label='Mean AI', linewidth=1.5)
    axes[1, 0].plot(times, max_ai, 'r-', label='Max AI', linewidth=1.5)
    # Thresholds
    for level, threshold in simulator.AI_THRESHOLDS.items():
        if threshold > 1:
            axes[1, 0].axhline(y=threshold, linestyle='--', alpha=0.5,
                             label=f'{level.name}: AI={threshold}')
    axes[1, 0].set_xlabel('Time')
    axes[1, 0].set_ylabel('Assembly Index')
    axes[1, 0].set_title('Assembly Index Evolution')
    axes[1, 0].legend(fontsize=8)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Phase space (AI vs C)
    axes[1, 1].scatter(mean_ai, c_values, c=times, cmap='viridis', s=10, alpha=0.6)
    axes[1, 1].axhline(y=1.0, color='r', linestyle='--', alpha=0.5)
    axes[1, 1].set_xlabel('Mean Assembly Index')
    axes[1, 1].set_ylabel('C Parameter')
    axes[1, 1].set_title('Phase Space (colored by time)')
    cbar = plt.colorbar(axes[1, 1].collections[0], ax=axes[1, 1])
    cbar.set_label('Time')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('/mnt/agents/output/hypothesis1_results.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Saved to /mnt/agents/output/hypothesis1_results.png")


def plot_h2_results(simulator: EntropyExportOptimizer,
                    title: str = "H2: Entropy-Export Optimization"):
    """Plot results from Hypothesis 2 simulation."""
    if not simulator.history:
        print("No history to plot")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    times = [s['t'] for s in simulator.history]
    c_values = [s['c_parameter'] for s in simulator.history]
    eta_values = [s['eta_thermo'] for s in simulator.history]
    I_pred = [s['I_predict'] for s in simulator.history]
    W_cost = [s['W_cost'] for s in simulator.history]
    magnetization = [s['magnetization'] for s in simulator.history]
    xi = [s['correlation_length'] for s in simulator.history]
    
    # Plot 1: C parameter
    axes[0, 0].plot(times, c_values, 'g-', linewidth=1.5)
    axes[0, 0].axhline(y=1.0, color='r', linestyle='--', label='C = 1')
    axes[0, 0].set_xlabel('Time')
    axes[0, 0].set_ylabel('C Parameter')
    axes[0, 0].set_title('Condensation Parameter')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Thermodynamic efficiency
    axes[0, 1].plot(times, eta_values, 'purple', linewidth=1.5)
    axes[0, 1].set_xlabel('Time')
    axes[0, 1].set_ylabel('η_thermo = I_predict / W_cost')
    axes[0, 1].set_title('Thermodynamic Efficiency')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: I_predict vs W_cost
    axes[1, 0].scatter(W_cost, I_pred, c=times, cmap='plasma', s=10, alpha=0.6)
    axes[1, 0].set_xlabel('Work Cost')
    axes[1, 0].set_ylabel('Predictive Information')
    axes[1, 0].set_title('Information vs Cost (colored by time)')
    cbar = plt.colorbar(axes[1, 0].collections[0], ax=axes[1, 0])
    cbar.set_label('Time')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: C vs η_thermo (key relationship)
    axes[1, 1].scatter(c_values, eta_values, c=times, cmap='coolwarm', s=10, alpha=0.6)
    axes[1, 1].axvline(x=1.0, color='r', linestyle='--', alpha=0.5, label='C = 1')
    axes[1, 1].set_xlabel('C Parameter')
    axes[1, 1].set_ylabel('η_thermo')
    axes[1, 1].set_title('Efficiency vs Condensation')
    cbar = plt.colorbar(axes[1, 1].collections[0], ax=axes[1, 1])
    cbar.set_label('Time')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('/mnt/agents/output/hypothesis2_results.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Saved to /mnt/agents/output/hypothesis2_results.png")


# ============================================================================
# EXAMPLE USAGE / DEMO
# ============================================================================

def create_test_assembly_graph(depth: int = 5, branching: int = 2) -> nx.DiGraph:
    """Create a test assembly graph as a DAG."""
    G = nx.DiGraph()
    
    # Root node
    G.add_node(0, mass=1.0, level='root')
    
    # Build hierarchical assembly graph
    node_id = 1
    nodes_at_level = {0: [0]}
    
    for level in range(1, depth + 1):
        nodes_at_level[level] = []
        parents = []
        # Collect all nodes from previous levels as potential parents
        for prev_level in range(level):
            parents.extend(nodes_at_level[prev_level])
        
        # Create new nodes combining pairs of existing nodes
        for i in range(min(branching * level, 20)):
            if len(parents) >= 2:
                p1, p2 = np.random.choice(parents, size=2, replace=False)
                G.add_node(node_id, mass=1.0 + level * 0.5, level=f'L{level}')
                G.add_edge(p1, node_id)
                if p2 != p1:
                    G.add_edge(p2, node_id)
                nodes_at_level[level].append(node_id)
                node_id += 1
    
    return G


def run_demo():
    """Run demonstration simulations for both hypotheses."""
    print("=" * 70)
    print("KID-AT Unified Framework: Simulation Demonstration")
    print("=" * 70)
    
    # Hypothesis 1: Assembly Phase Transitions
    print("\n[H1] Graph-Based Assembly Space Exploration")
    print("-" * 50)
    
    G = create_test_assembly_graph(depth=4, branching=2)
    print(f"Assembly graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Run with selection (alpha < 1) and comparable timescales
    sim1 = AssemblyPhaseTransitionSimulator(
        graph=G,
        alpha=0.3,      # Strong selection
        tau_d=5.0,      # Discovery timescale
        tau_p=5.0,      # Production timescale (comparable)
        N0=1000,
        V_eff=50.0,
        K_ref=1.0,
        kid_crit=10.0,
        seed=42
    )
    
    history1 = sim1.run(T_max=50000, record_interval=100)
    criteria1 = sim1.compute_success_criteria()
    transitions1 = sim1.detect_phase_transitions()
    
    print(f"Simulation steps: {len(history1)}")
    print(f"Final KID_K: {history1[-1].kid_k:.4f}")
    print(f"Final C: {history1[-1].c_parameter:.4f}")
    print(f"Final mean AI: {history1[-1].mean_ai:.2f}")
    print(f"Final max AI: {history1[-1].max_ai}")
    print(f"\nSuccess Criteria:")
    for k, v in criteria1.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"\nDetected transitions: {transitions1}")
    
    # Hypothesis 2: Entropy-Export Optimization
    print("\n[H2] Entropy-Export Optimization Dynamics")
    print("-" * 50)
    
    sim2 = EntropyExportOptimizer(
        N=50,               # Smaller for demo speed
        T=2.0,              # Near critical temperature
        J=1.0,
        learning_rate=0.005,
        V_eff=50.0,
        K_ref=1.0,
        kid_crit=5.0,
        seed=42
    )
    
    history2 = sim2.run(T_max=10000, record_interval=100)
    criteria2 = sim2.compute_success_criteria()
    
    print(f"Simulation steps: {len(history2)}")
    print(f"Final KID_K: {history2[-1]['kid_k']:.4f}")
    print(f"Final C: {history2[-1]['c_parameter']:.4f}")
    print(f"Final η_thermo: {history2[-1]['eta_thermo']:.4f}")
    print(f"Final magnetization: {history2[-1]['magnetization']:.4f}")
    print(f"\nSuccess Criteria:")
    for k, v in criteria2.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    
    print("\n" + "=" * 70)
    print("Demo complete. Generate plots with plot_h1_results() and plot_h2_results()")
    print("=" * 70)
    
    return sim1, sim2


if __name__ == "__main__":
    sim1, sim2 = run_demo()
