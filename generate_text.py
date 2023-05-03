import os
from glob import glob
from dataclasses import dataclass, field
import torch
from transformers import GPT2Config, GPT2LMHeadModel
import sys

@dataclass
class GenerationDeployArguments:

    def __init__(
            self,
            pretrained_model_name=None,
            downstream_model_dir=None,
            downstream_model_checkpoint_fpath=None,
    ):
        self.pretrained_model_name = pretrained_model_name
        if downstream_model_checkpoint_fpath is not None:
            self.downstream_model_checkpoint_fpath = downstream_model_checkpoint_fpath
        elif downstream_model_dir is not None:
            ckpt_file_names = glob(os.path.join(downstream_model_dir, "*.ckpt"))
            ckpt_file_names = [el for el in ckpt_file_names if "temp" not in el and "tmp" not in el]
            if len(ckpt_file_names) == 0:
                raise Exception(f"downstream_model_dir \"{downstream_model_dir}\" is not valid")
            selected_fname = ckpt_file_names[-1]
            min_val_loss = os.path.split(selected_fname)[-1].replace(".ckpt", "").split("=")[-1].split("-")[0]
            try:
                for ckpt_file_name in ckpt_file_names:
                    val_loss = os.path.split(ckpt_file_name)[-1].replace(".ckpt", "").split("=")[-1].split("-")[0]
                    if float(val_loss) < float(min_val_loss):
                        selected_fname = ckpt_file_name
                        min_val_loss = val_loss
            except:
                raise Exception(f"the ckpt file name of downstream_model_directory \"{downstream_model_dir}\" is not valid")
            self.downstream_model_checkpoint_fpath = selected_fname
        else:
            raise Exception("Either downstream_model_dir or downstream_model_checkpoint_fpath must be entered.")
        print(f"downstream_model_checkpoint_fpath: {self.downstream_model_checkpoint_fpath}")


def load_model():
    args = GenerationDeployArguments(
        pretrained_model_name="skt/kogpt2-base-v2",
        downstream_model_dir="/home/ubuntu/workspace/SemiPJT_team2", 
    )
    
    pretrained_model_config = GPT2Config.from_pretrained(
    args.pretrained_model_name,
    )

    model = GPT2LMHeadModel(pretrained_model_config)
    fine_tuned_model_ckpt = torch.load(
        args.downstream_model_checkpoint_fpath,
        map_location=torch.device("cpu"),
    )
    model.load_state_dict({k.replace("model.", ""): v for k, v in fine_tuned_model_ckpt['state_dict'].items()})
    return model

# 직무역량 상권에 따라 매장을 다르게 컨설팅하고 손익분석을 통해 성과를 창출하기 위해서는
def generate_result(input_text, model):
    
    from transformers import PreTrainedTokenizerFast
    tokenizer = PreTrainedTokenizerFast.from_pretrained(
        pretrained_model_name_or_path="skt/kogpt2-base-v2",
        eos_token="</s>",
    )
    
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    generated_texts = []
    for i in range(3):
        gen_ids = model.generate(input_ids,
                                max_length=200,
                                repetition_penalty=1.0,
                                pad_token_id=tokenizer.pad_token_id,
                                eos_token_id=tokenizer.eos_token_id,
                                bos_token_id=tokenizer.bos_token_id,
                                use_cache=True)
        generated = tokenizer.decode(gen_ids[0])
        generated_texts.append(generated)
        
    return generated_texts

if __name__ == "__main__":
        
    model = load_model()
    generated_texts = generate_result(input_text, model)
    print(generated_texts)