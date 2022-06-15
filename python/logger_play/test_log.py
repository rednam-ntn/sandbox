import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')

# Create handlers
# c_handler = logging.StreamHandler()
# c_handler.setLevel(logging.DEBUG)
# c_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))

# f_handler = logging.FileHandler('file.log')
# f_handler.setLevel(logging.ERROR)
# f_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s'))

# Add handlers to the logger
logger = logging.getLogger(__name__)

# logger.addHandler(c_handler)
# logger.addHandler(f_handler)


def word_count(myfile):
    try:
        with open(myfile, 'r') as f:
            file_data = f.read()
            words = file_data.split(" ")
            final_word_count = len(words)
            logger.info("this file has %d words", final_word_count)
            return final_word_count
    except Exception as e:
        logger.error(e, exc_info=True)
