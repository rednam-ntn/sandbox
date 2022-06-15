import logging
import test_log


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def record_word_count(myfile):
    logger.info("starting the function")
    try:
        word_count = test_log.word_count(myfile)
        with open('wordcountarchive.csv', 'a') as file:
            row = str(myfile) + ',' + str(word_count)
            file.write(row + '\n')
    except Exception as e:
        logger.warning(f"could not write file to destination with {e}")
    finally:
        logger.debug("the function is done for the file %s", myfile)


record_word_count("abc")
