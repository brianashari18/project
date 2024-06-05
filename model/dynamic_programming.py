INF = float("inf")


class DynamicProgramming:
    def __init__(self, matrix):
        self.matrix = matrix
        self.n = len(matrix)

    def calculate(self):
        dp = self._initialize_dp()
        self._fill_dp(dp)
        min_cost, path = self._find_minimum_cost_and_path(dp)
        return min_cost, path

    def _initialize_dp(self):
        dp = [[INF] * self.n for _ in range(1 << self.n)]
        dp[1][0] = 0  # Starting from the first city
        return dp

    def _fill_dp(self, dp):
        for mask in range(1 << self.n):
            for u in range(self.n):
                if mask & (1 << u):
                    for v in range(self.n):
                        if mask & (1 << v) and u != v and self.matrix[v][u] != 0:
                            dp[mask][u] = min(
                                dp[mask][u], dp[mask ^ (1 << u)][v] + self.matrix[v][u]
                            )

    def _find_minimum_cost_and_path(self, dp):
        min_cost = min(
            dp[(1 << self.n) - 1][i] + self.matrix[i][0] for i in range(1, self.n)
        )
        mask = (1 << self.n) - 1
        last = 0
        path = [0]
        for i in range(self.n - 1, 0, -1):
            index = self._find_next_city(mask, last, dp)
            path.append(index)
            mask ^= 1 << index
            last = index
        path.append(0)
        path.reverse()
        return min_cost, path

    def _find_next_city(self, mask, last, dp):
        index = -1
        for j in range(self.n):
            if mask & (1 << j) and (
                index == -1
                or dp[mask][j] + self.matrix[j][last]
                < dp[mask][index] + self.matrix[index][last]
            ):
                index = j
        return index
