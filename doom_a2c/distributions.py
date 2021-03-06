#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 11:35:22 2018

@author: anonymous
"""
import math

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


class Categorical(nn.Module):
    def __init__(self, num_inputs, num_outputs):
        super(Categorical, self).__init__()
        self.linear = nn.Linear(num_inputs, num_outputs)

    def forward(self, x):
        x = self.linear(x)
        return x

    def sample(self, x, deterministic):
        x = self(x)
        
        probs = F.softmax(x, dim=1)
        if deterministic is False:
            action = probs.multinomial(num_samples=1)
        else:
            action = probs.max(1, keepdim=True)[1]
        return action

    def logprobs_and_entropy(self, x, actions):
        x = self(x)
        log_probs = F.log_softmax(x, dim=1)
        probs = F.softmax(x, dim=1)
        action_log_probs = log_probs.gather(1, actions)

        dist_entropy = -(log_probs * probs).sum(-1).mean()
        return action_log_probs, dist_entropy, probs

