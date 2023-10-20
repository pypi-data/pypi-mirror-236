default_model_cache = {}


def load_model(model_str="gpt2"):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    return AutoModelForCausalLM.from_pretrained(
        model_str
    ), AutoTokenizer.from_pretrained(model_str)


def load_default_model():
    if "model" not in default_model_cache:
        model, tokenizer = load_model("gpt2")
        default_model_cache["model"] = model
        default_model_cache["tokenizer"] = tokenizer
    return default_model_cache["model"], default_model_cache["tokenizer"]


def detect_prob(text, lamb=10, mu=0.5, model=None, tokenizer=None):
    from . import dp, utils

    if model is None:
        model, tokenizer = load_default_model()

    ids, logprobs = utils.get_llm_logprob(model, tokenizer, text)
    strs = [
        tokenizer.convert_tokens_to_string([t])
        for t in tokenizer.convert_ids_to_tokens(ids, skip_special_tokens=True)
    ]

    a_s = utils.to_a_s(logprobs, utils.get_adv_logprob(tokenizer))
    ps = dp.dp_prob(a_s, lamb, mu)

    return list(zip(strs, ps))


def detect_opt(text, lamb=10, mu=0.0, model=None, tokenizer=None):
    from . import dp, utils

    if model is None:
        model, tokenizer = load_default_model()

    ids, logprobs = utils.get_llm_logprob(model, tokenizer, text)
    strs = [
        tokenizer.convert_tokens_to_string([t])
        for t in tokenizer.convert_ids_to_tokens(ids, skip_special_tokens=True)
    ]

    a_s = utils.to_a_s(logprobs, utils.get_adv_logprob(tokenizer))
    cs = dp.dp_opt(a_s, lamb, mu).tolist()

    return list(zip(strs, cs))
