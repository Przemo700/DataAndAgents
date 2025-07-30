import plotly.express as px
import streamlit as st

def title_formatting(title_text, subtitle_text=None):

    title = f"<span style='font-size:18px; font-weight:bold'>{title_text}</span><br>"
    subtitle = ""
    if subtitle_text:
        subtitle = f"<span style='font-size:14px; color:gray'>{subtitle_text}</span>"

    return title + subtitle


def draw_pie_chart(df, metric):

    # Create Pie Chart
    fig = px.pie(
        df, 
        names = 'Type', 
        values = metric,
        hole=0.4, 
        color = 'Type', 
        color_discrete_sequence=['green','lightgreen','lightblue','lightpink']
    ).update_layout(
        width=600, height=600,
        # showlegend = False,
        legend_title = None,
        legend_font_size = 11,
        legend = dict(
            orientation="v",
            yanchor="middle", y=0.5,
            xanchor="left", x=1.01
        ),
        title=dict(
            text= title_formatting("Type of expenditure"),
            y=1,  # moves the title closer to the chart (1.0 is top of the figure)
            yanchor='top',
            pad=dict(t=60)  # reduce top padding (default is around 40)
        )
    ).update_traces(
        textfont_size=12,
        texttemplate='%{percent:.1%}'    #'%{label}<br>%{percent:.1%}'
    )

    # Show chart
    st.plotly_chart(fig)

def draw_bar_chart(df, metric):

    # Define chart coordinates
    y_avg = df[metric].mean()
    x_start = df['Country_Code'].iloc[0]
    x_end = df['Country_Code'].iloc[-1]

    # Create bar chart
    fig = px.bar(
        df, 
        x ='Country_Code', y =metric, 
        text = metric,
        #color_discrete_sequence = ['#D1504A']
        color='Index', color_continuous_scale=px.colors.sequential.YlGn[::-1]
    ).update_layout(
        width=800, height=600,
        coloraxis_showscale=False,
        plot_bgcolor="white",
        yaxis=dict(
            gridcolor='lightgray',
            gridwidth=0.5    
        ),
        title = dict(
            text = title_formatting(f"Countries {metric}"),
            y=1, yanchor='top',
            pad=dict(t=50)
        )
    ).update_traces(
        texttemplate="%{y:.2f}"
    ).add_shape(
        type="line", 
        x0=x_start, x1=x_end,xref='x',
        y0=y_avg, y1=y_avg, yref='y',
        line=dict(color="red", width=1.25, dash="dash")
    ).add_annotation(
        x=x_end,
        y=y_avg,
        text=f"Avg: {y_avg:.1f}",
        showarrow=False,
        yshift=10,
        font=dict(color="red", size=12)
    )

    # Show figure
    st.plotly_chart(fig)

def draw_scatter_plot(df):

    # Calculate main chart coordinates
    x_avg = df["perc_of_gdp"].mean()
    y_avg = df["perc_of_bad_health"].mean()

    x_min = df["perc_of_gdp"].min()*0.9
    x_max = df["perc_of_gdp"].max()*1.05

    y_min = df["perc_of_bad_health"].min()*0.9
    y_max = df["perc_of_bad_health"].max()*1.05

    # Assign quadrant label
    def assign_quadrant(row):
        if row["perc_of_gdp"] > x_avg and row["perc_of_bad_health"] > y_avg:
            return "Top Right"
        elif row["perc_of_gdp"] < x_avg and row["perc_of_bad_health"] > y_avg:
            return "Top Left"
        elif row["perc_of_gdp"] < x_avg and row["perc_of_bad_health"] < y_avg:
            return "Bottom Left"
        else:
            return "Bottom Right"

    df["Quadrant"] = df.apply(assign_quadrant, axis=1)

    # Create scatter plot
    fig = px.scatter(
        df,
        x="perc_of_gdp",
        y="perc_of_bad_health",
        text="Country_Code",
        color="Quadrant",
        title = title_formatting(
            "Spending on helahcare vs reported health",
            "Quadrants by low/high spend and more/less bad health people"
        ),
        color_discrete_map={
            "Top Right": "red",
            "Top Left": "orange",
            "Bottom Left": "green",
            "Bottom Right": "blue"
        }
    )

    # Quadrant background shading
    for sq in [
        {"x0":x_min, "x1":x_avg, "y0":y_min, "y1":y_avg, "color":"green"}, 
        {"x0":x_avg, "x1":x_max, "y0":y_min, "y1":y_avg, "color":"blue"}, 
        {"x0":x_min, "x1":x_avg, "y0":y_avg, "y1":y_max, "color":"orange"}, 
        {"x0":x_avg, "x1":x_max, "y0":y_avg, "y1":y_max, "color":"red"}
    ]:
        fig.add_shape(
            type="rect",
            x0=sq["x0"], x1=sq["x1"],
            y0=sq["y0"], y1=sq["y1"],
            fillcolor=sq["color"], opacity=0.05, layer="below", line_width=0
        )

    # Add quadrant split lines
    for ln in [
        {"x0":x_avg, "x1":x_avg, "y0":y_min, "y1":y_max},
        {"x0":x_min, "x1":x_max, "y0":y_avg, "y1":y_avg}
    ]:   
        fig.add_shape(
            type="line", 
            x0=ln["x0"], x1=ln["x1"],
            y0=ln["y0"], y1=ln["y1"],
            line=dict(color="gray", width=1, dash="solid")
        )

    # Final layout settings
    fig.update_layout(
        #yaxis_scaleanchor='x',
        width=600, height=600,
        yaxis_range=[y_min, y_max], xaxis_range=[x_min, x_max],
        yaxis_title='% of bad or very bad health people', yaxis_title_font=dict(size=11),
        xaxis_title='% of healthcare spending to GDP', xaxis_title_font=dict(size=11)
    ).update_traces(
        marker=dict(size=10),
        textposition='top center',
        textfont=dict(size=10),
        showlegend=False
    )

    st.plotly_chart(fig)

def draw_histogram(df):

    # Create histogram figure
    fig = px.histogram(
        df,
        x="Age_Group",
        y="Number_of_People",
        color="Health_Assesement",
        barnorm='percent',
        text_auto='.1f',
        title=title_formatting("Reported health by age groups"),
        color_discrete_sequence=['red','lightpink','lightblue','lightgreen','green']
    )

    # Define the layout for specific elements
    fig.update_layout(
        width=600, height=600,
        xaxis_title="Age Group (Years)", xaxis_title_font=dict(size=11),
        yaxis_title="Percentage of People (%)", yaxis_title_font=dict(size=11),
        plot_bgcolor="white",
        yaxis=dict(
            gridcolor='lightgray',
            gridwidth=0.5    
        ),
        legend_title = None,
        legend_font_size = 11,
        legend = dict(
            orientation="h",
            yanchor="bottom", y=1,
            xanchor="left", x=0
        )
    ).update_traces(
        textposition='inside',
        insidetextanchor='middle',
        textfont_size=10
    )

    # Show figure
    st.plotly_chart(fig)