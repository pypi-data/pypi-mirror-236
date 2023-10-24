from typing import Optional, Type

from pydantic import BaseModel

from langup import api, base, config
from langup.base import MQ
from langup.utils import vid_transform
from langup.utils.thread import start_thread


class SessionSchema(BaseModel):
    user_nickname: str
    source_content: str
    uri: str
    source_id: int
    bvid: str
    aid: int
    at_time: int


class SessionAtListener(base.Listener):
    listener_sleep: int = 60 * 2
    newest_at_time: int = 0
    Schema: Type[SessionSchema] = SessionSchema

    async def _alisten(self):
        sessions = await api.bilibili.session.get_at(config.credential)
        items = sessions['items']
        schema_list = []
        for item in items[::-1]:
            at_type = item['item']['type']
            if at_type != 'reply':
                continue
            at_time = item['at_time']
            if at_time <= self.newest_at_time:
                continue
            user_nickname = item['user']['nickname']
            source_content = item['item']['source_content']
            uri = item['item']['uri']
            source_id = item['item']['source_id']
            bvid = "BV" + uri.split("BV")[1]
            aid = vid_transform.note_query_2_aid(uri)
            self.newest_at_time = at_time
            schema_list.append(self.Schema(
                user_nickname=user_nickname,
                source_content=source_content,
                uri=uri,
                source_id=source_id,
                bvid=bvid,
                aid=aid,
                at_time=at_time,
            ))
        return schema_list


class LiveListener(base.Listener):
    room_id: int
    max_size: int = 20
    Schema: dict = {}  # text type ...
    live_mq: Optional[MQ] = None

    def init(self, mq, listener_sleep=None):
        self.live_mq = base.SimpleMQ(maxsize=self.max_size)
        room = api.bilibili.live.BlLiveRoom(self.room_id, self.live_mq, config.credential)
        t = start_thread(room.connect)
        super().init(mq, listener_sleep)

    async def _alisten(self) -> dict:
        return self.live_mq.recv()

