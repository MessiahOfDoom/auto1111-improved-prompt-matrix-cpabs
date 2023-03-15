import re
import gradio as gr
import modules.shared as shared
import modules.scripts as scripts
import modules.sd_samplers
from modules.processing import process_images, StableDiffusionProcessingTxt2Img

class Script(scripts.Script):
    def title(self):
        return "Improved prompt matrix CPABS"

    def ui(self, is_img2img):
        gr.HTML('<br/>')
        opening = gr.Textbox(label="Opening Symbol")
        pipe = gr.Textbox(label="Pipe Symbol")
        closing = gr.Textbox(label="Closing Symbol")
        return [opening, pipe, closing]

    def run(self, p, opening, pipe, closing):
        
        opening = opening or '<'
        pipe = pipe or '|'
        closing = closing or '>'

        rex = re.compile(r'(' + re.escape(opening) +'(?!lora:)([^>]+)'+ re.escape(closing) +')')

        modules.processing.fix_seed(p)

        original_prompt = p.prompt[0] if type(p.prompt) == list else p.prompt

        matrix_count = 0
        prompt_matrix_parts = []
        for data in re.finditer(rex, original_prompt):
            if data:
                matrix_count += 1
                span = data.span(1)
                items = data.group(2).split(pipe)
                prompt_matrix_parts.extend(items)

        all_prompts = [original_prompt]
        while True:
            found_matrix = False
            for this_prompt in all_prompts:
                for data in re.finditer(rex, this_prompt):
                    if data:
                        found_matrix = True
                        # Remove last prompt as it has a found_matrix
                        all_prompts.remove(this_prompt)
                        span = data.span(1)
                        items = data.group(2).split(pipe)
                        for item in items:
                            new_prompt = this_prompt[:span[0]] + item.strip() + this_prompt[span[1]:]
                            all_prompts.append(new_prompt.strip())
                    break
                if found_matrix:
                    break
            if not found_matrix:
                break

        total_batches = len(all_prompts) * p.n_iter
        print(f"Prompt matrix will create {total_batches * p.batch_size} images")

        total_steps = p.steps * total_batches
        if isinstance(p, StableDiffusionProcessingTxt2Img) and p.enable_hr:
            total_steps *= 2
        shared.total_tqdm.updateTotal(total_steps)

        
        p.seed = [item + n for item in range(int(p.seed), int(p.seed) + p.n_iter * p.batch_size, p.batch_size) for _ in range(len(all_prompts)) for n in range(p.batch_size)]
        all_prompts = [x for x in all_prompts for i in range(0, p.batch_size)]
        p.prompt = all_prompts * p.n_iter
        p.n_iter = total_batches
        p.prompt_for_display = original_prompt

        return process_images(p)
