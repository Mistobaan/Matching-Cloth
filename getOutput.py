import cv2
import numpy


def getTarget(targetFile, imageFilenameRoot, inputFile, outputFile):

	target = open(targetFile, "r")
	outfile = open(outputFile, "w")
	infile = open(inputFile, "w")

	bottoms = ["trousers", "trouser", "jeans", "pants", "shorts", "sweatpants", "jogger", "chino"]
	num_top = 0
	num_bottom = 0
	num_suit = 0
	i = 20
	max_num = 50
	while 1:
		isTop = True 

		line = target.readline().split()
		if len(line) == 0: break
		if "Suit" in line[1]:
			if num_suit >= max_num:
				continue
			outfile.write("1 0 0\n")
			isTop = False
			#print "SUIT", line

			num_suit += 1

		for b in bottoms:
			if b == line[1].lower():
				if num_bottom >= max_num:
					continue
				outfile.write("0 1 0\n")
				#print "BOTTOM", line
				line[1]
				isTop = False

				num_bottom += 1


		if isTop:
			if num_top >= max_num:
				continue

			outfile.write("0 0 1\n")
			#print "TOP", line
			num_top += 1

		image = cv2.imread(imageFilenameRoot + line[0]+".jpg")
		# h = 144/2
		# w = 108/2
		h = 29
		w = 23

		smallImg = numpy.empty((h,w), 'uint8')
		image = cv2.resize(image, (w,h), smallImg, 0, 0, cv2.INTER_LANCZOS4)
		smallImg = smallImg.astype(float)
		smallGray = numpy.empty((h,w), 'uint8')
		smallImg = image
		# cv2.cvtColor(image, cv2.COLOR_RGB2GRAY, smallGray)
		#smallImg = numpy.divide(smallGray*1.0, 255.0)

		for x in range(image.shape[0]):
			for y in range(image.shape[1]):
				for c in range(image.shape[2]):
					color = float(image[x][y][c])/255.0
					# if i:
					# 	print type(image[x][y][c])
					# 	print int(image[x][y][c])

					# 	i -= 1

					infile.write("%.4f " % color)
				
		infile.write("\n")

	print "All done", "top:", num_top, "bottoms:", num_bottom, "suits:", num_suit	

		# print smallImg.shape







	target.close()
	outfile.close()
	infile.close()

# getTarget("inputs/all.dat", "img/lg-", "inputs/tbs-30-144*108-color-input.dat", "inputs/tbs-30-144*108-color-targets.dat")
getTarget("inputs/all.dat", "img/lg-", "inputs/test-inputs.dat", "inputs/test-targets.dat")