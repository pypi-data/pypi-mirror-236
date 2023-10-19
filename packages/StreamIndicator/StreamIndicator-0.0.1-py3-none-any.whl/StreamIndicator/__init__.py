import os
import streamlit.components.v1 as components
import plotly.graph_objects as go
import streamlit as st


parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
# StreamIndicator = components.declare_component("StreamIndicator", path=build_dir)
StreamIndicator = components.declare_component(
    "StreamIndicator", 
    url="http://localhost:3001"
)


def StreamIndicator(gVal, gTitle="", gMode='gauge+number', grLow=.30, grMid=.70, 
                gcLow='red', gcMid='yellow', gcHigh='green',
                xpLeft=0, xpRight=1, ypBot=0, ypTop=1, arBot=None, arTop=1):

    gaugeVal = gVal

    if gaugeVal < grLow: 
        gaugeColor = gcLow
    elif gaugeVal >= grLow and gaugeVal < grMid:
        gaugeColor = gcMid
    else:
        gaugeColor = gcHigh

    fig1 = go.Figure(go.Indicator(
        mode = gMode,
        value = gaugeVal,
        domain = {'x': [xpLeft, xpRight], 'y': [ypBot, ypTop]},
        title = {'text': gTitle},
        gauge = {
            'axis': {'range': [arBot, arTop]},
            'bar' : {'color': gaugeColor}
        }
    ))

    config = {'displayModeBar': False}

    gaugePlot = st.plotly_chart(
        fig1, 
        use_container_width=True, 
        theme="streamlit", 
        **{'config':config}
    )

    return gaugePlot

return_value = StreamIndicator
