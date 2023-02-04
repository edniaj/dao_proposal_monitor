import selenium

from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


'''
We are using json to store, not database

When proposal concludes, you need to routinely check for these proposals
We need to store the url

'''

temp_website = 'https://demo.snapshot.org/#/dumbo.eth'


class Website(ABC):

    @abstractmethod
    def check_for_new_post(self):
        pass

    '''
    04/02/2023 - @jd
    Different Dom object load at different pace, we shall explicitly wait for our proposal card to show up
    '''

    def wait_for_element_to_appear(self, _driver, _xpath):

        wait_for_element = (By.XPATH, _xpath)
        WebDriverWait(_driver, 10).until(
            EC.presence_of_element_located(wait_for_element))


class ScreenshotWebsite(Website):

    '''
    When intialisation, it only displays the recent 6 proposals.

    '''

    def click_on_filter_button(self, _driver):
        # click on filter dropdown menu
        xpath_filter_dropdown_button = "//div[@class='relative mb-3 flex px-3 md:px-0']//button[@class='button px-[22px] flex items-center']"
        _driver.find_element(
            by=By.XPATH, value=xpath_filter_dropdown_button).click()

        # click on active filter button
        xpath_filter_active_button = "//div[@class='bg-skin-header-bg text-skin-text cursor-pointer whitespace-nowrap px-3 py-2' and text()='Active']"
        self.wait_for_element_to_appear(_driver, xpath_filter_active_button)
        _driver.find_element(
            by=By.XPATH, value=xpath_filter_active_button).click()

    def initialise_active_proposals_storage(self):
        '''
        Display is from pyvirtualdisplay, allows us to run headless browser
        '''
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        self.active_proposals = {}

        driver = webdriver.Chrome(
            executable_path=self.chromedriver_path, options=options)
        driver.get(self.url)

        try:

            # FILTER dropdown menu
            self.wait_for_element_to_appear(
                driver, self.xpath_to_proposal_cards)
            self.click_on_filter_button(driver)

            # Find PROPOSAL CARDS
            self.wait_for_element_to_appear(
                driver, self.xpath_to_proposal_cards)
            proposal_cards = driver.find_elements(
                by=By.XPATH, value="//a[contains(@class, 'text-skin-text') and contains(@class, 'block')]")

            for each_proposal in proposal_cards:

                '''
                04/02/2023 @jd
                i.e. lines = ['0x8cBf...877A', 'Active', 'Title of proposal', 'Summary of proposal', '2 days left']

                '''
                lines = each_proposal.text.splitlines()

                proposal = {}

                '''
                05/02/2023 @ jd
                sometimes lazy fucks dont write any content except proposal title
                '''
                print('len of lines is :',len(lines))
                if len(lines) < 5:
                    proposal = {
                    'author': lines[0],
                    'title': lines[2],
                    'start_timestamp': lines[3],
                    'url': each_proposal.get_attribute('href')
                }    
                else :
                    proposal = {
                        'author': lines[0],
                        'title': lines[2],
                        'summary': lines[3],
                        'start_timestamp': lines[4],
                        'url': each_proposal.get_attribute('href')
                    }

                hash = proposal['url']
                self.active_proposals[hash] = proposal

        except Exception as e:
            print(e)
        finally:
            print(f'Driver quiting')
            driver.quit()

    def __init__(self, _name, _url, _chromedriver_path):

        self.name = _name
        self.url = _url
        self.chromedriver_path = _chromedriver_path
        self.xpath_to_proposal_cards = "//div[@class='my-4 space-y-4']//div[contains(@class, 'border-y border-skin-border')]"
        self.active_proposals = {}

        self.initialise_active_proposals_storage()
        print(f'Done Initializing for {self.name}\n this is the new self.active_proposals{self.active_proposals}')

    def check_for_new_post(self):

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        driver = webdriver.Chrome(
            executable_path=self.chromedriver_path, options=options)
        driver.get(self.url)

        # display = Display(visible=False, size=(1600, 1200))
        # display.start()

        try:

            # FILTER dropdown menu
            self.wait_for_element_to_appear(
                driver, self.xpath_to_proposal_cards)
            self.click_on_filter_button(driver)

            # Find PROPOSAL CARDS
            self.wait_for_element_to_appear(
                driver, self.xpath_to_proposal_cards)
            proposal_cards = driver.find_elements(
                by=By.XPATH, value="//a[contains(@class, 'text-skin-text')]")

            for each_proposal in proposal_cards:

                '''
                04/02/2023 @jd

                url stored inside element.get_attribute('href)
                i.e. lines = ['0x8cBf...877A', 'Active', 'Title of proposal', 'Summary of proposal', '2 days left']

                '''

                hash = each_proposal.get_attribute('href')

                is_new_proposal = hash not in self.active_proposals

                if is_new_proposal:

                    lines = each_proposal.text.splitlines()

                    proposal = {
                        'author': lines[0],
                        'title': lines[2],
                        'summary': lines[3],
                        'start_timestamp': lines[4],
                        'url': each_proposal.get_attribute('href')
                    }
                    self.active_proposals[hash] = proposal

                    print('New post spotted, added proposal + 1')
                    print(len(list(self.active_proposals.keys())))
                    print(proposal)

            print(f'Finished checking on new post for {self.name} ')

        except Exception as e:
            print(e)

        finally:
            driver.quit()


# ScreenshotWebsite(_url=temp_website, _chromedriver_path='C:\path\chromedriver_win32\chromedriver.exe').check_for_new_post()
