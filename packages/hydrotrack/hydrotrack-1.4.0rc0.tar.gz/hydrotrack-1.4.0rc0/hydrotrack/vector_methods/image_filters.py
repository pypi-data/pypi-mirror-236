import cv2
import numpy as np

# Function to add Gaussian noise to an image
def add_gaussian_noise(image, mean=0, stddev=25):
    # Generate Gaussian noise
    noise = np.random.normal(mean, stddev, image.shape).astype(np.uint8)
    # Add noise to the image
    noisy_image = cv2.add(image, noise)
    return noisy_image

# Function to apply Gaussian blur (smoothing) to an image
def apply_gaussian_blur(image, kernel_size=(5, 5), sigma=1.0):
    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(image, kernel_size, sigma)
    return blurred_image

# Function to scale the intensity of an image
def scale_image_intensity(image, scale_factor=2.0):
    # Scale the image intensity
    scaled_image = cv2.multiply(image, np.array([scale_factor]))
    return scaled_image

# Function to apply Z-score transformation to an image
def zscore_transform(image):
    # Convert image to float32 for Z-score calculation
    image_float = image.astype(np.float32)
    # Calculate mean and standard deviation of the image
    mean = np.mean(image_float)
    stddev = np.std(image_float)
    # Apply Z-score transformation
    zscore_image = (image_float - mean) / stddev
    
    return zscore_image


# Function to perform histogram equalization
def histogram_equalization(image):
    # Convert image to grayscale if it's in color
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image
    
    # Apply histogram equalization
    equalized_image = cv2.equalizeHist(gray_image)
    
    return equalized_image

# Function to perform image thresholding
def threshold_image(image, threshold_value=128, max_value=255, threshold_type=cv2.THRESH_BINARY):
    # Convert image to grayscale if it's in color
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image
    
    # Apply thresholding
    _, thresholded_image = cv2.threshold(gray_image, threshold_value, max_value, threshold_type)
    
    return thresholded_image

# Function to sharpen an image
def sharpen_image(image):
    # Define a sharpening kernel (Laplacian)
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]], dtype=np.float32)
    
    # Apply convolution with the sharpening kernel
    sharpened_image = cv2.filter2D(image, -1, kernel)
    
    return sharpened_image

# Function to perform median filtering for denoising
def denoise_median(image, kernel_size=5):
    # Apply median filtering
    denoised_image = cv2.medianBlur(image, kernel_size)
    
    return denoised_image

# Function to perform Canny edge detection
def detect_edges_canny(image, low_threshold=50, high_threshold=150):
    # Convert image to grayscale if it's in color
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray_image, low_threshold, high_threshold)
    
    return edges

# Function to perform dilation operation
def dilate_image(image, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated_image = cv2.dilate(image, kernel, iterations=1)
    
    return dilated_image

# Function to perform erosion operation
def erode_image(image, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    eroded_image = cv2.erode(image, kernel, iterations=1)
    
    return eroded_image

# Function to perform texture analysis (example: Gabor filter)
def texture_analysis(image, kernel_size=7, theta=0, sigma=2.0, frequency=0.2):
    # Create a Gabor kernel
    kernel = cv2.getGaborKernel((kernel_size, kernel_size), sigma, theta, 1.0, frequency, 0, ktype=cv2.CV_32F)
    
    # Apply Gabor filter to the image
    filtered_image = cv2.filter2D(image, cv2.CV_8UC3, kernel)
    
    return filtered_image
    
    
    
'''
The choice of strategy for increasing the standard deviation of your matrix depends on the specific goals and constraints of your application. There isn't a one-size-fits-all "best" strategy because it depends on what you're trying to achieve. Here are some common strategies, each with its own advantages and use cases:

    Gaussian Noise Addition:
        Advantages: This approach is statistically rigorous and can precisely control the standard deviation of the resulting matrix.
        Use Case: If you need to simulate data with a specific level of noise for testing or modeling purposes, adding Gaussian noise is a good choice.

    Smoothing or Blurring:
        Advantages: Applying a smoothing filter like Gaussian blur can effectively increase the standard deviation of a matrix while preserving some spatial characteristics.
        Use Case: When working with images or spatial data and you want to reduce high-frequency noise while increasing overall variability.

    Scaling or Amplification:
        Advantages: You can multiply the entire matrix by a scalar factor to increase its standard deviation. This is a straightforward method.
        Use Case: When you need to quickly adjust the standard deviation without introducing randomness or altering the data distribution.

    Data Transformation:
        Advantages: For specific types of data, you may use mathematical transformations to adjust the standard deviation. For example, for normally distributed data, you can use the Z-score transformation.
        Use Case: When working with data that follows a known distribution and you want to standardize it.

The "best" strategy depends on the nature of your data, your objectives, and the specific context of your application. Here are some considerations to help you choose:

    Preservation of Data Characteristics: Consider whether you need to preserve the original data characteristics, such as the data distribution or spatial features. Some methods (e.g., Gaussian noise addition) may introduce randomness that alters the data distribution.

    Application-Specific Requirements: Think about the requirements of your application. For example, if you're working on image processing, blurring might be suitable for noise reduction and increasing variability.

    Control and Reproducibility: If you require precise control over the standard deviation and need to reproduce the same results, methods like Gaussian noise addition or scaling may be better suited.

    Data Understanding: Understand the underlying data and the effect of each method on the data's interpretation and analysis. Consider how each approach may impact the quality of your results.

Ultimately, the choice of strategy should align with your specific objectives and the nature of your data. It may also involve experimentation to determine the best approach based on the results you achieve.
'''