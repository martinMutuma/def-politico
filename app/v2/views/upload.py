from flask import request, jsonify
from app.v2.models.upload_model import UploadImage
from app.blueprints import v2
from app.v2.utils.validator import response_error
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
        created_by = current_user
        new_url = data['url']
        if not new_url:
            return response_error(
                "{} field is required".format('url'), 400
            )

    upload = UploadImage(created_by, new_url)

    upload.updateimage()
    msg = "Profile image was updated successfully"
    return jsonify({
        "message": msg,
        "status": 200
    })
