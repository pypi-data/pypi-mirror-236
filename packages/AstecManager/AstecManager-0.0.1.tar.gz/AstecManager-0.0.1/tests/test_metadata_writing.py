import sys
from AstecManager.Manager import Manager,save_general_metadata_to_xml
manager = Manager()
from AstecManager.libs.analyze import write_xml_signal_camera,write_cell_count_to_XML,write_early_cell_death_to_XML

import os
from random import randrange
from datetime import datetime

manager = Manager()
searcher = "BG"
input_folder = "/path/on/microscope/source/"
embryo_name = "TEST_DATA"
embryo_dir = os.path.join(".",embryo_name)

print("Saving metadata for Raw Images Copy")
save_general_metadata_to_xml(embryo_dir, "raw_copy_date", "", datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
save_general_metadata_to_xml(embryo_dir, "raw_copy_source", "", input_folder)
save_general_metadata_to_xml(embryo_dir, "raw_copy_user", "", searcher)

print("Saving metadata for Fusion")
save_general_metadata_to_xml(embryo_dir, "fusion_user", "FUSE_01", searcher,identifier_text="fusion_instance")
save_general_metadata_to_xml(embryo_dir, "fusion_date","FUSE_01", datetime.now().strftime("%m/%d/%Y %H:%M:%S"),identifier_text="fusion_instance")

save_general_metadata_to_xml(embryo_dir, "fusion_upload_user",
                             "FUSE_01",
                             searcher, identifier_text="fusion_instance")
save_general_metadata_to_xml(embryo_dir, "fusion_upload_date",
                             "FUSE_01",
                             datetime.now().strftime("%m/%d/%Y %H:%M:%S"), identifier_text="fusion_instance")

average_by_time = {}
max_by_time = {}
csv = ""
for i in range(0,181):
    csv += str(i)+";"+str(randrange(0, 1000, 1))+";"+str(randrange(0, 1000, 1))+":"
f = open("data.csv","w+")
f.write(csv)
f.close()
write_xml_signal_camera("data.csv", "left_camera_stack_0", embryo_dir)
average_by_time = {}
max_by_time = {}
csv = ""
for i in range(0,181):
    csv += str(i)+";"+str(randrange(0, 1000, 1))+";"+str(randrange(0, 1000, 1))+":"
f = open("data.csv","w+")
f.write(csv)
f.close()
write_xml_signal_camera("data.csv", "right_camera_stack_0", embryo_dir)
average_by_time = {}
max_by_time = {}
csv = ""
for i in range(0,181):
    csv += str(i)+";"+str(randrange(0, 1000, 1))+";"+str(randrange(0, 1000, 1))+":"
f = open("data.csv","w+")
f.write(csv)
f.close()
write_xml_signal_camera("data.csv", "left_camera_stack_1", embryo_dir)
average_by_time = {}
max_by_time = {}
csv = ""
for i in range(0,181):
    csv += str(i)+";"+str(randrange(0, 1000, 1))+";"+str(randrange(0, 1000, 1))+":"
f = open("data.csv","w+")
f.write(csv)
f.close()
write_xml_signal_camera("data.csv", "right_camera_stack_1", embryo_dir)

os.system("rm data.csv")

print("Writing metadata for contour")

contour_suffix = "RELEASE_6"
user="KB"
backgroundinput = "Background_FUSE_01_down06"
reducvoxelsize=0.6
target_normalization_max=1000
save_general_metadata_to_xml(embryo_dir, "contour_date", "CONTOUR_" + str(contour_suffix),
                             datetime.now().strftime("%m/%d/%Y %H:%M:%S"), identifier_text="contour_instance")
save_general_metadata_to_xml(embryo_dir, "contour_user", "CONTOUR_" + str(contour_suffix), user,
                             identifier_text="contour_instance")
save_general_metadata_to_xml(embryo_dir, "contour_source", "CONTOUR_" + str(contour_suffix), backgroundinput,
                             identifier_text="contour_instance")
save_general_metadata_to_xml(embryo_dir, "contour_resolution", "CONTOUR_" + str(contour_suffix), str(reducvoxelsize),
                             identifier_text="contour_instance")
save_general_metadata_to_xml(embryo_dir, "contour_normalisation", "CONTOUR_" + str(contour_suffix),
                             str(target_normalization_max), identifier_text="contour_instance")


begin = 1
end = 180
lineage_name = embryo_name + "_intrareg_post_lineage.xml"
atlases_files = []
atlases_files.append("pm1.xml")
atlases_files.append("pm3.xml")
atlases_files.append("pm4.xml")
atlases_files.append("pm5.xml")
atlases_files.append("pm7.xml")
atlases_files.append("pm8.xml")
atlases_files.append("pm9.xml")

save_general_metadata_to_xml(embryo_dir, "naming_date", lineage_name,
                             datetime.now().strftime("%m/%d/%Y %H:%M:%S"), identifier_text="naming_target")
save_general_metadata_to_xml(embryo_dir, "naming_atlas", lineage_name,
                             str(atlases_files), identifier_text="naming_target")
save_general_metadata_to_xml(embryo_dir, "naming_user", lineage_name,
                             str(user), identifier_text="naming_target")
save_general_metadata_to_xml(embryo_dir, "naming_init_time", lineage_name,
                             str(begin), identifier_text="naming_target")

parameters = {}
parameters["EXP_FUSE"] = "01"
parameters["EXP_SEG"] = "01"
parameters["EXP_POST"] = "01"
parameters["EXP_INTRAREG"] = "01"
voxel_size = 0.6
save_general_metadata_to_xml(embryo_dir, "downscale_date",
                             "FUSE_" + str(parameters["EXP_FUSE"]) + "_down0" + str(voxel_size).split(".")[1],
                             datetime.now().strftime("%m/%d/%Y %H:%M:%S"), identifier_text="downscale_target")
save_general_metadata_to_xml(embryo_dir, "downscale_user",
                             "FUSE_" + str(parameters["EXP_FUSE"]) + "_down0" + str(voxel_size).split(".")[1],
                             user, identifier_text="downscale_target")
save_general_metadata_to_xml(embryo_dir, "downscale_source",
                             "FUSE_" + str(parameters["EXP_FUSE"]) + "_down0" + str(voxel_size).split(".")[1],
                             "FUSE_"+str(parameters["EXP_FUSE"]), identifier_text="downscale_target")
save_general_metadata_to_xml(embryo_dir, "downscale_resolution",
                             "FUSE_" + str(parameters["EXP_FUSE"]) + "_down0" + str(voxel_size).split(".")[1],
                             str(voxel_size), identifier_text="downscale_target")

mars = os.path.join(os.path.join(embryo_dir,"MARS"),embryo_name+"_mars_too.nii")
output_file = os.path.join(os.path.join(embryo_dir,"MARS06"),embryo_name+"_mars_too.nii")
fusion = os.path.join(os.path.join(embryo_dir,"FUSE"),"FUSE_01/"+embryo_name+"_mars_too.nii")
save_general_metadata_to_xml(embryo_dir, "mars_downscale_date", output_file,
                             datetime.now().strftime("%m/%d/%Y %H:%M:%S"), identifier_text="mars_downscale_target")
save_general_metadata_to_xml(embryo_dir, "mars_downscale_user", output_file,
                             user, identifier_text="mars_downscale_target")
save_general_metadata_to_xml(embryo_dir, "mars_downscale_template", output_file,
                             fusion, identifier_text="mars_downscale_target")
save_general_metadata_to_xml(embryo_dir, "mars_downscale_source", output_file,
                             mars, identifier_text="mars_downscale_target")
save_general_metadata_to_xml(embryo_dir, "mars_downscale_resolution", output_file,
                             str(voxel_size), identifier_text="mars_downscale_target")

save_general_metadata_to_xml(embryo_dir, "segmentation_date", "SEG_" + str(parameters["EXP_SEG"]),
                             datetime.now().strftime("%m/%d/%Y %H:%M:%S"), identifier_text="segmentation_instance")
save_general_metadata_to_xml(embryo_dir, "segmentation_mars_path", "SEG_" + str(parameters["EXP_SEG"]),
                             mars, identifier_text="segmentation_instance")
save_general_metadata_to_xml(embryo_dir, "segmentation_begin_time", "SEG_" + str(parameters["EXP_SEG"]),
                             str(begin), identifier_text="segmentation_instance")
save_general_metadata_to_xml(embryo_dir, "segmentation_end_time", "SEG_" + str(parameters["EXP_SEG"]),
                             str(end), identifier_text="segmentation_instance")
save_general_metadata_to_xml(embryo_dir, "segmentation_user", "SEG_" + str(parameters["EXP_SEG"]),
                             str(user), identifier_text="segmentation_instance")

save_general_metadata_to_xml(embryo_dir, "post_correction_date", "POST_" + str(parameters["EXP_POST"]),
                             datetime.now().strftime("%m/%d/%Y %H:%M:%S"), identifier_text="post_correction_instance")
save_general_metadata_to_xml(embryo_dir, "post_correction_begin_time", "POST_" + str(parameters["EXP_POST"]),
                             str(begin), identifier_text="post_correction_instance")
save_general_metadata_to_xml(embryo_dir, "post_correction_end_time", "POST_" + str(parameters["EXP_POST"]),
                             str(end), identifier_text="post_correction_instance")
save_general_metadata_to_xml(embryo_dir, "post_correction_user", "POST_" + str(parameters["EXP_POST"]),
                             str(user), identifier_text="post_correction_instance")

save_general_metadata_to_xml(embryo_dir, "intraregistration_date", "INTRAREG_" + str(parameters["EXP_INTRAREG"]),
                             datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                             identifier_text="intraregistration_instance")
save_general_metadata_to_xml(embryo_dir, "intraregistration_begin_time",
                             "POST_" + str(parameters["EXP_INTRAREG"]),
                             str(begin), identifier_text="intraregistration_instance")
save_general_metadata_to_xml(embryo_dir, "intraregistration_end_time",
                             "POST_" + str(parameters["EXP_INTRAREG"]),
                             str(end), identifier_text="intraregistration_instance")
save_general_metadata_to_xml(embryo_dir, "intraregistration_user", "POST_" + str(parameters["EXP_INTRAREG"]),
                             str(user), identifier_text="intraregistration_instance")
max_by_time = {}
csv = ""
for i in range(0,181):
    csv += str(i)+":"+str(randrange(0, 1000, 1))+";"
f = open("data.csv","w+")
f.write(csv)
f.close()
write_cell_count_to_XML("data.csv","POST_TEST",os.path.join(".",embryo_name))


max_by_time = {}
csv = ""
for i in range(0,181):
    csv += str(i)+":"+str(randrange(0, 1000, 1))+";"
f = open("data.csv","w+")
f.write(csv)
f.close()
write_early_cell_death_to_XML("data.csv","POST_TEST",os.path.join(".",embryo_name))

os.system("rm data.csv")

save_general_metadata_to_xml(embryo_dir, "seg_upload_user",
                             "SEG_01",
                             user, identifier_text="segmentation_instance")
save_general_metadata_to_xml(embryo_dir, "seg_upload_date",
                             "SEG_01",
                             datetime.now().strftime("%m/%d/%Y %H:%M:%S"), identifier_text="segmentation_instance")

save_general_metadata_to_xml(embryo_dir, "mars_upload_user",
                             "MARS_01",
                             user, identifier_text="mars_instance")
save_general_metadata_to_xml(embryo_dir, "mars_upload_date",
                             "MARS_01",
                             datetime.now().strftime("%m/%d/%Y %H:%M:%S"), identifier_text="mars_instance")

omero_project_name = embryo_name
omero_dataset_name = "FUSE_UPLOAD"
save_general_metadata_to_xml(embryo_dir, "upload_user",
                             omero_project_name + "/" + omero_dataset_name,
                             user, identifier_text="upload_instance")
save_general_metadata_to_xml(embryo_dir, "upload_date",
                             omero_dataset_name,
                             datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                             identifier_text="upload_instance")

