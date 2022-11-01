import numpy as np
from libtiff import TIFF
from PIL import Image
import os
import scipy.io as sio

Root='E:\\CODEX\\'
sample=['20220924_ZJL_WKX','20220925_ZJL_FZH','20220927_WSW_processed','20220928_ZJL_SCE_processed','20220930_ZJL_BA_4744615_processed','20221006_ZJL_BA_5587726_processed','20221006_ZJL_BA_55474617_processed','20221009_ZJL_BA_5472291_peocessed'];
roi=['1','2'];
cyc=['cyc002','cyc003','cyc004','cyc005','cyc006','cyc007','cyc008','cyc009','cyc010','cyc011','cyc012','cyc013','cyc014','cyc015','cyc016','cyc017'];
CH=['CH1','CH2','CH3','CH4'];
Pos=['00001','00002','00003','00004','00005','00006','00007','00008','00009'];

def tiffCombine(imageAll):
    image_0=np.concatenate([imageAll[:,:,0],imageAll[:,:,1],imageAll[:,:,2]],axis=1)
    image_1=np.concatenate([imageAll[:,:,5],imageAll[:,:,4],imageAll[:,:,3]],axis=1)
    image_2=np.concatenate([imageAll[:,:,6],imageAll[:,:,7],imageAll[:,:,8]],axis=1)
    image=np.concatenate([image_0,image_1,image_2],axis=0)
    imageCombine=np.delete(image,np.arange(144*17,1440*2),axis=0)
    imageCombine=np.delete(imageCombine,np.arange(144*7,1440),axis=0)
    imageCombine=np.delete(imageCombine,np.arange(192*17,1920*2),axis=1)
    imageCombine=np.delete(imageCombine,np.arange(192*7,1920),axis=1)
    return imageCombine






stain=[['DAPI_1','CD31','CD44','CD4'],
       ['DAPI_2','CD20','E-cadherin','CD68'],
       ['DAPI_3','CK19', 'CD45RO','CD45'],
       ['DAPI_4','HLA-ABC','b-Catenin1','CD11c'],
       ['DAPI_5','CD33','CD8','IDO1'],
       ['DAPI_6', 'CD16','CD21','Histone H3'],
       ['DAPI_7', 'Foxp3','Ki-67','HLA-DR'],
       ['DAPI_8', 'CD27', 'CD7','CD3'],
       ['DAPI_9', 'CD45RA','CD69','ZZ1'],
       ['DAPI_10', 'CD11b', 'CD141','CD117'],
       ['DAPI_11', 'GranzymeB','CollagenI','PD-L1'],
       ['DAPI_12', 'CD127','CD14','PD-1'],
       ['DAPI_13', 'aSMA','CD38','CD206'],
       ['DAPI_14', 'CD15','CD39', 'FOLR2'],
       ['DAPI_15', 'CD56','Vimentin','CD57'],
       ['DAPI_16', 'ZZ2', 'C1QA','ZZ3']]

uselessList=['DAPI_2','DAPI_3','DAPI_4','DAPI_5','DAPI_6','DAPI_7','DAPI_8','DAPI_9','DAPI_10','DAPI_11','DAPI_12','DAPI_13','DAPI_14','DAPI_15','DAPI_16','ZZ1','ZZ2','ZZ3']

stainDict={}
for i in range(len(cyc)):
    for j in range(len(CH)):
        item={cyc[i]+'_'+CH[j]:stain[i][j]}
        stainDict.update(item)

for sampleName in sample:
    for roiName in roi:
        imageDict = {}
        print(sampleName+'_'+roiName)
        cycID=0;
        for cycName in cyc:
            cycId=cycID+1
            print(cycName)
            folderRoot = Root + sampleName + '\\' + cycName + '_reg00' + roiName + '\\'
            for CHName in CH:
                stainName=stainDict[cycName+'_'+CHName]
                if stainName not in uselessList:
                    imageAll=np.zeros([1440,1920,9])
                    k=0
                    for posName in Pos:
                        tiffFileName=roiName+'_'+posName+'_Z001_'+CHName+'.tif'
                        tiffFileRoot = folderRoot + tiffFileName
                        tif = TIFF.open(tiffFileRoot, mode='r')
                        image_tif = tif.read_image(tiffFileName)
                        if CHName=='CH3':
                            bgFolderRoot_1=Root + sampleName + '\\' + 'cyc001' + '_reg00' + roiName + '\\'
                            bgFolderRoot_18=Root + sampleName + '\\' + 'cyc018' + '_reg00' + roiName + '\\'

                            bgtiffFileRoot_1=bgFolderRoot_1+tiffFileName
                            bgtiffFileRoot_18=bgFolderRoot_18+tiffFileName

                            bgtif_1 = TIFF.open(bgtiffFileRoot_1, mode='r')
                            bgimage_tif_1 = bgtif_1.read_image(bgtiffFileRoot_1)
                            bgtif_18 = TIFF.open(bgtiffFileRoot_18, mode='r')
                            bgimage_tif_18 = bgtif_18.read_image(bgtiffFileRoot_18)
                            unitSample=np.uint16(np.abs(np.int16(bgimage_tif_1-bgimage_tif_18))/16)
                            image_tif=image_tif-bgimage_tif_1+unitSample*cycId
                            ZZZZ=image_tif.astype(np.int16)
                            image_tif[ZZZZ<0]=0
                        imageAll[:,:,k]=image_tif;
                        k=k+1
                    cImage=tiffCombine(imageAll)
                    item_1={stainDict[cycName+'_'+CHName]:cImage}
                    imageDict.update(item_1)
        matFileName='D:\\CODEX\\CODEX2\\savemat\\'+sampleName+'_'+roiName+'.mat'
        sio.savemat(matFileName,imageDict)







