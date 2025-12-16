import numpy as np
from typing import List, Tuple, Optional


class AntColony:
    """
    Basit, stabil ve okunaklı ACO (TSP) implementasyonu.

    Kullanım:
        colony = AntColony(distance_matrix, n_ants=20, n_iterations=100,
                           alpha=1.0, beta=5.0, evaporation_rate=0.5,
                           Q=100.0, seed=42)
        best_tour, best_length, history = colony.run()

    Dönenler:
        best_tour   : En iyi rota (indeks listesi)
        best_length : En iyi rota uzunluğu
        history     : Her iterasyonda o ana kadarki EN İYİ (global best) mesafe
    """

    def __init__(
        self,
        distance_matrix: np.ndarray,
        n_ants: int = 20,
        n_iterations: int = 100,
        alpha: float = 1.0,
        beta: float = 5.0,
        evaporation_rate: float = 0.5,
        Q: float = 100.0,
        seed: Optional[int] = None,
    ):
        self.dist = np.array(distance_matrix, dtype=float)
        if self.dist.ndim != 2 or self.dist.shape[0] != self.dist.shape[1]:
            raise ValueError("distance_matrix kare (NxN) numpy array olmalı.")

        self.n = self.dist.shape[0]
        self.n_ants = max(1, int(n_ants))
        self.n_iterations = max(1, int(n_iterations))
        self.alpha = float(alpha)
        self.beta = float(beta)
        self.rho = float(evaporation_rate)
        self.Q = float(Q)

        # RNG (seed verilirse sonuçlar tekrar üretilebilir olur)
        self.rng = np.random.default_rng(seed)

    # =============================
    # Tur uzunluğu
    # =============================
    def _tour_length(self, tour: List[int]) -> float:
        total = 0.0
        for i in range(len(tour)):
            a = tour[i]
            b = tour[(i + 1) % len(tour)]  # kapanış
            d = self.dist[a, b]
            if np.isinf(d):
                total += 1e6  # ağır ceza
            else:
                total += float(d)
        return total

    # =============================
    # Tek karınca turu oluşturma
    # =============================
    def _construct_tour(
        self,
        start: int,
        pheromone: np.ndarray,
        visibility: np.ndarray
    ) -> List[int]:

        tour = [int(start)]
        unvisited = set(range(self.n))
        unvisited.remove(int(start))
        current = int(start)

        while unvisited:
            candidates = list(unvisited)

            tau_vals = pheromone[current, candidates] ** self.alpha
            eta_vals = visibility[current, candidates] ** self.beta
            numerators = tau_vals * eta_vals

            total = numerators.sum()
            if total <= 0.0:
                probs = np.ones(len(candidates)) / len(candidates)
            else:
                probs = numerators / total

            chosen = int(self.rng.choice(candidates, p=probs))
            tour.append(chosen)
            unvisited.remove(chosen)
            current = chosen

        return tour

    # =============================
    # ACO çalıştırma
    # =============================
    def run(self) -> Tuple[List[int], float, List[float]]:
        n = self.n

        pheromone = np.ones((n, n), dtype=float)

        epsilon = 1e-12
        visibility = 1.0 / (self.dist + epsilon)
        np.fill_diagonal(visibility, 1e-6)

        best_tour: Optional[List[int]] = None
        best_len: float = float("inf")
        history: List[float] = []

        for it in range(self.n_iterations):
            all_tours: List[List[int]] = []
            all_lengths: List[float] = []

            # === Karıncalar ===
            for _ in range(self.n_ants):
                start = int(self.rng.integers(0, n))
                tour = self._construct_tour(start, pheromone, visibility)
                L = self._tour_length(tour)

                all_tours.append(tour)
                all_lengths.append(L)

                # GLOBAL BEST güncelle
                if L < best_len:
                    best_len = L
                    best_tour = tour.copy()

            # ✅ YAKINŞAMA İÇİN DOĞRU KAYIT (GLOBAL BEST)
            history.append(best_len)

            # === Feromon buharlaşması ===
            pheromone *= (1.0 - self.rho)

            # === Feromon ekleme ===
            for tour, L in zip(all_tours, all_lengths):
                if L <= 0.0 or np.isinf(L):
                    continue
                delta = self.Q / L
                for i in range(len(tour)):
                    a = tour[i]
                    b = tour[(i + 1) % len(tour)]
                    pheromone[a, b] += delta
                    pheromone[b, a] += delta  # simetrik

        # Güvenlik (nadiren gerekebilir)
        if best_tour is None:
            best_tour = list(range(self.n))
            best_len = self._tour_length(best_tour)

        return best_tour, best_len, history
