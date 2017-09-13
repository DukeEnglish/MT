This is the folder for machine translation

BLEU (Bilingual Evaluation Understudy) is an efficient way to evaluate the quality of translation considering
51 the order of words. And it could get the score of similarity between reference and output.
52 The way to calculate BLEU depends on the n in n-gram we used:
BLEU-n = brevity_penalty*exp(
Pn
i=1 53 ilog(precisioni))
54 These is brevity penalty, which considers the problem of lossing word. Usually, we choose n =4 and  = 1,
55 so we have:
BLEU-4 = min (1, (output􀀀length)
(reference􀀀length) 
Q4
i=1 56 precisioni
57 One of BLEU-n for any n is 0, so BLEU-n is 0, which means there is no one n-gram matching with reference.
58 Therefore, we ofern calculate BLEU over the whole dataset.
