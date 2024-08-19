from aiogram.filters import BaseFilter
from aiogram.types import Message
from src.other.db import staff_check, student_check


class IsStaff(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await staff_check(message.from_user.id)


class IsStudent(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await student_check(message.from_user.id)


class IsRandom(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await student_check(message.from_user.id) or await staff_check(message.from_user.id)
