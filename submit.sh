#!/bin/bash

condor_submit part1_pre.sub

condor_submit part1_in.sub

condor_submit part1_post.sub

condor_submit part2.sub
