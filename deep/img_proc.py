import urllib
import cv2
import os
from PIL import Image, ImageChops
import random
import numpy as np

inDir0 = '../data/images/youtube'
inDir1 = '../data/images/flickr'
outDir0 = '../data/images/zeros'
outDir1 = '../data/images/ones'

def flickrDownloadUrl(url):
	urllist = []
	page = urllib.urlopen(url).read()
	closeindex = 0
	index = 0
	while(index > -1):
		index = page.find("url(", closeindex, len(page))
		closeindex = page.find(")",index,len(page))
		if(index > 0 and closeindex > 0):
			urllist.append(page[index + 6: closeindex])
	return urllist
	

def flickrDownloadDate(year, month, date, fileDir):
		datestr = "0" + str(date) if date < 10 else str(date)
		monthstr = "0" + str(month) if month < 10 else str(month)
		yearstr = str(year)
		url = "https://www.flickr.com/explore/" + str(year) + "/" + monthstr + "/" + datestr
		urllist = flickrDownloadUrl(url)

		for url in range(len(urllist)):
			print("Downloading " + urllist[url])
			f = open(fileDir + "/" + yearstr + "_" + monthstr + "_" + datestr + '_' + str(url) + '.jpg','wb')
			img = urllib.urlopen('http://' + urllist[url]).read()
			f.write(img)
			f.close()


def flickrDownload(inDir):
	for month in range(1,13):
		for day in range(1,28):
			print("Downloading:" + str(month) + str(day))
			flickrDownloadDate(2015, month, day, inDir)

def resize(inDir, outDir):
	dsize = (200,200)
	CV_LOAD_IMAGE_COLOR = 1

	for file in os.listdir(inDir):
	    if file.endswith(".jpg"):
			print(file)
			imgPath = inDir + "/" + file
			src = cv2.imread(imgPath,CV_LOAD_IMAGE_COLOR)
			dst = cv2.resize(src, dsize)
			cv2.imwrite(outDir + "/" + file, dst)

def trim(im):
	bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
	diff = ImageChops.difference(im, bg)
	diff = ImageChops.add(diff, diff, 2.0, -100)
	bbox = diff.getbbox()
	if bbox:
		return im.crop(bbox)
	else:
		return im

def cropImgs(inDir, outDir):
	for file in os.listdir(inDir):
		if file.endswith(".jpg"): # and os.stat(inDir + "/" + file).st_size > 1024 :
			imgPath = inDir + "/" + file
			# imgPath = inDir0 + '/' + str(count) + '.jpg'
			img = Image.open(imgPath)
			newimg = trim(img)
			newimg.save(outDir + "/" + file, "JPEG")

def getYTList(yturl, after):
	yturl_start = "\"url\": \"http://www.youtube.com/watch?v="
	yturl_end = "\","
	ytafter_start = "\"after\": \""
	ytafter_end = "\", \"before\":"
	
	urllist = []
	
	page = urllib.urlopen(yturl + after).read()
	closeindex = 0
	index = 0
	
	while(index > -1):
		index = page.find(yturl_start, closeindex, len(page))
		closeindex = page.find(yturl_end, index, len(page))
		if(index > 0 and closeindex > 0):
			urllist.append(page[index + 39: closeindex]) #closeindex])

	closeindex = 0
	index = 0
	index = page.find(ytafter_start, closeindex, len(page))
	closeindex = page.find(ytafter_end, index, len(page))
	after = page[index + 10: closeindex]

	return [urllist, after]

def ytDownload():
	urls = ["https://www.reddit.com/domain/youtube.com/.json?&limit=60&after=", 
			"https://www.reddit.com/domain/youtube.com/top/.json?&limit=60&after=", 
			"https://www.reddit.com/domain/youtube.com/new/.json?&limit=60&after=", 
			"https://www.reddit.com/domain/youtube.com/controversial/.json?&limit=60&after=", 
			"https://www.reddit.com/domain/youtube.com/top/.json?sort=top&t=hour&limit=60&after=",
			"https://www.reddit.com/domain/youtube.com/top/.json?sort=top&t=day&limit=60&after=",
			"https://www.reddit.com/domain/youtube.com/top/.json?sort=top&t=month&limit=60&after=",
			"https://www.reddit.com/domain/youtube.com/top/.json?sort=top&t=year&limit=60&after=",
			"https://www.reddit.com/domain/youtube.com/top/.json?sort=top&t=all&limit=60&after=",
			"https://www.reddit.com/domain/youtu.be/.json?&limit=60&after=", 
			"https://www.reddit.com/domain/youtu.be/top/.json?&limit=60&after=", 
			"https://www.reddit.com/domain/youtu.be/new/.json?&limit=60&after=", 
			"https://www.reddit.com/domain/youtu.be/controversial/.json?&limit=60&after=", 
			"https://www.reddit.com/domain/youtu.be/top/.json?sort=top&t=hour&limit=60&after=",
			"https://www.reddit.com/domain/youtu.be/top/.json?sort=top&t=day&limit=60&after=",
			"https://www.reddit.com/domain/youtu.be/top/.json?sort=top&t=month&limit=60&after=",
			"https://www.reddit.com/domain/youtu.be/top/.json?sort=top&t=year&limit=60&after=",
			"https://www.reddit.com/domain/youtu.be/top/.json?sort=top&t=all&limit=60&after="
			]

	#yturl = "https://www.reddit.com/r/all/search?q=%28and+timestamp:1373932800..1474019200+site:%27youtube.com%27%29&restrict_sr=on&sort=relevance&t=all&syntax=cloudsearch"
	#yturl = "https://www.reddit.com/r/all/search?q=%28and+timestamp%3A1372932200..1373068800+site%3A%27youtube.com%27%29&sort=new&restrict_sr=on&t=all&syntax=cloudsearch&after="

	urllist = []
	video_ids = []
	after = ""
	target_size = 1000
	n_batch = 50
	last_size = 0
	for url in urls:
		print(url)
		for i in range(target_size/n_batch):
			print("   " + str(i*n_batch) + " " + after)
			while (len(video_ids) < last_size + n_batch):
				try:
					vids, new_after = getYTList(url, after)
					video_ids.extend(vids)
					after = new_after
				except Exception:
					vids, new_after = getYTList(url, after)
					video_ids.extend(vids)
					after = new_after

				# vids, new_after = getYTList(url, after)
				# video_ids.extend(vids)
				# after = new_after

			#video_ids =[ 'QLqHZLdt_jE',  '8u-dxn8IgQo',  '4cAHL4LMNlY',  'LoebZZ8K5N0',  '8oA3dzcnQ5c',  'yE5yTBqVNvI',  'JIXkRXYbKaI',  'OPZ7FKyJ3A8',  '6VAkOhXIsI0',  'fNMEFbKCxfM',  'pYYtIdtjCCg',  '0gzmRehz4us',  'OKY6BGcx37k',  'SGdbPXR97lY',  'zkXpb20b-NQ',  'tVgWzYKN4J4',  '8uEwLQAxc78',  '-EbYLgTCl0Y',  'cZ3QToT4brk',  'Db1NEA_gkJw',  'GeDJAKvcZ9o',  'jp3_tyFGerI',  'HUE50xRpIuo',  'D7G7x6f9_mY',  'qeVhjVASsR8',  'TiXfnfBk3BM',  'M-LwSp4Upos',  'W0OLB51C4Vk',  'ehgoP9GIyQA',  '9AOFe_wYyjo',  'pThKc9BGBtI',  'U4oB28ksiIo',  't1J4fRl7ATE',  'kVIeUmsBGHc',  'Y1qlOMFGh0Q',  '0B-41g94cp0',  'qx5Y97xBkhc',  'p_7AgjO-QyI',  'fHP-Td7LZw8',  'WuDTBI0I8bk',  'mtBCbdezpks',  '6_tnQdHU7Vg',  'EViBA0JuLcc',  'EH41yfvrOwg',  'BbjH5CH698Y',  '66KeeTvrpDA',  'TYsKj-bx8hY',  'bZd0YxbAG6Y',  'dOuOsKrbN-A',  'r36wnaSqJtw',  'hnSeLy1e8VA',  '6W_emv8ANt0',  'GxbEwIvhr74',  'XmW7ogRxWxM',  'GMd048FH0dA',  'DTXJFGzxR1o',  'OVhdCHqx_AM',  'iCSQiry2VT8',  'b_KfnGBtVeA',  'ySEpq6A0q1g',  'gRwP87itEpU',  'qQZDQqEtLqU',  'm49oG06kMt8',  'rIkfishi5VQ',  'IDhnEJ1WPqE',  'Ucld8H_NPZY',  'rWweb5SILKI',  'JUx6VKiOOMc',  '8Ft039uzaKs',  'pCYMyQR6eEY',  'LSEBrgmfPsA',  '4rzEebuj1c4',  'SkYl_AH-qyk',  'ak1iojpiHpM',  '27rStHYjmNU',  'wuh5JkbmW7A',  'wQeZaBVRXpg',  'kNK3G4erfF8',  'GssGstMvpdU',  '1eLHQrjBwzs',  'WpaOn6y7QI8',  'yq4pNRU5sZg',  'E6nZfrF0Ngg',  'uczFP5jYt0E',  'f5B66zYkd-E',  '_1SmJUBT5q0',  '8EDq3cjHhz0',  'C-m0ehT3_mo',  '7nRYZK20i2o',  'qwFDgz48fO8',  'u6rA_gRfbSs',  'WPe1bSSyDMQ',  'Ks6VSOuNpqM',  'T-OiGi-e4PI',  '9sZhoBFGXdw',  'wKXDfDPMjyI',  'gvy_uB0-21s',  'x3aObgraifU',  'NqFcl-6l9aI',  'abPkNFzxeE4',  'uHwz6yHBcUk',  'DbXu5Uut-OA',  'AXZMKX3lTp4',  '9Ndi9hBgImI',  'KnZGNrSL8sk',  'SNlUyHvi5hI',  'F3gy5_fzW6g',  'Ow4miZYj-9Y',  'mnArCFSrkg8',  'pPFHQCp5nwA',  'WJzw7SeVnHI',  'v1K0e2Juvf0',  'rMtSc2MJLcw',  '6S9Og1buegE',  'nLUaBLynVNA',  '83N2FwsgfI8',  '1OqCVoW1W6I',  'no-F5WlIov8',  'kIskZmv1aY0',  'pnHsEiPu12w',  'fFVly3iZYaQ',  'H97EURPkxms',  'MrzDkw3qjtQ',  '_Y-_13eYwBQ',  'NiFTKJ28GRI',  'Bc80Mua8AMw',  'uSacS9ax-1U',  '8mGBaXPlri8',  'oTL_3WL5gfw',  'KWcNpV3BrGA',  'm761Z9hk1CA',  'we5q3utYPkM',  '-Xqe-O5Vnqk',  'ZZqxpXOH9GQ',  'bZqqKb6H9n8',  'Rh74ZbTh_N4',  '2t6mc1crKVo',  'QFBitnLgJSg',  'AC5q7clupPg',  'jBdXEDRQsaA',  'WTJabvfzRaw',  'PmBcnnad2TA',  'QMi1k0sg4uw',  '4um6_cNpb6M',  'U9tw5ypqEN0',  'uaowaFGCjtg',  'eBNVpAc5HiE',  'YzKvlyOr7O4',  'iixM7kRfGqo',  'vz2YfSaKRDk',  'axs6yoCwF0c',  '610sV2SG3Dw',  'l6X1vFJaX_I',  'j2hXpD-L3Vw',  'bdZpN67Knaw',  '_XDW6xo5scU',  'beez3iifOy8',  'yRtMA_aIwg8',  'b90EzNNrQ2M',  '5q0UXhNT-4c',  'nAVgjuZS9NQ',  'RBK5Jheu0To',  'JL1pKlnhvg0',  'jSvKO-C2y5g',  'JXJSQIak0O0',  'iURK1rareA0',  'wLqX7qbLqbU',  'maS9smxRubI',  'r0BRVOWA6PA',  'd0YkZgYgotw',  '-6YSeZeRPug',  'hOfRN0KihOU',  'z9utXoWkE-w',  'HR1HY_FUMgY',  'hpb2Him9CUo',  'MrlsWXZTWO0',  'oFklXdGpgxY',  'IMM-mrlZeaY',  '7LPMkop940o',  'rmhyVMpQbbY',  'hIpT0dyCYBE',  '-Im-DSUm4VQ',  'rZ9PkufwxXo',  'gaP84CssJlM',  'UPatfgoNBRo',  'NE_7Fmut3XA',  'PJIGbEnr8CY',  'ZPlwfED4tdo',  'x-pfz87So4Q',  'LuJdMxeyFvQ',  'k5AMl4zf9_g',  '-6r_OKjM-8s',  'xSzzHhu7GxU',  'AF_xRBii90U',  '4xOmwQD0Dm8',  'YaV7__D57_Q',  'Zk3rzPnpgzc',  'c15O5XfXpdk',  'uzKFmq444O4',  'zFab4i37geQ',  'toot69XZ9G8',  's44GC32d6Co',  '9SJh5ddyBqU',  'ASQJD0w9i-0',  'rH-ln5SVy9Q',  'fvv7RTbBB-U',  'lceQtP1-h5Y',  '56f4xH4ZoEM',  'KXwIK_tOuT8',  'N72ksDKrX6c',  'V_wK130-Ck4',  'ySoLPnGBelw',  '23Kn3DanEdQ',  '-X1oPcxZWEY',  '4XJItPC8SL8',  'pORFKiCqrJw',  '1Moge_dQPeU',  'XeJL-hcIQTk',  'bQDBXrDo5Rk',  'yX6Kkq7hPJY',  'nekR9Tr-B1M',  'wskmVPZBalw',  's45JT_-7v24',  'c2Nvy3SFs7M',  'cPgiROkTMiY',  'wyEYtlETcUY',  'YjPQcES4sQA',  'VypkQKVl7yo',  'xLEa3k-Kg2A',  '0OGZMfVQROY',  'w81cwKB69TY',  'aKYNNFdfXbw',  'Fine03q227s',  'EO6UwU6Kizw',  'WWMqUuCDoRI',  'KdDoVjjqYbI',  'CdhWhgA8Y0A',  'Hh-USn_USGw',  'tiiYrHGk6i4',  'TGCEeln0OBQ',  'lsYjdbrkWxk',  'Y-oPK72b2Fw',  'whmscFjHSn4',  'sKrryoGCw54',  'Wl5tH2dUcn0',  'zwn1YV1kJSQ',  'K1fbXw81mWg',  'jY_abnqWU2c',  'O8rh-0DRL-g',  'o1X8jgrMhc4',  'uEZyelhVbbc',  'MK9VfBKv298',  'hydbZ8F_txY',  'cJVqWzo6Vww',  'd5dtI6B2Az4',  'tnt2dA4w5v4',  'vSK3maq8Cyk',  '9iOFkXEEGDo',  'WA-ox1qNryI',  'IqrwPVtSHZI',  '-THMyqbmiYk',  '9rTQQ511Z6c',  'jr5lHY5vrO4',  'kgvGjm_jfgU',  'oHjqaFgcyVE',  'Od0RWahhaSw',  '0fufkRw7s2U',  '8dZ6MfaPscE',  'HSW9kdRxvMA',  'iifQBvbzaqQ',  'sUhAaI_BBps',  'TMH6Dmi5RUk',  'NKYPENJUeP8',  'FvO3GzAB0c4',  'NPQ75akxxr0',  'bB-hXsibDD4',  '3B_1itqCKHo',  '1uXp3MKT4tM',  'cpCy_sRZHYI',  'S1pBJK7YT-Y',  'EnMTt1ecxvY',  '09MRHRK_oxo',  'QNNvSRI6BL4',  'GTjnGZdZd2M',  'Gg7VBpbvqO0',  'CsE8tqtZyc4',  'kXAv8RXmsrc',  'nT5_iMZaCt4',  'fzMhh8zhTiY',  'YWMAyfhUk8I',  '_zkx_rWf92k',  'Cwmd6heE4k0',  'i2uDupq7TAY',  'iXjzYbpt9Ow',  'GSRslGA5-W0',  'fvp9bhvgwLQ',  '7ptbZJ9n4vU',  'EWANLy9TjRc',  'FoH7YkOQy24',  'zCgAURhsaTk',  'WnrAcd6ljiA',  'weohvyzS280',  'dRxBAUdlLjE',  'ueU5ayfjz0k',  'pgTiBFpi2Jw',  'WE72o9ncWaM',  'TBcEfyUGLH0',  'ZRwGa2fvJc8',  'PtB5IXCbWLI',  'cKmuF4NdjVs',  'h3BEteVRrdM',  'JZ7_UnqtYmw',  'mvptLbIigMk',  'PFqhlpr2x7Y',  'cFb0nLCKypg',  'Q6QksihDpg8',  '4ABg8TeDQMI',  'tE0Aq2DpsH8',  'UP638UwjaXA',  'UHwH-Eb-LMI',  '5wooOWP_3WE',  '9oiiKH3ki4E',  'Q5GMFxgbZuQ',  'Gbh2J6Biji0',  'h9Ekiqlg0J4',  'XLbcAY7r8XM',  'hwy-IxDN_3g',  'RH4Zq6j0hZQ',  'ftuA2KUf0d0',  'Kcb-hcdAUZs',  '07rT1t2hkDU',  'E0sgoOTUwyU',  'hnVs9LRdWBk',  'vdi-Lg9pwkY',  'aimgwzV-77U',  '6Y85r_RIjys',  'UxYY5tVllIo',  'XScxBQpNzXE',  'VqCerrO0HAA',  'Lz1cVnyFzvI',  '1SdGyllfKcQ',  'dzN2pgL0zeg',  'LbfvR5JOts8',  'ax8N0WJAhi4',  'nvBluREL9wY',  'dYQ-nXyfhho',  'z3ivMsAYn_E',  '3eRUTB_1CI8',  'dvaosZlQqrY',  'XOLOLrUBRBY',  'FYEB6vtgqWw',  'F9TNj1F9K4c',  '_2SiY0EF_3E',  'yJcRReGogW4',  'Z74r4nIVyyI',  'NwKXs28OjuQ',  'A1z6FLD8yCo',  'edct1X9DUVY',  'IWHkqCo9ztU',  'HxW59zXLwwg',  'UfF5LJZ8jkI',  'SliRFVLdhjs',  '0CVRV8KBtFE',  'pPqGrKg_HqA',  '4nPuZ9chE7s',  'm4qd1eSfVDo',  'V3ye9IxpJTY',  'DrhKmViuprU',  'tByk-FWHvHk',  'jVFVPIrNiqY',  'pQtQq3toH4o',  'FU4V4vsnCk8',  'ir6pabr4CD0',  'BLmxB3Z8COA',  '0IvhlF2wobo',  'QYJ7-3DasIM',  '5arwJJZBZdA',  'B4ZjUoEKiLs',  'opB80ULb05w',  'kYXwJ9R-N04',  'eWe3RejwaiU',  'sk4X3NuvvHc',  'psyiNMpwIbA',  'dgTU3ooyQ0o',  'HpN8BVwPz0Q',  'k2uLSvT0ERM',  'U86HZDfOe6M',  'sPo2GCTXPxU',  'eXB1DBRSvNQ',  '24pdz5s3Vk8',  '6shSvuewqfg',  'muvODWY6NZ0',  'DIRETcW2deE',  'x0rxRcaEEcg',  '0xOCFuXWVr8',  '0gXums4v490',  '2mV1X7Bvqb4',  'ui9egS_0PQ8',  'oXDWok09bXI',  'jaYmng9OXqc',  'N7jISJXA_HI',  'HF0wueK1SK4',  'p6QSinzz8tQ',  'rnhHid3rI9A',  'OIWSoBOF32U',  '4K2nsEGwoBE',  'Lp4xNdKy3l4',  '9mGumFMIONg',  'Yh_LNW_AVPY',  'lk6WSpvSJAI',  'm-QDLfcPe7E',  's4Ekck5i-_w',  'MTvHuvLmWEE',  'vFNtvOqbf5o',  'SVpw1KYh5mY',  'S4MPygTPM8Q',  'qVTrDX8y3-o',  'Wsscbdg0wYU',  'cYQdnb9GUGE',  'P2X8slGJgKU',  'ibTA3HMhxI0',  'Ov_3Ou2x0sE',  'UPYX0Ypv8DU',  'XtP88AGsslo',  'lIuYAHoJC2k',  'jWMBuz8k02I',  '0NAh6MWGjmg',  'U1hi6W5CZuA',  'ixUR9QJTrt0',  'WEhf_U9e6lo',  'EZ5G60LLxYU',  'Nzbl7-1jnks',  '0I1geB7U5VI',  'ybgsUo5kcyM',  'CmWJUfbbm5U',  'llneBR9o1zI',  'r71PwAfeUtc',  'XFZZ99OVI5M',  '0cSLzhAOYuo',  'GoZqakBAoHM',  'QyIpijrLlcM',  'CmzZeml54wA',  '7KDHt-1eG8I',  'KyOft0SNhgg',  'tiqAAuoL3_A',  'ABw6iIUTexQ',  'ZIkGuA8oe1g',  'DWpHVzqWg4o',  '8yZUIOZoqFk',  'kdf-OxIsSk4',  'j7gzz56ovlY',  'fY2BT9vXwRE',  '5c5hLIvWcVI',  '4z0FQb1aPG0',  'd7jNBlMKk5U',  'D1yTndz_73s',  'Siv3e_ywEAU',  'd0XEAxqpfyc',  'o6iBfJCuNKQ',  'Q6BcLXuuMts',  'gdfd5qnmtso',  '2slLf-b-R9Q',  'zUmfLRepTUI',  'ptKLBYlyU78',  '7Sn8fukGxUI',  'hT9yEHOjYjU',  'jeL1kdtrnQg',  'Bt0h7SpExeo',  '4bZlBfSpDlQ',  'c5G_aoEcwK4',  '_SoOjNVkAgE',  '_S5yR2NjUKk',  'f2G84k_3cdc',  '59E9FU8kH2s',  'r8utYBpYxwc',  'J2cM36mKoCo',  'vldaz_Cf7W0',  'pAwRJsYJ8A8',  '_QG4WBU6zdE',  'xGfsAc4YvAU',  'hq0mW4f5a9g',  'y1O2B7Y-fiA',  'GytDHQtVTXw',  '3qT6-gkYcWY',  'eoszGWVtMus',  '-eFDro7X_2g',  'HidjSJb7Hw8',  'XPNaZpRv6tk',  'db_phC-pYwY',  'nlHqQZxfhC4',  'nGZC97bkpjI',  '3bIxeYYSm-c',  'qPFZTYVJFH8',  'bKNBCuJhkP4',  'DPAAZNBsbmE',  'NHwKyZ49Zzc',  'iFo5a3PFn1M',  'xDCFM4XtwWw',  'aImcaXKVgxY',  'dUFDakvCO0Y',  'rYWn55bMKlc',  'GkINA2S0vck',  'Jc-LEG0T_4c',  'fkrPnwUxZ6o',  'O_B9Bs7Dwl8',  'kVgaB6DIhRg',  'rdPItntdmQM',  'a7WTJmVrBZM',  '8odlDqu56zo',  'HH4-IJEEnRc',  '7a5hUfbK9W4',  'fMgMWSJkFuw',  'm9XXEV-dzPA',  'z_qPKaVhX68',  'Lf7FiWpOhcE',  '4MKyOQU6EPc',  'I7imqO-OBVk',  'NVQCpI4GbKQ',  'csxI7JZ6c1o',  'zW66CCQ6ABM',  'aiubkHY370Y',  '6ZABhfsv3u8',  'rhp9gIlQLyE',  'm0Zj9LpJK8Y',  'EzCq-daYKRA',  'KYv2LiJhRkU',  'J0yMrcneQYQ',  'M5fs1Z8uwpg',  'W3_Waxhn7O4',  'BsMz3oEg5Ko',  'rloZiod9Tf0',  'oikLwLnoa00',  'ZRvafKSJ1ls',  'nQCCawtgY3o',  'WJxuNcwCt9E',  'sUAfc8zZoLU',  'y3C1SWVquXA',  'cCBFDmh3-cA',  'ZinU4vWp06E',  'cGHPt_9tBe0',  'VTpGZHduMzg',  'HzErFXsh2UM',  'VyNPrh5Kh1M',  'KELEb5RmRh0',  'NK5ivoMcorU',  'nBXU0cBNfUA',  'SCvAk-M7EcU',  'a2MhoXAWhO4',  'JvHWl7Bx9kw',  'YBgkfzW4_gk',  '4FbjI3b35u8',  'wp6dwIplkWs',  'XuKmCkj1-rs',  'wIV8jHnfwP8',  'oQU-GDIjz6E',  'l-N3d8AQp4Q',  'IjNgjr2Rilk',  'H5kTkzK4B-4',  'OgkGyIy119M',  'qUZOw4NO6rY',  'xXL7cOMHyHM',  'uSJbEzmn8AM',  'zFSWIOHmR8E',  'wA33PcINpuw',  'lRAquCpZEek',  'Ry-BRUr0GZg',  '9J1Y-SmZAtg',  '7dimo9pX2VY',  'NYz-_AsTASY',  'tm-R3bqHrCw',  'nzZNsP1U2ns',  'fqnMphMYTJU',  'NDpC01YTpgI',  '8d2XOjf61KM',  'IF_c89UNfK0',  'ME0-xB3E2NE',  'cfnqr26pInY',  'TVLKDtmSqUM',  'gSz-dN1_o8g',  'c_LYSUM-SNM',  'C6abicY6ncg',  '1V3es381Vmw',  'osbXcR8L2Po',  'oVWJ_q5JrwA',  'cyJqM2EcRjo',  '7z0m_h-4ihw',  'qhNeiUtHjZU',  'Hycln3Qt_nE',  'l7ibigmrsuo',  'IqFt7ljrfSI',  'uPZ98XSPZ6Y',  'jxF-FeOCxlg',  'ylbRDXKSauQ',  'p3bC1j_pVcs',  'w9IIoDgUx24',  'rPC6328ulVM',  '9q9ubvKQcaU',  'gnA6FIRpYrw',  '5gNtpV_xD7s',  'x4FMfUO0vkw',  'oGCSqBGy2r4',  'y0rDDFdYqOc',  'cpeoKaVLwTs',  'zTeiyeUcn9k',  'se008rX0iEg',  'BSmUr48uRTI',  'U9goQwh3MV0',  'PtkZxqTH9tE',  'URGNmDH46vM',  'BeWGJ0aPwJw',  'jORW11O8F-s',  'R0Ycdt-agOA',  'foD3dkZR3fI',  'Fhskvloj1gE',  'yy26CmLRgJ8',  'umqvYhb3wf4',  '_eHMCbR_s_Y',  'hssfzg_UHUE',  'IssksUd8EZw',  'uvgAblhAjIA',  'r4Wn0DZ6czo',  'XpA7qz6AH7o',  '8B8qKJ-jAnM',  '13be9aeBXJo',  'LcAMcRfPUhc',  'YVHiISp5z3c',  'JHKSqUtrNfw',  'neI76SsDGDk',  'jxbCRD_aeNQ',  'gWGE2swPziU',  'PvUTeAdhmyc',  'jzfIC5_WoUo',  'aQ0fn2yzCnE',  'sSUXTFceilo',  't79jdxvkccw',  'JKW-D8NuFEc',  'gUQuBBBzx-I',  'TUil667iT1k',  'fhdCslFcKFU',  '4bv_ALKkTjQ',  'kbA-EQZut1Q',  'lLXZVPqVR2c',  'rDiQ2Qt8H68',  'JHSlrkTwny4',  'UGHw30_hSQg',  '0-EqB-u2-A4',  'Yvewd6lgjQ0',  'pQ7y0i8XRCU',  'HzWtA5NJyYM',  'nKuGYvjzKvo',  '8Tp9lICKOrg',  'lpztW0naBWg',  '8CdAfYwEGCI',  'BHZMY0d3hUw',  'iwyEWvS3d8s',  'Ak7VfaG8-Vk',  'rj5wxsAxVfE',  'C0WGfJy6msY',  'JITI0FskSG0',  'kWffM-5-DzM',  'dsGkXhaBFZ4',  '51xA8xOEB1g',  '4Zlvj5pLCBQ',  '_jXPvFthdKY',  'UcJOySaLf0E',  'oT8Rl8-Tjbo',  'xlgmTF391qk',  'tJ3Aq-xt9y0',  'Ryg9KYXXq0U',  'ZXbpkKpaWj8',  'bYrmop7g2cU',  '0qbQETn4l9o',  '2UYURwjsMUI',  'yESOAH_4kcU',  'oYjZpO8aQRM',  'FZVcmsiMz1k',  '-ET_k1lOOPU',  'C1omp80WJa8',  'R5L9SExquao',  'q_H4FFDAQYM',  '_ZPzI-44gFM',  'gzHZezzm0B0',  'KdsbRyrGL9Y',  'WdQFDKB0gig',  '27Sc7gB65iU',  'PaEnaoydUUo',  'WJj_NMhYwf0',  'YA7BXN9yJxw',  '2YdkLEoTGj0',  'pl0l7qk8dL8',  'Kc-gEds3eTM',  'DWQI9zuHjYg',  'Nud8h9jjS94',  'jrI6SyXRWSE',  'QbBPpZ8aZQk',  'TDRAhaOv8Cc',  'WjOoC6bzMCk',  'xw08GQw0hBI',  '6TiVmHNMVwg',  'raXu6T0bjKY',  'sMyJqFDmtSs',  'Peaa1a4UgHs',  'PsvRCjzAGDo',  'v2go1rt23B4',  '2vspzt-yL_Q',  '3b4shT7EBZQ',  '-qWWfUXei0E',  'KGM2Heb4eGM',  'IEIzuJZj03U',  'GZkGiAvEhkk',  'X02Gt4z543U',  '0P6J2wT2MLc',  '1wn6vnd4xYc',  'cWZCyYYGhJM',  'PIdlJ5IcTBU',  'e0Ctv5ENJik',  'dCd_MTJPN64',  'sJGoaJqufhY',  'ZB5iqzIliZk',  'eftrQOVqZ9g',  'd1PkPODwX-Y',  'u8_TkK_zX-A',  '9BRIGVZyJhs',  'gXPsl1EP_FQ',  'J3a9EY2NKgY',  'qFhM1XZsh6o',  '9g3--WYH8SY',  'stuHt7ZRYrQ',  '5KTezYupt-k',  'QfZaaw9rheQ',  'mJ6Me4zVkwU',  '1BrfnXoe57w',  'VPCfLLr8U2k',  'Sc-ceS4o9hI',  'Xz7iJKnpik8',  'FvnhIR9E9Fc',  'Kk8sRKe8TuA',  'wQIWdpyIVws',  'UseyIqmeTy4',  'H0mCpEyPNI8',  '7VSj9xaNWpw',  'XYxbZkEvBU0',  'SzhOVP7BXUE',  'FJCaii97sgQ',  'oNTha7uxUDA',  'cHRhtshjpHs',  'gv0gQD-6ESc',  'DzRTYrKaBCA',  'vBZ5SLJmfdw',  'Slbs-3RE_Sw',  'ANtSSZJmP7M',  'ip4Q1pbrYDg',  'zBrwaCjJIFU',  'IDwiE8lwRKE',  'njYPx2htFao',  'Ti1gbVE0cWw',  'dhKaB8JP35I',  'wJQoxdSFTJ0',  'sGl2zcs9wqw',  '0RBVCp9Sksw',  'cu2K7Qij46c',  'aZND9dApFKU',  'dXtEtgW-Ydc',  'LcEN9r9MPM4',  'xka9QHKT8zU',  'b9ERaVeZCe0',  'wRjt3sTak1g',  'CWqdllFDePI',  'dZyJrkhNC6k',  'Wf012GrrIzo',  'aXfbMuBiu7g',  'OTCrmYu2nn0',  '8LIu_0KxTbs',  'CW2BcyuOUss',  'Ed7XJ_4ycT0',  'G6ddsTGG0zM',  '6ekStymeqm8',  '9vupRn3PJvg',  'rc5PZJ8TIQY',  'R939TYKyZUE',  'ifMrxK6QDj8',  'uYAhcAqPwO4',  'vhxZ8NefEYo',  'RxINpRAeOFU',  'wpsd25frYMw',  'P1ETDiUWjPk',  'k5dgSi4_Sfk',  'NXaCqWtL8hs',  'R7EEoWg6Ekk',  'TiC5meuzPoc',  'RDnFvw364IA',  'k0aRD8LekOs',  '0FJf0-DTKQ0',  'XBwnMJ7eMOc',  'zOpGjFBpJo8',  'trVeVghSzRs',  'FvCSRRuDYlc',  'LaDa-15AKFA',  '-td3uZUbMFU',  'OOqiQiMkXDA',  'vY0PACJFfHw',  'dJOawompuJQ',  '2rgepWg4rzw',  'O20KovFyfEg',  'vioEsbeC7r4',  'HrmtAQvmfN8',  'dzZ8g0RJnBM',  'RwRmR0QJ3nM',  'd_QaLBviKKM',  'AULOC--qUOI',  'zB2Kq29A4KQ',  'f9RwfkMgF4U',  'fajnao-jZpw',  'pnbuRlRbK5E',  '9FVmxXt1G2M',  '621Nk3Ubz4A',  'QsvQKpdf3HM',  'Tj5AF_m3-4I',  'INnZDMsS4CI',  'rjkiJJ5vsvA',  'o4z34lDKm_U',  'KPGPex851EE',  'LPYFGE954os',  'XpYQjH9xGS4' ]
			# "http://img.youtube.com/vi/" + video_ids[i] +  "/0.jpg"
			for v_index in range(last_size, len(video_ids)):
				f = open(inDir0 + '/' + video_ids[v_index] + '.jpg','wb')
				imgurl = "http://img.youtube.com/vi/" + video_ids[v_index] +  "/0.jpg"
				img = urllib.urlopen(imgurl).read()
				f.write(img)
				f.close()
			last_size = len(video_ids)

def create01():	
	resize(inDir0, outDir0)
	resize(inDir1, outDir1)

def convertImgs2DS(inDir):
	data = []
	for file in os.listdir(inDir):
		if file.endswith(".jpg"):
			imgPath = inDir + "/" + file
			src = cv2.imread(imgPath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
			img = []
			for row in src:
				img.extend(row)
			data.append(img)

	return data

def getImgDataSet():
	zeros = convertImgs2DS(outDir0)
	ones = convertImgs2DS(outDir1)

	#dataset_x = zeros + ones
	dataset_y = [0]*len(zeros) + [1]*len(ones)

	# combined = zip(dataset_x, dataset_y)
	random.shuffle(dataset_y)
	# dataset_x[:], dataset_y[:] = zip(*combined)

	# for x in dataset_y:
	# 	print(x) 

	dataset_x = []
	zeros_index = 0
	ones_index = 0
	for y in range(len(dataset_y)):
		if(dataset_y[y] == 0):
			dataset_x.append(zeros[zeros_index])
			zeros_index += 1
		else:
			dataset_x.append(ones[ones_index])
			ones_index += 1

	n_test = 1000
	n_valid = 1000
	test = [dataset_x[:n_test], dataset_y[:n_test]]
	valid = [dataset_x[n_test:n_test+n_valid], dataset_y[n_test:n_test+n_valid]]
	train = [dataset_x[n_test+n_valid:], dataset_y[n_test+n_valid:]]

	test[0] = np.array(test[0])
	valid[0] = np.array(valid[0])
	train[0] = np.array(train[0])

	return [train, valid, test]

def printImg(fileName, img):
	img = np.reshape(img,(200,200))
	cv2.imwrite(fileName, img)


def remImg(Dir):
	for file in os.listdir(Dir):
		if file.endswith("\".jpg"):
			os.remove(Dir + "/" + file)

#ifea = getImgDataSet()	

# flickrDownload()
#ytDownload()

# cropImgs(inDir0, outDir0)
# resize(outDir0, outDir0)
# resize(inDir1, outDir1)



