
#from src.lib import atoms
import uuid

def get_default(integer):
	if integer == 1:
		return 0
	elif integer == 5:
		return False
	elif integer == 6 or integer == 7:
		return 0.0 # TODO: make sure this is a float
	elif integer == 8:
		return ''
	elif integer == 9:
		from src.lib import objects
		return objects.BW_Object(0)
	elif integer == 0x12:
		return [] # atom list
	elif integer == 0x14:
		pass # mapping?
	elif integer == 0x15:
		return uuid.UUID('00000000-0000-0000-0000-000000000000').bytes
	elif integer == 0x16:
		pass # ???
	elif integer == 0x17:
		pass # color
	elif integer == 0x19: #string array
		return []

class_type_list = {
0:[],
17: [17, 18, 19],
30: [561],
36: [],
39: [2879],
40: [6194, 607, 2075],
42: [56, 1229, 58, 59],
46: [6194, 15, 68, 4531, 69, 4539, 4532, 4533, 4534, 4535, 4536, 4537, 4538, 70, 72, 5483, 3033, 401, 1245, 2439, 2751, 96, 2747, 77, 2721, 4941, 3035, 6159, 6160, 5702, 5933],
50: [6194, 301],
61: [498, 4741, 499, 500, 1384, 7174],
64: [697, 4830, 154, 5465, 155, 156, 158, 159, 161, 162, 163, 157, 4990, 6389, 6789, 7029, 6093, 6469, 6796, 6797, 6825, 3326, 153, 164],
67: [687, 166],
71: [687, 38, 4344, 6288, 648, 646, 640, 1186, 3041, 1187, 2378, 2379, 7515, 5897, 2958],
82: [509, 543],
87: [6194, 607, 608, 374, 821, 823, 701, 3826, 702, 7489, 7490, 210],
88: [687, 38],
105: [248, 249, 1943, 6443],
107: [6194, 252, 253, 254, 256, 257, 258],
109: [265, 2956, 267],
121: [509, 2447, 5639],
123: [292, 293, 891, 294, 295, 3014, 1988, 296, 297, 298, 4433, 4434],
127: [697, 303],
133: [697, 310],
136: [46, 1408, 6823, 1253, 1254, 1270, 1277, 2866, 3581, 4442, 4777, 5170, 5831, 5840, 5834, 5836, 5837, 5838],
138: [6194, 817, 324],
139: [509, 543],
143: [345, 346, 6956, 818, 819, 820, 4723, 4724],
144: [6194, 15, 347, 1356, 360, 4992, 2641, 354, 6816, 2343, 349, 2198, 2199, 3, 1210, 350, 351, 356, 357, 242, 2726, 2727, 3070, 4803, 4804, 2764, 400, 4980, 4981, 7189],
149: [382],
151: [6194, 173, 6213, 177, 178, 6566, 6834, 179, 1977, 1978, 385, 386, 2057, 387, 388, 389, 390, 391, 4846, 4847, 392, 6384, 6417, 7549, 9657],
154: [6194, 301],
155: [393, 394, 824, 6958],
159: [509, 3123, 3124, 3125, 525, 3],
171: [6194, 420, 421, 422, 424, 165, 5206],
179: [6194, 454, 455, 456],
180: [6194, 607, 608, 374, 821, 823, 701, 3826, 702, 7489, 7490, 457],
182: [509, 543],
189: [6194, 607],
191: [509, 2447, 1181, 2988, 2989, 641, 2368, 7499, 1180, 6821, 6822],
193: [3101, 3102, 2389],
198: [4755, 6957],
206: [509, 543],
210: [520, 521, 522, 4611, 4605, 4620, 4607],
211: [697, 524],
212: [687, 38, 4344, 6288],
215: [6194, 529, 530, 531, 532, 533, 2839, 2101, 2102, 2995, 3392, 2991, 3373, 3597, 5207],
225: [509, 566, 568, 569],
227: [576, 3021],
228: [3814, 312, 4658, 1847, 3842, 3843, 3844, 3845, 3846, 3847, 1404, 1301, 1941, 4677, 1739, 5106, 4391, 6396, 4818, 4843, 5174, 6030],
236: [612, 614, 615],
238: [687, 38, 4344, 6288],
239: [6194, 607, 608, 374, 821, 823],
241: [65, 4923, 4922],
242: [498, 4741, 499, 500, 1384, 7174, 372],
247: [697, 627, 2003],
251: [593, 594, 595],
258: [650, 651],
261: [509, 2447, 1181, 2988, 2989, 641, 2368, 7499, 1180],
269: [659],
275: [7398],
289: [6194, 607, 608, 374, 821, 823, 701, 3826, 702, 7489, 7490, 712],
294: [6194, 607, 608],
295: [6194, 607, 608],
297: [6194, 607, 608],
298: [6194, 607, 608, 720],
300: [6194, 607, 608],
301: [6194, 607, 608, 721],
303: [6194, 607, 608, 750],
304: [6194, 607, 608, 724],
305: [6194, 607, 608, 725],
306: [6194, 607, 608],
308: [6194, 607, 608, 750],
311: [6194, 607, 608],
312: [6194, 607, 608],
313: [6194, 607, 608, 7235],
314: [6194, 607, 608, 750],
316: [6194, 607, 608],
317: [6194, 607, 608],
318: [726],
319: [6194, 607, 608],
320: [6194, 607, 608, 727, 728],
321: [6194, 607, 608],
324: [6194, 607, 608, 1863],
327: [6194, 607, 608],
330: [6194, 607, 608],
331: [6194, 607, 608, 732, 733, 852],
335: [6194, 607, 608, 734, 735, 736, 737],
336: [6194, 607, 608, 738],
337: [6194, 607, 608, 3154],
338: [739],
339: [6194, 607, 608, 740],
340: [6194, 607, 608, 3154, 741],
343: [6194, 607, 608, 3154],
344: [6194, 607, 608, 742, 743, 744, 745, 746, 747, 5316],
345: [6194, 607, 608],
347: [6194, 607, 608],
348: [6194, 607, 608, 3154],
350: [6194, 607, 608],
352: [6194, 607, 608, 3154],
353: [6194, 607, 608],
354: [6194, 607, 608, 3154],
361: [4471, 5075], # maybe
363: [6194, 607, 608, 751],
364: [6194, 607, 608, 752, 753, 754],
365: [6194, 607, 608, 755],
367: [6194, 607, 608, 3154],
368: [6194, 607, 608],
370: [6194, 607, 608],
372: [6194, 607, 608],
374: [6194, 756, 757, 758, 4726],
394: [6194, 607, 608, 374, 821, 823, 701, 3826, 702, 7489, 7490, 828],
395: [6194, 607, 608, 833],
398: [6194, 607, 608],
400: [6194, 607, 608, 842, 843],
401: [6194, 607, 608],
402: [6194, 607, 608, 964],
404: [6194, 607, 608, 844, 845, 846],
405: [6194, 607, 608],
406: [6194, 607, 608, 2320],
407: [6194, 607, 608],
409: [6194, 607, 608],
410: [6194, 607, 608, 1750],
412: [6194, 607, 608, 858],
413: [6194, 607, 608, 1926],
414: [6194, 607, 608],
431: [6194, 607, 608],
437: [2910, 603, 4034],
466: [6194, 607, 608],
471: [6194, 607, 608],
475: [1204, 648, 3076, 3077, 7178, 4697, 4698, 6647, 6648, 6649, 6650],
477: [6194, 15, 347, 1356, 360, 4992, 2641, 1246, 1247, 1248, 1250, 88],
479: [5155, 5386, 2409, 5924, 5925, 5926],
482: [22, 150, 151, 2237, 2238, 2239, 2240, 2241],
486: [46, 314, 7045, 3637],
491: [6194, 607, 608],
515: [687, 1795],
520: [3696, 3958, 1403, 1109, 4696, 4486, 4604, 6746, 5918, 5921, 3710, 3608, 5638, 634, 635, 637, 638, 639, 831, 7307, 2741, 3036, 3678],
529: [6194, 1866, 4017, 4018],
541: [4290, 1932, 4285, 1935, 1936, 1938, 4287, 1944, 4291],
542: [6194, 607, 608],
545: [6194, 607, 608],
547: [6194, 607, 608],
556: [6194, 607, 2012, 2013],
558: [6194, 607, 169],
564: [6194, 607, 608, 2071],
565: [6194, 607, 608, 2072],
566: [6194, 607, 608],
567: [6194, 607, 608, 2073],
572: [675, 3005],
576: [2202, 4472],
577: [2203, 4471, 5075],
578: [6194, 607, 608, 2205, 2207, 3676, 3682],
584: [6194, 2267, 5987],
586: [6194, 836, 2434, 2435, 5768, 5769, 1373, 2076, 1374, 2079, 2077, 2220],
587: [6194, 836, 2434, 2435, 5768, 5769, 1373, 2076, 1374, 2079, 2077, 2220, 835, 2315, 2270, 5361],
591: [6194, 836, 2434, 2435, 5768, 5769, 1373, 2076, 1374, 2079, 2077, 2220, 3047, 3048, 3049, 3050],
600: [6194, 607, 608, 2291],
605: [2360, 2361, 4881, 5131, 5268, 5715, 7141],
615: [509, 543, 2449, 2450, 2444, 2445],
616: [687],
617: [687],
618: [509, 543, 2449, 2450],
635: [6194, 607, 608, 2738],
640: [6194, 2748],
670: [2909],
678: [3101, 3102],
692: [3163],
766: [6194, 607, 608, 3639, 3640, 5452],
769: [6194, 607, 608],
775: [2910, 603, 3653, 3654],
778: [6194, 607, 608, 3700, 3707, 3702, 3771],
780: [3576, 3711],
787: [6194, 607, 608],
794: [7193, 4516, 4478, 3758],
805: [2910, 603, 4034],
808: [2910, 603, 4034, 6856, 6857],
822: [3696, 3958, 1403, 1109, 4696, 4486, 4604, 6746, 5918, 5921, 6430, 3988, 4365, 4571, 4583, 4463, 4476, 4364, 4480, 4481, 4482, 6306, 4643, 6528, 433, 3098, 442, 443, 444, 445, 446, 5549, 6341, 5468, 5548],
823: [3696, 3958, 1403, 1109, 4696, 4486, 4604, 6746, 5918, 5921, 4645, 4646],
849: [3696, 3958, 1403, 1109, 4696, 4486, 4604, 6746, 5918, 5921, 6430, 3988, 4365, 4571, 4583, 4463, 4476, 4364, 4480, 4481, 4482, 6306, 4643, 6528, 433, 3098, 442, 443, 444, 445, 446, 5549, 6341],
850: [3696, 3958, 1403, 1109, 4696, 4486, 4604, 6746, 5918, 5921, 6430, 3988, 4365, 4571, 4583, 4463, 4476, 4364, 4480, 4481, 4482, 6306, 4643, 6528, 433, 3098, 442, 443, 444, 445, 446, 5549, 6341],
857: [6194, 4341, 4347, 7161],
858: [6194, 4341, 4347, 4313],
859: [6194, 4341, 4347, 7161],
860: [6194, 4341, 4347, 7161],
863: [6194, 4341, 4347, 4313],
875: [4329],
900: [4770, 4390, 4776],
1115: [2022, 2023, 4513, 4514, 7448, 2024],
1124: [3696, 3958, 1403, 1109, 4696, 4486, 4604, 6746, 5918, 5921, 4645, 4646, 4430],
1125: [3696, 3958, 1403, 1109, 4696, 4486, 4604, 6746, 5918, 5921, 4645, 4646, 4430],
1134: [4290, 1932, 4285],
1146: [6194, 607, 608],
1153: [6194, 607, 608],
1158: [6194, 607, 608],
1159: [6194, 607, 608],
1170: [6194, 607, 608],
1188: [6194, 607, 608, 4763],
1191: [1298, 3386, 3284, 3387, 21, 1299],
1193: [4767, 4766, 4269, 1200, 3788, 9663, 5156, 9675, 2569, 7462, 7463, 402, 4330, 7385],
1194: [4772, 7097, 7113, 7114],
1217: [6194, 607, 608, 821, 823, 701, 3826, 7489, 7490, 712],
1219: [6194, 607, 608, 821, 823, 701, 3826, 7489, 7490, 712],
1220: [6194, 607, 608, 821, 823, 701, 3826, 7489, 7490, 712],
1221: [6194, 607, 608, 821, 823, 701, 3826, 7489, 7490, 712],
1222: [6194, 607, 608, 821, 823, 701, 3826, 7489, 7490, 712],
1223: [6194, 607, 608, 821, 823, 701, 3826, 7489, 7490, 712],
1224: [6194, 607, 608, 821, 823, 701, 3826, 7489, 7490, 210],
1227: [6194, 607, 608, 821, 823, 701, 3826, 7489, 7490, 457],
1229: [6194, 607, 608, 821, 823, 701, 3826, 7489, 7490, 457],
1230: [6194, 607, 608, 821, 823, 701, 3826, 7489, 7490, 210],
1232: [6194, 607, 608],
1234: [6194, 607, 4828, 4826],
1235: [6194, 607, 608],
1236: [6194, 607, 608],
1371: [6194, 607, 608],
1377: [5155, 5386, 5153, 5154],
1388: [5171, 5172, 5173],
1404: [6194, 607, 608, 821, 823, 701, 3826, 7489, 7490, 712],
1405: [6194, 607, 608, 821, 823, 701, 3826, 7489, 7490, 457],
1435: [6194, 607, 608],
1437: [6194, 5331, 5333, 6435, 5334, 7158],
1438: [6194, 5331, 5333, 6435, 5334, 7158, 5335, 5332, 5336, 5337],
1488: [5455],
1546: [509, 543],
1594: [5739, 5909],
1596: [5739, 5909],
1644: [5908],
1654: [6194, 607, 5950, 5975, 5976, 5978, 5979, 5982, 5983, 5985],
1679: [6226, 6309, 6310, 6867, 6221, 6228, 6242, 6243, 6522, 6245, 6209, 6210, 6225],
1680: [6226, 6309, 6310, 6867, 6211, 6212, 6232, 6233, 6277],
1681: [6226, 6309, 6310, 6867, 6221, 6228, 6242, 6243, 6522, 6245],
1683: [6226, 6309, 6310, 6867, 6400, 6401, 6219, 6520, 7188],
1685: [6226, 6309, 6310, 6867, 6220, 6244, 6263, 7525],
1686: [6226, 6309, 6310, 6867],
1687: [6226, 6309, 6310, 6867, 6220, 6241, 6223, 7055, 7056, 7057],
1694: [6217, 6218, 6215, 6216],
1695: [6217, 6218, 7552, 7553],
1702: [6226, 6309, 6310, 6867, 6220, 6241, 6239, 6240, 6267, 6552, 6719, 7527, 7530],
1704: [6226, 6309, 6310, 6867, 6220],
1712: [6226, 6309, 6310, 6867, 6220, 6255, 6256, 6257, 7548],
1713: [6226, 6309, 6310, 6867, 6220, 6540, 6581, 7526],
1714: [6226, 6309, 6310, 6867, 6220, 6262, 6266, 7528],
1717: [6226, 6309, 6310, 6867, 6220, 6241, 6258],
1719: [6226, 6309, 6310, 6867, 6400, 6401, 6258, 6259, 6521, 6767, 6768],
1721: [6194, 607, 608, 6264, 6567],
1722: [6226, 6309, 6310, 6867, 6220, 6265, 7529],
1723: [6226, 6309, 6310, 6867, 6220],
1724: [6226, 6309, 6310, 6867, 6742, 6738, 6739, 6740, 6741, 6743],
1728: [6274, 6275, 6316],
1735: [6194, 173, 6213, 177, 178, 6566, 6834, 6369, 6370, 6371, 6372, 6373, 6374, 6375, 6376, 6695, 6707, 6724, 6725],
1740: [509, 6347],
1742: [509, 6347],
1751: [6194, 6387, 6386],
1754: [6194, 6387, 6391],
1762: [6226, 6309, 6310, 6867, 6220, 6402, 6684, 6685],
1763: [6194, 607, 608, 374, 821, 823, 701, 3826, 7489, 7490, 712, 6411, 6841, 6846],
1779: [2910, 603, 4034],
1803: [6217, 6218],
1804: [6226, 6309, 6310, 6867, 6221, 6228, 6242, 6243, 6522, 6245, 6504, 6505, 6506, 6507, 6508, 6509, 6510, 6511, 6737],
1805: [6226, 6309, 6310, 6867, 6888, 6889, 6890, 6891, 6516, 6517, 6714],
1806: [6226, 6309, 6310, 6867, 6499, 6518, 6496, 6500, 6501, 6512, 6513, 6730, 6893, 6894, 6991, 6992],
1807: [6226, 6309, 6310, 6867, 6499, 6518, 6497, 6503, 6498],
1810: [6226, 6309, 6310, 6867, 6515],
1815: [6194, 607, 608, 6533],
1816: [6226, 6309, 6310, 6867, 6499, 6518, 6496, 6513, 6553, 6554, 6555, 6715, 6895, 6896, 6897],
1817: [6226, 6309, 6310, 6867, 6221, 6228, 6242, 6243, 6522, 6245, 6537, 7243, 6731],
1839: [6194],
1847: [6194, 607, 608, 6564, 6569, 6570],
1851: [6194, 607, 6572, 6571, 6573],
1852: [6226, 6309, 6310, 6867, 6574, 6575, 6577, 6582],
1853: [6194, 607, 6572],
1855: [6226, 6309, 6310, 6867, 6499, 6518, 6496, 6500, 6501, 6512, 6513, 6730, 6893, 6894, 6991, 6992, 6579, 6580, 6597],
1870: [6194, 6614, 6609, 6613],
1872: [6226, 6309, 6310, 6867, 6499, 6518, 6615, 6616, 6617, 6618, 6620, 6621],
1880: [6226, 6309, 6310, 6867, 6220, 6241, 6694],
1887: [697, 6726],
1891: [6226, 6309, 6310, 6867, 6736],
1894: [6745],
1896: [6753],
1897: [6754],
1915: [7017, 7033, 6778],
1916: [6779, 6780, 6781, 6792],
1917: [6782],
1923: [6226, 6309, 6310, 6867, 6221, 6836],
1924: [6226, 6309, 6310, 6867, 6839, 6840, 6835, 6837, 6838],
1928: [6217, 6218],
1929: [6194, 607, 608, 3639, 3640, 5452, 6842],
1966: [7008],
1967: [7022, 7021],
1968: [6226, 6309, 6310, 6867, 6220, 7024, 7580],
1996: [6194],
1997: [6226, 6309, 6310, 6867, 6499, 6518, 7100, 7101, 7102, 7103, 7104, 7105, 7106, 7107],
2017: [6194, 607, 608],
2029: [6194, 607, 7293, 374],
2030: [6226, 6309, 6310, 6867, 7294],
2036: [6194, 607, 608, 374, 821, 823, 701, 3826, 702, 7489, 7490, 7358],
2042: [6226, 6309, 6310, 6867, 6220],
2050: [6194, 5331, 5333, 6435, 5334, 7158],
2067: [6194, 836, 2434, 2435, 5768, 5769, 1373, 2076, 1374, 2079, 2077, 2220],
2068: [6194, 836, 2434, 2435, 5768, 5769, 1373, 2076, 1374, 2079, 2077, 2220],
2072: [6194, 607],
2073: [6226, 6309, 6310, 6867, 7555, 7556, 7557],
2075: [6226, 6309, 6310, 6867, 7561, 7564, 7563, 7565, 7566, 7567, 7568],
2076: [6194, 607],
2077: [6194, 607],
}

field_type_list = {
15: 21,
17: 1,
18: 1,
19: 22,
21: 9,
22: 13,
38: 7,
46: 1,
56: 8,
58: 8,
59: 8,
65: 9,
68: 8,
69: 8,
70: 8,
72: 8,
77: 20,
88: 9,
96: 9,
135: 18,
150: 1,
151: 5,
153: 21,
154: 8,
155: 8,
156: 8,
157: 1,
158: 8,
159: 8,
161: 8,
162: 8,
163: 5,
164: 9,
165: 18,
166: 7,
169: 6,
173: 18,
177: 18,
178: 18,
179: 1,
210: 5,
242: 5,
248: 9,
249: 1,
252: 9,
253: 9,
254: 9,
256: 9,
257: 9,
258: 9,
265: 8,
267: 1,
292: 7,
293: 7,
294: 1,
295: 1,
296: 1,
297: 1,
298: 1,
301: 9,
303: 5,
310: 7,
312: 9,
314: 5,
324: 18,
345: 1,
346: 1,
347: 8,
349: 9,
350: 9,
351: None,
354: 5,
356: 9,
357: 9,
360: 20,
372: 1,
374: 8,
382: 18,
385: 21,
386: 8,
387: 8,
388: 8,
389: 8,
390: 8,
391: 1,
392: 5,
393: 18,
394: 1,
400: 9,
401: 9,
402: 9,
420: 9,
421: 9,
422: 9,
424: 5,
433: 9,
442: 1,
443: 1,
444: 1,
445: 1,
446: 1,
454: 5,
455: 7,
456: 5,
457: 1,
498: 8,
499: 8,
500: 5,
509: 1,
520: 5,
521: 5,
522: 5,
524: 18,
525: 9,
529: 9,
530: 9,
531: 9,
532: 9,
533: None,
543: 18,
561: 18,
566: 8,
568: 9,
569: 18,
576: 9,
593: 7,
594: 7,
595: 9,
603: 18,
607: 1,
608: 1,
612: 9,
614: 18,
615: 5,
627: 1,
634: 1,
635: 1,
637: 5,
638: 5,
639: 5,
640: 22,
641: 5,
646: 8,
648: 9,
650: 1,
651: 8,
659: 18,
675: 9,
687: 7,
697: 8,
701: 8,
702: 9,
712: 7,
720: 1,
721: 1,
724: 1,
725: 1,
726: 18,
727: 1,
728: 1,
732: 1,
733: 9,
734: 7,
735: 7,
736: 7,
737: 7,
738: 7,
739: 7,
740: 7,
741: 1,
742: 1,
743: 1,
744: 18,
745: 7,
746: 7,
747: 1,
750: 7,
751: 7,
752: 8,
753: 7,
754: 1,
755: 1,
756: 8,
757: 1,
758: 7,
817: 20,
818: 1,
819: 8,
820: 8,
821: 8,
823: 8,
824: 1,
828: 1,
831: 5,
833: 5,
835: 8,
836: 8,
841: 9,
842: 1,
843: 7,
844: 7,
845: 7,
846: 5,
852: 1,
858: 7,
891: 7,
964: 5,
1109: 7,
1180: 9,
1181: 18,
1186: 1,
1187: 7,
1200: 1,
1204: 9,
1210: 18,
1229: 8,
1245: 9,
1246: 18,
1247: 18,
1248: 9,
1250: 9,
1253: 9,
1254: 9,
1270: 5,
1277: 1,
1298: 8,
1299: 9,
1301: 9,
1356: 22,
1373: 5,
1374: 1,
1384: 5,
1403: 5,
1404: 1,
1408: 5,
1739: 5,
1750: 5,
1795: 7,
1847: 9,
1863: 5,
1866: 8,
1926: 5,
1932: 1,
1935: 7,
1936: 7,
1938: 7,
1941: 9,
1943: 5,
1944: 1,
1977: 7,
1978: 7,
1988: 7,
2003: 5,
2012: 7,
2013: 7,
2022: 8,
2023: 8,
2024: 21,
2057: 8,
2071: 1,
2072: 1,
2073: 1,
2075: 1,
2076: 5,
2077: 5,
2079: 5,
2081: 9,
2082: 9,
2083: 9,
2085: 9,
2101: 5,
2102: 5,
2198: 9,
2199: 9,
2202: 26,
2203: 26,
2205: 1,
2207: 1,
2220: 5,
2237: 5,
2238: 7,
2239: 7,
2240: 1,
2241: 7,
2267: 8,
2270: 5,
2271: 8,
2272: 18,
2291: 1,
2315: 8,
2320: 1,
2343: 1,
2360: 8,
2361: 21,
2368: 7,
2378: 1,
2379: 1,
2389: 1,
2409: 9,
2434: 5,
2435: 5,
2439: 18,
2444: 9,
2445: 9,
2447: 9,
2449: 5,
2450: 9,
2569: 5,
2641: 21,
2721: 5,
2726: 5,
2727: 5,
2738: 5,
2741: 7,
2747: 18,
2748: 8,
2751: 18,
2764: 5,
2839: 7,
2866: 5,
2879: 5,
2909: 9,
2910: 9,
2956: 8,
2958: 8,
2988: 18,
2989: 18,
2991: 1,
2995: 5,
3005: 1,
3014: 1,
3021: 5,
3026: 18,
3033: 9,
3035: 1,
3036: 5,
3041: 5,
3047: 1,
3048: 1,
3049: 1,
3050: 1,
3070: 5,
3076: 7,
3077: 7,
3098: 9,
3101: 1,
3102: 7,
3123: None,
3124: None,
3125: None,
3154: 5,
3163: 18,
3284: 8,
3326: 8,
3373: 5,
3386: 8,
3387: 9,
3392: 5,
3576: 5,
3581: 5,
3597: 5,
3608: 5,
3616: 18,
3634: 6,
3637: 5,
3639: 8,
3640: 8,
3645: 8,
3653: 7,
3654: 7,
3676: 7,
3678: 5,
3682: 1,
3696: 9,
3700: 1,
3702: 23,
3707: 8,
3710: 9,
3711: 18,
3758: 8,
3771: 8,
3788: 1,
3814: 9,
3826: 8,
3842: 9,
3843: 9,
3844: 9,
3845: 9,
3846: 9,
3847: 9,
3958: 9,
3988: 1,
4017: 8,
4018: 8,
4034: 5,
4269: 5,
4285: 1,
4287: 7,
4290: 5,
4291: 5,
4313: 9,
4329: 9,
4330: 9,
4341: 8,
4344: 5,
4347: 8,
4364: 5,
4365: 5,
4390: 1,
4391: 9,
4430: 1,
4433: 5,
4434: 5,
4442: 5,
4463: 5,
4471: None,
4472: 9,
4472: None,
4476: 5,
4478: 5,
4480: 5,
4481: 8,
4482: 1,
4486: 5,
4513: 8,
4514: 8,
4516: 18,
4531: 8,
4532: 8,
4533: 8,
4534: 8,
4535: 8,
4536: 8,
4537: 8,
4538: 8,
4539: 8,
4571: 5,
4583: 5,
4604: 9,
4605: 1,
4607: 1,
4611: 5,
4620: 1,
4643: 1,
4645: 9,
4646: 9,
4658: 5,
4677: 9,
4696: 1,
4697: 7,
4698: 7,
4723: 1,
4724: 7,
4726: 1,
4741: 8,
4755: 8,
4763: 1,
4766: 9,
4767: 8,
4770: 1,
4772: 1,
4776: 9,
4777: 26,
4803: 1,
4804: 1,
4818: 5,
4826: 1,
4828: 1,
4830: 8,
4843: 1,
4846: 5,
4847: 5,
4881: 1,
4916: 9,
4922: 8,
4923: 8,
4941: 5,
4980: 7,
4981: 7,
4990: 5,
4992: 5,
4993: 5,
5075: 1,
5106: 5,
5131: 18,
5153: 9,
5154: 18,
5155: 5,
5156: 1,
5170: 5,
5171: 8,
5172: 7,
5173: 7,
5174: 9,
5206: 9,
5207: 9,
5268: 5,
5316: 5,
5331: 1,
5332: 1,
5333: 1,
5334: 5,
5335: 1,
5336: 8,
5337: 8,
5361: 5,
5381: 22,
5386: 5,
5452: 20,
5455: 5,
5465: 8,
5468: 9,
5483: 5,
5548: 5,
5549: 5,
5638: 1,
5639: 9,
5702: 9,
5715: 9,
5739: 18,
5768: 5,
5769: 5,
5831: 1,
5834: 5,
5836: 8,
5837: 1,
5838: 5,
5840: 5,
5897: 7,
5908: 5,
5909: 20,
5918: 5,
5921: 5,
5924: 7,
5925: 7,
5926: 8,
5933: 1,
5950: 5,
5975: 22,
5976: 22,
5978: 22,
5979: 22,
5982: 1,
5983: 1,
5985: 22,
5987: 8,
6030: 1,
6093: None,
6159: 7,
6160: 1,
6194: 9,
6209: 5,
6210: 1,
6211: 8,
6212: 9,
6213: 18,
6215: 1,
6216: 1,
6217: 1,
6218: 1,
6219: 8,
6220: 9,
6221: 18,
6223: 1,
6225: 1,
6226: 9,
6228: 1,
6232: 1,
6233: 1,
6239: 8,
6240: 1,
6241: 8,
6242: 8,
6243: 5,
6244: 5,
6245: 1,
6255: 5,
6256: 1,
6257: 1,
6258: 8,
6259: 8,
6262: 1,
6263: 1,
6264: 8,
6265: 5,
6266: 1,
6267: 1,
6274: 8,
6275: 9,
6277: 18,
6288: 9,
6306: 5,
6309: 5,
6310: 5,
6316: 1,
6341: 1,
6342: 21,
6343: 9,
6347: 18,
6369: 21,
6370: 8,
6371: 8,
6372: 8,
6373: 8,
6374: 8,
6375: 8,
6376: 5,
6384: 1,
6386: 5,
6387: 8,
6389: 9,
6390: 8,
6391: 8,
6393: 5,
6396: 5,
6400: 1,
6401: 1,
6402: 5,
6411: 9,
6417: 9,
6430: 9,
6435: 5,
6443: 7,
6469: 18,
6496: 8,
6497: 7,
6498: 5,
6499: 5,
6500: 7,
6501: 7,
6503: 9,
6504: 7,
6505: 7,
6506: 1,
6507: 1,
6508: 7,
6509: 7,
6510: 1,
6511: 1,
6512: 9,
6513: 9,
6515: 9,
6516: 5,
6517: 5,
6518: 1,
6520: 1,
6521: 1,
6522: 1,
6528: 1,
6533: 1,
6537: 1,
6540: 1,
6552: 5,
6553: 1,
6554: 1,
6555: 1,
6559: 9,
6560: 1,
6564: 1,
6566: 1,
6567: 1,
6569: 1,
6570: 7,
6571: 7,
6572: 1,
6573: 1,
6574: 9,
6575: 1,
6577: 1,
6579: 9,
6580: 9,
6581: 5,
6582: 5,
6597: 1,
6609: 23,
6613: 1,
6614: 8,
6615: 9,
6616: 5,
6617: 9,
6618: 1,
6620: 1,
6621: 1,
6647: 7,
6648: 7,
6649: 1,
6650: 1,
6681: 5,
6682: 1,
6683: 1,
6684: 1,
6685: 1,
6694: 1,
6695: 9,
6707: 5,
6714: 5,
6715: 5,
6719: 5,
6724: 5,
6725: 5,
6726: 18,
6730: 5,
6731: 5,
6736: 5,
6737: 5,
6738: 1,
6739: 1,
6740: 7,
6741: 7,
6742: 9,
6743: 7,
6745: 1,
6746: 9,
6753: 1,
6754: 1,
6767: 7,
6768: 7,
6778: 18,
6779: 8,
6780: 8,
6781: 9,
6782: 18,
6789: 9,
6792: 1,
6796: 5,
6797: 5,
6816: 5,
6821: None,
6822: 5,
6823: 1,
6825: 5,
6831: 5,
6834: 9,
6835: 9,
6836: 8,
6837: 5,
6838: 5,
6839: 8,
6840: 8,
6841: 9,
6842: 9,
6846: 9,
6856: 7,
6857: 7,
6867: 8,
6888: 5,
6889: 5,
6890: 5,
6891: 5,
6893: 1,
6894: 7,
6895: 5,
6896: 5,
6897: 7,
6956: 1,
6957: 5,
6958: 1,
6991: 7,
6992: 7,
7008: 9,
7017: 8,
7021: 9,
7022: 8,
7024: 9,
7026: 8,
7027: 1,
7028: 5,
7029: 9,
7033: 8,
7045: 5,
7055: 1,
7056: 1,
7057: 1,
7097: 5,
7100: 8,
7101: 9,
7102: 1,
7103: 1,
7104: 1,
7105: 5,
7106: 5,
7107: 7,
7113: 1,
7114: 5,
7141: 18,
7158: 5,
7161: 5,
7174: 5,
7178: 7,
7188: 1,
7189: 9,
7193: 7,
7235: 5,
7243: 7,
7293: 5,
7294: 9,
7307: 5,
7358: 1,
7385: None,
7398: 1,
7448: 8,
7462: 5,
7463: 1,
7489: 5,
7490: 5,
7499: 1,
7515: 20,
7525: 1,
7526: 1,
7527: 1,
7528: 1,
7529: 1,
7530: 1,
7548: 1,
7549: 9,
7552: 5,
7553: 5,
7555: 5,
7556: 1,
7557: 1,
7561: 9,
7563: 7,
7564: 1,
7565: 7,
7566: 1,
7567: 7,
7568: 5,
7580: 5,
9657: 5,
9663: 1,
9675: 1,
9820: 9,
9821: 5,
9823: 7,
9824: 7,
9887: 5,
9895: 5,
9926: 5,
9954: 9,
9955: 9,
9956: 9,
9960: 5,
9972: None,#some sort of array
10018: 5,
10029: 1,
10034: 7,
10049: 5,
10057: 5,
'additional_device_types': 1,
'album': 8,
'application_version_name': 8,
'artist': 8,
'beat_length': 7,
'bpm': 7,
'branch': 8,
'comment': 8,
'copyright': 8,
'creator': 8,
'device_category': 8,
'device_creator': 8,
'device_description': 8,
'device_id': 8,
'device_name': 8,
'device_type': 8,
'device_uuid': 21,
'genre': 8,
'has_audio_input': 5,
'has_audio_output': 5,
'has_note_input': 5,
'has_note_output': 5,
'is_polyphonic': 5,
'orig_artist': 8,
'preset_category': 8,
'producer': 8,
'referenced_device_ids': 25,
'referenced_modulator_ids': 25,
'referenced_module_ids': 25,
'referenced_packaged_file_ids': 25,
'revision_id': 8,
'revision_no': 1,
'structure': 13,
'suggest_for_audio_input': 5,
'suggest_for_note_input': 5,
'tags': 8,
'title': 8,
'type': 8,
'used_files': 25,
'writer': 8,
'year': 8,
}
