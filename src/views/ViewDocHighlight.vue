<template>
  <div class="container is-fluid home">
    <div class="columns">
      <div class="column is-3">
        <div class="box instruction">
          <div class="content">
            <h1>
              Control
            </h1>
            <!-- eslint-disable -->
            <p class="my-text">Words that are important in the document have been highlighted using heatmap
              coloring (<strong>Darker color signifies higher importance</strong>). You have to decide which
              importance level that signifies the informativeness of words.</p>
            <p class="my-text">Use the slider to remove light color (less important highlights) by sliding it to
              the right. The number tells you how many color you can remove until there is only one color (the
              most important words) left.</p>
          </div>
          <div style="margin-bottom: 1.8rem; margin-top: 1.8rem; flex: 1;">
            <vue-slider ref="slider" v-model="intensitySlider.value"
                        v-bind="intensitySlider.options" v-on:input="onSliderInput">
            </vue-slider>
          </div>
        </div>
      </div>
      <div class="column">
        <div class="box document">
          <div ref="document">
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

const axios = require('axios');

function createAndMountWord(sent, token, wordIndex) {
  const WordClass = Vue.extend(Word);
  let aWord = token.word;
  if (aWord === '-LRB-') {
    aWord = '(';
  } else if (aWord === '-RRB-') {
    aWord = ')';
  } else if (aWord === '``') {
    aWord = '"';
  } else if (aWord === '\'\'') {
    aWord = '"';
  }
  const word = new WordClass({
    propsData: {
      sentIndex: sent.index,
      tokenIndex: token.index,
      word: aWord,
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

function redrawHighlight() {
  this.slidersValue.push(this.intensitySlider.value);
  for (let i = 0; i < Object.keys(this.highlight.intensities).length; i += 1) {
    const index = parseInt(Object.keys(this.highlight.intensities)[i], 10);
    const intensity = this.highlight.intensities[Object.keys(this.highlight.intensities)[i]];
    let low = 0;
    if (this.highlight.max !== this.highlight.min) {
      low = 1 - ((this.intensitySlider.value - this.highlight.min) /
        (this.highlight.max - this.highlight.min));
    }
    if (intensity >= low) {
      this.components[index].highlight(`rgba(255, ${255 - (intensity * 255)}, 0)`);
    } else {
      this.components[index].rmHighlight();
    }
  }
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
          this.highlight.intensities[highlight.indexes[k]] = 1;
        }
        if (this.highlight.intensities[highlight.indexes[k]] > this.highlight.max) {
          this.highlight.max = this.highlight.intensities[highlight.indexes[k]];
        }
        if (this.highlight.intensities[highlight.indexes[k]] < this.highlight.min) {
          this.highlight.min = this.highlight.intensities[highlight.indexes[k]];
        }
      }
    }
  }
  for (let i = 0; i < Object.keys(this.highlight.intensities).length; i += 1) {
    const intensity = this.highlight.intensities[Object.keys(this.highlight.intensities)[i]];
    let normIntensity = 0;
    if (this.highlight.max !== this.highlight.min) {
      normIntensity = (intensity - this.highlight.min) /
        (this.highlight.max - this.highlight.min);
    }
    this.highlight.intensities[Object.keys(this.highlight.intensities)[i]] = normIntensity;
  }
  // Slider setting
  for (let i = this.highlight.min; i <= this.highlight.max; i += 1) {
    this.intensitySlider.options.data.push(i);
  }
  this.intensitySlider.max = this.highlight.max;
  this.intensitySlider.min = this.highlight.min;
  this.intensitySlider.value = this.highlight.max;
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
  axios.get(`/highlight/get/${this.doc_id}`)
    .then((response) => {
      parseDoc.call(this, response.data.doc_json);
      redrawHighlight.call(this);
    })
    .catch((error) => {
      this.$toast.open({
        message: `${error}`,
        type: 'is-danger',
      });
    });
}

export default {
  name: 'ViewDocHighlight',
  components: {
    vueSlider,
  },
  methods: {
    onSliderInput() {
      redrawHighlight.call(this);
    },
  },
  data() {
    return {
      highlight: {
        intensities: {},
        max: -1,
        min: 999,
      },
      intensitySlider: {
        value: 0,
        options: {
          tooltip: 'always',
          data: [],
          speed: 0.3,
          min: 1,
          max: 0,
          piecewiseLabel: true,
          piecewise: true,
          reverse: true,
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
      slidersValue: [],
      doc_id: this.$route.params.doc_id,
    };
  },
  mounted: function onMounted() {
    getFile.call(this);
  },
};
</script>
<style scoped>
.content li + li {
  margin: 0;
}
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
