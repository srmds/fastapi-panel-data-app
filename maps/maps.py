import panel as pn
import param
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("log_file.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# see: https://panel.holoviz.org/user_guide/Param.html#parameter-dependencies
class GoogleMapViewer(param.Parameterized):
    continent = param.ObjectSelector(default='Europe', objects=['Africa', 'Asia', 'Europe'])
    country = param.ObjectSelector(default='The Netherlands', objects=['The Netherlands', 'Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht'])
    _countries = {'Africa': ['Ghana', 'Togo', 'South Africa', 'Tanzania'],
                  'Asia': ['China', 'Thailand', 'Japan'],
                  'Europe': ['Austria', 'Bulgaria', 'Greece', 'The Netherlands', 'Portugal', 'Switzerland']}

    @param.depends('continent', watch=True)
    def _update_countries(self):
        countries = self._countries[self.continent]
        self.param['country'].objects = countries
        self.country = countries[0]

    @param.depends('country')
    def view(self):
        iframe = """
        <iframe width="800" height="400" src="https://maps.google.com/maps?q={country}&z=6&output=embed"
        frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>
        """.format(country=self.country)

        return pn.pane.HTML(iframe, height=1200, width=800)

    def process_request(request):
        """
        If present, this function executes when an HTTP request arrives.
        :return:
        """
        logger.info("process REQQQQQQ")

        return {}
