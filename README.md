# AI Photo Editing with Inpainting

For Udacity course "Generative AI", based on (https://github.com/udacity/Computer-Vision-and-Generative-AI-Project).

The library app.py was modified to run with gradio 4 since the old versions from the original project don't runs with modern GPU hardware.

## Project

This project should demonstate a simple AI photo editing tool where the user can select an object in an image and then change the object or the background with an AI prompt.

## Pipeline

- Use a SAM model to segment the image in object and background
- Get the user prompt and negative prompt
- Call a diffusion model for image filling with the original image, the mask from the SAM model, the positive and negative prompt

## Results

### Lizard

#### Lizard replaced with a dragon

![alt lizard as dragon](lizard_as_dragon.png)

#### lizard on a table

![alt lizard on wooden table](lizard_on_wooden_table.png)

#### lizard on a steel table

![alt lizard on stelle table](lizard_on_steel_table.png)

### Teide (mountain)

#### Teide in the ocean with sun

![alt Teide in the ocean](teide_in_ocean.png)

#### Teide modified with sun in ocean with wooden island foreground

![alt Teide with sun](teide_with_sun.png)

#### Teide modified without sun with wooden island foreground

![alt Teide without sun](teide_without_sun.png)

## Parameter effect

### The diffusion model is tested with different "Classifier-Free Guidance Scales"

Value from left to right 1, 7, 14, 50

![alt lizard as dragon with different parameters](lizard_dragon_parameters.png)

It can be seen that the model changes the mask with in image that looks increasingly like the text prompt when the parameter is increased.

