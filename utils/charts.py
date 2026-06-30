import plotly.express as px


def bar_chart(
    data,
    x,
    y,
    title,
    color=None,
    height=420,
    color_scale="Blues"
):

    fig = px.bar(
        data,
        x=x,
        y=y,
        color=color if color else y,
        text=y,
        title=title,
        color_continuous_scale=color_scale
    )

    fig.update_layout(
        height=height,
        plot_bgcolor="white",
        paper_bgcolor="white",
        coloraxis_showscale=False,
        xaxis_title=None,
        yaxis_title=None
    )

    return fig


def pie_chart(
    data,
    names,
    values,
    title,
    height=420
):

    fig = px.pie(
        data,
        names=names,
        values=values,
        hole=0.45,
        title=title
    )

    fig.update_layout(
        height=height
    )

    return fig


def line_chart(
    data,
    x,
    y,
    title,
    height=420
):

    fig = px.line(
        data,
        x=x,
        y=y,
        markers=True,
        title=title
    )

    fig.update_layout(
        height=height,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    return fig


def scatter_chart(
    data,
    x,
    y,
    title,
    color=None,
    height=420
):

    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        size=y,
        title=title
    )

    fig.update_layout(
        height=height,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    return fig


def histogram_chart(
    data,
    x,
    title,
    bins=10,
    height=420
):

    fig = px.histogram(
        data,
        x=x,
        nbins=bins,
        title=title,
        color_discrete_sequence=["#1565C0"]
    )

    fig.update_layout(
        height=height,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    return fig


def gauge_color(score):

    if score >= 90:
        return "Excellent"

    if score >= 75:
        return "Good"

    if score >= 50:
        return "Average"

    return "Critical"