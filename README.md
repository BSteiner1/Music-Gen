# 🎵 Music-Gen

#### A project on Symbolic Music Generation

## ♯ Part 1: Generating New Bach Chorales

* We use the [Bach Doodle Dataset](https://magenta.tensorflow.org/datasets/bach-doodle) to generate new four-bar phrases of music.
* User melodies are harmonised in the style of Bach Chorales by [CoCoNet](https://magenta.tensorflow.org/coconet).
* We then train an LSTM-GAN to be able to generate new examples.

## ♭ Part 2: Long-Term Harmonic Structure

* Generating music with long-term structure such as repeated themes or chord progressions is still a challenge.
* The main idea is to develop an RNN architecture that effectively captures ideas from previous bars.
* For example, [Lookback and Attention](https://magenta.tensorflow.org/2016/07/15/lookback-rnn-attention-rnn) are methods that can be useful to create long-term structure.


### 🔮 For The Future:

#### 👀 Latent Feature Personalisation
* We can explore how the latent features affect the characteristics of the music produced.
* This could assist the composer in personalisation of the music.

#### 🟥 Penalty Term
* During the learning process, we could add a penalty term as well to the loss function that rewards various themes depending on the task.
* For Part 1, this could be in the form of penalising the presence of Parallel Fifths / Octaves.
* In Part 2, we could reward the model for repeating melodic themes or chord progressions.
