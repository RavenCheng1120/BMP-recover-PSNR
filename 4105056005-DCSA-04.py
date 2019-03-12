import cv2
import csv
import numpy as np
import os
from math import log10

def colorTran(source,target,number):
	sImg = cv2.imread('./source/'+source)
	sImg = cv2.cvtColor(sImg, cv2.COLOR_BGR2LAB)
	tImg = cv2.imread('./target/'+target)
	tImg = cv2.cvtColor(tImg, cv2.COLOR_BGR2LAB)

	#讀取平均值和標準差
	sMean, sStd = cv2.meanStdDev(sImg)
	tMean, tStd = cv2.meanStdDev(tImg)
	sMean = np.hstack(np.around(sMean, decimals=2))
	sStd = np.hstack(np.around(sStd, decimals=2))
	tMean = np.hstack(np.around(tMean, decimals=2))
	tStd = np.hstack(np.around(tStd, decimals=2))
	ds.append(sStd)
	dt.append(tStd)
	ms.append(sMean)
	mt.append(tMean)

	height, width, channel = sImg.shape
	for i in range (0,height): 
		for j in range (0,width): 
			for k in range (0,channel): 
				s = sImg[i,j,k] 
				s = (s - sMean[k]) * (tStd[k] / sStd[k]) + tMean[k]
				s = round(s)
				if s < 0:
					s = 0
				if s > 255:
					s = 255  
				sImg[i,j,k] = s
	sImg = cv2.cvtColor(sImg,cv2.COLOR_LAB2BGR) 
	cv2.imwrite('./transferResult/tr'+str(number)+'.bmp',sImg)


def recover(transImage,number):
	trImg = cv2.imread('./transferResult/'+transImage)
	trImg = cv2.cvtColor(trImg, cv2.COLOR_BGR2LAB)

	height, width, channel = trImg.shape
	for i in range (0,height): 
		for j in range (0,width): 
			for k in range (0,channel): 
				tr = trImg[i,j,k] 
				tr = (tr - mt[number-1][k]) * (ds[number-1][k] / dt[number-1][k]) + ms[number-1][k]
				tr = round(tr)
				if tr < 0:
					tr = 0
				if tr > 255:
					tr = 255  
				trImg[i,j,k] = tr
	trImg = cv2.cvtColor(trImg,cv2.COLOR_LAB2BGR) 
	cv2.imwrite('./recoverSource/rs'+str(number)+'.bmp',trImg)


def psnr(sourceImg,recoverImg,mse,num):
	sImg = cv2.imread('./source/'+sourceImg)
	sImg = cv2.cvtColor(sImg, cv2.COLOR_BGR2LAB)	
	rImg = cv2.imread('./recoverSource/'+recoverImg)
	rImg = cv2.cvtColor(rImg, cv2.COLOR_BGR2LAB)

	height, width, channel = sImg.shape
	for i in range (0,height): 
		for j in range (0,width):
			mse += (rImg[i,j]-sImg[i,j])**2
	mse = (mse[0]+mse[1]+mse[2])/3
	mse = np.around(mse/(height*width), decimals=2)
	print("\tMSE:",mse)
	if mse != 0:
		mse = np.around(log10((255*255)/mse)*10, decimals=2)
		print("\tPSNR:", mse)
	print()

	#儲存為CSV檔案
	csvName = "./PSNR_result/PsnrResult"+str(num)+".csv"
	with open(csvName, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['PSNR', mse])


print("Step1.Color transfer...")	#顏色轉換
ds=[]
dt=[]
ms=[]
mt=[]
sources = ['s1.bmp','s2.bmp','s3.bmp','s4.bmp','s5.bmp','s6.bmp']
targets = ['t1.bmp','t2.bmp','t3.bmp','t4.bmp','t5.bmp','t6.bmp']
trans = ['tr1.bmp','tr2.bmp','tr3.bmp','tr4.bmp','tr5.bmp','tr6.bmp']
recovers = ['rs1.bmp','rs2.bmp','rs3.bmp','rs4.bmp','rs5.bmp','rs6.bmp']

for i in range(6):
	if os.path.isfile('./source/'+sources[i]) and os.path.isfile('./target/'+targets[i]):
		print('transferring ',sources[i],' and ',targets[i])
		colorTran(sources[i],targets[i],i+1)
	else:
		print(sources[i],"or",targets[i]," doesn't exist!!!")
print()


print('Step2.Recovering transfered images...')	#反向顏色轉換
for i in range(6):
	if os.path.isfile('./transferResult/'+trans[i]):
		print('Recovering',trans[i])
		recover(trans[i],i+1)
print()

print('Step3.Calculating PSNR...')	#計算MSE和PSNR
mse = 0.0
for i in range(6):
	if os.path.isfile('./source/'+sources[i]) and os.path.isfile('./recoverSource/'+recovers[i]):
		print('Image', recovers[i], ":")
		psnr(sources[i],recovers[i],mse,i+1)

os.system('pause')