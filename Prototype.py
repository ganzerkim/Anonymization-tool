# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 15:39:29 2022

@author: Mingeon Kim, CT/MI Research Collaboration Scientist, SIEMENS Healthineers, Korea
"""

import glob, pylab, pandas as pd
import pydicom, numpy as np
from os import listdir
from os.path import isfile, join
import cv2 as cv

import matplotlib.pylab as plt
import numpy as np

import hmac
import binascii
import hashlib
import random

import os
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import * # __all__
from tkinter import filedialog
from PIL import Image


root = Tk()
root.title("SIEMENS MI Anonymization Tool")

def add_file():
    files = filedialog.askdirectory(title="추가할 파일경로를 선택하세요", \
        initialdir=r".\Desktop")
        # 최초에 사용자가 지정한 경로를 보여줌

    # 사용자가 선택한 파일 목록
    list_file.insert(END, files)

# 선택 삭제
def del_file():
    #print(list_file.curselection())
    for index in reversed(list_file.curselection()):
        list_file.delete(index)


# 추사 경로 (폴더)
def browse_dest_loadpath():
    folder_selected = filedialog.askdirectory()
    if folder_selected == "": # 사용자가 취소를 누를 때
        print("폴더 선택 취소")
        return
    #print(folder_selected)
    txt_dest_loadpath.delete(0, END)
    txt_dest_loadpath.insert(0, folder_selected)


# 저장 경로 (폴더)
def browse_dest_savepath():
    folder_selected = filedialog.askdirectory()
    if folder_selected == "": # 사용자가 취소를 누를 때
        print("폴더 선택 취소")
        return
    #print(folder_selected)
    txt_dest_savepath.delete(0, END)
    txt_dest_savepath.insert(0, folder_selected)
    
    
def hash_acc(num, length, sideID):
   try:
       siteID = str.encode(sideID)
       num = str.encode(num)
                              # hash
       m = hmac.new(siteID, num, hashlib.sha256).digest()
                              #convert to dec
       m = str(int(binascii.hexlify(m),16))
                              #split till length
       m=m[:length]
       return m
   except Exception as e:
          print("Something went wrong hashing a value :(")
          return

def anony():
    
    option_type = cmb_width.get()
    
    if option_type == "Protocol list-up":
        
        images_path = txt_dest_loadpath.get()
        print(images_path)
        
        path_tmp = []
        name_tmp = []
        
        for (path, dir, files) in os.walk(images_path):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
        
                if ext == '.dcm' or '.IMA':
                    print("%s/%s" % (path, filename))
                    path_tmp.append(path)
                    name_tmp.append(filename)
        dcm_tmp = []
        print("파일 로딩 중 입니다~ 처리 데이터 양이 많을 수록 오래 기다려주셔야 합니다 ㅠㅠ")
        for i in range(len(path_tmp)):
            dcm_p = pydicom.dcmread(path_tmp[i] + '/' + name_tmp[i], force = True)
            dcm_tmp.append(dcm_p)
    

        print("Scan 프로토콜 별로 폴더를 정리 중 입니다. 처리 데이터 양이 많을 수록 오래 기다려주셔야 됩니다.")


        folder_name = sorted(listdir(str(images_path)), key = int)

        idx = 0;

        savedir = txt_dest_savepath.get()
        if not(os.path.exists(savedir)):
            os.mkdir(savedir)
    
        for idx in range(0, len(name_tmp)):
    
            dcm_tmp = pydicom.dcmread(path_tmp[idx] + '/' +  name_tmp[idx])
            #dcm_tmp.PatientName = "777777"  # Patient Name    
    
            savedir2 = os.path.join(savedir +'/' + str(folder_name[0]) + '/' + str(dcm_tmp.AccessionNumber) + '/' + str(dcm_tmp.SeriesDescription))
            if not(os.path.exists(savedir2)):
                os.makedirs(savedir2)
        
            dcm_tmp.save_as(savedir2 + '/' + str(dcm_tmp.SeriesInstanceUID) + str(idx) + ".dcm")
            print("Total " + str(i) + " dataset 중 " + str(idx))
        
            progress = (idx + 1) / len(name_tmp) * 100 # 실제 percent 정보를 계산
            p_var.set(progress)
            progress_bar.update()
    
    
        msgbox.showinfo("알림", "교수님~! Series별 폴더정리가 완료되었습니다. 2번을 실행하여 익명화를 진행해 주세요~")

    else:
        
        start_study_num = txt_studynumb.get()
        print(start_study_num)
        save_path = txt_dest_savepath.get()
    

# 이미지 통합
def merge_image():
    # print("가로넓이 : ", cmb_width.get())
    # print("간격 : ", cmb_space.get())
    # print("포맷 : ", cmb_format.get())

    try:
        # 가로넓이
        img_width = cmb_width.get()
        if img_width == "원본유지":
            img_width = -1 # -1 일때는 원본 기준으로
        else:
            img_width = int(img_width)

        # 간격
        img_space = cmb_space.get()
        if img_space == "좁게":
            img_space = 30
        elif img_space == "보통":
            img_space = 60
        elif img_space == "넓게":
            img_space = 90
        else: # 없음
            img_space = 0

        # 포맷
        img_format = cmb_format.get().lower() # PNG, JPG, BMP 값을 받아와서 소문자로 변경

        #####################################

        images = [Image.open(x) for x in list_file.get(0, END)]    

        # 이미지 사이즈 리스트에 넣어서 하나씩 처리
        image_sizes = [] # [(width1, height1), (width2, height2), ...]
        if img_width > -1:
            # width  값 변경
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            # 원본 사이즈 사용
            image_sizes = [(x.size[0], x.size[1]) for x in images]

        # 계산식
        # 100 * 60 이미지가 있음. -> width 를 80 으로 줄이면 height 는?
        # (원본 width) : (원본 height) = (변경 width) : (변경 height)
        #     100      :     60       =      80      :     ?
        #      x       :     y        =      x'      :     y'
        #    xy' = x'y
        #    y' = x'y / x -> 이 식을 적용
        #  100:60=80:48

        # 우리 코드에 대입하려면?
        # x = width = size[0]
        # y = height = size[1]
        # x' = img_width # 이 값으로 변경 해야 함
        # y' = x'y / x = img_width * size[1] / size[0]

        widths, heights = zip(*(image_sizes))

        # 최대 넓이, 전체 높이 구해옴
        max_width, total_height = max(widths), sum(heights)
        
        # 스케치북 준비
        if img_space > 0: # 이미지 간격 옵션 적용
            total_height += (img_space * (len(images) - 1))

        result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255)) # 배경 흰색
        y_offset = 0 # y 위치

        for idx, img in enumerate(images):
            # width 가 원본유지가 아닐 때에는 이미지 크기 조정
            if img_width > -1:
                img = img.resize(image_sizes[idx])

            result_img.paste(img, (0, y_offset))
            y_offset += (img.size[1] + img_space) # height 값 + 사용자가 지정한 간격

            progress = (idx + 1) / len(images) * 100 # 실제 percent 정보를 계산
            p_var.set(progress)
            progress_bar.update()

        # 포맷 옵션 처리
        file_name = "nado_photo." + img_format
        dest_path = os.path.join(txt_dest_path.get(), file_name)
        result_img.save(dest_path)
        msgbox.showinfo("알림", "작업이 완료되었습니다.")
    except Exception as err: # 예외처리
        msgbox.showerror("에러", err)

# 시작
def start():
    # 각 옵션들 값을 확인
    # print("가로넓이 : ", cmb_width.get())
    # print("간격 : ", cmb_space.get())
    # print("포맷 : ", cmb_format.get())

    # 파일 목록 확인
    if len(txt_dest_loadpath.get()) == 0:
        msgbox.showwarning("경고", "추가하실 상위 폴더경로를 선택하세요")
        return

    # 저장 경로 확인
    if len(txt_dest_savepath.get()) == 0:
        msgbox.showwarning("경고", "저장 경로를 선택하세요")
        return

    # 이미지 통합 작업
    anony()



photo = PhotoImage(file="./check.png")
label2 = Label(root, image=photo)
label2.pack()

# 추가 경로 프레임
loadpath_frame = LabelFrame(root, text="Source data 경로")
loadpath_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_dest_loadpath = Entry(loadpath_frame)
txt_dest_loadpath.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) # 높이 변경

btn_dest_loadpath = Button(loadpath_frame, text="찾아보기", width=10, command=browse_dest_loadpath)
btn_dest_loadpath.pack(side="right", padx=5, pady=5)

# 저장 경로 프레임
savepath_frame = LabelFrame(root, text="저장경로")
savepath_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_dest_savepath = Entry(savepath_frame)
txt_dest_savepath.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) # 높이 변경

btn_dest_savepath = Button(savepath_frame, text="찾아보기", width=10, command=browse_dest_savepath)
btn_dest_savepath.pack(side="right", padx=5, pady=5)

# 옵션 프레임
frame_option = LabelFrame(root, text="Anonymization for cohort study.")
frame_option.pack(padx=15, pady=15, ipady=1)
################################################################

# 실행할 옵션 선택
lbl_option = Label(frame_option, text="실행옵션", width=8)
lbl_option.pack(side="left", padx=5, pady=5)

# 실행 옵션 콤보
opt_width = ["Protocol list-up", "Anonymization"]
cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width, width=10)
cmb_width.current(0)
cmb_width.pack(side="left", padx=5, pady=5)

# Study number 옵션
lbl_studynumb = Label(frame_option, text="Study Number", width = 10)
lbl_studynumb.pack(side="top", padx = 5, pady = 0, fill="both", expand=True)

txt_studynumb = Text(frame_option, width=5, height = 1)
txt_studynumb.pack(pady = 5)
txt_studynumb.insert(END, "0")

# 익명화 이름 옵션
lbl_studyname = Label(frame_option, text="Study Name", width = 10)
lbl_studyname.pack(side="top", padx = 5, pady = 0, ipadx = 5, fill="both", expand=True)

txt_studyname = Text(frame_option, width=10, height = 1)
txt_studyname.pack(pady = 5)
txt_studyname.insert(END, "ex) R-")


##################################################################
# 진행 상황 Progress Bar
frame_progress = LabelFrame(root, text="진행상황")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5)

# 실행 프레임
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="닫기", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="시작", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False, False)
root.mainloop()