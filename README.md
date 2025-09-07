# AI Photo Editing with Inpainting

For Udacity course "Generative AI"

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

#### Teide in the ocean

![alt lizard as dragon](teide_in_ocean.png)

#### lizard on a table

![alt lizard on wooden table](lizard_on_wooden_table.png)

#### lizard on a steel table

![alt lizard on stelle table](lizard_on_steel_table.png)
