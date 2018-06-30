#%%
from os.path import isfile
from re import compile
from time import time
from datetime import datetime
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

def get_player(driver):
    element = driver.find_element_by_xpath('/html/body/div[3]/table/tbody/tr[4]/td[2]/table[2]/tbody/tr/td/div/div')
    player = get_text_excluding_children(driver, element)
    return player

def get_last_active(driver):
    regex = compile(r'atividade: (\d*)h,')
    element = driver.find_element_by_xpath('//*[@id="tribeinfo"]/table[1]/tbody/tr/td/div')
    text = get_text_excluding_children(driver, element)
    last_active = regex.search(text).group(1)
    return last_active

def write_csv(player, last_active):
    filename = '../players/' + player + '.csv' 
    if(isfile(filename)):
        with open(filename, 'a', newline='\n') as csvfile:
            csvfile.write(datetime.now().strftime("%a %d-%m-%y %H:%M:%S") + ', ' + last_active + '\n')
    else:
        with open(filename, 'w', newline='\n') as csvfile:
            csvfile.write('time, time_since_last_active\n')
            csvfile.write(datetime.now().strftime("%a %d-%m-%y %H:%M:%S") + ', ' + last_active + '\n')

def main():
    display = Display(visible=0, size=(800, 600))
    display.start()
    player_id = '919440665'
    player, last_active = None, None
    with webdriver.Chrome() as driver:
        driver.get('http://br89.tribalwarsmap.com/br/history/player/' + player_id)
        t = time()
        timeout = 15
        while time() <= t+15:
            try:
                last_active = get_last_active(driver)
                player = get_player(driver)
                break
            except Exception as e:
                #print(e)
                print('Waiting for page to load')
                time.sleep(1)

        write_csv(player, last_active)

if __name__ == '__main__':
    main()
