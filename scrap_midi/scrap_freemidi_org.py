import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

if len(sys.argv) != 3:
    print("Usage ./scrap_freemidi_org.py <genre> <Headless State 1/0>")
    sys.exit(1)

CHROMEDRIVER_PATH = './scrap_midi/chromedriver'
HEADLESS = int(sys.argv[2])
WINDOW_SIZE = "1920,1080"
DEBUG = True  # Debug mode

# Make sure the paths for the chromedriver and chrome is correct
if sys.platform == "linux" or sys.platform == "linux2":
    # linux
    CHROME_PATH = '/usr/bin/google-chrome'
elif sys.platform == "darwin":
    # OSX
    CHROME_PATH = (
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
elif sys.platform == "win32":
    # Windows
    CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Check for HEADLESS state for the chrome driver
# and add window and executable options for chrome
chrome_options = Options()
if HEADLESS:
    chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH
# Initiate the webdriver
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                          options=chrome_options)


def find_artists(genre):
    # Value Hardcoded as the entire script will be specific to freemidi.org
    driver.get("https://freemidi.org/genre-" + genre)
    print(f"driver.title = {driver.title}") if (DEBUG) else print('', end='')

    # div containing artists
    mainContent = driver.find_element_by_xpath("//div[@id='mainContent']")
    # List of artists
    mainContentList = mainContent.find_elements_by_xpath(".//div/a[2]")

    # making sure element not found erros are ignored
    # any errors will be logged in the error_log file
    os.makedirs("logs", exist_ok=True)
    with open('./logs/error_log', 'a') as elog:
        try:
            artist_link_count = len(mainContentList)
            for list_index in range(artist_link_count):
                # div containing artists
                mainContent = driver.find_element_by_xpath(
                    "//div[@id='mainContent']")
                # goto artist page
                mainContent.find_elements_by_xpath(
                    ".//div/a[2]")[list_index].click()

                # div containing artist songs
                mainContentSong = driver.find_element_by_xpath(
                    "//div[@id='mainContent']")
                songContentList = mainContentSong.find_elements_by_xpath(
                    ".//div[1]/div[@class='artist-container']/div[1]/div/div[@class='artist-song-cell']/span/a")

                song_link_count = len(songContentList)
                for song_list_index in range(song_link_count):
                    # div containing artist songs
                    mainContentSong = driver.find_element_by_xpath(
                        "//div[@id='mainContent']")
                    # goto song download page
                    song_download_link = mainContentSong.find_elements_by_xpath(".//div[1]/div[@class='artist-container']/div[1]/div/div[@class='artist-song-cell']")[song_list_index]
                    song_download_link = song_download_link.find_element_by_xpath(".//span/a")

                    # goto download page
                    song_download_link.click()

                    midi_download_link = driver.find_element_by_id('downloadmidi').click()
                    time.sleep(2)

                    driver.back()
                driver.back()
        except Exception as ex:
            template = time.time() + "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            elog.write((message + '\n'))

def main():
    # Get the music genre
    genre = sys.argv[1]

    find_artists(genre)
    driver.close()


if __name__ == "__main__":
    main()
