from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
import logging
import socket
from datetime import datetime
from time import strftime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Hello World!')

def help(bot, update):
	update.message.reply_text('Hi! Use /set <seconds> to set a timer')

def alarm(bot, job):
    bot.send_message(job.context, text='Beep!')

def seta(bot, update, args, job_queue, chat_data):
    """Adds a job to the queue"""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue
        job = job_queue.run_once(alarm, due, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')

def unset(bot, update, chat_data):
    """Removes the job if the user changed their mind"""

    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Timer successfully unset!')

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def echo(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def whatsmyip(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text='My ip address is: %s' % (socket.gethostbyname(socket.gethostname())))

def time(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="The time now is: %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

def unknown(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


def main():
	updater = Updater('445125368:AAGe1O1gtiDAy1NHjfpwAoyLHYZ56ORb-pw')

	dp = updater.dispatcher

	dp.add_handler(CommandHandler('start', start))
	dp.add_handler(CommandHandler('help', help))
	dp.add_handler(CommandHandler('hello', hello))
	dp.add_handler(CommandHandler('whatsmyip', whatsmyip))
	dp.add_handler(CommandHandler('time', time))
	dp.add_handler(MessageHandler(Filters.text, echo))
	dp.add_handler(CommandHandler("set", seta,
	                                  pass_args=True,
	                                  pass_job_queue=True,
	                                  pass_chat_data=True))
	dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))

	dp.add_error_handler(error)
	dp.add_handler(MessageHandler(Filters.command, unknown))
	

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
    main()