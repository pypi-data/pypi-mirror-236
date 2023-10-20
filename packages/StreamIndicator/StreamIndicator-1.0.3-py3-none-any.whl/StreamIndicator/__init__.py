_RELEASE = True
"""StreamIndicator

Reusable Ploty indicator and gauge data visualization component for Streamlit

2023 Derek Evans
"""

import os
import streamlit.components.v1 as components
import plotly.graph_objects as go
import streamlit as st

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
StreamIndicator = components.declare_component("StreamIndicator", path=build_dir)

def StreamIndicator(gVal, gTitle="", gMode='gauge+number', gSize="MED",
                    grLow=.30, grMid=.70, gcLow='#FF1708', gcMid='#FF9400', 
                    gcHigh='#1B8720', xpLeft=0, xpRight=1, ypBot=0, ypTop=1, 
                    arBot=None, arTop=1, pTheme="streamlit", cWidth=True, sFix=None):

    """Deploy Plotly gauge or indicator data visualization

    Keyword arguments:

    gVal -- Gauge Value (required)
        Description:
            The value passed to this argument is displayed in
            the center of the visualization, drives the color & position
            of the gauge and is required to successfully call this function.
        Data Type:
            integer, float

    gTitle -- Gauge Title (default '')
        Description:
            Adds a header displayed at the top
            of the visualization.
        Data Type:
            string

    gMode -- Gauge Mode (default gauge+number)
        Description:
            Declares which type of visualization should
            be displayed.
        Options:
            gauge+number, gauge, number
        Data Type:
            string

    gSize -- Gauge Size (default MED)
        Description:
            Automatically resizes the gauge or indicator using 
            pre-defined values options.

            The size of visualization can also be customized by passing the 'CUST' value to
            the argument and assigning a decimal value from 0 to 1 to the following 
            arguments; xpLeft, xpRight, ypBot, and ypTop.
        Options:
            SML, MED, LRG, FULL, CUST
        Data Type:
            String

    grLow -- Low Gauge Range (default 0.30)
        Description:
            Sets the bottom (lowest) percentile target group for the gauge value.  
            When the Gauge Value (gVal) is less than the value assigned to this
            argument, the color assigned to the gcLow (Low Gauge Color) argument
            is displayed.
        Data Type:
            integer, float

    grMid -- Middle Gauge Range (default 0.70) -- 
        Description:
            Sets the middle percentile target group for the gauge value.  When
            the Gauge Value (gVal) is less than the value assigned to this argument,
            the color assigned to the gcMid (Middle Gauge Color) argument is displayed.
            
            If the value assigned to the gVal argument is greater than or equal to
            the value assigned to the grMid argument, the color value assigned to
            gcHigh will then be displayed.
        Data Type:
            integer, float

    gcLow -- Low Gauge Color (default #FF1708)
        Description:
            Gauge color for bottom percentile target group. Default value
            is a hex code for red.  Argument excepts hex color codes and 
            there associated names.
        Data Type:
            string

    gcMid -- Middle Gauge Color (default #FF9400)
        Description:
            Gauge color for middle percentile target group. Default value
            is a hex code for orange.  Argument excepts hex color codes and 
            there associated names.
        Data Type:
            string

    gcHigh -- High Gauge Color (default #1B8720)
        Description:
            Gauge color for middle percentile target group. Default value
            is a hex code for green.  Argument excepts hex color codes and 
            there associated names.
        Data Type:
            string

    sFix -- Gauge Value Suffix (default 0.0)
        Description:
            Adds a suffix (character) to the gauge value displayed in the
            center of the visualization.
            
            Assigning the '%' character to this argument will display the
            percentage symbol at the end of the value shown in the center
            of the visualization and convert the gauge value from a floating
            point integer so the value displays correctly as a percentage.
        Options:
            %
        Data Type:
            string

    xpLeft -- X-Axis Position 1 for Plot (default 0.0)
    xpRight --  X-Axis Position 2 for Plot (default 0.0)
    ypBot --  X-Axis Position 1 for Plot (default 0.0)
    ypTop --  X-Axis Position 2 for Plot (default 0.0)
    arBot -- Bottom Axis Range Value (default 0.0) 
    arTop --  Bottom Axis Range Value (default 0.0)
    pTheme -- Plot Theme (default 0.0)
    cWidth -- Container Width (default 0.0)
    """

    if sFix == "%":

        gaugeVal = round((gVal * 100), 1)
        top_axis_range = (arTop * 100)
        bottom_axis_range = arBot
        low_gauge_range = (grLow * 100)
        mid_gauge_range = (grMid * 100)

    else:

        gaugeVal = gVal
        top_axis_range = arTop
        bottom_axis_range = arBot
        low_gauge_range = grLow
        mid_gauge_range = grMid


    if gSize == "SML":
        x1, x2, y1, y2 =.25, .25, .75, 1
    elif gSize == "MED":
        x1, x2, y1, y2 = .50, .50, .50, 1
    elif gSize == "LRG":
        x1, x2, y1, y2 = .75, .75, .25, 1
    elif gSize == "FULL":
        x1, x2, y1, y2 = 0, 1, 0, 1
    elif gSize == "CUST":
        x1, x2, y1, y2 = xpLeft, xpRight, ypBot, ypTop   

    if gaugeVal < low_gauge_range: 
        gaugeColor = gcLow
    elif gaugeVal >= low_gauge_range and gaugeVal < mid_gauge_range:
        gaugeColor = gcMid
    else:
        gaugeColor = gcHigh

    fig1 = go.Figure(go.Indicator(
        mode = gMode,
        value = gaugeVal,
        domain = {'x': [x1, x2], 'y': [y1, y2]},
        number = {"prefix": pFix, "suffix": sFix},
        title = {'text': gTitle},
        gauge = {
            'axis': {'range': [bottom_axis_range, top_axis_range]},
            'bar' : {'color': gaugeColor}
        }
    ))

    config = {'displayModeBar': False}

    gaugePlot = st.plotly_chart(
        fig1, 
        use_container_width=cWidth, 
        theme=pTheme, 
        **{'config':config}
    )

    return gaugePlot

return_value = StreamIndicator
