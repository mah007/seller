from lxml import etree


class PriceAutomaticallyRunner(object):

	def run(self):
		root = etree.XML("http://www.lazada.vn/kep-gia-do-cho-xe-hoi-cao-cap-keo-dai-da-nang-gan-duoc-nhieu-vi-triden-5839088.html")
		find = etree.XPath('//*[@id="multisource"]')
		print(find(root)[0].tag)