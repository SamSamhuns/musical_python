import os
import sys
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Warning download does not currently work with HEADLESS MODE
if len(sys.argv) != 3:
    print("Usage: python scrap_freemidi_org.py <genre> <Headless State 1/0>")
    sys.exit(1)

CHROMEDRIVER_PATH = './scrap_midi/chromedriver'
HEADLESS = int(sys.argv[2])
WINDOW_SIZE = "800,600"
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
    CHROME_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

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
    # print(f"driver.title = {driver.title}") if (DEBUG) else print('', end='')

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
            list_index = 405
            while list_index < artist_link_count:
                time.sleep(0.4)
                # div containing artists
                try:
                    mainContent = driver.find_element_by_xpath(
                        "//div[@id='mainContent']")
                    artist_name = mainContent.find_elements_by_xpath(
                        ".//div/a[2]")[list_index].text
                except:
                    print(f"Artist list page index {list_index} out of range")
                    list_indexex += 1
                    continue
                # goto artist page
                mainContent.find_elements_by_xpath(
                    ".//div/a[2]")[list_index].click()

                # div containing artist songs
                mainContentSong = driver.find_element_by_xpath(
                    "//div[@id='mainContent']")
                songContentList = mainContentSong.find_elements_by_xpath(
                    ".//div[1]/div[@class='artist-container']/div[1]/div/div[@class='artist-song-cell']/span/a")

                song_link_count = len(songContentList)
                current_song_page = 2  # Due to the indexing of the elements, it starts with 2
                song_list_index = 0
                while song_list_index < song_link_count:
                    try:
                        # for song_list_index in range(initial_Start, song_link_count):
                        # div containing artist songs
                        mainContentSong = driver.find_element_by_xpath(
                            "//div[@id='mainContent']")
                        time.sleep(0.7)  # To make sure page has loaded
                        # goto song download page
                        song_download_link = mainContentSong.find_elements_by_xpath(
                            ".//div[1]/div[@class='artist-container']/div[1]/div/div[@class='artist-song-cell']")[song_list_index]
                    except:
                        print(f"Song List index {song_list_index} out of range on page title {driver.title}")
                        song_list_index += 1
                        continue
                    song_download_link = song_download_link.find_element_by_xpath(
                        ".//span/a")

                    with open('./logs/downloaded_songs.txt', 'a') as f:
                        log = "artist_list_index = " + str(list_index) + ", artist = " + \
                            str(artist_name) + ", song_list_index = " +\
                            str(song_list_index) + ', ' + \
                            song_download_link.text
                        print(log.encode("utf-8"), file=f)
                        print(log)

                    # goto download page
                    song_download_link.click()
                    time.sleep(0.4)
                    try:
                        midi_download_link_str = "//*[@id='downloadmidi']"
                        midi_download_link = ui.WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, midi_download_link_str)))

                    except:
                        print("Download link absent")
                        song_list_index += 1
                        driver.back()
                        continue
                    time.sleep(0.5)
                    midi_download_link.click()
                    song_list_index += 1

                    driver.back()  # Go back to song list page for artist

                    # If we are at the last song, check if another song page exists
                    if song_list_index == (song_link_count - 1):
                        page_lists = driver.find_elements_by_xpath(
                            "//div[@id='mainContent']/div[1]/div[2]/div[2]/nav/ul/li")
                        page_count = len(page_lists)
                        if page_count >= 4 and current_song_page < (page_count-1):  # if page_count == 3 then only one page exists
                            current_song_page += 1
                            next_page_string = "//div[@id='mainContent']/div[1]/div[2]/div[2]/nav/ul/li[" \
                                + str(current_song_page) + ']/a'
                            next_page = ui.WebDriverWait(driver, 50).until(
                                EC.element_to_be_clickable((By.XPATH, next_page_string)))

                            # go to the next page
                            next_page.click()
                            # div containing artist songs
                            mainContentSong = driver.find_element_by_xpath(
                                "//div[@id='mainContent']")
                            songContentList = mainContentSong.find_elements_by_xpath(
                                ".//div[1]/div[@class='artist-container']/div[1]/div/div[@class='artist-song-cell']/span/a")

                            song_link_count = len(songContentList)
                            song_list_index = 0

                driver.back()
                list_index += 1
        except Exception as ex:
            template = "Unix Time: " + \
                str(time.time()) + \
                ": An exception of type {0} occurred. Arguments:\n{1!r}"
            traceback.print_exc()
            message = template.format(type(ex).__name__, ex.args)
            elog.write((message + '\n'))



def main():
    # Get the music genre
    genre = sys.argv[1]

    find_artists(genre)
    driver.close()


if __name__ == "__main__":
    main()
