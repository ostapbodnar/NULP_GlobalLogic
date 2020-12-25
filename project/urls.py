from flask import request, jsonify
from marshmallow.utils import EXCLUDE
from .models import Advertisement, PlaceSchema, Place, User, AdvertisementSchema, UserSchema, Tag, Status
from project import session, app, bcrypt, auth


def get_or_404(cls, pk):
    obj = session.query(cls).get(pk)
    if obj is None:
        raise Exception
    return obj


@auth.verify_password
def verify_password(email, password):
    user = session.query(User).filter(User.email == email).first()
    if user is None:
        return False
    return bcrypt.check_password_hash(user.password, password)
    # return jsonify({'message': "Invalid user login"}), 400


# advertisement roures


@app.route("/advertisement", methods=['POST'])
@auth.login_required()
def advertisement_add():
    data = request.get_json()

    try:
        advertisement = AdvertisementSchema(
            partial=("name", "description", "quantity", "status", "tag")).load(data, unknown=EXCLUDE)

        advertisement.owner = get_or_404(User, int(data['owner_id']))
    except Exception:
        return jsonify({'message': "Invalid ID supplied"}), 400

    try:
        session.add(advertisement)
        session.commit()
    except Exception:
        return jsonify({'message': "Commitment to db was fieled"}), 405

    return jsonify({'message': "Success"}), 200


@app.route("/advertisement/<int:pk>", methods=['GET'])
@auth.login_required()
def get_advertisement(pk):
    email = auth.current_user()
    user = session.query(User).filter(User.email == email).first()
    user_id = user.id
    try:
        pk = int(pk)
    except ValueError:
        return jsonify({'message': "Invalid ID supplied"}), 400

    try:
        advertisement = session.query(Advertisement).get(pk)
        if advertisement.owner_id != user_id:
            raise Exception
    except Exception:
        return jsonify({'message': "Advertisement not found"}), 404

    return AdvertisementSchema().dump(advertisement)


@app.route("/advertisement/<int:pk>", methods=['PUT'])
@auth.login_required()
def update_advertisement(pk):
    email = auth.current_user()
    user = session.query(User).filter(User.email == email).first()
    user_id = user.id
    data = request.get_json()
    try:
        pk = int(pk)
    except ValueError:
        return "Invalid ID supplied", 400

    try:
        advertisement = session.query(Advertisement).get(pk)
        if advertisement.owner_id != user_id:
            raise Exception
    except Exception:
        return jsonify({'message': "Advertisement not found"}), 404

    session.query(Advertisement).filter(Advertisement.id == pk).update(data)
    session.commit()

    return jsonify({'message': "Success"}), 200


@app.route("/advertisement/<int:pk>", methods=['DELETE'])
@auth.login_required()
def delete_advertisement(pk):
    email = auth.current_user()
    user = session.query(User).filter(User.email == email).first()
    user_id = user.id
    try:
        pk = int(pk)
    except ValueError:
        return "Invalid ID supplied", 400

    try:
        advertisement = session.query(Advertisement).get(pk)
        if advertisement.owner_id != user_id:
            raise Exception
    except Exception:
        return jsonify({'message': "Advertisement not found"}), 404

    session.delete(advertisement)
    session.commit()
    return jsonify({'message': "Success"}), 200


# board


@app.route("/board", methods=["GET"])
def board():
    global_advetrisement = session.query(Advertisement).filter(
        Advertisement.tag == Tag.Global.name).order_by(Advertisement.createdate.desc()).all()

    return jsonify(AdvertisementSchema(many=True).dump(global_advetrisement))


@app.route("/board/place/", methods=["GET"])
@auth.login_required()
def board_place():
    email = auth.current_user()
    user = session.query(User).filter(User.email == email).first()
    pk = user.place_id

    local_advetrisement = session.query(Advertisement) \
        .filter(Advertisement.tag == Tag.Local.name) \
        .filter(Advertisement.owner.has(place_id=pk)) \
        .order_by(Advertisement.createdate.desc())

    return jsonify(AdvertisementSchema(many=True).dump(local_advetrisement))


@app.route("/place", methods=['POST'])
def place_add():
    data = request.get_json()
    try:
        place = PlaceSchema(partial=True).load(data, unknown=EXCLUDE)
    except Exception:
        return jsonify({'message': "Invalid input"}), 405

    try:
        session.add(place)
        session.commit()
    except Exception:
        return jsonify({'message': "Commitment to db was fieled"}), 405

    return jsonify({'message': "Success"}), 200


@app.route("/place/<int:pk>", methods=["GET"])
def place_get(pk):
    try:
        place = get_or_404(Place, pk)
    except Exception:
        return jsonify({'message': "Place not found"}), 404

    return jsonify(PlaceSchema().dump(place))


@app.route("/place", methods=["GET"])
def place_get_all():
    places = session.query(Place).all()

    return jsonify(PlaceSchema(many=True).dump(places))


@app.route("/place/<int:pk>", methods=['PUT'])
def place_update(pk):
    data = request.get_json()
    try:
        pk = int(pk)
    except ValueError:
        return "Invalid ID supplied", 400

    try:
        place = get_or_404(Advertisement, pk)
    except Exception:
        return jsonify({'message': "Advertisement not found"}), 404

    session.query(Place).filter(Place.id == pk).update(data)
    session.commit()

    return jsonify({'message': "Success"}), 200


@app.route("/place/<int:pk>", methods=['DELETE'])
def place_delete(pk):
    try:
        pk = int(pk)
    except ValueError:
        return "Invalid ID supplied", 400

    try:
        place = get_or_404(Place, pk)
    except Exception:
        return jsonify({'message': "Place not found"}), 404

    session.delete(place)
    session.commit()
    return jsonify({'message': "Success"}), 200


# user


@app.route("/user", methods=["POST"])
def user_add():
    data = request.get_json()
    try:
        data['password'] = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
        user = UserSchema(partial=True).load(data, unknown=EXCLUDE)
        user.place = get_or_404(Place, int(data['place_id']))
    except Exception:
        return jsonify({'message': "Invalid input"}), 405

    try:
        session.add(user)
        session.commit()
    except Exception:
        return jsonify({'message': "Commitment to db was fieled"}), 405

    return jsonify({'message': "Success"}), 200


@app.route("/user/login", methods=["POST"])
def user_login():
    data = request.get_json()
    try:
        email = data['email']
        password = str(data['password'])
    except Exception:
        return jsonify({'message': "Invalid input"}), 405

    user = session.query(User).filter(User.email == email).first()
    login_success = bcrypt.check_password_hash(user.password, password)
    if login_success:
        return jsonify({'username': email, 'password': password}), 200
    return jsonify({'message': 'Bad login!'}), 400


@app.route("/user/logout", methods=["GET"])
@auth.login_required()
def user_logout():
    return jsonify({'message': "Success"}), 200


@app.route("/user/", methods=['GET'])
@auth.login_required()
def get_user():
    email = auth.current_user()
    user = session.query(User).filter(User.email == email).first()
    pk = user.id
    try:
        pk = int(pk)
    except ValueError:
        return jsonify({'message': "Invalid ID supplied"}), 400

    try:
        user = get_or_404(User, pk)
    except Exception:
        return jsonify({'message': "Advertisement not found"}), 404

    return UserSchema().dump(user)


@app.route("/user/", methods=['PUT'])
@auth.login_required
def update_user():
    email = auth.current_user()
    user = session.query(User).filter(User.email == email).first()
    pk = user.id
    data = request.get_json()
    if "password" in data:
        data["password"] = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
    try:
        pk = int(pk)
    except ValueError:
        return "Invalid ID supplied", 400

    try:
        session.query(User).filter(
            User.id == pk).update(data)
        session.commit()

    except Exception:
        return jsonify({'message': "User not found"}), 404

    return jsonify({'message': "Success"}), 200


@app.route("/user/", methods=['DELETE'])
@auth.login_required()
def delete_user():
    email = auth.current_user()
    user = session.query(User).filter(User.email == email).first()
    pk = user.id
    try:
        pk = int(pk)
    except ValueError:
        return "Invalid ID supplied", 400

    try:
        user = get_or_404(User, pk)
    except Exception:
        return jsonify({'message': "User not found"}), 404

    session.delete(user)
    session.commit()
    return jsonify({'message': "Success"}), 200
