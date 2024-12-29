import numpy as np
import matplotlib.image as mpimg
from stl import mesh

"""
Program Overview:
    mesh3D is a program to convert an image to a 3D mesh, output as an STL file with the original file name.
        The program makes use of matplotlib's image processing, numpy for large array manipulation, and numpy-stl 
        for the mesh processing. 
Input:
    Program takes image as input. Ideally the input image is downscaled to approximately 1280 x 720 to keep 
        runtime to a few seconds. Each block on the heatmap must be a minimum of 9x9 pixels to maintain a flat
        top, otherwise the mesh algorithm creates a point (16x or 32x is ideal).
Output:
    Program outputs a gaussian stl model of the input image with the same filename.
Necessary Modules:
    numpy
    matplotlib.image
    numpy-stl
"""

def threeDMesh(fname):
    """ Return 3D stl file of the input file. """

    # Process Image
    img = mpimg.imread(fname)  # Read in image
    lum_img = np.array(img[:, :, 0])  # Keep luminosity values
    (lnth, wdth) = lum_img.shape  # Get image dimensions

    # Scale array
    scaleVal = 100
    lum_img /= np.max(np.abs(lum_img))  # normalize values
    lum_img *= scaleVal / lum_img.max()  # scale array

    # Construct empty numpy array & account for edges
    verts = np.zeros((lnth, wdth, 3))

    # Assign skirts
    for y in range(0, wdth):
        verts[0][y] = (0, y, 0)
    for x in range(0, lnth):
        verts[x][0] = (x, 0, 0)
    for y in range(0, wdth):
        verts[lnth - 1][y] = (lnth - 1, y, 0)
    for x in range(0, lnth):
        verts[x][wdth - 1] = (x, wdth - 1, 0)

    # Assign lum from image to vertices array for heatmap values
    for y in range(1, wdth - 1):
        for x in range(1, lnth - 1):
            z = lum_img[x][y]
            verts[x][y] = (x, y, z)

    # Construct numpy array of faces
    faces = []
    for y in range(0, wdth - 1):
        for x in range(0, lnth - 1):
            tri1 = np.array([verts[x][y], verts[x + 1][y], verts[x + 1][y + 1]])
            tri2 = np.array([verts[x][y], verts[x][y + 1], verts[x + 1][y + 1]])
            faces.append(tri1)
            faces.append(tri2)

    # Assign Bottom (2 big triangles)
    botTri1 = np.array([verts[0][0], verts[lnth - 1][0], verts[lnth - 1][wdth - 1]])
    botTri2 = np.array([verts[0][0], verts[0][wdth - 1], verts[lnth - 1][wdth - 1]])
    faces.append(botTri1)
    faces.append(botTri2)

    # Construct mesh from faces
    facesNp = np.array(faces)
    surface = mesh.Mesh(np.zeros(facesNp.shape[0], dtype=mesh.Mesh.dtype))
    for index, face in enumerate(faces):
        for vertex in range(3):
            surface.vectors[index][vertex] = facesNp[index][vertex]

    # Save file
    getName = fname.strip('.png')
    surface.save(getName + '.stl')


if __name__ == '__main__':
    threeDMesh('hm.png')
