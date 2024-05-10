from bot.database.main import engine, Base, SessionLocal
from .user import User
from .channels import ObservingChannels, TriggerWordsList, UsersBlacklist, Settings
from ..methods.create import create_if_not_exist


async def register_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal.begin() as session:
        await create_if_not_exist(session, Settings, Settings, {}, id=1)
