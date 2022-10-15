import os
import numpy as np
from PIL import Image
from PIL import ImageChops

##搜索指定的資料夾下重複的相片


def checkFileAllLevel(Path):
# walk 的方式則會將指定路徑底下所有的目錄與檔案陳列出來(包含子目錄以及子目錄底下的檔案)
#並將資料存進字典 vector

    vector = dict()

    #列出所有子目錄與子目錄底下所有的檔案
    for root, dirs, files in os.walk(Path):
        
        #列出目前讀取到的路徑
        print("path：", root)

        for f in files:
            #絕對路徑不會重複，故以此當 key 值，檔名作為 value 值
            vector[os.path.join(root, f)] = f
            print("- file：", f)
    
    print('\n合計共 ' + str(len(vector)) + ' 筆檔案')
    return vector    


def catchFileExtension(filename):
#擷取出副檔名(含點)
    
    ##該方式會受檔名含有相同的點號而受影響
    #print(filename.split('.')[1])
    #return filename.split('.')[1]

    #print(os.path.splitext(filename))
    #print(os.path.splitext(filename)[-1])

    return os.path.splitext(filename)[-1]


def mse(imageA, imageB):
#比較兩圖檔，值為 0 表示幾乎相似，超過 1 則表示差異
    image_err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    image_err /= float(imageA.shape[0] * imageA.shape[1])
	
    return image_err


###main
#目標路徑
#ex:'C:\\Users\\user\\Desktop\\'
yourPath = str(input('輸入目標路徑(亦可用拖曳的)：'))

total = dict()
total = checkFileAllLevel(yourPath)

#統計所有檔案的附檔名
#統計副檔名
sta = set()

for key, value in total.items():
#遍歷所有資料
    FileExtension = catchFileExtension(value)
    sta.add(FileExtension)

print('============================ ~ 結算啦 ~ ==========================')
print('所有副檔名統計名單：')

for target in sta:
    print(target, ' ', end = '')
print()
os.system('pause')


pointFileExtension = str(input('輸入指定副檔名，可以一次多個並以空白間隔：')).split(' ')
target_dict = {}

#過濾出指定的附檔名
for key, value in total.items():
#遍歷所有資料
    for FileExt in range(len(pointFileExtension)):
    #比對指定副檔名
        FileExtension = catchFileExtension(value)
        
        if FileExtension == pointFileExtension[FileExt]:
            #符合者保留
            target_dict[key] = value

count = 0
for key, value in target_dict.items():
    print(value)
    count += 1

print('共計 ', count, ' 筆\n')
os.system('pause')


file_link = list(target_dict.keys())
before_long = len(file_link)
del_count = 0

for main_file in file_link:
    main_file_compare = target_dict.pop(main_file)
#逐一作為主要比對目標
    
    #發生檔案讀取問題的一律略過
    try:
        main_file_size = os.path.getsize(main_file)
    except FileNotFoundError:
        continue
    
    print('- compare : ', main_file_compare)

    for match_file in target_dict:
    #逐一作為次要比對目標
        
        #發生檔案讀取問題的一律略過
        try:
            match_file_size = os.path.getsize(match_file[0])
        except FileNotFoundError:
            continue
        
        if main_file_size == match_file_size:
        #倘若尺寸相同才進行近一步比較
        
            print('\n-- Find same file size!')
            print(' 0 >> ', main_file, '\n 1 >> ', match_file[0], '\n')

            #讀入檔案
            with Image.open(main_file) as main_file_pic ,\
                 Image.open(match_file[0]) as match_file_pic:
                
                if main_file_pic.size == match_file_pic.size and \
                   main_file_pic.format == match_file_pic.format and \
                   ImageChops.difference(main_file_pic, \
                                         match_file_pic).getbbox() == None:
                #確認圖片大小、讀取格式(副檔名)、像素皆相符才進入刪除階段
                #選擇要保留下來的檔案名稱
                    
                    while(True):
                        leave_name = input('確認相同，輸入 0 or 1 決定保留的檔名：')
                        
                        if len(leave_name) == 0:
                            print('未輸入內容，請重新輸入...\n')
                        elif leave_name == '0':
                            break
                        elif leave_name == '1':
                            break
                        else:
                            print('例外答案，請重新輸入...\n')
                    
                    if os.path.isfile(main_file) == True:
                    #確認檔案存在再進行刪除
                    #沒關閉的話，操作上可能會發生權限問題
                    # PermissionError
                        main_file_pic.close()
                        match_file_pic.close()

                        #依據要保留的選擇刪除相對的選擇
                        if leave_name == '0':
                            os.remove(match_file[0])
                        elif leave_name == '1':
                            os.remove(main_file)
                                
                        print('已排除相同圖片 ', main_file_compare, '\n')
                        del_count += 1
                        break

after_long = before_long - del_count
print('Finish ~')
print('Before number: ', before_long, ' / After number: ', after_long)
os.system('pause')           
            
