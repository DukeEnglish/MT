This is the folder for machine translation

BLEU (Bilingual Evaluation Understudy) is an efficient way to evaluate the quality of translation considering
51 the order of words. And it could get the score of similarity between reference and output.
52 The way to calculate BLEU depends on the n in n-gram we used:

\subsubsection{BLEU}
BLEU (Bilingual Evaluation Understudy) is an efficient way to evaluate the quality of translation considering the order of words. And it could get the score of similarity between reference and output. 

The way to calculate BLEU depends on the n in n-gram we used:

BLEU-n = brevity\_penalty*exp$(\sum_{i=1}^{n}\lambda_ilog(precision_i))$

These is brevity penalty, which considers the problem of lossing word. Usually, we choose n =4 and $\lambda$ = 1, so we have:

BLEU-4 = min (1, $\frac{(output-length)}{(reference-length)}*\prod_{i=1}^{4}precision_i$

One of BLEU-n for any n is 0, so BLEU-n is 0, which means there is no one n-gram matching with reference. Therefore, we ofern calculate BLEU over the whole dataset.
\subsubsection{CHRF}
In this experiment we also choose a metrics using Fscore based on character n-grams, CHRF
score. The general formula for CHRF score is:

$CHRF\beta=(1+\beta^2)\frac{(CHRP*CHRR)}{(\beta ^2*CHRP+CHRR)}$

Where CHRP and CHRR stand for character n-gram precision and recall arithmetically aceraged over all n-gram:
\begin{itemize}
\item CHRP
percentage of n-gram in the hypothesis which have a counterpart in the reference;

\item CHRR
percentage of character n-grams in the reference which are also present in the hypothesis.

\item where $\beta$ is a parameter which assign $\beta$ times more importance to recall than to precision $-$ if $\beta = 1$, they have the same importance. In terms of Popovic (2015), $\beta = 3$ in our experiment.
\end{itemize}
