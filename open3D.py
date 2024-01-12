import math
import pygame
import numpy as np

# Global variables
# Internal
main_cam_pos = [0, 0, 0]
main_cam_rot = [0, 0, 0]
main_cam_plane = [0, 0, 5]

scene_vertices = []
scene_faces = []

# Core functions
# File reading
def read_obj(path):
    with open(path, "r") as f:
        # Get information from OBJ file
        data = f.readlines()
        
        # Get vertices from OBJ file
        for line in data:
            if line[0] == "v" and line[1] == " ":
                # line is a vertex
                
                vertex = []
                
                i = 0
                
                for substring in line.split(" ")[1:]:
                    vertex.append(float(substring))
                    i += 1
                
                scene_vertices.append(vertex)
                
        
        # Get faces from OBJ file
        for line in data:
    
            if line[0] == "f":
                # line is a face
                face = []
                
                for substring in line.split(" ")[1:]:
                    face.append(scene_vertices[int(substring.split("/")[0]) - 1])
                scene_faces.append(face)

# Projection
def project_scene(faces, cam_pos, cam_rot, cam_plane):
    # Declare output array
    projected_scene = []

    # Declare the projection matrix
    proj_rot_matrix = [
        [
            math.cos(cam_rot[0]) * math.cos(cam_rot[2]), 
            math.sin(cam_rot[0]) * math.sin(cam_rot[1]) * math.cos(cam_rot[2]) - math.cos(cam_rot[0]) * math.sin(cam_rot[2]), 
            math.cos(cam_rot[0]) * math.sin(cam_rot[1]) * math.cos(cam_rot[2]) + math.sin(cam_rot[0]) * math.sin(cam_rot[2])
        ], 
        [
            math.cos(cam_rot[0]) * math.cos(cam_rot[2]), 
            math.sin(cam_rot[0]) * math.sin(cam_rot[1]) * math.cos(cam_rot[2]) + math.cos(cam_rot[0]) * math.sin(cam_rot[2]), 
            math.cos(cam_rot[0]) * math.sin(cam_rot[1]) * math.sin(cam_rot[2]) - math.sin(cam_rot[0]) * math.cos(cam_rot[2])
        ], 
        [
            -math.sin(cam_rot[1]),
            math.sin(cam_rot[0]) * math.cos(cam_rot[1]),
            math.cos(cam_rot[0]) * math.cos(cam_rot[1])
        ]
    ]
    
    # Loop through scene faces to project them
    for face in faces:
        # Prepare face to store vertices
        current_projected_face = []
    
        # Loop through each vertex in current face
        for vertex in face:
            # Project current vertex
            projected_vertex = proj_rot_matrix @ np.subtract(np.array(vertex), np.array(cam_pos))
            
            # Convert projected vertex to screen space and add to face
            current_projected_face.append([(cam_plane[2] / projected_vertex[2]) * projected_vertex[0] + cam_plane[0], (cam_plane[2] / projected_vertex[2]) * projected_vertex[1] + cam_plane[1]])
        
        # Append projected face to output array
        projected_scene.append(current_projected_face)
        
    # Return projected scene
    return projected_scene