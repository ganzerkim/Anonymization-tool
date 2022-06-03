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
import shutil

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
        # print("폴더 선택 취소")
        return
    #print(folder_selected)
    txt_dest_loadpath.delete(0, END)
    txt_dest_loadpath.insert(0, folder_selected)


# 저장 경로 (폴더)
def browse_dest_savepath():
    folder_selected = filedialog.askdirectory()
    if folder_selected == "": # 사용자가 취소를 누를 때
        # print("폴더 선택 취소")
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
    try:
        
        option_type = cmb_width.get()
    
        if option_type == "Protocol list-up":
            
            # images_path = txt_dest_loadpath.get()
            images_path = list_file.get(0, END)
            # print(images_path)
            # print(len(images_path))
            
            
            path_tmp = []
            name_tmp = []
            
            f_i = 0;
            for f_i in range(len(images_path)):
                for (path, dir, files) in os.walk(images_path[f_i]):
                    for filename in files:
                        ext = os.path.splitext(filename)[-1]
                        
                        if ext == '.dcm' or '.IMA':
                            print("%s/%s" % (path, filename))
                            path_tmp.append(path)
                            name_tmp.append(filename)
                        
                # for (path, dir, files) in os.walk(images_path):
                #     for filename in files:
                #         ext = os.path.splitext(filename)[-1]
                            
                            #         if ext == '.dcm' or '.IMA':
                            #             print("%s/%s" % (path, filename))
                            #             path_tmp.append(path)
                            #             name_tmp.append(filename)
            
            dcm_tmp = []
            # print("파일 로딩 중 입니다~ 처리 데이터 양이 많을 수록 오래 기다려주셔야 합니다 ㅠㅠ")
            idx = 0;
            i = 0
            for i in range(len(path_tmp)):
                dcm_p = pydicom.dcmread(path_tmp[i] + '/' + name_tmp[i], force = True)
                dcm_tmp.append(dcm_p)
                
                progress = (idx + i + 1) / (len(name_tmp) + len(path_tmp)) * 100 # 실제 percent 정보를 계산
                p_var.set(progress)
                progress_bar.update()
        
    
            # print("Scan 프로토콜 별로 폴더를 정리 중 입니다. 처리 데이터 양이 많을 수록 오래 기다려주셔야 됩니다.")
    
    
            #folder_name = sorted(listdir(str(images_path[f_i])), key = int)
    
           
    
            savedir = txt_dest_savepath.get()
            if not(os.path.exists(savedir)):
                os.mkdir(savedir)
                
            for idx in range(0, len(name_tmp)):
                dcm_tmp = pydicom.dcmread(path_tmp[idx] + '/' +  name_tmp[idx])
                #dcm_tmp.PatientName = "777777"  # Patient Name    
                savedir2 = os.path.join(savedir +'/' + str("Protocol_list-up") + '/' + str(dcm_tmp.AccessionNumber) + '/' + str(dcm_tmp.SeriesDescription))
                if not(os.path.exists(savedir2)):
                    os.makedirs(savedir2)
            
                dcm_tmp.save_as(savedir2 + '/' + str(dcm_tmp.SeriesInstanceUID) + str(idx) + ".dcm")
                print("Total " + str(i) + " dataset 중 " + str(idx))
            
                progress = (idx + i + 1) / (len(name_tmp) + len(path_tmp))  * 100 # 실제 percent 정보를 계산
                p_var.set(progress)
                progress_bar.update()
            msgbox.showinfo("알림", "교수님~! Series별 폴더정리가 완료되었습니다. 익명화를 원하시면 다음을 진행해 주세요~")
    
        else:      
            images_path = list_file.get(0, END)
            print(images_path)
            print(len(images_path))     
            
            path_tmp = []
            name_tmp = []
            
            f_i = 0;
            for f_i in range(len(images_path)):
                for (path, dir, files) in os.walk(images_path[f_i]):
                    for filename in files:
                        ext = os.path.splitext(filename)[-1]
                        
                        if ext == '.dcm' or '.IMA':
                            print("%s/%s" % (path, filename))
                            path_tmp.append(path)
                            name_tmp.append(filename)
                        
                # for (path, dir, files) in os.walk(images_path):
                #     for filename in files:
                #         ext = os.path.splitext(filename)[-1]
                            
                            #         if ext == '.dcm' or '.IMA':
                            #             print("%s/%s" % (path, filename))
                            #             path_tmp.append(path)
                            #             name_tmp.append(filename)
            print(path_tmp[0])
            print(name_tmp[0])
            print(len(path_tmp[0]))
            print(len(name_tmp[0]))
            
            path_tmp_1 = os.path.abspath(os.path.join(path_tmp[0], os.pardir))
            path_tmp_2 = os.path.abspath(os.path.join(path_tmp_1, os.pardir))
            
            
            
            dcm_tmp = []
            # print("파일 로딩 중 입니다~ 처리 데이터 양이 많을 수록 오래 기다려주셔야 합니다 ㅠㅠ")
            idx = 0;
            i = 0
            for i in range(len(path_tmp)):
                dcm_p = pydicom.dcmread(path_tmp[i] + '/' + name_tmp[i], force = True)
                dcm_tmp.append(dcm_p)
                
                progress = (idx + i + 1) / (len(name_tmp) + len(path_tmp)) * 100 # 실제 percent 정보를 계산
                p_var.set(progress)
                progress_bar.update()
        
    
            #folder_name = sorted(listdir(str(images_path[f_i])), key = int)
    
            savedir = txt_dest_savepath.get()
            if not(os.path.exists(savedir)):
                os.mkdir(savedir)
            
            
            # dd = 0
            # AccNumb = []
            # for dd in range(len(name_tmp)):
            #     dcm_p = pydicom.dcmread(path_tmp[dd] + '/' +  name_tmp[dd])
            #     if dcm_p.AccessionNumber in AccNumb:
            #         print("We already have this Accnumber.")
            #     else:
            #         AccNumb.append(dcm_p.AccessionNumber)
            start_study_num = txt_studynumb.get()
            cohort_name = txt_studyname.get()
            AccNumb = []
            ac = -1
            cohort_num = []
            acc_inform = []
            for idx in range(0, len(name_tmp)):
                
                dcm_p = pydicom.dcmread(path_tmp[idx] + '/' +  name_tmp[idx])
                dcm_tmp = dcm_p    
                savedir3 = os.path.join(savedir +'/' + str("Anonymization"))
                savedir2 = os.path.join(savedir +'/' + str("Anonymization") + '/' + str(dcm_p.AccessionNumber) + '/' + str(dcm_p.SeriesDescription))
                if not(os.path.exists(savedir2)):
                    os.makedirs(savedir2)
                if dcm_p.AccessionNumber in AccNumb:
                    print("We already have this Accnumber.")
                else:
                    AccNumb.append(dcm_p.AccessionNumber)
                    ac += 1
                    cohort_num.append(cohort_name + '-' + str(ac + int(start_study_num)))
                    acc_inform.append(str(dcm_p.AccessionNumber))
                
                #dcm_tmp.PatientName = hash_acc(dcm_tmp.PatientID,16, "Korhospital1" ) # Patient Name
                dcm_p.PatientName = cohort_name + '-' + str(ac + int(start_study_num)) # Patient Name
                dcm_p.PatientBirthDate = "777777" # Patient Birtday 
                dcm_p.PatientID = hash_acc(dcm_p.PatientID,16, "Korhospital") # Patient ID
                dcm_p.AccessionNumber = hash_acc(dcm_p.AccessionNumber,16,"Korhospital1") # Accession number 
                # dcm_p.StudyID = hash_acc(dcm_p.studyID,16,"Korhospital1") # Patient ID
                dcm_p.StudyInstanceUID = hash_acc(dcm_p.StudyInstanceUID,16,"Korhospital1")
                dcm_p.SeriesInstanceUID = hash_acc(dcm_p.SeriesInstanceUID,16,"Korhospital1")
                dcm_p.SOPInstanceUID = hash_acc(dcm_p.SOPInstanceUID,16,"Korhospital1")
                dcm_p.InstitutionName = "Annoymized"
                dcm_p.StudyID = hash_acc(dcm_p.StudyID,16,"Korhospital1")
                if "ProcedureCodeSequence" in dcm_p:
                    dcm_p.ProcedureCodeSequence[0].CodeValue = "Annoymized"
                if "OtherPatientIDsSequence" in dcm_p:
                    dcm_p.OtherPatientIDsSequence[0].PatientID = hash_acc(dcm_p.PatientID,16, "Korhospital")
                if "RequestedProcedureCodeSequence" in dcm_p:
                    dcm_p.RequestedProcedureCodeSequence[0].CodeValue = "Annoymized"
                if "RequestAttributesSequence" in dcm_p:
                    dcm_p.RequestAttributesSequence[0].ScheduledProcedureStepID = "Annoymized"
                    dcm_p.RequestAttributesSequence[0].RequestedProcedureID = "Annoymized"
    
                #RequestedProcedureCodeSequence
                    
                dcm_p.save_as(savedir2 + '/' + str(dcm_p.SeriesDescription) + str(idx) + ".dcm")
                print("Total " + str(i) + " dataset 중 " + str(idx))
                
                
                print(ac)
            
                progress = (idx + i + 1) / (len(name_tmp) + len(path_tmp))  * 100 # 실제 percent 정보를 계산
                p_var.set(progress)
                progress_bar.update()
            
            
            annoy = {'익명화 이름': cohort_num, 'Accession Number 정보': acc_inform}
            df = pd.DataFrame(annoy)
            # .to_csv 
            # 최초 생성 이후 mode는 append
            if not os.path.exists(savedir3 + '/information.csv'):
                df.to_csv(savedir3 + '/information.csv', index=False, mode='w', encoding='utf-8-sig')
            else:
                df.to_csv(savedir3 + '/information.csv', index=False, mode='a', encoding='utf-8-sig', header=False) 
            
            for remove_path in images_path:
                shutil.rmtree(remove_path)
            msgbox.showinfo("알림", "익명화가 완료되었습니다~ Anonymization 폴더를 확인해주세요.")
            
    except Exception as err: # 예외처리
        msgbox.showerror("에러", err + ", Research Scientist에게 문의해주세요!")
        
        
        
'''
shutil.rmtree(r"path")
'''      

# 시작
def start():
    # 각 옵션들 값을 확인
    # print("가로넓이 : ", cmb_width.get())
    # print("간격 : ", cmb_space.get())
    # print("포맷 : ", cmb_format.get())

    # 파일 목록 확인
    if list_file.size() == 0:
        msgbox.showwarning("경고", "폴더 경로를 추가해주세요")
        return

    # 저장 경로 확인
    if len(txt_dest_savepath.get()) == 0:
        msgbox.showwarning("경고", "저장 경로를 선택해주세요")
        return

    # 이미지 통합 작업
    anony()



photo = PhotoImage(file="./pics/siemens.png")
label2 = Label(root, image=photo)
label2.pack()

# 파일 프레임 (파일 추가, 선택 삭제)
file_frame = Frame(root)
file_frame.pack(fill="x", padx=5, pady=5) # 간격 띄우기

btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text="폴더추가", command=add_file)
btn_add_file.pack(side="left")

btn_del_file = Button(file_frame, padx=5, pady=5, width=12, text="선택삭제", command=del_file)
btn_del_file.pack(side="right")

# 리스트 프레임
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=5, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# # 추가 경로 프레임
# loadpath_frame = LabelFrame(root, text="Source data 경로")
# loadpath_frame.pack(fill="x", padx=5, pady=5, ipady=5)

# txt_dest_loadpath = Entry(loadpath_frame)
# txt_dest_loadpath.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) # 높이 변경

# btn_dest_loadpath = Button(loadpath_frame, text="찾아보기", width=10, command=browse_dest_loadpath)
# btn_dest_loadpath.pack(side="right", padx=5, pady=5)

# 저장 경로 프레임
savepath_frame = LabelFrame(root, text="저장경로")
savepath_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_dest_savepath = Entry(savepath_frame)
txt_dest_savepath.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) # 높이 변경

btn_dest_savepath = Button(savepath_frame, text="찾아보기", width=10, command=browse_dest_savepath)
btn_dest_savepath.pack(side="right", padx=5, pady=5)

# 옵션 프레임
frame_option = LabelFrame(root, text="*Anonymization 시 추가하신 폴더들은 삭제됩니다.*")
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

txt_studynumb = Entry(frame_option, width=5)
txt_studynumb.pack(pady = 5)
txt_studynumb.insert(END, "0")

# 익명화 이름 옵션
lbl_studyname = Label(frame_option, text="Study Name", width = 10)
lbl_studyname.pack(side="top", padx = 5, pady = 0, ipadx = 5, fill="both", expand=True)

txt_studyname = Entry(frame_option, width=10)
txt_studyname.pack(pady = 5)
txt_studyname.insert(END, "ex) Sub")


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