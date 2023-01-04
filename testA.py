import cv2 
import pytesseract
from PIL import Image
from fuzzywuzzy import fuzz


word = '请登录后进行操作'
# word ='智能调控空调系统，直到座舱降低至舒适温度'
# word = '也许你会想顺道看个电影'
#
# word = '添加途经点成功'
# word = "爱奇艺|宝藏视频不看不行"
word = '系统发现有小宝贝上车'
# word = '目前已打开1个车窗'
word = '即将到达目的地'
# print(base_ocr('check.png', word))
# exit()
app = 'ipa'
# app = 'mpp'
# img = Image.open('checklogin.png')
# img = Image.open('check-lot.png')
img = Image.open('../../Automation/Code/MyProject/check.png')


# img = Image.open('30c2e7fb2ffa8524.png')

length_word = len(word)
width = 1920/2
start_width = 71
if app == 'mpp':
    img = img.crop((width-20*length_word-20, 674, width+20*length_word+20, 736))
    img.save('check_word_show.png')
    img = cv2.imread('check_word_show.png')
    if not length_word == 4:
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 100, 256, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # if length_word in [4, 8]:
    #     img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 3)
    # if length_word == 4:
    #     img = cv2.Canny(img, 50, 150)
elif app == 'ipa':
    if start_width == 70:
        if length_word < 10:
            img = img.crop((70, 270, 80+40*length_word, 325))
        else:
            img = img.crop((70, 270, 720, 390))
    elif start_width == 71:
        if word in ['油量过低', '即将到达目的地']:
            img = img.crop((160, 80, 185+40*length_word, 140))
        elif word in ['添加途经点成功']:
            img = img.crop((width-20*length_word, 640, width+20*length_word+100, 760))
        else:
            img = img.crop((70, 80, 160+40*length_word, 145))
    elif start_width == 72:
        img = img.crop((420, 100, 800, 600))
    elif start_width == 73:
        img = img.crop((160, 655, 410, 710))
    img.save('check_word_show.png')
    img = cv2.imread('check_word_show.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 10, 250, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    if start_width == 70 or word in ['即将到达目的地', '目前已打开', '午餐时间到了']: 
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 3)
elif app == 'phone':
    img = img.crop((0, 0, windows_size['width'], windows_size['height']))
    img.save('check_word_show.png')
    img = cv2.imread('check_word_show.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 100, 256, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

result = pytesseract.image_to_string(img, lang='chi_sim').replace(' ', '').split('\n')
if len(result) > 2:
    result[0] = result[0] + result[1]
for item in result:
    print(fuzz.ratio(word, item))
print(f'pick all words in screen: {result}')