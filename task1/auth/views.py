from auth.helpers import add_token_to_database, is_token_revoked, revoke_token
from auth.schemas import UserCreateSchema, UserSchema, UserUpdateSchema
from extensions import db, jwt, pwd_context
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from marshmallow.exceptions import ValidationError
from models import User

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")
users_blueprint = Blueprint("users", __name__, url_prefix="/users")


@auth_blueprint.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    schema = UserCreateSchema()
    user = schema.load(request.json)
    db.session.add(user)
    db.session.commit()

    schema = UserSchema()

    return {"msg": "User created", "user": schema.dump(user)}


@auth_blueprint.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get("email")
    password = request.json.get("password")
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    if user is None or not pwd_context.verify(password, user.password):
        return jsonify({"msg": "Bad credentials"}), 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token_to_database(access_token)
    add_token_to_database(refresh_token)

    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200


@users_blueprint.route("/<uuid:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    """Fetches details of a specific user by ID."""
    current_user_id = get_jwt_identity()
    print(str(id) == str(current_user_id))

    # Check if the user trying to access the data is authorized
    if str(current_user_id) != str(id):
        return jsonify({"error": "Unauthorized to view this user's details"}), 403

    user = User.query.get(str(id))

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": UserSchema().dump(user)}), 200


@users_blueprint.route("/<uuid:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    current_user_id = get_jwt_identity()

    # Check if the user trying to update the data is authorized
    if str(current_user_id) != str(id):
        return jsonify({"error": "Unauthorized to update this user's details"}), 403

    user = User.query.get(str(id))

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    try:
        schema = UserUpdateSchema()
        data = schema.load(request.json)  # Validate input

        # Update user fields
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
        if "role" in data:
            user.role = data["role"]
        if "password" in data:
            user.password = pwd_context.hash(data["password"])  # Hash new password

        db.session.commit()

        return jsonify({"msg": "User updated successfully", "user": UserSchema().dump(user)}), 200

    except ValidationError as err:
        return jsonify({"error": "Validation Error", "message": err.messages}), 400


@users_blueprint.route("/<uuid:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    current_user_id = get_jwt_identity()

    # Check if the user trying to delete the data is authorized
    if str(current_user_id) != str(id):
        return jsonify({"error": "Unauthorized to delete this user's account"}), 403

    user = User.query.get(str(id))

    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Error occurred: {str(e)}"}), 500


# jwt auth


@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    add_token_to_database(access_token)
    return jsonify({"access_token": access_token}), 200


@auth_blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@auth_blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@jwt.user_lookup_loader
def user_loader_callback(jwt_headers, jwt_payload):
    identity = jwt_payload[current_app.config["JWT_IDENTITY_CLAIM"]]
    return User.query.get(identity)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    return is_token_revoked(jwt_payload)
