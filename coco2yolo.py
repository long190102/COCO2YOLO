import re
 import string
 import numpy as np
 import os
 import glob
 import json
 keypoint =
 ["nose","left_eye","right_eye","left_ear","right_ear","left_shoulder","right
 _shoulder","left_elbow","right_elbow","left_wrist","right_wrist","left_hip",
 "right_hip","left_knee","right_knee","left_ankle","right_ankle"]
 output = np.zeros((17,3))
 pointcoord = []
 path = "YOUR PATH TO LABEL FILE"
 os.chdir(path)
 my_files =
 glob.glob(r'YOUR PATH TO LABEL FILE*.json')
 file_name = []
 for i in range(len(my_files)):
 file_name.append(my_files[i].split("/")[-1])
 #print(my_files)

 #width and height of the image (for batch norm)
 w = 848
 h = 480
 
 string = ""
 namecount = 0
 for name in my_files:
 with open(name,'r', encoding = "utf-8") as file:
 data = json.load(file)
 image_path = data["imagePath"]
 image_width = data["imageWidth"]
 image_height = data["imageHeight"]
 txt_file_name = image_path.replace(".jpg",".txt")
 print(txt_file_name)
 num_object = 0
 for shape in data["shapes"]:
 # label = shape["label"]
 # points = shape["points"]
 # shape_type = shape["shape_type"]
group_id = shape["group_id"]
 if group_id != None and num_object< group_id:
 num_object = group_id
 output = np.zeros((num_object+1,56))
 keypointarray = np.zeros((num_object+1,17,3))
 bb_count = 0
 for shape in data["shapes"]:
 label = shape["label"]
 points = shape["points"]
 shape_type = shape["shape_type"]
 group_id = shape["group_id"]
 # print(shape)
 # print(label)
 # print(shape_type)
 # print(group_id)
 # print(points)
 count = 0
 if label != 'person':
 for i in range(num_object+1):
 for j in range(17):
 if label == keypoint[j] and group_id == i:
 keypointarray[i][j][0] =
 points[0][0]/image_width
 points[0][1]/image_height
 keypointarray[i][j][1] =
 keypointarray[i][j][2] = 2
 if label == 'person':
 if bb_count < num_object+1:
 w = (points[1][0]- points[0][0])
 h = (points[2][1]- points[1][1])
 center_x = points[0][0]+w/2
 center_y = points[0][1]+h/2
 output[bb_count][0] = 0
 output[bb_count][1] = center_x/image_width
 output[bb_count][2] = center_y/image_height
 output[bb_count][3] = w/image_width
 output[bb_count][4] = h/image_height
 bb_count +=1
 #print(output)
 for i in range (num_object+1):
 count = 5
 for j in range (17):
 output[i][count] = keypointarray[i][j][0]
 count +=1
 output[i][count] = keypointarray[i][j][1]
 count +=1
 output[i][count] = keypointarray[i][j][2]
 count +=1
 #print(output)
 text_file = open(txt_file_name,'+w')
 for i in range(num_object +1):
 string = ""
 for j in range(56):
 if j == 0:
 string = string + "0 "
else:
 string = string + str(round(output[i][j],6)) + " "
 string = string + "\n"
 text_file.write(string)
 #text_file.write("\n")
 text_file.close()
 #print(keypointarray)
