"""Plotly graphs for the dashboard."""
import copy
from enum import Enum

import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

from dojo.vis import variables

pio.templates["myname"] = go.layout.Template(
    layout=go.Layout(colorway=["#6BD6E3", "#BE97D2", "#FF929C"])
)
pio.templates.default = "myname"


ActionType = Enum("ActionType", ["Trade", "Quote"])

COLORS = ["#BE97D2", "#6BD6E3", "#FEE26C", "#FF929C"]
GLOW_WIDTH = 5
GLOW_COLOR = "rgba(255,255,255,0.1)"


def _add_bookmarks_to_fig(fig):
    for i, bm in enumerate(variables.bookmarks):
        fig.add_vline(
            x=bm.block,
            line_width=1,
            line_dash="dash",
            line_color="#FF67C3",
            label=dict(
                text=f"{i}", textposition="end", textangle=0, font=dict(color="#FF67C3")
            ),
        )
    return fig


def _empty_graph():
    fig = go.Figure()
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x",
    )
    fig.update_layout(font_family="Quicksand")
    return fig


def custom_figure(v1, v2):
    """TODO."""
    x = copy.copy(sorted(list(variables.data.blockdata.keys())))
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # signals_keys = [list(variables.data.blockdata[i].signals.keys()) for i in x]
    # signals_keys = set([item for sublist in signals_keys for item in sublist])
    # print(signals_keys)

    def _v_to_traces(x, v1, index=0):
        quantity = v1.lower().rsplit("-")[-1]
        if v1.lower().startswith("agent"):
            agent_name = v1.split("-")[1]
            iagent = variables.data.params.agents.index(agent_name)
            y = [variables.data.blockdata[i].agentdata[int(iagent)].reward for i in x]
        elif v1.lower().startswith("pool"):
            poolname = v1.split("-", maxsplit=1)[1].rsplit("-", maxsplit=1)[0]
            if quantity == "price":
                y = [variables.data.blockdata[i].pooldata[poolname].price for i in x]
            elif quantity == "liquidity":
                y = [
                    variables.data.blockdata[i].pooldata[poolname].liquidity for i in x
                ]
            else:
                raise ValueError(quantity)
        elif v1.lower().startswith("signal"):
            quantity = v1.rsplit("-")[-1]
            y = [variables.data.blockdata[i].signals[quantity] for i in x]
        else:
            x = None
            y = None
        trace1 = go.Scatter(
            x=x, y=y, line=dict(color=COLORS[index], width=1), name=v1, showlegend=False
        )
        trace1glow = go.Scatter(
            x=x,
            y=y,
            line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
            showlegend=False,
            hoverinfo="skip",
        )
        return trace1, trace1glow

    trace1, trace1glow = _v_to_traces(x, v1, 0)
    trace2, trace2glow = _v_to_traces(x, v2, 1)

    fig.add_trace(trace1, secondary_y=False)
    fig.add_trace(trace1glow, secondary_y=False)
    fig.add_trace(trace2, secondary_y=True)
    fig.add_trace(trace2glow, secondary_y=True)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x",
    )
    fig.update_layout(font_family="Quicksand")
    fig.update_yaxes(title=v1, secondary_y=False, title_font_color=COLORS[0])
    fig.update_yaxes(title=v2, secondary_y=True, title_font_color=COLORS[1])
    fig.update_xaxes(title="Block")

    fig = _add_bookmarks_to_fig(fig)
    return fig


def positions_graph():
    """Plots the current positions of the agent."""
    if len(variables.data.params.pool_info) == 0:
        return _empty_graph()
    keys = copy.copy(list(variables.data.blockdata.keys()))

    # Create figure with secondary y-axis
    subplot_titles = ("wallet agent 1", "LP agent 1", " wallet agent 2", "LP agent 2")

    subplot_titles = []
    for agent in variables.data.params.agents:
        subplot_titles += [
            f"Tokens in Wallet - {agent}",
            f"Tokens in LP Positions - {agent}",
        ]

    # if not variables.data.params.agents or variables.data.params.agents == []:
    #     variables.data.params.num_agents = 2

    num_rows = len(variables.data.params.agents)

    fig = make_subplots(
        rows=num_rows,
        cols=2,
        subplot_titles=subplot_titles,
        shared_xaxes=True,
        vertical_spacing=0.1,
        specs=[[{"secondary_y": True}, {"secondary_y": True}]] * num_rows,
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=400 * len(variables.data.params.agents),
        hovermode="x",
    )
    fig.update_layout(font_family="Quicksand")

    for iagent, agent in enumerate(variables.data.params.agents):
        blocks = [
            i
            for i in keys
            if variables.data.blockdata[i].agentdata[iagent].liquidities is not None
        ]
        trace_lp_token0 = [
            variables.data.blockdata[block].agentdata[iagent].liquidities.lp.token0
            for block in blocks
        ]
        trace_lp_token1 = [
            variables.data.blockdata[block].agentdata[iagent].liquidities.lp.token1
            for block in blocks
        ]
        trace_wallet_token0 = [
            variables.data.blockdata[block].agentdata[iagent].liquidities.wallet.token0
            for block in blocks
        ]
        trace_wallet_token1 = [
            variables.data.blockdata[block].agentdata[iagent].liquidities.wallet.token1
            for block in blocks
        ]
        wallet_token0 = go.Scatter(
            x=blocks,
            y=trace_wallet_token0,
            hoverinfo="x+y",
            mode="lines",
            name="wallet token 0",
            line=dict(color=COLORS[0], width=1),
            showlegend=False,
        )
        glow_wallet_token0 = go.Scatter(
            x=blocks,
            y=trace_wallet_token0,
            hoverinfo="skip",
            mode="lines",
            line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
            showlegend=False,
        )
        lp_token0 = go.Scatter(
            x=blocks,
            y=trace_lp_token0,
            hoverinfo="x+y",
            mode="lines",
            name="lp token 0",
            line=dict(color=COLORS[0], width=1),
            showlegend=False,
        )
        glow_lp_token0 = go.Scatter(
            x=blocks,
            y=trace_lp_token0,
            hoverinfo="skip",
            mode="lines",
            line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
            showlegend=False,
        )
        wallet_token1 = go.Scatter(
            x=blocks,
            y=trace_wallet_token1,
            hoverinfo="x+y",
            mode="lines",
            name="wallet token 1",
            line=dict(color=COLORS[1], width=1),
            showlegend=False,
        )
        glow_wallet_token1 = go.Scatter(
            x=blocks,
            y=trace_wallet_token1,
            hoverinfo="skip",
            mode="lines",
            line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
            showlegend=False,
        )
        lp_token1 = go.Scatter(
            x=blocks,
            y=trace_lp_token1,
            hoverinfo="x+y",
            mode="lines",
            name="lp token 1",
            line=dict(color=COLORS[1], width=1),
            showlegend=False,
        )
        glow_lp_token1 = go.Scatter(
            x=blocks,
            y=trace_lp_token1,
            hoverinfo="skip",
            mode="lines",
            line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
            showlegend=False,
        )

        fig.add_trace(wallet_token0, row=iagent + 1, col=1)
        fig.add_trace(glow_wallet_token0, row=iagent + 1, col=1)

        fig.add_trace(wallet_token1, row=iagent + 1, col=1, secondary_y=True)
        fig.add_trace(glow_wallet_token1, row=iagent + 1, col=1, secondary_y=True)

        fig.add_trace(lp_token0, row=iagent + 1, col=2)
        fig.add_trace(glow_lp_token0, row=iagent + 1, col=2)

        fig.add_trace(lp_token1, row=iagent + 1, col=2, secondary_y=True)
        fig.add_trace(glow_lp_token1, row=iagent + 1, col=2, secondary_y=True)
        fig.update_yaxes(
            row=iagent + 1,
            col=1,
            secondary_y=False,
            title=f"{variables.data.params.pool_info[0].token0}",
            title_font_color=COLORS[0],
        )
        fig.update_yaxes(
            row=iagent + 1,
            col=1,
            secondary_y=True,
            title=f"{variables.data.params.pool_info[0].token1}",
            title_font_color=COLORS[1],
        )
        fig.update_yaxes(
            row=iagent + 1,
            col=2,
            secondary_y=False,
            title=f"{variables.data.params.pool_info[0].token0}",
            title_font_color=COLORS[0],
        )
        fig.update_yaxes(
            row=iagent + 1,
            col=2,
            secondary_y=True,
            title=f"{variables.data.params.pool_info[0].token1}",
            title_font_color=COLORS[1],
        )

        fig.update_yaxes(row=iagent + 1, col=1, spikemode="across")
        fig.update_yaxes(row=iagent + 1, col=2, spikemode="across")

        fig.update_xaxes(row=len(variables.data.params.agents), col=1, title="Block")
        fig.update_xaxes(row=len(variables.data.params.agents), col=2, title="Block")

    return fig


def reward_graph(agent_name):
    """Plot reward graph."""

    def actions2string(block, actions):
        result = f"BLOCK: {block}<br>"
        result += "ACTIONS:<br>"
        for action in actions:
            result += f" {action.type}: {action.info}"
        return result

    blocks = sorted(list(variables.data.blockdata.keys()))

    fig = make_subplots(
        rows=1,
        cols=1,
        # subplot_titles=[f"agent {i+1}" for i in range(1)],
        shared_xaxes=True,
        vertical_spacing=0.1,
        specs=[[{"secondary_y": True}]] * 1,
    )
    if agent_name is not None:
        iagent = variables.data.params.agents.index(agent_name)

        y0 = [
            variables.data.blockdata[block].agentdata[iagent].reward for block in blocks
        ]
        trace = go.Scatter(
            x=blocks,
            y=y0,
            hoverinfo="skip",
            showlegend=False,
            mode="lines",
            line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
        )
        fig.add_trace(trace)

        trace = go.Scatter(
            x=blocks,
            y=y0,
            name="reward",
            hoverinfo="text",
            showlegend=False,
            hovertext=[
                f"BLOCK {block}<br>REWARD {round(variables.data.blockdata[block].agentdata[iagent].reward,3)}"
                for block in blocks
            ],
            mode="lines",
            line=dict(color=COLORS[0], width=1),
        )
        fig.add_trace(trace)
        blocks_with_actions = [
            block
            for block in blocks
            if len(variables.data.blockdata[block].agentdata[iagent].actions) > 0
        ]
        trace_actions = go.Scatter(
            x=blocks_with_actions,
            y=[
                variables.data.blockdata[block].agentdata[iagent].reward
                for block in blocks_with_actions
            ],
            mode="markers",
            hoverinfo="text",
            marker=dict(
                size=8,
                color=COLORS[0],
                line=dict(width=2, color="rgba(255,255,255,0.2)"),
            ),
            name="actions",
            hovertext=[
                actions2string(
                    block, variables.data.blockdata[block].agentdata[iagent].actions
                )
                for block in blocks_with_actions
            ],
            showlegend=False,
        )
        fig.add_trace(trace_actions)

    names = set()
    fig.for_each_trace(
        lambda trace: trace.update(showlegend=False)
        if (trace.name in names)
        else names.add(trace.name)
    )
    fig.update_layout(
        yaxis=dict(title="Reward"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(title_text="Block")
    fig.update_layout(hovermode="x")
    fig.update_layout(font_family="Quicksand")
    fig = _add_bookmarks_to_fig(fig)
    return fig


def price_graph(pool: str):
    """Plot price graph."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if pool is not None:
        blocks = sorted(list(variables.data.blockdata.keys()))
        prices = [
            variables.data.blockdata[block].pooldata[pool].price for block in blocks
        ]
        liquidities = [
            variables.data.blockdata[block].pooldata[pool].liquidity for block in blocks
        ]

        trace1 = go.Scatter(
            x=blocks,
            y=prices,
            name="price",
            hoverinfo="text",
            hovertext=[f"Price: {price}" for price in prices],
            mode="lines",
            line=dict(color=COLORS[0], width=1),
        )
        glow_trace1 = go.Scatter(
            x=blocks,
            y=prices,
            hoverinfo="skip",
            mode="lines",
            line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
            showlegend=False,
        )
        trace2 = go.Scatter(
            x=blocks,
            y=liquidities,
            name="total liquidity",
            hoverinfo="text",
            hovertext=[f"Liquidity: {liquidity}" for liquidity in liquidities],
            mode="lines",
            line=dict(color=COLORS[1], width=1),
        )
        glow_trace2 = go.Scatter(
            x=blocks,
            y=liquidities,
            hoverinfo="skip",
            mode="lines",
            line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
            showlegend=False,
        )
        fig.add_trace(trace1, secondary_y=False)
        fig.add_trace(trace2, secondary_y=True)
        fig.add_trace(glow_trace1, secondary_y=False)
        fig.add_trace(glow_trace2, secondary_y=True)
        fig.update_layout(
            yaxis=dict(
                title=f"Price [{variables.data.params.pool_info[0].token0}/{variables.data.params.pool_info[0].token1}]"
            ),
            yaxis2=dict(title="Active Liquidity"),
        )
    fig.update_layout(
        xaxis=dict(title="Block"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(font_family="Quicksand")
    fig = _add_bookmarks_to_fig(fig)
    return fig
