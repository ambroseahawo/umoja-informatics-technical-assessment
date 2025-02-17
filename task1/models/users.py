from extensions import db, pwd_context
from sqlalchemy import CheckConstraint, Column
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, validates


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, nullable=False)
    _password = Column("password", db.String(255), nullable=False)

    # Check constraint to ensure fields are not empty
    __table_args__ = (
        CheckConstraint("char_length(name) > 0", name="check_name_not_empty"),
        CheckConstraint("char_length(email) > 0", name="check_email_not_empty"),
        CheckConstraint("char_length(role) > 0", name="check_role_not_empty"),
        CheckConstraint("char_length(password) > 0", name="check_password_not_empty"),
    )

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    @validates("name", "email", "role", "_password")
    def validate_non_empty(self, key, value):
        if not value or not value.strip():
            raise ValueError(f"{key} cannot be empty")
        return value

    # Define the relationship with TokenBlocklist and apply cascade
    token_blocklists = relationship("TokenBlocklist", back_populates="user", cascade="all, delete-orphan")
