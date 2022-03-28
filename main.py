import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import statistics
import time

CORRECT = []
PRESENT = []
ABSENT = []

ITERATIONS = 100

def main():
    tries = []
    for i in range(ITERATIONS):
        print('\nTrial', i + 1)
        dict = read_txt('wordle-answers-alphabetical.txt')
        driver = webdriver.Chrome()
        driver.get('https://www.powerlanguage.co.uk/wordle/')
        action = ActionChains(driver)

        exit = driver.find_elements(By.XPATH, '//*[@id="game"]/game-modal//div/div/div/game-icon//svg/path')
        action.click(on_element=exit)
        action.perform()

        atts = solve_wordle(dict, driver)
        driver.close()
        tries.append(atts)
    print(tries)
    print('Average tries:', statistics.mean(tries), '\n')

def solve_wordle(dict, driver):
    tries = 0
    print('Solving...')
    for i in range(1, 7):
        if len(dict) > 0:
            p = 1 / len(dict)
            print('Probability of success in trial', i, ':', p)
            dict = make_guess(dict, driver)
            tries += 1
        else:
            break
    print('Solved in', tries, 'tries!')
    return tries

def make_guess(dict, driver):
    action = ActionChains(driver)
    guess = random.choice(dict)
    dict.remove(guess)
    action.send_keys(guess + Keys.RETURN)
    action.perform()
    time.sleep(2)
    evals = [my_elem.get_attribute("evaluation") for my_elem in driver.execute_script(
        "return document.querySelector('game-app').shadowRoot.querySelector('game-row[letters=" + guess + "]').shadowRoot.querySelectorAll('game-tile[letter]')")]
    for i in range(len(evals)):
        eval = evals[i]
        letter = guess[i]
        if eval == 'correct':
            CORRECT.append(letter)
            dict = list(filter(lambda s: s[i] == letter, dict))
        elif eval == 'present':
            PRESENT.append(letter)
            dict = list(filter(lambda s: ((letter in s) and (letter != s[i])), dict))
        elif eval == 'absent' and letter not in CORRECT and letter not in PRESENT:
            ABSENT.append(letter)
            dict = list(filter(lambda s: letter not in s, dict))
    return dict

def read_txt(file):
    f = open(file, 'r')
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i][:5]
    f.close()
    return lines

if __name__ == '__main__':
    main()
