import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load a grayscale image (adjust the path to your image file)
img = cv2.imread('images.jpg', cv2.IMREAD_GRAYSCALE)
if img is None:
    raise IOError("Image not found. Please check the file path.")

# Define multiple convolution kernels
kernels = {
    'Sobel X': np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]]),
    
    'Sobel Y': np.array([[-1, -2, -1],
                         [ 0,  0,  0],
                         [ 1,  2,  1]]),
    
    'Laplacian': np.array([[0,  1, 0],
                           [1, -4, 1],
                           [0,  1, 0]]),
    
    'Sharpen': np.array([[ 0, -1,  0],
                         [-1,  5, -1],
                         [ 0, -1,  0]]),
    
    'Box Blur': np.array([[1/9, 1/9, 1/9],
                          [1/9, 1/9, 1/9],
                          [1/9, 1/9, 1/9]]),
    
    'Emboss': np.array([[-2, -1, 0],
                        [-1,  1, 1],
                        [ 0,  1, 2]])
}

# Apply each kernel to the image
results = {}
for name, kernel in kernels.items():
    results[name] = cv2.filter2D(img, -1, kernel)

# Plot the original image and the results
plt.figure(figsize=(12, 8))

# Show original image
plt.subplot(2, 4, 1)
plt.imshow(img, cmap='gray')
plt.title('Original Image')
plt.axis('off')

# Show each filtered image
idx = 2
for name, result in results.items():
    plt.subplot(2, 4, idx)
    plt.imshow(result, cmap='gray')
    plt.title(name)
    plt.axis('off')
    idx += 1

plt.tight_layout()
plt.show()
