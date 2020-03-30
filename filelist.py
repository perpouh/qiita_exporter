import os
if __name__ == '__main__':
  filelist = os.listdir('../blog/qiita')
  for item in filelist:
    print("['qiita/"+item[-4::-1][-1::-1]+"', '"+item[-4::-1][-1::-1]+"'],")