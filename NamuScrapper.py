#-*-coding:utf-8-*-
#나무위키-알파위키 크롤러 by 뒹굴뒹굴 심심의화신
#DBMS 적용 & 디버깅 by DPS0340
import time
import re
import requests
import os
import sqlite3
print("=" * 80)
print("나무위키-알파위키 크롤러 1.1.0")
print("made by BoredGod Studios")
print("=" * 80)
count = 0
max = 5
wtype = 0
short = 0
lashort = 0
changer = 0
nameit = 1
title = 0
checker = 0
check = 'a'
#경로를 입력하세요
path = "path\\to\\file\\"
max = int(input("크롤링 반복 횟수를 입력해 주세요."))
short = int(input("시작 글자수를 입력해 주세요."))
awaittime = float(input("크롤링 대기시간을 입력해 주세요.\n(대기시간이 줄어들면 속도가 빨라지지만, 리캡챠가 뜰 가능성도 높아집니다. 평균 0.3에서 0.5초를 추천합니다.)"))
pick = re.compile('<li>.+\'\/w\/(.+)\'>(.+)<\/a> \((.+)글자\)<\/li>')
cap = re.compile('<title>비정상적인 트래픽 감지</title>')
numchecker = re.compile('[" (][0-9]+[글자)"]')
before1 = ['&#39;','&quot;','&lt;','&gt;','&amp;']
after1 = ["'",'"','<','>','&']
convert = re.compile('<textarea.+>(.+)</textarea>', re.S)
black = ['\/',':','\*','\?','"','<','>','\|',]
while checker < max:
	req = requests.get('https://namu.wiki/ShortestPages?from=%s-1' % short)
	source = req.text
	print(source)
	while True:
		try:
			if checker >= max:
				break
			m = pick.search(source)
			if m:
				if int(m.group(3)) < short:
					break
				else:
					checker += 1
					print(m.group(3))
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
					fork = find.text
					n = convert.search(fork)
					fork = n.group(1)
					for i in before1:
						change = re.compile(i)
						fork = change.sub(after1[changer], fork)
					if fork:
						conn = sqlite3.connect("%s\\data.db" % path)
						cur = conn.cursor()
						sql = "insert into namuwiki (title,body) values (?, ?)"
						cur.execute(sql, (title, fork))
						conn.commit()
						conn.close()
						print('%s 문서 스크랩 완료' % m.group(2))
						source = pick.sub('finished', source, count=1)
					short = int(m.group(3))
					time.sleep(awaittime)
			else:
				break
		except:
			print('오류 발생. 재시작합니다.')
print('완료되었습니다.')
print('총 %s개의 문서가 저장되었습니다. 감사합니다.' % max)
time.sleep(20)
