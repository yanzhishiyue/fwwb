def gettime():
    from datetime import datetime
    res=datetime.now().strftime('%Y-%m-%d %H:%M')
    return res
