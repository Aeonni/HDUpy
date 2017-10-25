import requests
import pytesseract
from bs4 import BeautifulSoup
from PIL import Image
import hashlib
import re

# 设置 UA
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'

class User:
	header = {
		"User-Agent" : UA,
	}
	CurrentPage = ''
	HomePage = ''
	SubPage = {}
	Page = {}
	def __init__(self, usn, pwd):
		self.username = usn # 保存用户名为 username
		m = hashlib.md5()
		m.update(pwd.encode())
		self.password = m.hexdigest() # 保存MD5加密的密码为 password
		self.s = requests.session() # 启动一个回话
		self.HomePage = 'http://jxgl.hdu.edu.cn/xs_main.aspx?xh=' + self.username
	def get(self, url, **kwargs):
		self.CurrentPage = url
		r = self.s.get(url, headers=self.header, **kwargs)
		self.SubPage = FindSubPage(r.text)
		return r

	def post(self, url, data=None, json=None, **kwargs):
		self.CurrentPage = url
		r = self.s.post(url, data=data, headers=self.header, **kwargs)
		self.SubPage = FindSubPage(r.text)
		return r

	def login(self):
		url = 'http://cas.hdu.edu.cn/cas/login?service=http://jxgl.hdu.edu.cn/default.aspx'
		CaptchaUrl = "http://cas.hdu.edu.cn/cas/Captcha.jpg"
		# 获取登录页面
		r = self.get(url)
		
		text = r.text
        # 获取 ltcode
		ltcode = re.findall(r'<input type="hidden" name="lt" value="(.*)" />', text)[0]
		# 如果有验证码则识别、处理验证码
		captchaIMG = self.get(CaptchaUrl)
		if captchaIMG.status_code == 201:
			f = open("captcha.jpg",'wb')
			f.write(captchaIMG.content)
			f.close()
			image = Image.open('captcha.jpg')
			captcha = pytesseract.image_to_string(image)
		# 生成登录所需数据包
		postDict = {
    	    'encodedService': 'http%3a%2f%2fjxgl.hdu.edu.cn%2fdefault.aspx',
    	    'service': 'http://jxgl.hdu.edu.cn/default.aspx',
    	    'serviceName': 'null',
    	    'loginErrCnt': '0',
    		'username': self.username,
    		'password': self.password,
    		'lt': ltcode,
    		# 'captcha': captcha
		}
		# 尝试登录
		r = self.post('http://cas.hdu.edu.cn/cas/login',
                postDict)
        # print(r.text)
		try:
			finalurl = re.findall(r'window.location.href="(.*)"', r.text)[0]
		except IndexError:
			return 500
		r = self.get(finalurl)
		r = self.get(self.HomePage)
		self.Page = self.SubPage
		self.header['Referer'] = self.HomePage
		print("Login Success!")
		temp = re.findall(r'href="xskbcx(.+?)&gnmkdm=', r.text)
		self.name = temp[0][21:]
		print("User: " + self.name)
		return self.name

	def gotoSubPage(self, index):
		return self.get(self.SubPage[index]).text

	def gotoPage(self, index):
		return self.get(self.Page[index]).text

	def BackHome(self):
		return self.get(self.HomePage)

	def Logout(self):
		return self.get('http://jxgl.hdu.edu.cn/logout0.aspx')

def FindSubPage(html):
    	soup = BeautifulSoup(html)
	urllist = {}
	for i in soup.find_all('a'):
		if('#' not in i['href']):
			if('http:' in i['href']):
				urllist[i.string] = UrlModify(i['href'])
			else:
				urllist[i.string] = 'http://jxgl.hdu.edu.cn/'+UrlModify(i['href'])
	return urllist

def UrlModify(url):
	db = ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F')
	str = ''
	temp = url.encode('gb2312')
	loop = 0
	i = 0 # 计算汉字数
	stat = 0
	while i < len(temp):
		while(temp[i]>128):
			str += '%'
			str += db[int(temp[i]/16)]
			str += db[int(temp[i]%16)]
			i += 1
		if(stat == 0 and int((i-loop)/2) != 0):
			loop += int((i-loop)/2)
			stat = 1
		str += url[loop]
		loop += 1
		i += 1
	return str


def MainPageTags(tag):
	return tag.has_attr('class')

