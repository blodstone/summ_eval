<template>
    <div class="container is-fluid">
        <div class="columns">
            <div class="column is-3">
                <div class="box instruction">
                    <div class="content">
                        <h2>
                            Instructions
                        </h2>
                        <!-- eslint-disable -->
                        <h5 class="my-title">Task Description</h5>
                        <p class="my-text">Your task is to assess the quality of the summary based on the article.</p>
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
                        <p class="my-text">summary</p>
                        <hr>
                        <h5 class="my-header">
                            Your Assessment
                        </h5>
                        <h5 class="my-title">Question #1</h5>
                        <p class="my-text"> Is the summary missing important information?</p>
                        <p class="my-text">
                            <strong>{{ coverage }} % </strong> of information is missing
                        </p>
                        <div class="level" align="center">
                            <span class="level-left">
                                <label class="label is-small">Nothing is <br> missing</label>
                            </span>
                            <span class="level-item">
                            <input type="range" min="0" max="100"
                                   v-model="coverage" class="my-slider slider is-info is-fullwidth ">
                            </span>
                            <span class="level-right">
                                <label class="label is-small">Everything <br> is missing</label>
                            </span>
                        </div>
                        <h5 class="my-title">Question #2</h5>
                        <p class="my-text"> Does the summary contain only important information?</p>
                        <p class="my-text">
                            <strong>{{ redundancy }} % </strong> of information is important
                        </p>
                        <div class="level" align="center">
                            <span class="level-left">
                                <label class="label is-small">Nothing is <br> important</label>
                            </span>
                            <span class="level-item">
                            <input type="range" min="0" max="100"
                                   v-model="redundancy" class="my-slider slider is-info is-fullwidth ">
                            </span>
                            <span class="level-right">
                                <label class="label is-small">Everything <br> is important</label>
                            </span>
                        </div>

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

// const randomColor = require('randomcolor');
const axios = require('axios');

// const waitTimeForButton = 1;


function createAndMountWord(sent, token, wordIndex, opacities) {
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
  if (this.components.length in opacities) {
    word.highlight('#ff0000', opacities[this.components.length]);
  }
  this.words[wordIndex] = word;
  this.words2Groups[wordIndex] = [];
  this.$refs.document.appendChild(word.$el);
}

function createAndMountWhitespace(whitespace, whitespaceIndex, opacities) {
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
  if (this.components.length in opacities) {
    char.highlight('#ff0000', opacities[this.components.length]);
  }
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

function collectAndCountHighlight(results) {
  const opacities = {};
  let max = -1;
  for (let i = 0; i < Object.keys(results).length; i += 1) {
    const result = results[Object.keys(results)[i]];
    for (let j = 0; j < Object.keys(result.highlights).length; j += 1) {
      const highlight = result.highlights[Object.keys(result.highlights)[j]];
      for (let k = 0; k < highlight.indexes.length; k += 1) {
        if (Object.keys(opacities).includes(highlight.indexes[k])) {
          opacities[highlight.indexes[k]] += 1;
        } else {
          opacities[highlight.indexes[k]] = 1;
        }
        if (opacities[highlight.indexes[k]] > max) {
          max = opacities[highlight.indexes[k]];
        }
      }
    }
  }
  for (let i = 0; i < Object.keys(opacities).length; i += 1) {
    opacities[Object.keys(opacities)[i]] /= max;
  }
  return opacities;
}

function parseDoc(textJSON) {
  const opacities = collectAndCountHighlight(textJSON.results);
  let wordIndex = 0;
  let whitespaceIndex = 0;
  const { endSentIndex } = textJSON.paragraph;
  for (let i = 0; i < textJSON.sentences.length; i += 1) {
    const sent = textJSON.sentences[i];
    for (let j = 0; j < sent.tokens.length; j += 1) {
      const token = sent.tokens[j];
      createAndMountWord.call(this, sent, token, wordIndex, opacities);
      // check is last element
      if (j !== sent.tokens.length - 2) {
        createAndMountWhitespace.call(this, ' ', whitespaceIndex, opacities);
        whitespaceIndex += 1;
      }
      wordIndex += 1;
    }
    if (endSentIndex.includes(sent.index + 1)) {
      createAndMountLineBreaker.call(this);
    }
  }
}

function highlightDoc(textJSON) {
  for (let i = 0; i < Object.keys(textJSON.highlights).length; i += 1) {
    const key = Object.keys(textJSON.highlights)[i];
    const highlight = textJSON.highlights[key];
    for (let j = 0; j < highlight.indexes.length; j += 1) {
      const index = highlight.indexes[j];
      this.words[index].highlight('#ff0000');
    }
  }
}

function getFile() {
  axios.get(`project/${this.project_id}/single_doc`)
    .then((response) => {
      parseDoc.call(this, JSON.parse(response.data.doc_json));
      this.doc_status_id = response.data.doc_status_id;
    })
    .catch((error) => {
      this.$toast.open({
        message: `${error}`,
        type: 'is-danger',
      });
    });
}

export default {
  name: 'InformativenessEval',
  data() {
    return {
      components: [],
      // A collection of Word components
      words: {},
      // A collection of Char components
      whitespaces: {},
      // A mapping of whitespace index to group index
      whitespaces2Groups: {},
      // A mapping of word index to group index
      words2Groups: {},
      redundancy: 50,
      coverage: 50,
      project_id: this.$route.params.project_id,
    };
  },
  mounted: function onMounted() {
    getFile.call(this);
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
</style>
