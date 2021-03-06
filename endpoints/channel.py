from database import db_session
from models import Channel
from schemata import ChannelSchema
from utils import admin_only


# GET channels
def get_all():
    channels = Channel.query.order_by(Channel.id).all()
    data = ChannelSchema(many=True).dump(channels)

    return data, 200


# POST channels
@admin_only
def create(body, **kwargs):
    id = body.get('id')
    user_id = body.get('user_id')
    cohort_id = body.get('cohort_id')
    existing_channel_1 = Channel.query.filter_by(id=id).one_or_none()
    existing_channel_2 = Channel.query.filter_by(user_id=user_id)\
        .filter_by(cohort_id=cohort_id)\
        .one_or_none()

    if existing_channel_1 is None and existing_channel_2 is None:
        channel_schema = ChannelSchema()
        channel = channel_schema.load(body)
        db_session.add(channel)
        db_session.commit()
        data = channel_schema.dump(channel)

        return data, 201
    else:
        data = {
            'title': 'Conflict',
            'status': 409,
            'detail': 'Channel with posted details already exists'
        }

        return data, 409


# GET channels/<id>
def get_one(id):
    channel = Channel.query.filter_by(id=id).one_or_none()

    if channel is not None:
        data = ChannelSchema().dump(channel)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Channel {id} not found'
        }

        return data, 404


# PUT channels/<id>
@admin_only
def update(id, body, **kwargs):
    existing_channel = Channel.query.filter_by(id=id).one_or_none()

    if existing_channel is not None:
        channel_schema = ChannelSchema()
        channel = channel_schema.load(body)
        channel.id = existing_channel.id
        db_session.merge(channel)
        db_session.commit()
        data = channel_schema.dump(existing_channel)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Channel {id} not found'
        }

        return data, 404


# DELETE channels/<id>
@admin_only
def delete(id, **kwargs):
    channel = Channel.query.filter_by(id=id).one_or_none()

    if channel is not None:
        db_session.delete(channel)
        db_session.commit()
        data = {
            'title': 'OK',
            'status': 200,
            'detail': f'Channel {id} deleted'
        }

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Channel {id} not found'
        }

        return data, 404
