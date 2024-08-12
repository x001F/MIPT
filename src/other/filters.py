from aiogram.filters import BaseFilter
from aiogram.types import Message
from src.other.db import admin_check, instructor_check, student_check, random_check, block_check


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await admin_check(message.from_user.id)


class IsInstructor(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await instructor_check(message.from_user.id)


class IsStuff(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await instructor_check(message.from_user.id) or await admin_check(message.from_user.id)


class IsStudent(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await student_check(message.from_user.id)


class IsNotRandom(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await random_check(message.from_user.id)


class IsNotBlocked(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await block_check(message.from_user.id)
