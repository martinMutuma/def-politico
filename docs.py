from app import create_app
from flasgger import Swagger
from flask_cors import CORS


app = create_app('production')
app.config['SWAGGER'] = {
    "swagger": "2.0",
    "uiversion": "3",
    "info": {
        "title": "Kura Yangu",
        "contact": {
            "email": "bedank6@gmail.com"
        },
        "description": """
        This is the official documentation of the Kura Yangu API.
        Use these endpoints to create a voting system
        """,
        "version": "2.0",
        "license": {
            "name": "MIT license",
            "url": "https://opensource.org/licenses/MIT"
        }
    },
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
swagger = Swagger(app)
# introduce CORS
CORS(app)


@app.route('/api/v2/auth/signup', methods=['POST'])
def signup():
    """ Endpoint for registering a User.
    ---
    tags:
        - Users
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: false
          example: Bearer
      - in: body
        name: Users
        required: true
        schema:
          type: object
          properties:
            firstname:
              type: string
              example: "Governor"
            lastname:
              type: string
              example: "Mani"
            othername:
              type: string
              example: "Mili"
            email:
              type: string
              example: "bedank6@gmail.com"
            phoneNumber:
              type: string
              example: "0700000000"
            passportUrl:
              type: string
              example: "federal"
            isAdmin:
              type: bool
              example: True
            password:
              type: string
              example: "jivutie"
    responses:
      '201':
        description: Created
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/auth/signup', methods=['PUT'])
def set_admin():
    """ Endpoint for changing a user's Admin status.
    ---
    tags:
        - Users
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
      - in: body
        name: Users
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: "james@gmail.com"
    responses:
      '200':
        description: Updated
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/auth/login', methods=['POST'])
def login():
    """ Endpoint for log in.
    ---
    tags:
        - Users
    parameters:
      - in: body
        name: Users
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: "bedank6@gmail.com"
            password:
              type: string
              example: "jivunie"
    responses:
      '200':
        description: Created
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/auth/reset', methods=['POST'])
def reset():
    """ Endpoint for resetting password.
    ---
    tags:
        - Users
    parameters:
      - in: body
        name: Users
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: "bedank6@gmail.com"
    responses:
      '200':
        description: Created
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/offices', methods=['POST'])
def offices():
    """ Endpoint for creating an office.
    ---
    tags:
        - Offices
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
      - in: body
        name: Offices
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Governor"
            type:
              type: string
              example: "federal"
    responses:
      '201':
        description: Created
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/offices', methods=['GET'])
def get_offices():
    """ Endpoint for getting all offices.
    ---
    tags:
        - Offices
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
    responses:
      '200':
        description: Success
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/offices/<office_id>', methods=['GET'])
def get_single_office(office_id):
    """ Endpoint for getting a specific office.
    ---
    tags:
        - Offices
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
      - in: path
        name: office_id
        required: true
        type: integer
    responses:
      '200':
        description: Success
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/offices/<office_id>', methods=['DELETE'])
def delete_single_office(office_id):
    """ Endpoint for deleting an office.
    ---
    tags:
        - Offices
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
      - in: path
        name: office_id
        required: true
        type: integer
    responses:
      '200':
        description: Success
      '404':
        description: Not found
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/parties', methods=['POST'])
def parties():
    """ Endpoint for creating a party.
    ---
    tags:
        - Parties
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
      - in: body
        name: Parties
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "SOME PARTY"
            hq_address:
              type: string
              example: "federal"
            logo_url:
              type: string
              example: "..."
            slogan:
              type: string
              example: "federal"
    responses:
      '201':
        description: Created
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/parties', methods=['GET'])
def get_parties():
    """ Endpoint for getting a list of parties.
    ---
    tags:
        - Parties
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
    responses:
      '200':
        description: Success
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/parties/<party_id>', methods=['GET'])
def get_single_party(party_id):
    """ Endpoint for getting a single party.
    ---
    tags:
        - Parties
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
      - in: path
        name: party_id
        required: true
        type: integer
    responses:
      '200':
        description: Success
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/parties/<party_id>', methods=['DELETE'])
def delete_single_party(office_id):
    """ Endpoint for deleting a party.
    ---
    tags:
        - Parties
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
      - in: path
        name: party_id
        required: true
        type: integer
    responses:
      '200':
        description: Success
      '404':
        description: Not found
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/parties/<party_id>/name', methods=['PATCH'])
def patch_single_party(party_id):
    """ Endpoint for editting the name of a party.
    ---
    tags:
        - Parties
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
      - in: path
        name: party_id
        required: true
        type: integer
      - in: body
        name: Party
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: New name
    responses:
      '200':
        description: Success
      '404':
        description: Not found
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/office/<id>/register', methods=['POST'])
def candidates(id):
    """ Endpoint for creating a candidate.
    ---
    tags:
        - Candidates
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
      - in: path
        name: id
        required: true
        type: integer
      - in: body
        name: Candidate
        required: true
        schema:
          type: object
          properties:
            party:
              type: int
              example: 1
            candidate:
              type: int
              example: 1
    responses:
      '201':
        description: Created
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/candidates', methods=['GET'])
def get_candidates():
    """ Endpoint for getting a list of all candidates.
    ---
    tags:
        - Candidates
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
    responses:
      '200':
        description: Success
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/candidates/<candidate_id>', methods=['GET'])
def get_single_candidate(candidate_id):
    """ Endpoint for getting a specific candidate.
    ---
    tags:
        - Candidates
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
      - in: path
        name: candidate_id
        required: true
        type: integer
    responses:
      '200':
        description: Success
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/votes', methods=['POST'])
def votes(id):
    """ Endpoint for casting a vote.
    ---
    tags:
        - Votes
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
      - in: body
        name: Candidate
        required: true
        schema:
          type: object
          properties:
            candidate:
              type: int
              example: 1
            office:
              type: int
              example: 1
    responses:
      '201':
        description: Created
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/office/<office_id>/result', methods=['GET'])
def get_votes(office_id):
    """ Endpoint for getting election results for an office.
    ---
    tags:
        - Votes
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
      - in: path
        name: office_id
        required: true
        type: integer
    responses:
      '200':
        description: Success
      '409':
        description: Duplicate
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


@app.route('/api/v2/voting-history', methods=['GET'])
def get_voting_history():
    """ Endpoint for getting voting history
    ---
    tags:
        - Votes
    parameters:
      -
          name: authorization
          in: header
          type: string
          required: true
          example: Bearer
    responses:
      '200':
        description: Success
      '404':
        description: Not Found
      '422':
        description: Unprocessable
      '400':
        description: Bad Request
    """


if __name__ == '__main__':
    app.run()
