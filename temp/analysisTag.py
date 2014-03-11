#coding=utf-8
__author__ = 'ding'
import json
from pymongo import Connection

con = Connection('h37:20010')
clct_user = con.tiercel.user

data = \
    '''{"male":[{"name":"体育","picture":"videoCMS_firstTag_m-tiyu.png","color":"#f6faff","bgColor":"#529eb1","tags":["NBA十佳","NBA巨星","扣篮集锦","世界杯","四大满贯","五大联赛","经典足球","CBA","体坛美女","德州扑克"]},{"name":"游戏","picture":"videoCMS_firstTag_m-youxi.png","color":"#f6faff","bgColor":"#4db4df","tags":["游戏资讯","英雄联盟","单机攻略","Dota","炉石传说","手游通关秘籍"]},{"name":"美女","picture":"videoCMS_firstTag_m-meinv.png","color":"#f6faff","bgColor":"#a8cb19","tags":["嫩模","女主播","女星","萝莉","熟女","女同"]},{"name":"精选","picture":"videoCMS_firstTag_m-jingxuan.png","color":"#f6faff","bgColor":"#f29e33","tags":["互联网人物","科幻元素","汽车","数码发烧友","技术宅","历史传奇","军事观察","武器装备","台湾政局","中国领导人","科学揭秘","新闻头条追踪"]}],"female":[{"name":"男神","picture":"videoCMS_firstTag_f-nanshen.png","color":"#fff8fa","bgColor":"#bfe77b","tags":["花美男","型男","正太"]},{"name":"时尚/娱乐","picture":"videoCMS_firstTag_f-shishang.png","color":"#fff8fa","bgColor":"#fc8bb6","tags":["时尚走秀","美妆美发","潮人搭配","新片预告","日韩偶像MV","MV速递","影视原声"]},{"name":"八卦","picture":"videoCMS_firstTag_f-bagua.png","color":"#fff8fa","bgColor":"#8bc3fc","tags":["两性八卦","国内明星","爆料","耽美BL"]},{"name":"生活/情感","picture":"videoCMS_firstTag_f-qinggan.png","color":"#fff8fa","bgColor":"#fefa93","tags":["音乐心情","DIY美食","吃遍天下","减肥塑形","环球旅行","海岛风情","恋爱诀窍","创意婚居","星座运势","母婴早教","养生健康","萌宠逗乐"]}]}'''


data = json.loads(data)

tags = [one['tags'] for one in data['male']]
tags += [one['tags'] for one in data['female']]

tags = reduce(lambda a,b:a+b,tags)

print tags

S = {}
for tag in tags:
    S[tag] = 0

it  = clct_user.find({'createTime':{'$gte':'20140301'} ,'version':"36"},{'tagList':1})
print it.count()

for user in it:
    for tag in user.get('tagList',[]):
        if tag not in S:
            continue
        S[tag] += 1


for item in sorted(S.items(),key =lambda a:a[1],reverse=True):
    print item[0],item[1]


