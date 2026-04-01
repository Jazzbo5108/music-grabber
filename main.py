from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from webdriver_manager.chrome import ChromeDriverManager

if (len(sys.argv) < 3) or (sys.argv[1] == "--help"):
	print("Usage: python3 main.py artist title1 [title2 ...]")
	quit()

class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.query = (artist + " " + title).replace(" ", "+")

download_dir = "/home/james/Music/Auto-download/"
artist = sys.argv[1]

song_count = len(sys.argv) - 2
songs = []
for song_title in sys.argv:
    songs.insert(0, Song(song_title, artist))
del songs[song_count]
del songs[song_count]

options = webdriver.ChromeOptions()
prefs = {}
prefs["download.default_directory"]=download_dir
prefs["profile.default_content_settings.popups"]=0
options.add_experimental_option("prefs", prefs)
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

current_song = 0
for song in songs:
    current_song += 1

    #Get song link
    driver.get("https://www.youtube.com/results?search_query=" + song.query)

    links = driver.find_elements("xpath", "//a[@href]")
    for link in links:
        song_url = link.get_attribute("href")
        if ("watch" in song_url) and ("start_radio" in song_url):
            break
    
    if song_url == "https://www.youtube.com/" or len(song_url) > 400:
        print("Failed on song \'" + song.title + "\'")
        if len(songs) > (song_count + 8):
            print("Exceeded max retry count. Will not retry.")
        else:
            print("Will retry.")
            songs.append(song)
        continue
    else:
        print(song.title + " by " + song.artist + " found at " + song_url)

    #Download mp3
    driver.get("https://ytmp3.ai/")

    url_field = driver.find_element("id", "v")
    url_field.clear()
    url_field.send_keys(song_url)

    buttons = driver.find_elements("xpath", "//button")
    for btn in buttons:
        if "Convert" in btn.get_attribute("innerHTML"):
            btn.click()
            break

    wait = WebDriverWait(driver, 180)
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()=\"Download\"]")))

    buttons = driver.find_elements("xpath", "//button")
    for btn in buttons:
        if "Download" in btn.get_attribute("innerHTML"):
            btn.click()
            break
    
    print("Song completed, " + str(len(songs) - current_song) + " songs remaining.")
