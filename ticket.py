from kivy.config import Config
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button    import Button
from kivy.uix.dropdown  import DropDown
from kivy.uix.checkbox  import CheckBox
from selenium import webdriver
from selenium.webdriver.support.ui import Select #option value drop-down
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
#from pywinauto import application
import numpy as np
import os , requests , base64 ,cv2 ,pytesseract, time, random

Config.set('graphics','width','300')
Config.set('graphics','height','200')
Config.write()

class Ticket(FloatLayout):

    def __init__(self,**kwargs):
        super(Ticket,self).__init__(**kwargs)

        
        self.add_widget(Label(text='공연코드',
                              font_name='malgunsl.ttf',
                              pos_hint={'x':0.0,'y':0.8},
                              size_hint=(.2,.0)))
        
        self.code = TextInput(multiline=False,
                              pos_hint={'x':0.22,'y':0.72},
                              size_hint=(.25,.15))
        self.add_widget(self.code)
        
        btn1 = Button(text='시작',font_name='malgunsl.ttf',pos_hint={'x':0.55,'y':0.718},size_hint=(.2,.15))
        #btn1.bind(on_press=self.Start)
        self.add_widget(btn1)

        btn = Button(text='계속',font_name='malgunsl.ttf',pos_hint={'x':0.75,'y':0.718},size_hint=(.2,.15))
        btn.bind(on_press=self.Continue)
        self.add_widget(btn)
        
        self.add_widget(Label(text='날짜',
                              font_name='malgunsl.ttf',
                              pos_hint={'x':0.0,'y':0.6},
                              size_hint=(.2,.0)))
        
        self.day = TextInput(multiline=False,
                             pos_hint={'x':0.22,'y':0.52},
                             size_hint=(.1,.15))
        self.add_widget(self.day)

        #DropDown 사용시 size_hint 기본값으로 size로 따로 정의해서 설정 해야 작동함
        self.dropdown = DropDown()
        values=['KB국민카드', 'BC카드', '우리카드', '삼성카드', '삼성올앳카드', '현대카드', '신한카드', '롯데카드', '씨티카드', '하나카드', '외환카드', 'NH카드', '수협카드', '조흥카드', '전북카드', '광주카드', '제주카드', '문화누리카드']
        
        for i in values:
            btn2 = Button(text= i,font_name='malgunsl.ttf',pos_hint = {'x':0.4,'y':0.52},size_hint_y=None, height=44,on_release=self.First_Drop_Down)
            btn2.bind(on_release=lambda btn2: self.dropdown.select(btn2.text))
            self.dropdown.add_widget(btn2)
        
        self.mainbutton = Button(text='신용카드',font_name='malgunsl.ttf',pos_hint = {'x':0.417,'y':0.52},size_hint=(None,None),size=(100,29))
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.add_widget(self.mainbutton)


        self.dropdown2 = DropDown()
        values2 = ['농협(중앙)','국민은행','우리은행','기업은행','씨티은행','신한은행','우체국','하나은행']
        for j in values2:
            
            btn3 = Button(text= j,font_name='malgunsl.ttf',pos_hint = {'x':0.4,'y':0.52},size_hint_y=None, height=44,on_release=self.Second_Drop_Down)
            btn3.bind(on_release=lambda btn3: self.dropdown2.select(btn3.text))
            self.dropdown2.add_widget(btn3)
        
        mainbutton2 = Button(text='무통장입금',font_name='malgunsl.ttf',pos_hint = {'x':0.417,'y':0.32},size_hint=(None,None),size=(100,29))
        mainbutton2.bind(on_release=self.dropdown2.open)
        self.dropdown2.bind(on_select=lambda instance2, y: setattr(mainbutton2, 'text', y))
        self.add_widget(mainbutton2)


        self.add_widget(Label(text='카카오페이',font_name='malgunsl.ttf',pos_hint = {'x':0.4,'y':0.22},size_hint=(.2,.0)))
        self.check_box = CheckBox(pos_hint = {'x':0.5,'y':0.12},size_hint=(.4,.2))
        self.check_box.bind(active=self.First_Check_Box)
        self.add_widget(self.check_box)

        self.add_widget(Label(text='매수',font_name='malgunsl.ttf',pos_hint={'x':0.0,'y':0.4},size_hint=(.2,.0)))
        self.certain = TextInput(multiline=False,pos_hint={'x':0.22,'y':0.32},size_hint=(.1,.15))
        self.add_widget(self.certain)


        self.add_widget(Label(text='좌석',font_name='malgunsl.ttf',pos_hint={'x':0.0,'y':0.2},size_hint=(.2,.0)))
        self.seat = TextInput(multiline=False,pos_hint={'x':0.22,'y':0.12},size_hint=(.1,.15))
        self.add_widget(self.seat)
        
    def Start(self,instance):#시작 버튼
        
        Show_Sertain = self.certain.text
        Show_Seat = self.seat.text
        
        self.driver = webdriver.Chrome('./chdr')
        self.driver.get('http://ticket.interpark.com/Ticket/Goods/TPBridge.asp?GoodsCode='+self.code.text)
        self.Day_parsing()
        time.sleep(random.randint(4,6))
        

    def Continue(self,instance1):
        self.driver.switch_to_frame(self.driver.find_element_by_id('ifrCalendar'))#날짜 iframe
        self.driver.find_element_by_partial_link_text(self.day.text).click()#날짜 설정

        #step1 관람일/회차선택
        self.driver.switch_to_default_content()
        self.driver.find_element_by_class_name('tk_dt_btn_TArea').click()#예매하기
        time.sleep(random.randint(2,4))
        self.driver.switch_to_window(self.driver.window_handles[1])#새로운창 지정
        time.sleep(random.randint(2,4))
        self.driver.find_elements_by_class_name('btn')[0].click()#다음단계

        #step2 captcha bypass

        Image_Url = driver.page_source
        soup = BeautifulSoup(Image_Url,'html.parser')
        image_url = soup.select('#imgCaptcha')
        image1 = str(image_url[0]).split('base64,')[1].split('" style')[0]

        jpg_str=base64.b64decode(image1)
        a = BytesIO(jpg_str)
        n = Image.open(a)
        n.save(os.path.expanduser('~\\Desktop\\')+'image.jpg')

        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
        src = cv2.imread(os.path.expanduser('~\\Desktop\\')+'image.jpg')#,cv2.IMREAD_GRAYSCALE)
        gray = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
        ret, blmage = cv2.threshold(gray, 123,255,cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,3))
        blmage = cv2.dilate(blmage, kernel,iterations = 1)
        text1 = pytesseract.image_to_string(blmage,lang='eng')
        captcha = soup.select('.alertNotice')

    def Day_parsing(self):
        date = requests.get('http://ticket.interpark.com/Ticket/Goods/TPBridge.asp?GoodsCode='+self.code.text)
        soup = BeautifulSoup(date.content,'html.parser')
        total = soup.select('.m_T5')
        a = list(map(str,total[0]))
        self.add_widget(Label(text=a[0],
                              font_name='malgunsl.ttf',
                              pos_hint={'x':.0,'y':.88},
                              size_hint=(0.9,0.1)))
    

    def First_Drop_Down(self,first_button):#신용카드 
        print(first_button.text)
        
    def Second_Drop_Down(self,second_button):#무통장입금
        print(second_button.text)

    def First_Check_Box(self,check_box,value):#체크박스
        if value:
            print('카카오')
            #driver.find_elements_by_class_name('chk')[1].click()#카카오페이

        

        
class Second(App):
    def build(self):
        self.title = 'InterPark Ticket'
        return Ticket()

if __name__ == '__main__':
    Second().run()

    
