import panel as pn

from sinewave.sinewave import SineWave


def sinewave():
    sw = SineWave()
    return pn.Row(sw.param, sw.plot).servable()

