import logging
import time
import datetime
from .config import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserBannedInChannel, UserNotParticipant, MessageNotModified
from .database import *

logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

GB_USERS = []


async def premium_check(c, m):
	user_id = m.from_user.id
	mention = m.from_user.mention
	user_name = m.from_user.username
	if not await db.is_user_exist(m.from_user.id):
		await db.add_user(m.from_user.id)
	if PAID_BOT.upper() == "YES":
		try:
			paid_status = await db.get_paid_status(user_id)
		except:
			await m.reply_text(text="⚠️ First Click on /start, Then try again")
			return False
		if paid_status["is_paid"]:
			current_date = datetime.datetime.now()
			paid_duration = paid_status["paid_duration"]
			paid_on = paid_status["paid_on"]
			paid_reason = paid_status["paid_reason"]
			integer_paid_duration = int(paid_duration)
			will_expire = paid_on + datetime.timedelta(days=integer_paid_duration)
			if will_expire < current_date:
				try:
					await db.remove_paid(user_id)
				except Exception as e:
					print(f"⚠️ Error: {e}")
				try:
					await c.send_message(m.chat.id, text=EXPIRE_TEXT.format(mention=mention, user_id=user_id, user_name=user_name, paid_duration=paid_duration, paid_on=paid_on, will_expire=will_expire), reply_markup=PAID_BUTTONS)
				except Exception as e:
					print(f"⚠️ Error: {e}")
				for i in AUTH_USERS:
					try:
						await c.send_message(i,text=f"🌟 **Plan Expired:** \n\n**User Id:** `{m.from_user.id}`\n\n**User Name:** @{m.from_user.username}\n\n**Plan Validity:** {paid_duration} plans\n\n**Joined On** : {paid_on}\n\n**Discription** : {paid_reason}")
					except Exception:
						pass
				return False
			else:
				pass
		else:
			await m.reply_text(text=f"{PAID_TEXT}",reply_markup=PAID_BUTTONS,disable_web_page_preview=True,quote=True)
			return False
