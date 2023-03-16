# QQ bot
- 删除`/data`和`/logs`QQ号缓存文件夹，修改`config.yml`文件QQ号和密码

# 运行Bot

# 命令介绍

```
【群管】：
权限：permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER
  禁言:
    禁 @某人 时间（s）[1,2591999]
    禁 时间（s）@某人 [1,2591999]
    禁 @某人 缺省时间则随机
    禁 @某人 0 可解禁
    解 @某人
    禁言时，该条消息中所有数字都会组合作为禁言时间，如：‘禁@某人 1哈2哈0哈’，则禁言120s
    
  全群禁言 若命令前缀不为空，请使用//all,若为空，需用 /all 来触发
    /all 
    /all 解
    
  改群昵称
    改 @某人 群昵称
    
  踢出：
    踢 @某人
  踢出并拉黑：
   黑 @某人
   
  撤回:
   撤回 (回复某条消息即可撤回对应消息)
   撤回 @user [(可选，默认n=5)历史消息倍数n] (实际检查的历史数为 n*19)
   
  设置精华
    回复某条消息 + 加精
  取消精华
    回复某条消息 + 取消精华
【头衔】
  改头衔
    自助领取：头衔 xxx 
    自助删头衔：删头衔
    超级用户更改他人头衔：头衔 @某人 头衔
    超级用户删他人头衔：删头衔 @某人
【管理员】permission=SUPERUSER | GROUP_OWNER
  管理员+ @xxx 设置某人为管理员
  管理员- @xxx 取消某人管理员
  
【加群自动审批】：
群内发送 permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER
  查看词条 ： 查看本群审批词条   或/审批
  词条+ [词条] ：增加审批词条 或/审批+
  词条- [词条] ：删除审批词条 或/审批-

【superuser】：
  所有词条 ：  查看所有审批词条   或/su审批
  指定词条+ [群号] [词条] ：增加指定群审批词条 或/su审批+
  指定词条- [群号] [词条] ：删除指定群审批词条 或/su审批-
  自动审批处理结果将发送给superuser
  
  【分群管理员设置】*分管：可以接受加群处理结果消息的用户
群内发送 permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER
  分管+ [user] ：user可用@或qq 添加分群管理员
  分管- [user] ：删除分群管理员
  查看分管 ：查看本群分群管理员

群内或私聊 permission=SUPERUSER
  所有分管 ：查看所有分群管理员
  群管接收 ：打开或关闭超管消息接收（关闭则审批结果不会发送给superusers）
  【群词云统计】
该功能所用库 wordcloud 未写入依赖，请自行安装
群内发送：
  记录本群 ： 开始统计聊天记录 permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER
  停止记录本群 ：停止统计聊天记录
  群词云 ： 发送词云图片
  更新mask : 更新mask图片
  增加停用词 停用词1 停用词2 ...
  删除停用词 停用词1 停用词2 ...
  停用词列表 ： 查看停用词列表

群发言排行
 - 日:
  - 日榜首：今日榜首, aliases={'今天谁话多', '今儿谁话多', '今天谁屁话最多'}
  - 日排行：今日发言排行, aliases={'今日排行榜', '今日发言排行榜', '今日排行'}
  - 昨日排行
 - 总
  - 总排行：排行, aliases={'谁话多', '谁屁话最多', '排行', '排行榜'}
 - 某人发言数
  - 日：今日发言数@xxx, aliases={'今日发言数', '今日发言', '今日发言量'}
  - 总：发言数@xxx, aliases={'发言数', '发言', '发言量'}
  【被动识别】
违禁词检测：
 - 支持正则表达式(使用用制表符分隔)
 - 可定义触发违禁词操作(默认为禁言+撤回)
 - 可定义生效范围(排除某些群 or 仅限某些群生效)
 - 示例：
  - 加(群|君\S?羊|羣)\S*\d{6,}		$撤回$禁言$仅限123456789,987654321
  - 狗群主				$禁言$排除987654321
  【功能开关】
群内发送：
  开关xx : 对某功能进行开/关  permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER
  开关状态 ： 查看各功能的状态
  xx in ：
    ['管理', '踢', '禁', '改', '基础群管']  #基础功能 踢、禁、改、管理员+-
    ['加群', '审批', '加群审批', '自动审批'] #加群审批
    ['词云', '群词云', 'wordcloud'] #群词云
    ['违禁词', '违禁词检测'] #违禁词检测
    ['图片检测', '图片鉴黄', '涩图检测', '色图检测'] #图片检测
    ['消息记录', '群消息记录', '发言记录'],
    ['早安晚安', '早安', '晚安'],
    ['广播消息', '群广播', '广播'],
    ['事件通知', '变动通知', '事件提醒'],
     ['防撤回', '防止撤回']
图片检测和违禁词检测默认关,其他默认开

【广播】permission = SUPERUSER
本功能默认关闭
   "发送【广播】/【广播+[消息]】可广播消息" 
   "发送【群列表】可查看能广播到的所有群" 
   "发送【排除列表】可查看已排除的群" 
   "发送【广播排除+】可添加群到广播排除列表" 
   "发送【广播排除-】可从广播排除列表删除群"
   "发送【广播帮助】可查看广播帮助"
   发送【开关广播】来开启/关闭（意义不大）
【特殊事件提醒】
包括管理员变动，加群退群等...
待完善
  发送【开关事件通知】来开启/关闭功能 permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER


【防撤回】
默认关闭
 发送【开关防撤回】开启或关闭功能 permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER
```

# 配置介绍

默认配置文件和资源文件存放于项目根目录的 `./data/group`文件夹下

# 各文件功能介绍

## 功能文件

- `admin.py`文件

**禁言/解禁、全体禁言和解禁、改群昵称、给头衔和删除头衔、踢人和黑人、添加和删除群管理、加精和取消精华、撤回**功能的实现

实现拉黑，除黑功能

- `approve.py`文件

分群管理设置

词条添加和删除

- `auto_ban.py`文件

违禁词禁言

- `auto_ban_.py`文件

删除、添加、查看违禁词功能

- `broadcast.py`文件（功能用处似乎不大，似乎也有用处）

广播、广播排除、群列表、添加和排除群广播列表

- `func_hook.py`文件

运行相应功能之前进行hook处理，检查某群某功能是否开启，开启再执行对应功能

- `group_msg.py`文件

群消息定时推送随机一言（早上发送和晚上发送功能），配置需要自己静态配置（文件写入配置）

- `group_recall.py`文件

防撤回功能实现

- `group_request_verify.py`文件

入群验证功能实现

- `notice.py`文件（暂时不知道分管是什么功能）

群分管、查看群分管、添加分群管理、删除分群管理、超管接收

- `particular_e_notice.py`

常见通知事件的某些功能

- `reqquest_manual.py`

不知道是干什么的，同意拒绝啥的

- `requests.py`

加群验证：实现对加群验证词条的管理

加群审批：目前似乎不能实现（或者黑名单设置为不能再申请加群了，所以收不到加群通知）

- `switcher.py`

功能开关实现，通过事件预处理进行功能开关检查

- `utils.py`

各种工具函数

- `word_analyze.py`

聊天消息记录

- `wordcloud.py`

群词云功能

## 配置文件

- `config.py`文件

全局变量

# 预期功能

- 虚拟管理

虽然不是管理，但是有管理或者超级用户授权，同样可以在群内进行撤回踢人等基础操作

- 黑名单

群内出现黑名单人物提醒并提出，可以对黑名单做出对应变化

- 分群管理

优化文件结构，优化存储结构，希望做到多个群的共同协作





