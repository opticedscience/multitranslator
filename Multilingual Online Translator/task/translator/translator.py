import requests
import sys
from bs4 import BeautifulSoup

supportLanguage=['1. Arabic','2. German','3. English',
                 '4. Spanish','5. French','6. Hebrew','7. Japanese',
                 '8. Dutch','9. Polish','10. Portuguese','11. Romanian',
                 '12. Russian','13. Turkish']

supportLanguageSimple=[lan.split()[1].lower() for lan in supportLanguage]

modeA=sys.argv[1]
modeB=sys.argv[2]
word=sys.argv[3]

def printTranslation(fromLan, toLan, offset):
    link="https://context.reverso.net/translation/{0}-{1}/".format(fromLan.lower(),toLan.lower())

    message=link+word
    headers={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

    try:
        response=requests.get(message,headers=headers)
    except requests.exceptions.ConnectionError:
        print("Something wrong with your internet connection")
        return

    statecode=response.status_code
    if  statecode== 200:
        print(f'{toLan.capitalize()} Translations:')
        soup = BeautifulSoup(response.content, 'html.parser')
        p2 = soup.find_all('a',{"class":"translation"})
        p3 = soup.find_all('div',{"class":"example"})
        translation=[]
        examples=[]
        filename=word+'.txt'
        with open(filename,'a') as file:
            file.write(f'{toLan.capitalize()} Translations:')
            for p in p2[1:offset+1]:
                translate=p.text.strip()
                print(translate)
                file.writelines(translate)

            print('\n')
            print(f'{toLan} Examples:')
            file.writelines(f'\n{toLan} Examples:')

            for p in p3[:offset]:
                example=p.text.strip().split('\n\n\n\n')
                for ex in example:
                    print(ex.strip())
                    file.writelines(ex.strip())
                print('\n')
    else:
        print(f'Sorry, unable to find {word}')


if modeB in supportLanguageSimple or modeB =='all':
    fromLan=modeA
    toLan=modeB

    if modeB == 'all':
        for lan in supportLanguageSimple:
            if lan not in fromLan.lower():
                printTranslation(fromLan,lan,1)
    else:
        printTranslation(fromLan,toLan,5)
else:
    print(f"Sorry, the program doesn't support {modeB}")

