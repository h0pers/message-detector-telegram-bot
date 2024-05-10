from sqlalchemy import String, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy_utils import URLType

from bot.database.main import Base


class Settings(Base):
    __tablename__ = 'settings'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, )
    auto_answer_text: Mapped[str] = mapped_column(String(4096), nullable=True)
    is_auto_answer_enable: Mapped[bool] = mapped_column(Boolean(), default=False)
    notification_chat_id = mapped_column(BigInteger(), nullable=True)

    @validates('id')
    def validate_id(self, key, value):
        if self.id > 1:
            raise ValueError("Settings has already set. Update him or create new.")

        return value


class ObservingChannels(Base):
    __tablename__ = 'observing_channels'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    invite_link = mapped_column(URLType(), unique=True)
    invite_link_validator = 'https://t.me/'

    @validates('invite_link')
    def validate_invite_link(self, key, value):
        if self.invite_link_validator not in value:
            raise ValueError("Invalid invite link. The url have to start with https://t.me/")

        return value


class TriggerWordsList(Base):
    __tablename__ = 'trigger_words'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String(), unique=True)

    @validates('word')
    def validate_word(self, key, value):
        if ' ' in value:
            raise ValueError("The attached string is not a word. Please make sure you have written word without space.")

        return value


class UsersBlacklist(Base):
    __tablename__ = 'black_list'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger(), nullable=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
