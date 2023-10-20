"""Callbacks for the dashboard."""
import base64
from enum import Enum

import jsons
import plotly.io as pio
from dash import Dash
from dash.dependencies import Input, Output, State

from dojo.vis import variables
from dojo.vis.graphs import custom_figure, positions_graph, price_graph, reward_graph

ActionType = Enum("ActionType", ["Trade", "Quote"])


pio.templates.default = "plotly_dark"


def register_interactions(app: Dash):
    """Helper function."""

    @app.callback(
        Output("custom-graph", "figure"),
        [Input("explore-select-0", "value"), Input("explore-select-1", "value")],
    )
    def custom_select(v1, v2):
        return custom_figure(v1, v2)

    @app.callback(
        Output("download-csv", "data"),
        Input("button-save", "n_clicks"),
        prevent_initial_call=True,
    )
    def save_data(clickData):
        return dict(
            content=jsons.dumps(variables.data),
            filename="dojo.json",
        )

    @app.callback(
        Output("file_upload_success_modal", "is_open", allow_duplicate=True),
        Input("button-load", "n_clicks"),
        prevent_initial_call=True,
    )
    def open_modal(n_clicks):
        return True

    @app.callback(
        Output("file_upload_success_modal", "is_open", allow_duplicate=True),
        Input("upload-data", "contents"),
        prevent_initial_call=True,
    )
    def update_output(contents):
        json_string = contents.split(",")[1]
        decoded_data = base64.b64decode(json_string)
        variables.data = jsons.loads(decoded_data, variables.Data)
        return False

    @app.callback(
        [Output("inspector-modal", "is_open"), Output("bookmarks-table", "data")],
        Input("live-update-graph", "clickData"),
    )
    def display_click_data(clickData):
        if clickData:
            bm = variables.Bookmark(name="name", block=int(clickData["points"][0]["x"]))
            variables.bookmarks += [bm]

        data = [
            {"number": f"{i}", "name": f"bookmark-{i}"}
            for i, bm in enumerate(variables.bookmarks)
        ]
        return False, data

    @app.callback(
        Output("interval-component", "n_intervals"),
        Input("button-reset", "n_clicks"),
    )
    def reset_dashboard(a):
        if variables.is_demo:
            variables._from_file("./assets/example_sim.json")
        else:
            variables.reset()
        return 0

    # Define the callback function to update the plot
    @app.callback(
        [
            Output("live-update-graph", "figure"),
            Output("graph-price", "figure"),
            Output("positions-graph", "figure"),
            Output("progress-bar", "value"),
            Output("info-start-date", "children"),
            Output("info-end-date", "children"),
            Output("info-pools", "children"),
            Output("info-num-agents", "children"),
            Output("explore-select-0", "data"),
            Output("explore-select-1", "data"),
            Output("pool-select", "data"),
            Output("agent-select", "data"),
        ],
        [Input("interval-component", "n_intervals")],
        [State("pool-select", "value"), State("agent-select", "value")],
        prevent_initial_call=True,
    )
    def update_graph(n, selected_pool, selected_agent):
        """Refresh the graph.

        :param n: Unused parameter.
        """
        fig_rewards = reward_graph(selected_agent)
        fig_price = price_graph(selected_pool)

        fig_liquidities = positions_graph()

        progress = variables.data.params.progress_value

        options = []
        for iagent, agent in enumerate(variables.data.params.agents):
            options.append(
                {
                    "value": f"agent-{agent}-reward",
                    "label": "Reward",
                    "group": f"Agent-{agent}",
                }
            )
        for pool_info in variables.data.params.pool_info:
            options.append(
                {
                    "value": f"pool-{pool_info.name}-liquidity",
                    "label": "Liquidity",
                    "group": f"Pool-{pool_info.name}",
                }
            )
            options.append(
                {
                    "value": f"pool-{pool_info.name}-price",
                    "label": "Price",
                    "group": f"Pool-{pool_info.name}",
                }
            )
        for signal_name in variables.data.params.signal_names:
            options.append(
                {
                    "value": f"signal-{signal_name}",
                    "label": f"{signal_name}",
                    "group": "Signals",
                }
            )

        return (
            fig_rewards,
            fig_price,
            fig_liquidities,
            progress,
            f"{variables.data.params.start_date}",
            f"{variables.data.params.end_date}",
            ", ".join([info.name for info in variables.data.params.pool_info]),
            ", ".join(variables.data.params.agents),
            options,
            options,
            [
                {"value": f"{pool_info.name}", "label": f"{pool_info.name}"}
                for pool_info in variables.data.params.pool_info
            ],
            [
                {"value": agent, "label": agent}
                for agent in variables.data.params.agents
            ],
        )

    return app
