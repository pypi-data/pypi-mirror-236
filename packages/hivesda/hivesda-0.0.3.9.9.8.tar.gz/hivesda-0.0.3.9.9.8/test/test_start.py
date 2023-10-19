from hivesda import test
import os

# # setting cuda

device = "GPU"   # CPU or GPU
gpu = "0"        # set gpu numer
input_size = 300 # set image size e.g.) 300 -> (300x300)    
output_dir = "./"
run_model_path = "/workspace/output_custom_list/bgad_fas_10/weights/custom_tf_efficientnet_b6_conditional_flow_model_bottle.pt"
save_heatmap_path = ""
######################################################################################################################################################################
# set data
train_list = []
val_list = []
ng_list = []

val_normal_list = os.listdir("/workspace/Data_toptec_center_png300/bottle/test/good")
for v in val_normal_list:
    val_list.append(["/workspace/Data_toptec_center_png300/bottle/test/good/"+v,0,None,'good'])

total_ng_list = os.listdir("/workspace/Data_toptec_center_png300/bottle/test/NG")
for n in total_ng_list:
    ng_list.append(["/workspace/Data_toptec_center_png300/bottle/test/NG/"+n,1,"/workspace/Data_toptec_center_png300/bottle/ground_truth/NG/"+n.split(".")[0]+"_mask.png",'NG'])

val_list = val_list + ng_list
######################################################################################################################################################################



img_auc, pix_auc = test.main_single(device,gpu,input_size,val_list,run_model_path)
print(f'Image-AUC: {img_auc}, Pixel-AUC: {pix_auc} ')


