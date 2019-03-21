from flask import Blueprint, request, jsonify
from flask import make_response
from app.v2.models.upload_model import UploadImage
from app.blueprints import v2
from app.v2.utils.validator import response_error, response
from flask_jwt_extended import (jwt_required, get_jwt_identity)


@v2.route('/user/update_image', methods=['PATCH'])
@jwt_required
def update_image():
    """ Update user image """

    data = request.get_json()
    current_user = get_jwt_identity()

    if not data:
        return response_error("No data was provided", 400)

    if request.method == 'PATCH':
        try:
            created_by = current_user
            new_url = data['url']
        except KeyError as e:
            return response_error(
                "{} field is required".format(e.args[0]), 400
            )

    upload = UploadImage(created_by, new_url)

    upload.updateimage()
 
    msg = "Profile image was updated successfully"

    return jsonify({
        "message": msg,
        "status": 200
    })