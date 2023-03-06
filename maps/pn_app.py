import panel as pn
from maps.maps import GoogleMapViewer


def maps():
    viewer = GoogleMapViewer(name='Google Map Viewer')
    return pn.Row(viewer.param, viewer.view)

