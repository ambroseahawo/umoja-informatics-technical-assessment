from extensions import db


class TokenBlocklist(db.Model):
    id = db.Column(db.String(36), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    jti = db.Column(db.String(36), nullable=False, unique=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False, index=True)
    revoked_at = db.Column(db.DateTime)
    expires = db.Column(db.DateTime, nullable=False)

    # Relationship with User, cascade delete is defined in the User model
    user = db.relationship("User", back_populates="token_blocklists")
