#距離・種類判定AI"yolov5s"を学習

import torch
import pandas
import requests
import cv2

# PyTorch Hubから学習済みモデルをダウンロード 
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
# 検出できる物体を表示する(80種類)
#print(model.names)

def Let_there_be_light():

    import tkinter as tk
    import time
    from time import sleep

    root = tk.Tk()
    root.title("Tkinter test")
    root.geometry("200x200")
    label = tk.Label(root, text="This is light")
    #表示
    label.grid()

    root.after(100, lambda: root.destroy()) 

    root.mainloop()



############30fpsでカメラを動かす################

import cv2
import numpy as np
import time
import tkinter as tk
from time import sleep

# Webカメラ
DEVICE_ID = 0 

WIDTH = 800
HEIGHT = 600
FPS = 30

def decode_fourcc(v):
        v = int(v)
        return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

def main():
    cap = cv2.VideoCapture (DEVICE_ID)
    rgb = []

    # フォーマット・解像度・FPSの設定
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    # フォーマット・解像度・FPSの取得
    fourcc = decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC))
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("fourcc:{} fps:{}　width:{}　height:{}".format(fourcc, fps, width, height))
    
    #状態変数の定義
    k=0
    x_times=[]
    step_times=[]
    move_times=[]
    Timers=[]
    t_cnt_stop=[]
    t_cnt_move=[]
    s_stop=0
    name ='angel'
    tester=[]
    

    while True:
        name_list = []
        xmin_list = []
        ymin_list = []
        xmax_list = []
        width_list =[]
        height_list=[]
        
        t1 = time.time() #毎回のループの時間を取得
        
        # カメラ画像取得
        _, frame = cap.read()
        if(frame is None):
            continue

        # 画像表示
        cv2.imshow('frame', frame)
        
        #rgbを取得
        rgb=np.array(frame)
        
        #AINI 
        results = model(frame)  # 画像パスを設定し、物体検出を行う
        objects = results.pandas().xyxy[0]  # 検出結果を取得してobjectに格納
        # objectに格納したデータ
        # => バウンディングBOX左上のx座標とy座標、信頼度、クラスラベル、物体名
        
        
        
        

        for i in range(len(objects)):
            names = objects.name[i]
            name_list.append(names)
            
        #print(len(objects))    
            
        for i in range(len(objects)+1):
            
            #print('ATTEND!!!!!!!!!!!!!')
            
            if len(objects)==0:
                xmin = 0
                ymin = 0
                xmax = 0
                width = 0
                height = 0
                
                
            else:
                if name_list[i]=='person':
                    xmin = objects.xmin[i]
                    ymin = objects.ymin[i]
                    xmax = objects.xmax[i]
                    width = objects.xmax[i] - objects.xmin[i]
                    height = objects.ymax[i] - objects.ymin[i]
                    
                
                if name_list[i]!='person':
                    xmin = 0
                    ymin = 0
                    xmax = 0
                    width = 0
                    height = 0
                    
            name_list.append(name)
            xmin_list.append(xmin)
            ymin_list.append(ymin)
            width_list.append(width)
            height_list.append(height)

            
            
        
            
    
        max_value=max(height_list)
        Number=height_list.index(max_value)
        
#         print(Number)
        
        xmin = name_list[Number]
        ymin = xmin_list[Number]
        xmax = ymin_list[Number]
        width = width_list[Number]
        height = height_list[Number]
        
      
        # キュー入力判定(1msの待機)
        # waitKeyがないと、imshow()は表示できない
        # 'q'をタイプされたらループから抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        #光点滅判断
        f_i=0.002344/2 #1pixelあたり何mm
        g_i=f_i*1500 #焦点距離*pixel
        h_i=(height+0.001)+f_i #写真内での物体の高さ
        w_i=(width+0.001)*f_i #写真内での物体の幅
        #w_i=xmax*f_i #幅からxmaxへ変更
        height_true=1690 #人間の伸長169cmほどと仮定
        width_true=350 #人間の肩幅を35cm程度と仮定
        
        y=height_true*g_i/h_i #カメラと人との推定距離
        x=width_true*g_i/w_i #人の推定幅
        
        
        
        
        
        if k==0:
            x_times.append(x)
            Timers.append(t1)
            
        else:
            x_times.append(x)
            Timers.append(t1)
            delta_t=t1-Timers[k-1]
            x_v=(x-x_times[k-1])/delta_t
            

    
    
            if abs(x_v)<500 and width!=0: #秒速5センチメートル以内なら停止判定をする
#             if abs(x_v)<500: #秒速5センチメートル以内なら停止判定をする
                
                t2=time.time()
                t_cnt_stop.append(t2)
                
                t_cnt_move=[]
                
                
                
#             if abs(x_v)>500 or width==0:
            if abs(x_v)>500 or width==0:
                t3=time.time()
                t_cnt_move.append(t3)
                
                t_cnt_stop=[]
                
            
                
                    
            
            
        if len(t_cnt_stop)>=1:
            T_cnt_UP=t_cnt_stop[-1]-t_cnt_stop[0]
        else:
            T_cnt_UP=0


        if len(t_cnt_move)>=1:
            T_cnt_DOWN=t_cnt_move[-1]-t_cnt_move[0]
        else:
            T_cnt_DOWN=0

        #print("name,",name)
#         print("T_cnt_UP",T_cnt_UP)
        print("T_cnt_DOWN",T_cnt_DOWN)



        if T_cnt_UP>=3:
            Let_there_be_light()
#             step_times=[]
#             t_cnt_move=[]
            tester.append(1)#ライト保持

        if T_cnt_DOWN<3 and len(tester)>1:
            Let_there_be_light()
            print('amazing')


        if T_cnt_DOWN>=3: #約3秒停止判定が出た場合、ライトを消し、step_itemsをリセットする
            tester=[]
#             step_times=[]
#             t_cnt_stop=[]
            print('!!!!!!!!!STOP!!!!!!!!!')


                
        k=k+1 #時刻更新
    
    # VideoCaptureオブジェクト破棄
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()