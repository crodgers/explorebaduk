import pytest

from explorebaduk.database import UserModel, TokenModel


def test_token(db, user1, token1):
    token = db.query(TokenModel).filter_by(user_id=user1.user_id, token_id=token1.token_id).first()
    assert token.is_active


def test_expired_token(db, user1, token_expired):
    token = db.query(TokenModel).filter_by(user_id=user1.user_id, token_id=token_expired.token_id).first()
    assert not token.is_active
