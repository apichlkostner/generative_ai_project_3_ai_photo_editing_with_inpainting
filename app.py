import gradio as gr
import numpy as np
from PIL import Image, ImageDraw

IMG_SIZE = 512

def generate_app(get_processed_inputs, inpaint):
    
    with gr.Blocks() as demo:
        # State components for session-specific data
        input_points = gr.State([])
        input_image = gr.State(None)
        
        gr.Markdown(
        """
        # Image inpainting
        1. Upload an image by clicking on the first canvas.
        2. Click on the subject you would like to keep. Immediately SAM will be run and you will see the results. If you
           are happy with those results move to the next step, otherwise add more points to refine your mask.
        3. Write a prompt (and optionally a negative prompt) for what you want to generate for the infilling. 
           Adjust the CFG scale and the seed if needed. You can also invert the mask, i.e., infill the subject 
           instead of the background by toggling the relative checkmark.
        4. Click on "run inpaint" and wait for up to two minutes. If you are not happy with the result, 
           change your prompts and/or the settings (CFG scale, random seed) and click "run inpaint" again.

        # EXAMPLES
        Scroll down to see a few examples. Click on an example and the image and the prompts will be filled for you. 
        Note however that you still need to do step 2 and 4.
        """)

        with gr.Row():
            display_img = gr.Image(
                label="Input", 
                interactive=True,
                type='pil',
                height=IMG_SIZE,
                width=IMG_SIZE
            )
            sam_mask = gr.AnnotatedImage(
                label="SAM result",
                height=IMG_SIZE,
                width=IMG_SIZE,
                color_map={"background": "#a89a00"}
            )
            result = gr.Image(
                label="Output",
                interactive=False,
                type='pil',
                height=IMG_SIZE,
                width=IMG_SIZE,
            )            
        
        # Define other UI components here, before any event handlers that use them
        with gr.Row():
            cfg = gr.Slider(
                label="Classifier-Free Guidance Scale", 
                minimum=0.0, 
                maximum=20.0, 
                value=7, 
                step=0.05
            )
            random_seed = gr.Number(
                label="Random seed", 
                value=74294536, 
                precision=0
            )
            checkbox = gr.Checkbox(
                label="Infill subject instead \nof background"
            )

        with gr.Row():
            prompt = gr.Textbox(label="Prompt for infill")
            neg_prompt = gr.Textbox(label="Negative prompt")
            
            reset_btn = gr.Button(value="Reset")
            submit_inpaint = gr.Button(value="Run inpaint")

        with gr.Row():
            examples = gr.Examples(
                examples=[
                    [
                        "car.png", 
                        "a car driving on planet Mars. Studio lights, 1970s", 
                        "artifacts, low quality, distortion",
                        74294536
                    ],
                    [
                        "dragon.jpeg",
                        "a dragon in a medieval village",
                        "artifacts, low quality, distortion",
                        97
                    ],
                    [
                        "monalisa.png",
                        "a fantasy landscape with flying dragons",
                        "artifacts, low quality, distortion",
                        97
                    ]
                ],
                inputs=[
                    display_img,
                    prompt,
                    neg_prompt,
                    random_seed
                ]
            )
        
        def get_points(img, points, evt: gr.SelectData):
            x, y = evt.index[0], evt.index[1]
            updated_points = points + [[x, y]]
            
            if len(updated_points) == 1:
                input_image_val = img.copy()
            else:
                input_image_val = img
            
            sam_output = run_sam(input_image_val, updated_points)
            
            img_copy = img.copy()
            draw = ImageDraw.Draw(img_copy)
            size = 10
            for point in updated_points:
                x, y = point
                draw.line((x - size, y, x + size, y), fill="green", width=5)
                draw.line((x, y - size, x, y + size), fill="green", width=5)
            
            return updated_points, input_image_val, sam_output, img_copy

        def run_sam(img, points):
            if img is None:
                raise gr.Error("No image provided. Upload an image first.")
            try:
                mask = get_processed_inputs(img, [points])
                res_mask = np.array(Image.fromarray(mask).resize((IMG_SIZE, IMG_SIZE)))
                return (
                    img.resize((IMG_SIZE, IMG_SIZE)), 
                    [
                        (res_mask, "background"), 
                        (~res_mask, "subject")
                    ]
                )
            except Exception as e:
                raise gr.Error(str(e))
        
        def run(prompt, negative_prompt, cfg, seed, invert, img, points):
            if img is None:
                raise gr.Error("No image provided. Upload an image first.")
            amask = run_sam(img, points)[1][0][0]
            what = 'subject' if invert else 'background'
            if invert:
                amask = ~amask
            gr.Info(f"Inpainting {what}... (this will take up to a few minutes)")
            try:
                inpainted = inpaint(img, amask, prompt, negative_prompt, seed, cfg)
            except Exception as e:
                raise gr.Error(str(e))
            return inpainted.resize((IMG_SIZE, IMG_SIZE))
        
        def reset_points():
            # Return default values for all components that need to be reset
            return [], None, None, None, None, "", "", False

        def preprocess(input_img):
            if input_img is None:
                return None
            width, height = input_img.size
            if width != height:
                gr.Warning("Image is not square, adding white padding")
                new_size = max(width, height)
                new_image = Image.new("RGB", (new_size, new_size), 'white')
                left = (new_size - width) // 2
                top = (new_size - height) // 2
                new_image.paste(input_img, (left, top))
                input_img = new_image
            return input_img.resize((IMG_SIZE, IMG_SIZE))

        # Event handlers
        display_img.select(
            fn=get_points,
            inputs=[display_img, input_points],
            outputs=[input_points, input_image, sam_mask, display_img]
        )
        display_img.clear(
            fn=reset_points,
            outputs=[input_points, input_image, display_img, sam_mask, result, prompt, neg_prompt, checkbox]
        )
        display_img.change(
            fn=preprocess,
            inputs=[display_img],
            outputs=[display_img]
        )
        
        reset_btn.click(
            fn=reset_points,
            outputs=[input_points, input_image, display_img, sam_mask, result, prompt, neg_prompt, checkbox]
        )
        
        submit_inpaint.click(
            fn=run,
            inputs=[prompt, neg_prompt, cfg, random_seed, checkbox, input_image, input_points],
            outputs=[result]
        )

    demo.queue(max_size=1).launch(share=True, debug=True)
    return demo