# -*- coding: utf-8 -*-
#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2004-2006  Donald N. Allingham
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
Simplified-Chinese-specific classes for parsing and displaying dates.
"""

#-------------------------------------------------------------------------
#
# Python modules
#
#-------------------------------------------------------------------------
from __future__ import unicode_literals
import re

#-------------------------------------------------------------------------
#
# GRAMPS modules
#
#-------------------------------------------------------------------------
from gen.lib import Date
from _DateParser import DateParser
from _DateDisplay import DateDisplay
from _DateHandler import register_datehandler

#-------------------------------------------------------------------------
#
# Simplified-Chinese parser
#
#-------------------------------------------------------------------------
class DateParserZH_CN(DateParser):
    """
    Convert a text string into a Date object. If the date cannot be
    converted, the text string is assigned.
    """
    
    # modifiers before the date
    modifier_to_int = {
        '以前'   : Date.MOD_BEFORE,
        '以后'   : Date.MOD_AFTER,
        '大约'   : Date.MOD_ABOUT,
        }

    month_to_int = DateParser.month_to_int

    month_to_int["正"] = 1
    month_to_int["一"] = 1
    month_to_int["zhēngyuè"] = 1
    month_to_int["二"] = 2
    month_to_int["èryuè"] = 2
    month_to_int["三"] = 3
    month_to_int["sānyuè"] = 3
    month_to_int["四"] = 4
    month_to_int["sìyuè"] = 4
    month_to_int["五"] = 5
    month_to_int["wǔyuè"] = 5
    month_to_int["六"] = 6
    month_to_int["liùyuè"] = 6
    month_to_int["七"] = 7
    month_to_int["qīyuè"] = 7
    month_to_int["八"] = 8
    month_to_int["bāyuè"] = 8
    month_to_int["九"] = 9
    month_to_int["jiǔyuè"] = 9
    month_to_int["十"] = 10
    month_to_int["shíyuè"] = 10
    month_to_int["十一"] = 11
    month_to_int["shíyīyuè"] = 11
    month_to_int["十二"] = 12
    month_to_int["shí'èryuè"] = 12
    month_to_int["假閏"] = 13
    month_to_int["jiǎ rùn yùe"] = 13
    
    calendar_to_int = {
        '阳历'             : Date.CAL_GREGORIAN,
        'g'                : Date.CAL_GREGORIAN,
        '儒略历'           : Date.CAL_JULIAN,
        'j'                : Date.CAL_JULIAN,
        '希伯来历'         : Date.CAL_HEBREW,
        'h'                : Date.CAL_HEBREW,
        '伊斯兰历'         : Date.CAL_ISLAMIC,
        'i'                : Date.CAL_ISLAMIC,
        '法国共和历'       : Date.CAL_FRENCH,
        'f'                : Date.CAL_FRENCH,
        '伊郎历'           : Date.CAL_PERSIAN,
        'p'                : Date.CAL_PERSIAN, 
        '瑞典历'           : Date.CAL_SWEDISH,
        's'                : Date.CAL_SWEDISH,
        }
        
    quality_to_int = {
        '据估计'     : Date.QUAL_ESTIMATED,
        '据计算'     : Date.QUAL_CALCULATED,
        }
        
    # FIXME translate these English strings into simplified-Chinese ones
    bce = ["before calendar", "negative year"] + DateParser.bce

    def init_strings(self):
        """
        This method compiles regular expression strings for matching dates.
        """
        DateParser.init_strings(self)
        _span_1 = ['自']
        _span_2 = ['至']
        _range_1 = ['介于']
        _range_2 = ['与']
        self._span =  re.compile("(%s)\s+(?P<start>.+)\s+(%s)\s+(?P<stop>.+)" %
                                 ('|'.join(_span_1), '|'.join(_span_2)),
                                 re.IGNORECASE)
        self._range = re.compile("(%s)\s+(?P<start>.+)\s+(%s)\s+(?P<stop>.+)" %
                                 ('|'.join(_range_1), '|'.join(_range_2)),
                                 re.IGNORECASE)
                                    
#-------------------------------------------------------------------------
#
# Simplified-Chinese display
#
#-------------------------------------------------------------------------
class DateDisplayZH_CN(DateDisplay):
    """
    Simplified-Chinese language date display class. 
    """

    # this is used to display the 12 gregorian months
    long_months = ( "", "正月", "二月", "三月", "四月", "五月", 
                    "六月", "七月", "八月", "九月", "十月", 
                    "十一月", "十二月" )
    
    short_months = ( "", "一月", "二月", "三月", "四月", "五月", "六月",
                     "七月", "八月", "九月", "十月", "十一月", "十二月" )

    formats = (
        "年年年年-月月-日日 (ISO)",  "数字格式",  "月 日，年",
        "月 日，年",  "日 月 年",  "日 月 年",
        )
        # this must agree with DateDisplayEn's "formats" definition
        # (since no locale-specific _display_gregorian exists, here)
    
    calendar = (
        "", "儒略历", "希伯来历", "法国共和历", 
        "伊郎历", "伊斯兰历", "瑞典历" 
        )

    _mod_str = ("", "以前 ", "以后 ", "大约 ", "", "", "")

    _qual_str = ("", "据估计 ", "据计算 ", "")

    # FIXME translate these English strings into simplified-Chinese ones
    _bce_str = "%s B.C.E."


    def display(self, date):
        """
        Return a text string representing the date.
        """
        mod = date.get_modifier()
        cal = date.get_calendar()
        qual = date.get_quality()
        start = date.get_start_date()
        newyear = date.get_new_year()

        qual_str = (self._qual_str)[qual]

        if mod == Date.MOD_TEXTONLY:
            return date.get_text()
        elif start == Date.EMPTY:
            return ""
        elif mod == Date.MOD_SPAN:
            d1 = self.display_cal[cal](start)
            d2 = self.display_cal[cal](date.get_stop_date())
            scal = self.format_extras(cal, newyear)
            return "%s%s %s %s %s%s" % (qual_str, '自', d1, '至', d2, scal)
        elif mod == Date.MOD_RANGE:
            d1 = self.display_cal[cal](start)
            d2 = self.display_cal[cal](date.get_stop_date())
            scal = self.format_extras(cal, newyear)
            return "%s%s %s %s %s%s之间" % (qual_str, '介于', d1, '与',
                                        d2, scal)
        else:
            text = self.display_cal[date.get_calendar()](start)
            scal = self.format_extras(cal, newyear)
            return "%s%s%s%s" % (qual_str, (self._mod_str)[mod], text, 
            scal)

#-------------------------------------------------------------------------
#
# Register classes
#
#-------------------------------------------------------------------------

register_datehandler(('zh_CN', 'zh_SG', 'zh_TW', 'zh_HK',
                      'zh', 'chinese', 'Chinese'), 
                     DateParserZH_CN, DateDisplayZH_CN)
