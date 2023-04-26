#csv df로 불러오기
import pandas as pd
df=pd.read_csv('jobkorea.csv')

# 코드 순서 변경 하면 안됩니다! 
df.drop(df.index[28636: 28638],inplace=True) #28636~28638
df.drop(df.index[27273],inplace= True)
df.drop(df.index[26109 :26114],inplace=True) #26109 ~26113
df.drop(df.index[25158 : 25160],inplace=True) #25158 ~25159
df.drop(df.index[25011:25015],inplace=True) #25011 ~25014
df.drop(df.index[22693:22696],inplace=True) #22693 ~22695
df.drop(df.index[21204:21207],inplace=True) #21204 ~21206
df.drop(df.index[19898:19902],inplace=True) #19898~19901
df.drop(df.index[16941],inplace= True)
df.drop(df.index[16927:16931],inplace=True) #16927~16930
df.drop(df.index[16894:16898],inplace=True) #16894~16897
df.drop(df.index[16581:16585],inplace=True) #16581~16584
df.drop(df.index[16305],inplace= True)
df.drop(df.index[16128:16130],inplace=True) #16128~16129
df.drop(df.index[13519],inplace= True)
df.drop(df.index[9580:9582],inplace=True) #9580~9581
df.drop(df.index[9087:9090],inplace=True) #9087~9089 
df.drop(df.index[7915:7917],inplace=True) # 7915~7916
df.drop(df.index[7497:7500],inplace=True) # 7497~7499
df.drop(df.index[6644],inplace= True)
df.drop(df.index[1526],inplace= True)
df.drop(df.index[1207:1210],inplace=True) #1207~1209
df.drop(df.index[1179:1186],inplace=True) # 1179, 1180, 1181, 1182, 1183, 1184, 1185 삭제