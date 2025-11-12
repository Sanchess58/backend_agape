from sqladmin import ModelView

from api.events.models import Event, EventUser


class EventAdmin(ModelView, model=Event):
    column_list = [Event.id, Event.name, Event.date_and_time, Event.location]


class EventUserAdmin(ModelView, model=EventUser):
    column_list = [EventUser.id, EventUser.user_id, EventUser.event_id, EventUser.attended]
