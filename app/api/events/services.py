from app.api.events.models import EventUser
from app.api.events.dao import EventDAO
from app.api.users.dao import UserDAO


class EventService:
    @classmethod
    async def get_reward_by(cls, event_user: EventUser) -> dict:
        user = await UserDAO.find_one_or_none_by_id(event_user.user_id)
        event = await EventDAO.find_one_or_none_by_id(event_user.event_id)

        if user is None or event is None:
            raise ValueError("Incorrect ids")

        return {
            "reward": event.reward if event_user.attended else -(event.reward // 2),
            "event_name": event.name,
            "balance": user.balance,
        }
