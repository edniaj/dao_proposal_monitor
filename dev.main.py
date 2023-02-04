from routine import RoutineController
from scrape import ScreenshotWebsite

controller = RoutineController()
'''
Things to do

1. Add the conclusion timestamp for each proposal and check after the proposal ends. Create a class called Mission and it only checks once and then deletes itself
2. Maybe create Json file to store

'''

# screenshot_governance_page = ['https://demo.snapshot.org/#/karate-combat-stage.eth','https://demo.snapshot.org/#/yojacobtest.eth', 'https://demo.snapshot.org/#/dumbo.eth']


dumbo_governance = ScreenshotWebsite(_url='https://demo.snapshot.org/#/dumbo.eth', _chromedriver_path='C:\path\chromedriver_win32\chromedriver.exe')

controller.add_routine_task( lambda:print('hello1'), 1)
controller.add_routine_task( dumbo_governance.check_for_new_post, 5)

controller.run_controller()