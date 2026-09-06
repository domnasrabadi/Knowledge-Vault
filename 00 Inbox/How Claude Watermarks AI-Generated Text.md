---
type: article
status: inbox
quality: 
topics: []
source: https://magazine.sebastianraschka.com/p/claude-watermarking
created: 2026-09-06
published: 2026-08-22
author: Sebastian Raschka, PhD
flashcards: none
updated: 2026-09-06
---

# How Claude Watermarks AI-Generated Text

<div align="center">
  <img src="https://substackcdn.com/image/fetch/$s_!2E7U!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb73bfb5-0291-4e5e-b425-6c3be054276e_1914x1076.png" width="220" />
</div>

- Anthropic announced that they will watermark the text outputs of their Claude models
- So, my goal here is really to explain how the underlying mechanism works and how they are going to implement this type of watermarking, text watermarking.

### How LLM Text Generation Works

- So assume again that our prompt is the capital of Germany is. And the first step here is to convert this into token IDs. So tokenizing it and converting it into token IDs is one of the main steps at the beginning. This is outside. It’s not inside the LLM; it’s outside of the LLM. So we are simply converting the text into token IDs. It’s just a format that embedding layers can work with.
- And then this passes through the LLM. And the LLM gives us a score distribution for the next token.
- The important part is that when we generate the next token (for example, “Berlin”), we have, at this point, a distribution of scores. So this is the output produced by the LLM.
- we’re looking at logit values. So these are just scores from minus infinity to plus infinity, like a range of scores. Here’s an example, ranging from about -8 or -9 to 20. We could convert these into a probability distribution, but technically, it’s not strictly necessary depending on how we sample. But so you can think of the logit values as the raw scores.

![](https://substackcdn.com/image/fetch/$s_!gpfA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25e84186-eb07-4bfa-ae49-3e8e01efe418_6667x3750.png)

- If you would run this prompt through an LLM, you would even see something more extreme: that everything is, like, very, very, very close to zero. And “Berlin” would probably be much, much higher even.
- ow here, “Berlin” is the highest score because you can think of it as the most, I guess, probable or plausible next token

![](https://substackcdn.com/image/fetch/$s_!u2Kj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5f5e5d5-de7f-4925-81cc-4e561aff444a_6667x3750.png)

- And this score is then detokenized, and we get “Berlin” back. So that is the process here on this slide: from an input prompt to conversion into token IDs and tokenization, passing it to the LLM, getting this score distribution, getting the next token, and converting it back into text.

![](https://substackcdn.com/image/fetch/$s_!ok-i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7255cfa-288b-4e42-9078-3fd42df67337_6667x3750.png)

- And then this text is appended to the input. So if we have a question that requires multiple output tokens, we keep going in this loop until the answer is complete. That usually means that the LLM generates an end-of-text token
- we could just technically select the highest one, the one with the highest score. This is called greedy decoding
- There are modifications like top-k sampling or top-p sampling where, let’s say, just for simplicity in top-k sampling, we would select the top 100 tokens and then apply this random choice only to the top 100, the 100 highest-scoring ones, so that we don’t get nonsense tokens in there.
- Now the prompt is: today’s weather is “cold,” and a possible answer could be, for example, “gray” or “overcast”. So in contrast to the “Berlin” example, I would say “gray” and “overcast” kind of are interchangeable.
- They are both reasonable next tokens for this prompt, given the goal of completing this text or writing the next token. So it’s almost like a coin flip which one we want to select. There is not really an objectively worse one of one or the other. So when we do the random sampling, because they also have relatively high scores and their scores are similarly high since they are both plausible tokens, we might get one or the other.
- with a random seed, we get a reproducible sequence of numbers.
- mentioned before that we might get either “gray” or “overcast” if we randomly sample. Now, if we use a specific random seed like 42, we would always, for example, select “overcast”. I mean, it’s still a random selection, but we make it deterministic.

![](https://substackcdn.com/image/fetch/$s_!L-VB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6547aa47-2631-4fda-a65d-06f7336e6794_6667x3750.png)

- Claude watermarking is kind of like the idea that it sets a random seed.
- instead of being like a number that is fixed based on
- they’re using a secret key that is essentially like an API key, a secret key, and from that key, together with the four previous words, they derive this random seed essentially.
- so instead of using random seed 99 here, for example, they have a secret key and also use information about the previous tokens to derive this random seed.

![](https://substackcdn.com/image/fetch/$s_!0dqQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4c3d6c6-4a48-4f13-8830-eb3e339129ba_6667x3750.png)

- So that means if we are, this is without watermarking, if we are running the prompt, or given the prompt through the LLM, we might sometimes get this answer here, sometimes this answer, and so forth.
- based on the number of positions, we might have 128 possible answers here. And of course, the longer the text, the more positions we have where we can have terms interchangeably, the more combinations, or the more output texts, there are.
- So, using a random seed, we can kind of fix which answer we get, because then the random sampling is still random, but it’s deterministic in the sense that it’s reproducible.
- Now, instead of just using a simple random seed, they have a so-called random key, where this random key is involved in selecting the text
- So detecting the watermark is only possible if we have access to the key
- it’s impossible to know because, in order to know, you would need the watermarking key. You need this scoring function, and then you have to score basically the text with a scoring function. And then the idea is that if the score is above a certain threshold, then the text is watermarked.
- Only Anthropic will have the key.

### How to Remove a Watermark


![](https://substackcdn.com/image/fetch/$s_!oeAq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71d15440-51d3-4039-8b10-fcb8777f25d9_6667x3750.png)

- Now, removing the watermark is interesting. So now that we know how the watermarking works, we also know the shortcomings. I mean, this is really highly dependent on specific tokens in certain positions.
- So we don’t know where these words are because we haven’t generated the watermark.
- So we don’t know which positions to look at.
- So the practical scenario here is that we could just randomly edit the text. So we would randomly change a few words and hope that we change enough positions to edit the watermark. So that would be one way to remove it.

### How the Watermark Scoring Function Works

- wanted to briefly also explain how this scoring function works because that is also interesting information.
- But the reason why they do it the certain way they do is to make the detection cheaper.
- if you wanted to check if something is watermarked, if even they wanted to check, they would have to rerun the prompt to get these scores and then apply this watermarking random seed to get this text and then compare.
- And that would be very expensive because then essentially every text you want to compare, you would have to rerun the LLM.
- It was a Nature paper, and this method is called SynthID-Text.
- It was by Google, and they use a similar technique they call Claude watermarking.

### SynthID Text and Tournament Sampling


![](https://substackcdn.com/image/fetch/$s_!DUPH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fab7ffafb-9733-4b4f-9789-1bd7d7bb15af_6667x3750.png)

- So instead, what they use, they also use it during the sampling, during the generation, so that it can be reused later during detection. What they use is called tournament sampling.

![](https://substackcdn.com/image/fetch/$s_!lUpe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27a7a689-db67-4c21-9f9b-7912ad7b0825_6667x3750.png)

- Here we have three watermarking functions, G1, G2, and G3. In reality, they might have 30, 50, or even more. Here I’m just using three because that is simpler on this slide.
- It’s basically like a bit string, like if you have bits of zeros and ones. Okay. So this is for “gray”. So we get the signature 101 through using these watermarking functions. Now we can do the same thing for all the other ones.

### Detecting Watermarks Without Rerunning the LLM


![](https://substackcdn.com/image/fetch/$s_!Hxlf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2b79f05-4b0f-4045-a07c-224d89465d28_6667x3750.png)

- We could have used NumPy’s `random.choice`. But the shortcoming of that is that if we want to score random text on the internet, we would have to rerun the LLM. With this technique, we don’t.
- it’s essentially just to make the detection easier and cheaper.
