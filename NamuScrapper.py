#-*-coding:utf-8-*-
#나무위키-알파위키 크롤러 by 뒹굴뒹굴 심심의화신
import time
import re
import requests
import os
print("=" * 80)
print("나무위키-알파위키 크롤러 1.1.0")
print("made by BoredGod Studios")
print("\n파일은 C드라이브 NamuScrap 폴더에 저장됩니다.")
print("=" * 80)
short = 1
count = 0
max = 5
availd = 0
wtype = 0
short = 0
lashort = 0
changer = 0
nameit = 1
title = 0
check = 'a'
while availd == 0:
max = int(input("크롤링 반복 횟수를 입력해 주세요."))
short = int(input("시작 글자수를 입력해 주세요."))
pick = re.compile('<li>.+\'\/w\/(.+)\'>(.+)<\/a> \((.+)글자\)<\/li>')
cap = re.compile('<title>비정상적인 트래픽 감지</title>')
before1 = ['&#39;','&quot;','&lt;','&gt;','&amp;']
after1 = ["'",'"','<','>','&']
convert = re.compile('<textarea.+>(.+)</textarea>', re.S)
black = ['\/',':','\*','\?','"','<','>','\|',]
if os.access("C:/NamuScrap", os.F_OK) == False:
	os.mkdir("C:/NamuScrap")
while count < max:
	req = requests.get('https://namu.wiki/ShortestPages?from=%s-1' % short)
	source = req.text
	print(source)
	lashort = short
	while True:
		m = pick.search(source)
		if m:
			source = pick.sub('finished', source, count=1)
			short = m.group(3)
		else:
			break
		print(short)
	source = req.text
	if os.access("C:/NamuScrap/%s-%s" % (lashort,short), os.F_OK) == False:
		os.mkdir("C:/NamuScrap/%s-%s" % (lashort,short))
	occur = 0
	while True:
		try:
			m = pick.search(source)
			if m:
				if int(lashort) == int(short):
					occur = 1
				if (m.group(3) == short) & (int(lashort) < int(short)) == True:
					break
				else:
					changer = 0
					nameit = m.group(1)
					title = m.group(2)
					for i in before1:
						change = re.compile(i)
						nameit = change.sub(after1[changer], nameit)
					for i in before1:
						change = re.compile(i)
						title = change.sub(after1[changer], title)
					find = requests.get('https://namu.wiki/edit/%s' % nameit)
					if cap.search(find.text):
						print("리캡챠 오류가 발생했습니다. 수동으로 리캡챠를 눌러주세요.")
						check = input("완료되었으면 아무 키나 눌러주세요.")
						find = requests.get('https://namu.wiki/edit/%s' % nameit)
					for i in black:
						change = re.compile(i)
						title = change.sub('', title)
					save = open('C:/NamuScrap/%s-%s/%s.txt' % (lashort,short,title), 'w', encoding = 'utf-8')
					fork = find.text
					n = convert.search(fork)
					fork = n.group(1)
					for i in before1:
						change = re.compile(i)
						fork = change.sub(after1[changer], fork)
					if fork:
						save.write(fork)
						save.close()
						print('%s 문서 스크랩 완료' % m.group(2))
						source = pick.sub('finished', source, count=1)
					time.sleep(0.4)
			else: break
		except:
			print('오류 발생. 재시작합니다.')
	if int(lashort) == int(short):
		short = int(short) + 1
	count = count + 1
	print('총 %s개 세트 중 현재 %s개 세트가 완료되었습니다.' % (max,count))
print('완료되었습니다.')
print('총 %s개 세트의 문서가 저장되었습니다. 감사합니다.' % max)
time.sleep(20)
