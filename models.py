# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy()
#
# class Contact(db.Model):
#     __tablename__ = 'contacts'  # Explicit table name
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), nullable=False, index=True)  # Indexed for faster lookups
#     message = db.Column(db.Text, nullable=True)
#     created_at = db.Column(
#         db.DateTime,
#         default=datetime.utcnow,
#         nullable=False,
#         index=True  # Index timestamp for ordering/queries
#     )
#
#     def __repr__(self):
#         return f"<Contact id={self.id} email={self.email}>"
