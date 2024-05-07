from typing import List

from sqlalchemy import String, ForeignKey, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlalchemy_utils import URLType

from bot.database.main import Base


class ObservingChannels(Base):
    __tablename__ = 'observing_channels'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    invite_link = mapped_column(URLType(), unique=True)
    trigger_words: Mapped[List["TriggerWordsList"]] = relationship(back_populates='channel')
    auto_answer_text: Mapped[str] = mapped_column(String(4096), nullable=True)
    is_auto_answer_enable: Mapped[bool] = mapped_column(Boolean(), default=False)
    notification_chat_id = mapped_column(BigInteger(), nullable=True)
    banned_users: Mapped[List["UsersBlackList"]] = relationship(back_populates='channel')
    invite_link_validator = 'https://t.me/'

    @validates('invite_link')
    def validate_invite_link(self, key, value):
        if self.invite_link_validator not in value:
            raise ValueError("Invalid invite link. The url have to start with https://t.me/")

        return value


class TriggerWordsList(Base):
    __tablename__ = 'channel_trigger_words'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String())
    channel_id = mapped_column(ForeignKey("observing_channels.id"))
    channel = relationship("ObservingChannels", back_populates="trigger_words")

    @validates('word')
    def validate_word(self, key, value):
        if ' ' in value:
            raise ValueError("The attached string is not a word. Please make sure you have written word without space.")

        return value


class UsersBlackList(Base):
    __tablename__ = 'channel_user_black_list'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger())
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    channel_id = mapped_column(ForeignKey("observing_channels.id"))
    channel = relationship("ObservingChannels", back_populates="banned_users")
