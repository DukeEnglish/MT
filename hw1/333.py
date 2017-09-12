#!/usr/bin/env python
import optparse
import sys
import numpy as np
import models
from collections import namedtuple

optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="data/input", help="File containing sentences to translate (default=data/input)")
optparser.add_option("-t", "--translation-model", dest="tm", default="data/tm", help="File containing translation model (default=data/tm)")
optparser.add_option("-l", "--language-model", dest="lm", default="data/lm", help="File containing ARPA-format language model (default=data/lm)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to decode (default=no limit)")
optparser.add_option("-k", "--translations-per-phrase", dest="k", default=1, type="int", help="Limit on number of translations to consider per phrase (default=1)")
optparser.add_option("-s", "--stack-size", dest="s", default=1, type="int", help="Maximum stack size (default=1)")
optparser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False,  help="Verbose mode (default=off)")
opts = optparser.parse_args()[0]

tm = models.TM(opts.tm, opts.k)
lm = models.LM(opts.lm)
french = [tuple(line.strip().split()) for line in open(opts.input).readlines()[:opts.num_sents]]

# tm should translate unknown words as-is with probability 1
for word in set(sum(french,())):
  if (word,) not in tm:
    tm[(word,)] = [models.phrase(word, 0.0)]

sys.stderr.write("Decoding %s...\n" % (opts.input,))
for f in french:
  # The following code implements a monotone decoding
  # algorithm (one that doesn't permute the target phrases).
  # Hence all hypotheses in stacks[i] represent translations of 
  # the first i words of the input sentence. You should generalize
  # this so that they can represent translations of *any* i words.
  hypothesis = namedtuple("hypothesis", "logprob, lm_state, predecessor, phrase")
  initial_hypothesis = hypothesis(0.0, lm.begin(), None, None)
  stacks = [{} for _ in f] + [{}]
  stacks[0][lm.begin()] = initial_hypothesis
  for i, stack in enumerate(stacks[:-1]):
    for h in sorted(stack.itervalues(),key=lambda h: -h.logprob)[:opts.s]: # prune
      for j in xrange(i+1,len(f)+1):
        if f[i:j] in tm:
          for phrase in tm[f[i:j]]:

            #The monotone, unchanged
            logprob = h.logprob + phrase.logprob

            lm_state = h.lm_state
            for word in phrase.english.split():
              (lm_state, word_logprob) = lm.score(lm_state, word)
              logprob += word_logprob
            logprob += lm.end(lm_state) if j == len(f) else 0.0
            new_hypothesis = hypothesis(logprob, lm_state, h, phrase)

            if lm_state not in stacks[j] or stacks[j][lm_state].logprob < logprob: # second case is recombination
              stacks[j][lm_state] = new_hypothesis 


        # need to iterate through every possible adjacent phrase
        # phrase2 can extend from end of phrase1 until end of tm
        for k in range(i+1, j):
          
          if f[i:k] in tm and f[k:j] in tm:
            
            for phrase1 in tm[f[i:k]]:
              
              for phrase2 in tm[f[k:j]]:
                
                logprob2 = h.logprob + phrase2.logprob

                # summate logprob for words in phrase 2
                lm_state2 = h.lm_state
                for word in phrase2.english.split():
                  (lm_state2, word_logprob) = lm.score(lm_state2, word)
                  logprob2 += word_logprob
                # set new hypothesis for phrase 2
                new_hypothesis2 = hypothesis(logprob2, lm_state2, h, phrase2)

            logprob1 = logprob2 + phrase1.logprob

            #summate logprob for words in phrase 1
            lm_state1 = lm_state2
            for word in phrase1.english.split():
              (lm_state1, word_logprob) = lm.score(lm_state1, word)
              logprob1 += word_logprob

            # if phrase extends to end of sentence add EOS
            logprob1 += lm.end(lm_state1) if j == len(f) else 0.0
            new_hypothesis1 = hypothesis(logprob1, lm_state1, new_hypothesis2, phrase1)

            if lm_state1 not in stacks[j] or stacks[j][lm_state1].logprob < logprob1: # second case is recombination
              stacks[j][lm_state1] = new_hypothesis1

  # unchanged
  winner = max(stacks[-1].itervalues(), key=lambda h: h.logprob)
  def extract_english(h): 
    return "" if h.predecessor is None else "%s%s " % (extract_english(h.predecessor), h.phrase.english)
  print extract_english(winner)

  if opts.verbose:
    def extract_tm_logprob(h):
      return 0.0 if h.predecessor is None else h.phrase.logprob + extract_tm_logprob(h.predecessor)
    tm_logprob = extract_tm_logprob(winner)
    sys.stderr.write("LM = %f, TM = %f, Total = %f\n" % 
      (winner.logprob - tm_logprob, tm_logprob, winner.logprob))
