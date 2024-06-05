INF = float("inf")


class Backtracking:
    def __init__(self, rows, matrix):
        self.rows = rows
        self.matrix = matrix

    def calculate(self):
        n = self.rows
        dist = self.matrix
        visited = [False] * n
        min_cost = INF
        best_path = []
        path = [0]
        best_result = [min_cost, best_path]
        self._tsp(0, 1, 0, path, dist, visited, n, best_result)
        min_cost = best_result[0]
        best_path = best_result[1]
        return min_cost, best_path

    def _tsp(self, current_city, count, cost, path, dist, visited, n, best_result):
        if count == n and dist[current_city][0] != 0:
            self._update_best_path(current_city, count, cost, path, dist, best_result)
            return

        for i in range(n):
            if not visited[i] and dist[current_city][i] != 0:
                self._explore_neighbour(
                    current_city, i, count, cost, path, dist, visited, n, best_result
                )

    def _update_best_path(self, current_city, count, cost, path, dist, best_result):
        total_cost = cost + dist[current_city][0]
        if total_cost < best_result[0]:
            best_result[0] = total_cost
            best_result[1] = path[:] + [0]

    def _explore_neighbour(
        self, current_city, next_city, count, cost, path, dist, visited, n, best_result
    ):
        visited[next_city] = True
        path.append(next_city)
        self._tsp(
            next_city,
            count + 1,
            cost + dist[current_city][next_city],
            path,
            dist,
            visited,
            n,
            best_result,
        )
        path.pop()
        visited[next_city] = False
