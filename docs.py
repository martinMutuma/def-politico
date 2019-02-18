from app import create_app
from flasgger import Swagger


app = create_app('production')
swagger = Swagger(app, template_file='../apidocs.yaml')


@app.route('/parties')
def colors(palette):
    """
    file:apidocs.yaml
    """


app.run(debug=True)
