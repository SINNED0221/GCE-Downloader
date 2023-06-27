# GCE-Downloader by Dennis Zhang
A software to batch download papers from GCEGguide.com
version 1.06

这是一个可以从GCEGuide.com批量下载卷子的程序
希望可以节省一点找卷子下的时间
帮助大家享受生活（

使用方法很简单
按顺序选卷子的信息
然后在Resource Types里勾选需要的卷子 或者打勾Select All全部选择
然后点Add to list放入准备列表
选择完卷子之后点击DOWNLOAD下载

如果下载有失败 有可能是某年的某套卷子不按套路出牌
或者是GCEGuide网站文件命名有误
如果有需要还请到 GCEGuide.com自行下载

如果下载全部失败
请尝试使用vpn

-NEW-新功能！
第一次运行软件时，会在C:/user/你的用户/appdara/roaming生成一个下载历史文件
之后下载的每个文件都会记录
如果之后选择了之前下载过的卷子
会在右边的列表里标记上(downloaded)

-NEW-新功能！
在下载列表里添加卷子之后
可以直接双击浏览器跳转到对应的卷子

点击下方的Update Latest Information就能更新最新的卷子
然后就可以在年份里选择下载了
（更新失败会提示，多试几次就好了）

enable multi-thread download下拉菜单可以选择下载线程数
更高的线程数理论上会下载更快 但是会造成更大的系统负载
默认为4 按需提高

Bug汇报请到
https://github.com/SINNED0221/GCE-Downloader

下载更新请到
https://wwt.lanzouq.com/b03j2ecxe
密码:lostfeather

---------------------------更新日志-----------------------
ver1.06
新增了下载历史
新增了一键访问
修复了更新信息的功能
修复了alevel物理化学生物的3卷下载不到45的问题

ver1.05
修复了几个bug

ver1.04
新增了下载进度条(伪)

ver1.03
新增Update Latest Information按钮
增加了所有科目的年份数量

ver1.02
调整了界面布局

ver1.01
新增多线程下载
新增resource types全选按钮
将remove last item按钮更改为remore selected并可使用键盘del操作
