import matplotlib

matplotlib.use("Agg")
import os
import time
import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, send_file
from model import backtracking as bt, dynamic_programming as dp

INF = float("inf")

app = Flask(__name__)


@app.route("/")
def index():
    rows = request.form.get("rows", default=2, type=int)
    cols = request.form.get("cols", default=2, type=int)
    return render_template("index.html", rows=rows, cols=cols)


@app.route("/generate_graph", methods=["POST"])
def generate_graph():
    try:
        rows = int(request.form["rows"])
        cols = rows

        matrix = []
        for i in range(rows):
            row = [int(request.form[f"matrix_{i}_{j}"]) for j in range(cols)]
            matrix.append(row)

        adj_matrix = np.array(matrix)

        G = nx.from_numpy_array(adj_matrix)
        pos = nx.spring_layout(G)  # Layout graf

        plt.figure(figsize=(8, 6))
        nx.draw(
            G,
            pos,
            node_color="skyblue",
            node_size=2000,
            edge_color="gray",
        )

        # Tambahkan label tepi
        edge_labels = {
            (i, j): adj_matrix[i][j]
            for i in range(rows)
            for j in range(cols)
            if adj_matrix[i][j] != 0
        }

        node_labels = {i: chr(i + 65) for i in range(len(adj_matrix))}

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

        if not os.path.exists("static"):
            os.makedirs("static")
        plt.savefig("static/graph.png")
        plt.close()

        code_to_measure = """
        BT_length, BT_routes = BT.calculate()
        """
        BT = bt.Backtracking(rows, matrix)
        BT_length, BT_routes = BT.calculate()
        temp1 = [node_labels[route] for route in BT_routes]
        BT_routes = " ---> ".join(map(str, temp1))
        print(f"current: {time.time()}")

        DP = dp.DynamicProgramming(matrix)
        DP_length, DP_routes = DP.calculate()
        temp2 = [node_labels[route] for route in DP_routes]
        DP_routes = " ---> ".join(map(str, temp2))

        return render_template(
            "index.html",
            graph_generated=True,
            rows=rows,
            cols=cols,
            BT_length=BT_length,
            BT_routes=BT_routes,
            DP_length=DP_length,
            DP_routes=DP_routes,
        )
    except Exception as e:
        return render_template(
            "index.html", graph_generated=False, error=str(e), rows=rows, cols=cols
        )


@app.route("/graph")
def graph():
    return send_file("static/graph.png", mimetype="image/png")


@app.route("/about-us")
def about_us():
    with open("authors.json", "r") as file:
        authors = json.load(file)

    return render_template("about-us.html", authors=authors)


if __name__ == "__main__":
    app.run(debug=True)
