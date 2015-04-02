# -*- coding: utf-8 -*-
import re


class StringUtil:

	@staticmethod
	def removeMultipleBlankSpace(string):
		return re.sub(' +',' ', string).strip()