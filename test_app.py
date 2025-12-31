# test_app.py
import pytest
from new_app import app
import chromedriver_autoinstaller

# Automatically install ChromeDriver
chromedriver_autoinstaller.install()

def test_header_presence(dash_duo):
    dash_duo.start_server(app)
    header = dash_duo.find_element("h1")
    assert header.text == "Pink Morsel Sales Visualizer"

def test_graph_presence(dash_duo):
    dash_duo.start_server(app)
    graph = dash_duo.find_element("#sales-line-chart")
    assert graph is not None

def test_region_picker_presence(dash_duo):
    dash_duo.start_server(app)
    region_picker = dash_duo.find_element("#region-radio")
    assert region_picker is not None
