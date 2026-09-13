---
type: article
status: structured
quality: 
topics: [llm-fundamentals]
source: https://magazine.sebastianraschka.com/p/claude-watermarking
created: 2026-09-06
published: 2026-08-22
author: Sebastian Raschka, PhD
flashcards: none
updated: 2026-09-13
---

# How Claude Watermarks AI-Generated Text

<div align="center">
  <img src="https://substackcdn.com/image/fetch/$s_!2E7U!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb73bfb5-0291-4e5e-b425-6c3be054276e_1914x1076.png" width="220" />
</div>

- Anthropic announced that they will watermark the text outputs of their Claude models.
    - The underlying mechanism works as follows, along with how they are going to implement this type of text watermarking.

### How LLM Text Generation Works

- Assume the prompt is “the capital of Germany is”. The first step is to convert this into token IDs. Tokenizing and converting into token IDs is one of the main steps at the beginning.
    - This happens outside the LLM, not inside it. The text is simply converted into token IDs — a format that embedding layers can work with.
- This then passes through the LLM, which gives a score distribution for the next token.
    - When the next token is generated (for example, “Berlin”), there is at this point a distribution of scores. This is the output produced by the LLM.
    - These are logit values: scores from minus infinity to plus infinity. One example ranges from about -8 or -9 to 20.
        - They can be converted into a probability distribution, but that is not strictly necessary depending on how we sample. The logit values are the raw scores.

![](https://substackcdn.com/image/fetch/$s_!gpfA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25e84186-eb07-4bfa-ae49-3e8e01efe418_6667x3750.png)

- Running this prompt through an LLM would show something more extreme: everything is very close to zero, and “Berlin” would probably be much higher still.
- “Berlin” has the highest score because it is the most probable or plausible next token.

![](https://substackcdn.com/image/fetch/$s_!u2Kj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5f5e5d5-de7f-4925-81cc-4e561aff444a_6667x3750.png)

- This score is then detokenized, returning “Berlin”. The full process runs from an input prompt, to tokenization and conversion into token IDs, to passing it to the LLM, to getting the score distribution, to getting the next token, to converting it back into text.

![](https://substackcdn.com/image/fetch/$s_!ok-i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7255cfa-288b-4e42-9078-3fd42df67337_6667x3750.png)

- This text is then appended to the input.
    - A question that requires multiple output tokens keeps going in this loop until the answer is complete, which usually means the LLM generates an end-of-text token.
- One option is to select the token with the highest score. This is called greedy decoding.
    - Modifications include top-k sampling and top-p sampling. In top-k sampling, the top 100 tokens are selected and the random choice is applied only to those 100 highest-scoring ones, so that nonsense tokens don’t get in.
- For the prompt “today’s weather is cold,” a possible answer could be “gray” or “overcast”. In contrast to the “Berlin” example, “gray” and “overcast” are interchangeable.
    - Both are reasonable next tokens for this prompt, given the goal of completing the text or writing the next token. Which one gets selected is almost a coin flip.
        - Neither is objectively worse than the other. Under random sampling, because both are plausible tokens with similarly high scores, either one might come out.
- A random seed produces a reproducible sequence of numbers.
    - Random sampling might return either “gray” or “overcast”. With a specific random seed like 42, the selection would always be “overcast”.
        - It is still a random selection, but made deterministic.

![](https://substackcdn.com/image/fetch/$s_!L-VB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6547aa47-2631-4fda-a65d-06f7336e6794_6667x3750.png)

- Claude watermarking works like setting a random seed.
    - They use a secret key, essentially like an API key, and from that key together with the four previous words they derive the random seed.
    - Instead of using a fixed random seed such as 99, they use a secret key plus information about the previous tokens to derive the random seed.

![](https://substackcdn.com/image/fetch/$s_!0dqQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4c3d6c6-4a48-4f13-8830-eb3e339129ba_6667x3750.png)

- Without watermarking, running the prompt through the LLM might sometimes give one answer and sometimes another.
    - Based on the number of positions, there might be 128 possible answers. The longer the text, the more positions there are where terms are interchangeable, and the more combinations or output texts there are.
- A random seed fixes which answer comes out, because the random sampling is still random but deterministic in the sense that it is reproducible.
    - Instead of just a simple random seed, they use a so-called random key, where this random key is involved in selecting the text.
- Detecting the watermark is only possible with access to the key.
    - Without the watermarking key it is impossible to know. Detection requires the scoring function, and the text has to be scored with that scoring function.
        - If the score is above a certain threshold, the text is watermarked.
    - Only Anthropic will have the key.

### How to Remove a Watermark

![](https://substackcdn.com/image/fetch/$s_!oeAq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71d15440-51d3-4039-8b10-fcb8777f25d9_6667x3750.png)

- Knowing how the watermarking works also reveals its shortcomings.
    - It is highly dependent on specific tokens in certain positions.
- The positions of these words are unknown to anyone who did not generate the watermark.
    - So it is unclear which positions to look at.
- The practical scenario is to randomly edit the text.
    - Randomly changing a few words, in the hope of changing enough positions to edit the watermark, is one way to remove it.

### How the Watermark Scoring Function Works

- The reason they do it the particular way they do is to make the detection cheaper.
    - Checking whether something is watermarked would otherwise require rerunning the prompt to get the scores, applying the watermarking random seed to get the text, and then comparing.
    - That would be very expensive, because every text to be compared would require rerunning the LLM.
- The method comes from a Nature paper and is called SynthID-Text.
    - The paper was by Google, and they use a similar technique they call Claude watermarking.

### SynthID Text and Tournament Sampling

![](https://substackcdn.com/image/fetch/$s_!DUPH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fab7ffafb-9733-4b4f-9789-1bd7d7bb15af_6667x3750.png)

- Instead, the technique is applied during sampling, at generation time, so that it can be reused later during detection. It is called tournament sampling.

![](https://substackcdn.com/image/fetch/$s_!lUpe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27a7a689-db67-4c21-9f9b-7912ad7b0825_6667x3750.png)

- There are three watermarking functions, G1, G2, and G3. In reality there might be 30, 50, or even more.
    - The result is a bit string of zeros and ones. This one is for “gray”.
        - Using these watermarking functions gives the signature 101. The same is then done for all the other ones.

### Detecting Watermarks Without Rerunning the LLM

![](https://substackcdn.com/image/fetch/$s_!Hxlf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2b79f05-4b0f-4045-a07c-224d89465d28_6667x3750.png)

- NumPy’s `random.choice` could have been used instead, but its shortcoming is that scoring random text on the internet would require rerunning the LLM. With this technique, that is not needed.
    - The point is essentially just to make the detection easier and cheaper.
