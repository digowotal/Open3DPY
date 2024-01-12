import math
import pygame
import numpy as np

# Global variables
# Internal
main_cam_pos = [0, 0, 0]
main_cam_rot = [0, 0, 0]
main_cam_plane = [0, 0, 5]

# Core functions
def project_scene(faces, cam_pos, cam_rot, cam_plane):
    # Declare output array
    projected_scene = []

    # Declare the projection matrix
    proj_rot_matrix = [
        [
            math.cos(cam_rot[0]) * math.cos(cam_rot[2]), 
            math.sin(cam_rot[0]) * math.sin(cam_rot[1]) * math.cos(cam_rot[2]) - math.cos(cam_rot[0]) * math.sin(cam_rot[2]), 
            math.cos(cam_rot[0]) * math.sin(cam_rot[1]) * math.cos(cam_rot[2]) + math.sin(cam_rot[0]) * math.sin(cam_rot[2])
        ], [
            math.cos(cam_rot[0]) * math.cos(cam_rot[2]), 
            math.sin(cam_rot[0]) * math.sin(cam_rot[1]) * math.cos(cam_rot[2]) + math.cos(cam_rot[0]) * math.sin(cam_rot[2]), 
            math.cos(cam_rot[0]) * math.sin(cam_rot[1]) * math.sin(cam_rot[2]) - math.sin(cam_rot[0]) * math.cos(cam_rot[2])
        ], [
            -math.sin(cam_rot[1]),
            math.sin(cam_rot[0] * math.cos(cam_rot[1]),
            math.cos(cam_rot[0] * math.cos(cam_rot[1])
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

