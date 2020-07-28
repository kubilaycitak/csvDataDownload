import os
import imaplib
from email import message_from_string as convert_string_to_email_message
import urllib.request
import logging
import uuid
import shutil

# Initializing Logger
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(funcName)s - %(message)s")
LOGGER = logging.getLogger(__name__)


class EmailManager:

    # Getting main information.
    def __init__(self):
        self.mail = imaplib.IMAP4_SSL(os.environ['host'], int(os.environ['port']))
        self.mail.login(os.environ['email_address'], os.environ['password'])

        self.mail.select(os.environ['mail_directory'])
        sender = os.environ['sender']
        subject_keyword = os.environ['subject_keyword']
        self.search_criteria = 'FROM "' + sender + '" HEADER Subject "' + subject_keyword + '" (UNSEEN)'

    # Getting the IDs of unread mails in the inbox.
    def __get_mail_id_list(self):
        LOGGER.info('Getting the IDs of unread mails.')
        id_list = self.mail.search(None, self.search_criteria)[1][0].decode().split(" ")
        if id_list == ['']:
            return []
        return id_list

    # Getting the download path and directing it with unread mail IDs.
    def download_attachments(self):
        LOGGER.info('Getting the download path and requesting unread mail IDs.')
        download_path = os.path.abspath(os.environ['download_path'])

        for mail_id in self.__get_mail_id_list():
            self.__download_attachments_from_mail_id(mail_id, download_path)

    # Obtaining details of the specified unread mails and directing those details.
    def __download_attachments_from_mail_id(self, mail_id, download_path):
        LOGGER.info('Getting details of the unread mail.')
        email = convert_string_to_email_message(self.mail.fetch(mail_id, '(RFC822)')[1][0][1].decode())

        try:
            # Directing an unread mail.
            LOGGER.info('Attempting to download the file from the mail.')
            self.__download_attachments_from_the_email_message(email, download_path)

            # After downloading the file, tagging the mail as "Seen".
            LOGGER.info('Tagging the mail as "read" and getting to the next unread mail if it exists.')
            self.mail.store(mail_id, '+FLAGS', '\\Seen')

        # Case of an error.
        except Exception as exp:
            LOGGER.info('An error occurred.')
            self.mail.store(mail_id, '-FLAGS', '\\Seen')
            raise exp

    # Downloading the file from the directed mail.
    def __download_attachments_from_the_email_message(self, email_message, download_path):

        # Splitting the mail string in order to get the link in the mail.
        message = email_message.as_string()
        LOGGER.info('Obtaining the link from the mail string.')
        firstSplit = message.split('<a href="')
        partialURL = firstSplit[1]
        finalSplit = partialURL.split('">CSV')
        mainURL = finalSplit[0]
        finalURL = mainURL.replace('amp;', '')

        # Saving the file, and moving it to the specified download path.
        LOGGER.info('Saving the file. (Please make sure download path does not include special characters.)')
        randomFilename = str(uuid.uuid4())
        filename = "CrowdtangleCSV_" + randomFilename + ".csv"
        urllib.request.urlretrieve(finalURL, filename)
        currentPath = os.path.dirname(__file__)
        shutil.move(currentPath + "\\" + filename, download_path + "\\" + filename)

        LOGGER.info('File is successfully downloaded.')
