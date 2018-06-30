#%%
import re
import csv
import time
from selenium import webdriver
from pyvirtualdisplay import Display

def get_text_excluding_children(driver, element):
    return driver.execute_script("""
        var parent = arguments[0];
        var child = parent.firstChild;
        var ret = "";
        while(child) {
            if (child.nodeType === Node.TEXT_NODE)
                ret += child.textContent;
            child = child.nextSibling;
        }
        return ret;
        """, element) 

def write_csv(player_id, last_active):
    with open(player_id + '.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        pass

def main():
    display = Display(visible=0, size=(800, 600))
    display.start()
    player_id = '919440665'
    text = None
    last_active = None
    regex = re.compile(r'atividade: (\d*)h,')
    with webdriver.Chrome() as driver:
        driver.get('http://br89.tribalwarsmap.com/br/history/player/' + player_id)
        t = time.time()
        timeout = 15
        while time.time() <= t+15:
            try:
                element = driver.find_element_by_xpath('//*[@id="tribeinfo"]/table[1]/tbody/tr/td/div')
                text = get_text_excluding_children(driver, element)
                # text = element.text
                break
            except Exception as e:
                print(e)
                print('Waiting for page to load')
                time.sleep(1)
        print(text)
        last_active = regex.search(text).group(1)
        print(last_active)

if __name__ == '__main__':
    main()
