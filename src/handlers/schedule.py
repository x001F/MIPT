from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from src.config.get_logger import *

logger = get_logger('main.handlers')
schedule_router = Router()

import datetime
from aiogram.types import Chat, User, UsersShared, Contact

Message(message_id=156,
        date=datetime.datetime(2024, 8, 5, 10, 21, 50),
        chat=Chat(id=6568348462,
                  type='private', title=None, username='xfoqw', first_name='ᅠ ᅠ'),
        message_thread_id=None,
        from_user=User(id=6568348462, is_bot=False, first_name='ᅠ ᅠ', last_name=None, username='xfoqw',
                       language_code='en', is_premium=None, added_to_attachment_menu=None, can_join_groups=None,
                       can_read_all_group_messages=None, supports_inline_queries=None), sender_chat=None,
        sender_boost_count=None, forward_origin=None, is_topic_message=None, is_automatic_forward=None,
        reply_to_message=None, external_reply=None, quote=None, reply_to_story=None, via_bot=None, edit_date=None,
        has_protected_content=None, media_group_id=None, author_signature=None, text=None, entities=None,
        link_preview_options=None, animation=None, audio=None, document=None, photo=None, sticker=None, story=None,
        video=None, video_note=None, voice=None, caption=None, caption_entities=None, has_media_spoiler=None,
        contact=None, dice=None, game=None, poll=None, venue=None, location=None, new_chat_members=None,
        left_chat_member=None, new_chat_title=None, new_chat_photo=None, delete_chat_photo=None,
        group_chat_created=None, supergroup_chat_created=None, channel_chat_created=None,
        message_auto_delete_timer_changed=None, migrate_to_chat_id=None, migrate_from_chat_id=None, pinned_message=None,
        invoice=None, successful_payment=None, users_shared=UsersShared(request_id=1, user_ids=[5317896824, 6568348462],
                                                                        users=[{'user_id': 5317896824},
                                                                               {'user_id': 6568348462}]),
        chat_shared=None, connected_website=None, write_access_allowed=None, passport_data=None,
        proximity_alert_triggered=None, boost_added=None, forum_topic_created=None, forum_topic_edited=None,
        forum_topic_closed=None, forum_topic_reopened=None, general_forum_topic_hidden=None,
        general_forum_topic_unhidden=None, giveaway_created=None, giveaway=None, giveaway_winners=None,
        giveaway_completed=None, video_chat_scheduled=None, video_chat_started=None, video_chat_ended=None,
        video_chat_participants_invited=None, web_app_data=None, reply_markup=None, forward_date=None,
        forward_from=None, forward_from_chat=None, forward_from_message_id=None, forward_sender_name=None,
        forward_signature=None, user_shared=None)


class ContentType:
    """
    This object represents a type of content in message
    """

    TEXT = "text"
    ANIMATION = "animation"
    AUDIO = "audio"
    DOCUMENT = "document"
    PHOTO = "photo"
    STICKER = "sticker"
    VIDEO = "video"
    VIDEO_NOTE = "video_note"
    VOICE = "voice"
    HAS_MEDIA_SPOILER = "has_media_spoiler"
    CONTACT = "contact"
    DICE = "dice"
    GAME = "game"
    POLL = "poll"
    VENUE = "venue"
    LOCATION = "location"
    SUCCESSFUL_PAYMENT = "successful_payment"
    USERS_SHARED = "users_shared"
    CHAT_SHARED = "chat_shared"
    PASSPORT_DATA = "passport_data"
    USER_SHARED = "user_shared"


Message(message_id=293, date=datetime.datetime(2024, 8, 6, 8, 36, 46),
        chat=Chat(id=6568348462, type='private', title=None, username='xfoqw', first_name='ᅠ ᅠ', last_name=None,
                  from_user=User(id=6568348462, is_bot=False, first_name='ᅠ ᅠ', last_name=None, username='xfoqw',
                                 contact=Contact(phone_number='79954415449', first_name='паша к', last_name=None,
                                                 user_id=None, vcard=None))))

Message(message_id=296, date=datetime.datetime(2024, 8, 6, 8, 40, 29),
        chat=Chat(id=6568348462, type='private', title=None, username='xfoqw', first_name='ᅠ ᅠ', last_name=None),
        from_user=User(id=6568348462, is_bot=False, first_name='ᅠ ᅠ', last_name=None, username='xfoqw',
                       reply_to_message=Message(message_id=295, date=datetime.datetime(2024, 8, 6, 8, 40, 24),
                                                chat=Chat(id=6568348462, type='private', title=None, username='xfoqw',
                                                          first_name='ᅠ ᅠ', last_name=None),
                                                from_user=User(id=6857583661, is_bot=True, first_name='МФТИ',
                                                               last_name=None,
                                                               username='mipt_announce_bot'), user_shared=None),
                       contact=Contact(phone_number='+79019933462', first_name='ᅠ ᅠ', last_name=None,
                                       user_id=6568348462, vcard=None))
        )

Message(message_id=297, date=datetime.datetime(2024, 8, 6, 8, 42, 13),
        chat=Chat(id=6568348462, type='private', title=None, username='xfoqw', first_name='ᅠ ᅠ', last_name=None),
        from_user=User(id=6568348462, is_bot=False, first_name='ᅠ ᅠ', last_name=None, username='xfoqw'),
        contact=Contact(phone_number='+79805328788', first_name='разливной рай', last_name=None, user_id=1288906307,
                        vcard='BEGIN:VCARD \nVERSION:3.0 \nPRODID:-//Apple Inc.//iPhone OS 18.0//EN \nN:;разливной '
                              'рай;;; \nFN:разливной рай \nTEL;type=CELL;type=VOICE;type=pref:+7 980 532-87-88 '
                              '\nEND:VCARD \n'))
