from routine import RoutineController
from scrape import ScreenshotWebsite

controller = RoutineController()
'''
04/04/2023 @ jd
Things to do

1. Add the conclusion timestamp for each proposal and check after the proposal ends. Create a class called Mission and it only checks once and then deletes itself
2. Maybe create Json file to store
3. Add code to automatically find new DAO on screenshot. Dynamically adds

'''

screenshot_governance_page = [('karate-combat-stage', 'https://demo.snapshot.org/#/karate-combat-stage.eth'),
                              ('revi', 'https://demo.snapshot.org/#/irrevi.eth'), ('dumbo', 'https://demo.snapshot.org/#/dumbo.eth')]



for each_governance_page in screenshot_governance_page:

    scrape_screenshot_website = ScreenshotWebsite(
        _name= each_governance_page[0],
        _url=each_governance_page[1],
        _chromedriver_path='C:\path\chromedriver_win32\chromedriver.exe')

    controller.add_routine_task(
        scrape_screenshot_website.check_for_new_post, 5)


controller.add_routine_task(lambda: print('hello1'), 1)
controller.add_routine_task(lambda: print('hello1'), 2)

controller.run_controller()
