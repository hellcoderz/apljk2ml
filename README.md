# apljk2ml

Source to source convertor from J/K source to ML libraires source like tensorflow/keras/mxnet/pytorch etc.

## Introduction

- the motive of this project is to create source to source convertor
- Input language will be J or K (which are both decendant of APL)
- Array programming languages work on with vectors/array and are terse and easy to express mathematical notation in code
- Tensorflow/keras/pytorch etc have their own DSLs to create model architecture
- main use case for this project is to use same high level syntax of J or K language to generate source for different backend (source code for ML libs)
- translating mathematical concepts in machine learning models will becore easier when coded in J or K
- sharing of code will easier (due to J or K terseness)
- thinking in mathematical terms will be easier
- reasoning about code will be easier
- optimization of destination src code will be easier for someone new to that library
