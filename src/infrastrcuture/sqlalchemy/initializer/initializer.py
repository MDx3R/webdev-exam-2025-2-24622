from sqlalchemy.orm import Session

from .role_seeder import seed_roles


def initialize_data(session: Session):
    seed_roles(session)
