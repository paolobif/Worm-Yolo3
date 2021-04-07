import os
import sys
import cv2
import csv
import tqdm
import pandas as pd
import random
import numpy as np



def draw_on_im(frame, outputs, out_path, writer, text=None):
        """Takes img, then coordinates for bounding box, and optional text as arg"""
        img = frame
        for output in outputs:
            #output = [int(n) for n in output]
            frameN, x, y, text, *_ = output
            
            # Draw rectangles
            if text is not None: 
                text = str(text)
                cv2.putText(img, text, (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,102,102), 2)
        ## write image to path
        #cv2.imwrite(out_path, img)
        writer.write(img)



if __name__ == "__main__":
    # declare source directory and out path
    """
    IMG_DIR is path to the folder with the images
    OUT_PATH is the path to the csv file you would like the output to go to
    i.e './output/sample.csv'
    """
    VID_PATH = sys.argv[1]
    CSV_SORT_PATH = sys.argv[2]
    OUT_PATH = sys.argv[3]
    
    
    vid = cv2.VideoCapture(VID_PATH)
    total_frame_count = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    video_name = os.path.basename(VID_PATH).strip('.avi')
    out_video_path = f"{OUT_PATH}/{os.path.basename(VID_PATH).strip('.avi')}_SORT.avi"

    df = pd.read_csv(CSV_SORT_PATH,names=('frame', 'x1', 'y1', 'x2', 'y2','label'))
    df['X']=df[['x1','x2']].mean(axis=1)
    df['Y']=df[['y1','y2']].mean(axis=1)
    df = df[['frame', 'X', 'Y','label']]
    unique = df["frame"].unique()
    
      
    while (1):
        ret, frame = vid.read()
        frame_count = vid.get(cv2.CAP_PROP_POS_FRAMES)
        print(frame_count)
        if frame_count == 1:
            height, width, channels = frame.shape
            print(height, width)
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter(out_video_path, fourcc, 10, (width, height), True)
        
        #print(frame_count)
        #frame_cur = int(frame_count)
        #print(frame_cur)
        filtval = df['frame'] == frame_count
        #print(filtval)
        csv_outputs = np.asarray(df[filtval])[:,:]
        print(csv_outputs)
        if csv_outputs is not None: 
            draw_on_im(frame,csv_outputs,out_video_path,writer)   
        
        
        if frame_count == total_frame_count:
            break
    writer.release()        