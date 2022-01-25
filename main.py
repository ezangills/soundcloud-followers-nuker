import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


def __scroll__(driver, times):
    html = driver.find_element(By.TAG_NAME, 'html')
    for i in range(times):
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)


def __scroll_up__(driver, times):
    html = driver.find_element(By.TAG_NAME, 'html')
    for i in range(times):
        html.send_keys(Keys.PAGE_UP)

# replace ${USERNAME} with ur username
# replace ${AUTH_COOKIE} with ur cookie


followers = set()
driver = webdriver.Chrome()
driver.get("https://soundcloud.com/${USERNAME}/followers")  # open followers page
driver.add_cookie({"name": "oauth_token", "value": "${AUTH_COOKIE}"})  # set cookie
time.sleep(5)  # wait for the page to load
ActionChains(driver).click(driver.find_element(By.ID, 'onetrust-accept-btn-handler')).perform()  # accept all cookies
driver.get("https://soundcloud.com/${USERNAME}/followers")  # reload page followers
__scroll__(driver, 100)  # scroll down 100 times to see all followers
names = driver.find_elements(By.CLASS_NAME, 'userBadgeListItem__heading')  # get all followers' names
for name in names:
    followers.add(name.get_attribute("textContent").strip())  # add all followers names to set trimmed
print('followers count: ', len(followers))


driver.get("https://soundcloud.com/${USERNAME}/following")  # open up following page
__scroll__(driver, 100)  # scroll down 100 times to see all followings
__scroll_up__(driver, 50)  # scroll up 50 times to get up on the page
followingBoxes = driver.find_elements(By.CLASS_NAME, 'badgeList__item')  # get all boxes that contain user's name and unfollow button
for box in followingBoxes:  # iterate thru all the boxes that contain user's name and unfollow button
    followingName = box.find_element(By.CLASS_NAME, 'userBadgeListItem__heading').get_attribute("textContent").strip()  # get that highlighted user's name trimmed
    if followingName in followers:
        print("Mutual: ", followingName)  # print if it's mutual
    if followingName not in followers:
        ActionChains(driver).move_to_element(box.find_element(By.CLASS_NAME, 'sc-button-follow')).perform()  # highlight unfollow button for that user
        time.sleep(0.2)
        ActionChains(driver).click(box.find_element(By.CLASS_NAME, 'sc-button-follow')).perform()  # click unfollow button for that user
        time.sleep(0.1)

