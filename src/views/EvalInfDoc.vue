<template>
    <div class="container is-fluid home">
        <div class="columns is-2 is-variable">
            <div class="column is-3">
                <div class="box instruction">
                    <div class="content">
                        <h1>
                            Instructions & Controls
                        </h1>
                        <!-- eslint-disable -->
                        <h5 class="my-header">Instruction</h5>
                        <h5 class="my-title">Task Description</h5>
                        <p class="my-text">
                            Your task is to assess the quality of the summary based on the article.
                        </p>
                        <hr>
                        <h5 class="my-header">Controls</h5>
                        <h5 class="my-title">Heatmap</h5>
                        <p class="my-text">Phrases that are important in the document have been marked using heatmap coloring. The higher the intensity the greater the phrases' importance. You can view certain intensities range by changing the slider below.</p>
                        <div style="margin-bottom: 1.8rem; margin-top: 1.8rem">
                            <vue-slider v-model="intensitySlider.value"
                                        v-bind="intensitySlider.options"
                                        v-on:input="onSliderInput"></vue-slider>
                        </div>
                    </div>
                </div>
            </div>
            <div class="column">
                <div class="box document">
                    <div ref="document">
                    </div>
                </div>
            </div>
            <div class="column is-3">
                <div class="box summary">
                    <div class="content">
                        <h1>Assessment</h1>
                        <h5 class="my-header">Summary to be assessed</h5>
                        <p class="my-summary">{{ system_text }}</p>
                        <hr>
                        <h5 class="my-header">
                            Your Assessment
                        </h5>
                        <h5 class="my-title">Question #1</h5>
                        <p class="my-text"> Is the summary missing important information?</p>
                        <p class="my-text">
                            <strong>{{ recall }} % </strong> of information is missing
                        </p>
                        <div class="level" align="center">
                            <span class="level-left">
                                <label class="label is-small">Nothing <br/> is <br/> missing</label>
                            </span>
                            <span class="level-item">
                            <input type="range" min="0" max="100"
                                   v-model="recall" class="my-slider slider is-info is-fullwidth">
                            </span>
                            <span class="level-right">
                                <label class="label is-small">Everything <br/> is <br/> missing</label>
                            </span>
                        </div>
                        <h5 class="my-title">Question #2</h5>
                        <p class="my-text"> Does the summary contain only important information?</p>
                        <p class="my-text">
                            <strong>{{ precision }} % </strong> of information is important
                        </p>
                        <div class="level" align="center">
                            <span class="level-left">
                                <label class="label is-small">Nothing <br/> is <br/> important</label>
                            </span>
                            <span class="level-item">
                            <input type="range" min="0" max="100"
                                   v-model="precision" class="my-slider slider is-info is-fullwidth">
                            </span>
                            <span class="level-right">
                                <label class="label is-small">Everything <br/> is <br/> important</label>
                            </span>
                        </div>
                        <a class="button is-primary" :disabled="timer.isRunning"
                    v-on:click="saveEvaluation()">{{ timenow }}</a>
                    </div>
                </div>
            </div>
            <!-- eslint-enable -->
        </div>
    </div>
</template>

<script>
import Word from '@/components/Component/Word.vue';
import Char from '@/components/Component/Char.vue';
import LineBreaker from '@/components/Component/LineBreaker.vue';
import Vue from 'vue';
import vueSlider from 'vue-slider-component';
// const randomColor = require('randomcolor');
const axios = require('axios');

const waitTimeForButton = 5;

function createAndMountWord(sent, token, wordIndex) {
  const WordClass = Vue.extend(Word);
  const word = new WordClass({
    propsData: {
      sentIndex: sent.index,
      tokenIndex: token.index,
      word: token.word,
      index: wordIndex,
      compIndex: this.components.length,
      type: 'word',
    },
  });
  word.$mount();
  this.components.push(word);
  this.words[wordIndex] = word;
  this.words2Groups[wordIndex] = [];
  this.$refs.document.appendChild(word.$el);
}

function createAndMountWhitespace(whitespace, whitespaceIndex) {
  const CharClass = Vue.extend(Char);
  const char = new CharClass({
    propsData: {
      bgColor: '#ffffff',
      type: 'whitespace',
      index: whitespaceIndex,
      compIndex: this.components.length,
    },
  });
  char.$slots.default = [whitespace];
  char.$mount();
  this.components.push(char);
  this.whitespaces[whitespaceIndex] = char;
  this.whitespaces2Groups[whitespaceIndex] = [];
  this.$refs.document.appendChild(char.$el);
}

function createAndMountLineBreaker() {
  const LineBreakerClass = Vue.extend(LineBreaker);
  const lineBreaker = new LineBreakerClass();
  lineBreaker.$mount();
  this.$refs.document.appendChild(lineBreaker.$el);
}

function getIntensities(results) {
  for (let i = 0; i < Object.keys(results).length; i += 1) {
    const result = results[Object.keys(results)[i]];
    for (let j = 0; j < Object.keys(result.highlights).length; j += 1) {
      const highlight = result.highlights[Object.keys(result.highlights)[j]];
      for (let k = 0; k < highlight.indexes.length; k += 1) {
        if ((highlight.indexes[k] in this.highlight.intensities)) {
          this.highlight.intensities[highlight.indexes[k]] += 1;
        } else {
          this.highlight.intensities[highlight.indexes[k]] = 0;
        }
        if (this.highlight.intensities[highlight.indexes[k]] > this.highlight.max) {
          this.highlight.max = this.highlight.intensities[highlight.indexes[k]];
        }
      }
    }
  }
  for (let i = 0; i < Object.keys(this.highlight.intensities).length; i += 1) {
    this.highlight.intensities[Object.keys(this.highlight.intensities)[i]] /= this.highlight.max;
  }
  // Slider setting
  for (let i = 0; i <= this.highlight.max; i += 1) {
    this.intensitySlider.options.data.push(i);
  }
  this.intensitySlider.value = [0, this.highlight.max];
}

function redrawHighlight() {
  for (let i = 0; i < Object.keys(this.highlight.intensities).length; i += 1) {
    const index = parseInt(Object.keys(this.highlight.intensities)[i], 10);
    const intensity = this.highlight.intensities[Object.keys(this.highlight.intensities)[i]];
    const nLow = this.intensitySlider.value[0] / this.highlight.max;
    const nHigh = this.intensitySlider.value[1] / this.highlight.max;
    if (intensity <= nHigh && intensity >= nLow) {
      this.components[index].highlight(`rgba(255, ${255 - (intensity * 255)}, 0)`);
    } else {
      this.components[index].rmHighlight();
    }
  }
}

function parseDoc(textJSON) {
  getIntensities.call(this, textJSON.results);
  let wordIndex = 0;
  let whitespaceIndex = 0;
  const { endSentIndex } = textJSON.paragraph;
  for (let i = 0; i < textJSON.sentences.length; i += 1) {
    const sent = textJSON.sentences[i];
    for (let j = 0; j < sent.tokens.length; j += 1) {
      const token = sent.tokens[j];
      createAndMountWord.call(this, sent, token, wordIndex);
      // check is last element
      if (j !== sent.tokens.length - 2) {
        createAndMountWhitespace.call(this, ' ', whitespaceIndex);
        whitespaceIndex += 1;
      }
      wordIndex += 1;
    }
    if (endSentIndex.includes(sent.index + 1)) {
      createAndMountLineBreaker.call(this);
    }
  }
}

function getFile() {
  axios.get(`project/evaluation/informativeness_doc/${this.project_id}/single_doc`)
    .then((response) => {
      parseDoc.call(this, response.data.doc_json);
      this.system_text = response.data.system_text;
      this.summ_status_id = response.data.summ_status_id;
    })
    .catch((error) => {
      this.$toast.open({
        message: `${error}`,
        type: 'is-danger',
      });
    });
}

function getColor(val) {
  return 255 - ((val / this.highlight.max) * 255);
}

function sendResult(resultJSON) {
  axios.post('project/save_result/evaluation', resultJSON)
    .then(() => {
      this.$toast.open({
        message: 'Submission successful.',
        type: 'is-success',
      });
    })
    .catch((error) => {
      this.$toast.open({
        message: `${error}`,
        type: 'is-danger',
      });
    });
}

export default {
  name: 'EvalInfDoc',
  components: {
    vueSlider,
  },
  computed: {
    timenow() {
      if (this.timer.isRunning === true) {
        if ((this.timer.now - this.timer.date) < waitTimeForButton) {
          return `Wait ${waitTimeForButton - (this.timer.now - this.timer.date)} seconds`;
        }
        // eslint-disable-next-line
        this.timer.isRunning = false;
        window.clearInterval(this.timer.timer);
      }
      return 'Click to submit';
    },
  },
  methods: {
    onSliderInput() {
      const first = getColor.call(this, this.intensitySlider.value[0]);
      const second = getColor.call(this, this.intensitySlider.value[1]);
      this.intensitySlider.options.processStyle.backgroundImage =
        `-webkit-linear-gradient(left, rgba(255,${first},0,1), rgba(255,${second},0,1))`;
      this.intensitySlider.options.sliderStyle = [
        {
          backgroundColor: `rgba(255,${first},0,1)`,
        },
        {
          backgroundColor: `rgba(255,${second},0,1)`,
        }];
      redrawHighlight.call(this);
    },
    saveEvaluation() {
      const resultJSON = {
        project_id: this.project_id,
        status_id: this.summ_status_id,
        precision: this.precision,
        recall: this.recall,
        category: 'Informativeness_Doc',
      };
      sendResult.call(this, resultJSON);
    },
  },
  data() {
    return {
      highlight: {
        intensities: {},
        max: -1,
      },
      timer: {
        now: Math.trunc(new Date().getTime() / 1000),
        date: Math.trunc(new Date().getTime() / 1000),
        isRunning: true,
        timer: null,
      },
      intensitySlider: {
        value: [0, 2],
        options: {
          tooltip: 'always',
          tooltipDir: [
            'bottom',
            'top',
          ],
          piecewise: false,
          piecewiseLabel: true,
          data: [],
          sliderStyle: [
            {
              backgroundColor: 'rgba(255,255,0,1)',
            },
            {
              backgroundColor: 'rgba(255,0,0,1)',
            },
          ],
          processStyle: {
            backgroundImage:
              '-webkit-linear-gradient(left, rgba(255,255,0,1), rgba(255,0,0,1))',
          },
        },
      },
      components: [],
      // A collection of Word components
      words: {},
      // A collection of Char components
      whitespaces: {},
      // A mapping of whitespace index to group index
      whitespaces2Groups: {},
      // A mapping of word index to group index
      words2Groups: {},
      precision: 50,
      recall: 50,
      project_id: this.$route.params.project_id,
      system_text: '',
    };
  },
  mounted: function onMounted() {
    getFile.call(this);
    this.timer.timer = window.setInterval(() => {
      this.timer.now = Math.trunc((new Date()).getTime() / 1000);
    }, 1000);
  },
};
</script>

<style scoped>
.document {
  font-family: 'Lora', serif;
  font-size: 1.2rem;
  line-height: 1.5rem;
}
.summary {
  position: sticky;
  position: -webkit-sticky;
  top: 70px;
}
.instruction {
  position: sticky;
  position: -webkit-sticky;
  top: 70px;
}
.my-header {
  font-size: 1.1rem;
}
.my-title {
    font-size: 1rem;
    text-decoration: underline;
}
.my-text {
    font-size: 0.9rem;
}
.my-summary{
    font-size: 1.1rem;
}
.home {
    padding-top: 25px;
}
</style>
