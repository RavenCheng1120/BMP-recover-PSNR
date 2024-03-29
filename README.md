# 圖片的色彩轉換與計算PSNR    
Recover from color transfer. Calculate PSNR between source and recovered images.    

#### 讀取照片的RGB值，平均值，標準差    
```python
sImg = cv2.imread('./source/'+source)
sImg = cv2.cvtColor(sImg, cv2.COLOR_BGR2LAB)
sMean, sStd = cv2.meanStdDev(sImg)
sMean = np.hstack(np.around(sMean, decimals=2))
sStd = np.hstack(np.around(sStd, decimals=2))
```

#### 色彩轉換的公式    
```python
R = (S - sMean) * (tStd / sStd) + tMean
```

#### 計算PSNR的公式    
```python
mse += (rImg[i,j]-sImg[i,j])**2
mse = (mse[0]+mse[1]+mse[2])/3
mse = np.around(mse/(height*width), decimals=2)
if mse != 0:
     = np.around(log10((255*255)/mse)*10, decimals=2)
```

source image:    
![image](https://github.com/RavenCheng1120/BMP-recover-PSNR/blob/master/source/s5.bmp)    

target image:    
![image](https://github.com/RavenCheng1120/BMP-recover-PSNR/blob/master/target/t5.bmp)    

transfer result:    
![image](https://github.com/RavenCheng1120/BMP-recover-PSNR/blob/master/transferResult/tr5.bmp)    

recover image:    
![image](https://github.com/RavenCheng1120/BMP-recover-PSNR/blob/master/recoverSource/rs5.bmp)     

此程式將transfer result轉為recover image，計算recover image和source image的峰值信噪比PSNR，輸出在csv檔案裡。     
使用pyinstaller將python打包成exe檔 `pyinstaller -F .\4105056005-DCSA-04.py`    
    
圖源:https://unsplash.com/
