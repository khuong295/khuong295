# -*- coding: UTF-8 -*-

from fbchat import log, Client
from fbchat.models import *

# ID nhom chat (co dang: https://www.facebook.com/messages/t/447364562099098)
old_thread_id = '1760329423987984'

# Thay doi mot so noi dung duoi day neu ban thich

# Mau khung chat: https://fbchat.readthedocs.io/en/master/api.html#fbchat.models.ThreadColor
old_color = ThreadColor.MESSENGER_BLUE
# Emoji cua nhom chat
old_emoji = '😡'
# Ten nhom chat
old_title = 'Team chuyên Tùng'
# ID thanh vien (whitelist) va nickname trong nhom chat
old_nicknames = {
    '100003731211469': "Khương Lọ",
    '100011427606599': "Anh Sinh",
    '100004368789558': "Đỗ Nhân",
    '100009450979587': "Hoàng Tiến",
    '100013025464367': "Linh Chieg",
    '100004842373091': "Nguyễn Văn Thược",
    '100003763325666': "LỒN NGÔ SÀI LÙA ĐẢO",
    '100004653215957': "Tạ Văn Tấn"
}

class KeepBot(Client):
    def onColorChange(self, author_id, new_color, thread_id, thread_type, **kwargs):
        if old_thread_id == thread_id and old_color != new_color:
            log.info("{} changed the thread color. It will be changed back".format(author_id))
            self.changeThreadColor(old_color, thread_id=thread_id)

    def onEmojiChange(self, author_id, new_emoji, thread_id, thread_type, **kwargs):
        if old_thread_id == thread_id and new_emoji != old_emoji:
            log.info("{} changed the thread emoji. It will be changed back".format(author_id))
            self.changeThreadEmoji(old_emoji, thread_id=thread_id)

    def onPeopleAdded(self, added_ids, author_id, thread_id, **kwargs):
        if old_thread_id == thread_id and author_id != self.uid:
            log.info("{} got added. They will be removed".format(added_ids))
            for added_id in added_ids:
                self.removeUserFromGroup(added_id, thread_id=thread_id)

    def onPersonRemoved(self, removed_id, author_id, thread_id, **kwargs):
        # No point in trying to add ourself
        if old_thread_id == thread_id and removed_id != self.uid and author_id != self.uid:
            log.info("{} got removed. They will be re-added".format(removed_id))
            self.addUsersToGroup(removed_id, thread_id=thread_id)

    def onTitleChange(self, author_id, new_title, thread_id, thread_type, **kwargs):
        if old_thread_id == thread_id and old_title != new_title:
            log.info("{} changed the thread title. It will be changed back".format(author_id))
            self.changeThreadTitle(old_title, thread_id=thread_id, thread_type=thread_type)

    def onNicknameChange(self, author_id, changed_for, new_nickname, thread_id, thread_type, **kwargs):
        if old_thread_id == thread_id and changed_for in old_nicknames and old_nicknames[changed_for] != new_nickname:
            log.info("{} changed {}'s' nickname. It will be changed back".format(author_id, changed_for))
            self.changeNickname(old_nicknames[changed_for], changed_for, thread_id=thread_id, thread_type=thread_type)

client = KeepBot("khuong295", "khuongvip")
client.listen()
