# -*- coding: utf-8 -*-
# 字符转码

class convert(object):
    """
    convert for coding
    """

    @staticmethod
    def toUnicode(s):
        if not s:
            return
        if isinstance(s, unicode):
            return s
        try:
            from utils import chardet
            enc = chardet.detect(s)['encoding']
            if enc == 'ISO-8859-2' or enc == "TIS-620":
                enc = 'gbk'
                return unicode(s, enc, 'ignore')
        except Exception, e:
            print e
            return
        ###
        charsets = ('gbk', 'gb18030', 'gb2312', 'iso-8859-1', 'utf-16', 'utf-8', 'utf-32', 'ascii')
        for charset in charsets:
            try:
                return unicode(s, charset)
            except:
                continue

    @staticmethod
    def toGB2312(s):
        s = convert.toUnicode(s)
        if s:
            return s.encode('gb2312')

    @staticmethod
    def toGBK(s):
        s = convert.toUnicode(s)
        if s:
            return s.encode('gbk')

    @staticmethod
    def toUTF8(s):
        try:
            if not isinstance(s, unicode) and not isinstance(s, str) and not isinstance(s, bytes):
                return
            if isinstance(s, unicode):
                return s.encode('utf-8')
            from utils import chardet
            enc = chardet.detect(s)['encoding']
            if enc == 'utf-8':
                return s
            else:
                s = convert.toUnicode(s)
                if s:
                    return s.encode('utf-8')
        except Exception as e:
            print e
            return

    @staticmethod
    def getEncoding(s):
        try:
            from utils import chardet
            enc = chardet.detect(s)
            return enc
        except:
            return

    @staticmethod
    def toStr(s):
        if not s: return ""
        try:
            if not isinstance(s, unicode) and not isinstance(s, str) and not isinstance(s, bytes):
                return str(s)
            import sys
            if sys.stdout.encoding == "cp936":
                return convert.toGB2312(s)
            return convert.toUTF8(s)
        except Exception as e:
            print str(e)
            return s

if __name__ == "__main__":
    print(convert.toStr("hello"))
    print(convert.toStr("你好"))