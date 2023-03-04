from routine import RoutineController
from scrape import ScreenshotWebsite
from dotenv import load_dotenv
import os

load_dotenv()

controller = RoutineController()
'''
04/02/2023 @ jd
Things to do

1. Add the conclusion timestamp for each proposal and check after the proposal ends. Create a class called Mission and it only checks once and then deletes itself
2. Maybe create Json file to store ?
3. Add code to automatically find new DAO on screenshot. Dynamically adds

'''

screenshot_governance_page = [('Stargate DAO' ,'https://snapshot.org/#/stgdao.eth'),('Arbitrum Odyssey', 'https://snapshot.org/#/arbitrum-odyssey.eth'), ('Trader Joe','https://snapshot.org/#/joegovernance.eth')]

screenshot_governance_scrape = []

for each_governance_page in screenshot_governance_page:
    print(each_governance_page)
    scrape_screenshot_website = ScreenshotWebsite(
        _name= each_governance_page[0],
        _url=each_governance_page[1],
        _chromedriver_path=os.getenv('DRIVER_PATH')
    )
    screenshot_governance_scrape.append(scrape_screenshot_website)

    controller.add_routine_task(
        scrape_screenshot_website.check_for_new_post, 5)


controller.add_routine_task(lambda: print('hello1'), 1)
controller.add_routine_task(lambda: print('hello1'), 2)

controller.run_controller()
