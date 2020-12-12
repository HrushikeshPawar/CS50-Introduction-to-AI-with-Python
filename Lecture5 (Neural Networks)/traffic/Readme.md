# Project 5  -  Traffic

In this project I tried using different combinations of setting to get different results. Below is a summary of these combinations :

* The first trial was a simplest of all, sequential model with one convolution layer with 32 filters each with 3x3 kernel, a max-pooling layer of size 2x2 and a dropout of 50%. This model gave a training accuracy of 86.20%  and  a test accuracy of 90.79% Quite a good result for such a simplestic model.

* The next was same as the first one, but with a convalution layer with 64 filters. This model increased the accuracy by very tiny model, train - 87.96%  and  test - 90.92%

* The third try was the best with two convolution layers with a max-pooling layer in between and a dropout of 50%. This model gave a training accuracy of 92.66%  and  a testing accuracy of 95.61%

* This forth combination turned out to be the worst of all, two convolution layers and two max-pooling layers arranged in alternate manner with a dropout of 50%, gave a result whose accuracy couldn't cross the 20% mark. Too much of good can also harm you. I guess the reason behind this was, we started with images of size 30x30 and when the model went through 2nd max-pooling layer the size have reduced to 6x6, very small to work with.

* All the next combinations were to add different numbers of hidden dense layers with 128 nodes to all the above combinations. Tried adding 1 to 3 dense layers to above combinations. But the accuracy was between 92% to 96% marks, very tiny increase considering the amount of calculations done.

* Hence, the model with two convolutions layers with 64 filters of 3x3 kernels and a single max-pooling layer of size 2x2 with dropout of 50% is best I tried, considering the amount of resources required and the accuracy achieved.
