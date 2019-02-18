from app import create_app
from flasgger import Swagger


app = create_app('production')
swagger = Swagger(app, template_file='apidocs.yaml')


# @app.route('/api/v2/auth/signup', methods=['POST'])
# def signup():
#     """ endpoint for registering users.
#     ---
#     parameters:
#       - name: username
#         required: true
#         type: string
#       - name: email
#         type: string
#         required: true
#       - name: password
#         type: string
#         required: true
#       - name: lastname
#         type: string
#         required: true
#     """


if __name__ == '__main__':
    app.run()
