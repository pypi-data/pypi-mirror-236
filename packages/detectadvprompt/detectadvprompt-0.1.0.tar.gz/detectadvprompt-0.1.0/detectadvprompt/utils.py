import torch
import numpy as np


def get_llm_logprob(
    model,
    tokenizer,
    text=None,
    text_input_ids=None,
    prompt=None,
):
    if prompt is None:
        #  prompt = tokenizer.bos_token
        prompt_input_ids = [model.config.bos_token_id]
    else:
        prompt_input_ids = tokenizer.encode(prompt)
    if text_input_ids is None:
        text_input_ids = tokenizer.encode(text, add_special_tokens=False)
    input_ids = np.concatenate([prompt_input_ids, text_input_ids])
    leading_tokens = len(prompt_input_ids)

    # get the logits for the last token
    with torch.no_grad():
        output = model(torch.tensor(input_ids, device=model.device).unsqueeze(0))
        logits = output.logits[0, leading_tokens - 1 : -1, :]
        logprobs = torch.nn.functional.log_softmax(logits, dim=-1)
        logprobs = torch.gather(
            logprobs,
            dim=-1,
            index=torch.tensor(
                input_ids[leading_tokens:], device=model.device
            ).unsqueeze(-1),
        ).squeeze(-1)

    return text_input_ids, logprobs.cpu().numpy()


def get_all_adv_logprob(tokenizer):
    return -np.log(tokenizer.vocab_size)


def get_ascii_adv_logprob(tokenizer):
    #  For each symbol in the tokenizer, check whether they are pure ascii
    def is_ascii(s):
        return s.isascii() and s.isprintable()

    ascii_symbols = []
    for i in range(3, tokenizer.vocab_size):
        if not is_ascii(tokenizer.decode([i])):
            ascii_symbols.append(i)

    return -np.log(len(ascii_symbols))


def get_adv_logprob(tokenizer):
    return get_ascii_adv_logprob(tokenizer)
    #  return get_all_adv_logprob(tokenizer)


def to_a_s(logprobs, adv_logprob):
    a_s = logprobs - adv_logprob
    # the probability for first token is unreliable
    a_s[0] = 0
    return a_s
