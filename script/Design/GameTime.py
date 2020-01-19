from script.Core import CacheContorl,GameConfig,TextLoading
from dateutil import relativedelta
import datetime
import time

def initTime():
    '''
    初始化游戏时间
    '''
    CacheContorl.gameTime  = {
        "year":GameConfig.year,
        "month":GameConfig.month,
        "day":GameConfig.day,
        "hour":GameConfig.hour,
        "minute":GameConfig.minute
    }

def getDateText(gameTimeData = None) -> str:
    '''
    获取时间信息描述文本
    Keyword arguments:
    gameTimeData -- 时间数据，若为None，则获取当前CacheContorl.gameTime
    '''
    if gameTimeData == None:
        gameTimeData = CacheContorl.gameTime
    dateText = TextLoading.getTextData(TextLoading.stageWordPath,'65')
    gameYear = str(gameTimeData['year'])
    gameMonth = str(gameTimeData['month'])
    gameDay = str(gameTimeData['day'])
    gameHour = str(gameTimeData['hour'])
    gameMinute = str(gameTimeData['minute'])
    gameYearText = gameYear + TextLoading.getTextData(TextLoading.stageWordPath,'59')
    gameMonthText = gameMonth + TextLoading.getTextData(TextLoading.stageWordPath,'60')
    gameDayText = gameDay + TextLoading.getTextData(TextLoading.stageWordPath,'61')
    gameHourText = gameHour + TextLoading.getTextData(TextLoading.stageWordPath,'62')
    gameMinuteText = gameMinute + TextLoading.getTextData(TextLoading.stageWordPath,'63')
    dateText = dateText + gameYearText + gameMonthText + gameDayText + gameHourText + gameMinuteText
    return dateText

def getWeekDayText() -> str:
    '''
    获取星期描述文本
    '''
    weekDay = getWeekDate()
    weekDateData = TextLoading.getTextData(TextLoading.messagePath,'19')
    return weekDateData[int(weekDay)]

def subTimeNow(minute=0,hour=0,day=0,month=0,year=0) -> datetime.datetime:
    '''
    增加当前游戏时间
    Keyword arguments:
    minute -- 增加的分钟
    hour -- 增加的小时
    day -- 增加的天数
    month -- 增加的月数
    year -- 增加的年数
    '''
    newDate = getSubDate(minute,hour,day,month,year)
    CacheContorl.gameTime['year'] = newDate.year
    CacheContorl.gameTime['month'] = newDate.month
    CacheContorl.gameTime['day'] = newDate.day
    CacheContorl.gameTime['hour'] = newDate.hour
    CacheContorl.gameTime['minute'] = newDate.minute

def getSubDate(minute=0,hour=0,day=0,month=0,year=0,oldDate=None) -> datetime.datetime:
    '''
    获取旧日期增加指定时间后得到的新日期
    Keyword arguments:
    minute -- 增加分钟
    hour -- 增加小时
    day -- 增加天数
    month -- 增加月数
    year -- 增加年数
    oldDate -- 旧日期，若为None，则获取当前游戏时间
    '''
    if oldDate == None:
        oldDate = datetime.datetime(
            int(CacheContorl.gameTime['year']),
            int(CacheContorl.gameTime['month']),
            int(CacheContorl.gameTime['day']),
            int(CacheContorl.gameTime['hour']),
            int(CacheContorl.gameTime['minute'])
        )
    newDate = oldDate + relativedelta.relativedelta(
        years=year,
        months=month,
        days=day,
        hours=hour,
        minutes=minute
    )
    return newDate

def getWeekDate() -> datetime.datetime:
    '''
    获取当前游戏日期星期数
    '''
    return datetime.datetime(int(CacheContorl.gameTime['year']),int(CacheContorl.gameTime['month']),int(CacheContorl.gameTime['day'])).strftime("%w")

def getRandDayForYear(year:int) -> "time.time" :
    '''
    随机获取指定年份中一天的日期
    Keyword arguments:
    year -- 年份
    Return arguments:
    time.time -- 随机日期
    '''
    a1 = (year,1,1,0,0,0,0,0,0)
    a2 = (year,12,31,23,59,59,0,0,0)
    start = time.mktime(a1)
    end = time.mktime(a2)
    return getRandDayForDate(start,end)

def getRandDayForDate(startDate:"time.time",endDate:"time.time") -> "time.time":
    '''
    随机获取两个日期中的日期
    Keyword arguments:
    startDate -- 开始日期
    endDate -- 结束日期
    Return arguments:
    time.localtime -- 随机日期
    '''
    t = random.randint(start,end)
    return time.mktime(time.localtime(t))

def countDayForDateToDate(startDate:"datetime.datetime",endDate:"datetime.datetime") -> int:
    '''
    计算两个时间之间经过的天数
    Keyword arguments:
    startDate -- 开始时间
    endDate -- 结束时间
    Return arguments:
    int -- 经过天数
    '''
    return (startDate - endDate).days

def getNowTimeSlice():
    '''
    获取当前时间段
    '''
