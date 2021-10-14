"""State File Handle."""
from typing import cast

from datetime import datetime

import pytz

from TEx.models.database.temp_db_models import StateFileOrmEntity
from TEx.database import temp_session


class StateFileHandler:
    """State File Handler."""

    @staticmethod
    def file_exist(path: str) -> bool:
        """
        Return if a File Exists.

        :param path: File Path
        :return:
        """
        return bool(temp_session.query(StateFileOrmEntity).filter_by(path=path).count() > 0)

    @staticmethod
    def read_file_text(path: str) -> str:
        """Read All File Content.

        :param path: File Path
        :return: File Content
        """
        entity: StateFileOrmEntity = cast(StateFileOrmEntity, temp_session.query(StateFileOrmEntity).filter_by(path=path).first())
        return str(entity.data)

    @staticmethod
    def write_file_text(path: str, content: str) -> None:
        """Write Text Content into File.

        :param path: File Path
        :param content: File Content
        :param validate_seconds: File Validation in Seconds
        :return: None
        """
        # Delete if Exists
        temp_session.execute(
            StateFileOrmEntity.__table__.delete().where(StateFileOrmEntity.path == path)
            )

        entity: StateFileOrmEntity = StateFileOrmEntity(
            path=path,
            data=content,
            created_at=int(datetime.now(tz=pytz.UTC).timestamp())
            )
        temp_session.add(entity)

        # Execute
        temp_session.flush()
        temp_session.commit()