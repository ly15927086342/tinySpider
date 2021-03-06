#coding = 'utf-8'

from chuzuSpider import *

# 线程数
THREAD_MAX = 4

# 总时间间隔（秒）
# 实际时间间隔为 TIMESPAN/THREAD_MAX
TIMESPAN = 12

# 文件夹相对路径
DICT_PATH = './result_chuzu'

def run(id):
	time.sleep(1)
	print(id)

# 主程序入口
if __name__ == '__main__':
	# regionTotal = ['xinzhouqu','hannan','hongshan','wuchang','jiangan','hanyang','jiangxia','jianghan','dongxihu','qiaokou','huangpo','whtkfq','whqingshanqu','caidian']
	region = ['hongshan','wuchang','jiangan','hanyang','jiangxia','jianghan','dongxihu','qiaokou','huangpo']
	field = ['title','price','unit','type','area','direction','floor','decoration','community','subway','address','bdlat','bdlng','description']
	region.reverse()

	app = chuzuSpider(regions = region,
		fields = field,
		thread_num = THREAD_MAX,
		dict_path = DICT_PATH,
		timespan = TIMESPAN)
	app.run()