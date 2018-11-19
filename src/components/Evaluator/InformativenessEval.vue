<template>
    <div>
        <header>
          <nav class="navbar fixed-top">
            <a class="navbar-brand" href="#">Manual Evaluation: Assessment Form</a>
          </nav>
        </header>
        <div class="card instruction">
          <div class="card-header my-header">
              Instructions
          </div>
            <!-- eslint-disable -->
          <div class="card-body">
            <h5 class="card-title my-title">Task Description</h5>
            <p class="card-text my-text">Your task is to assess the quality of the summary based on the article.</p>
          </div>
            <!-- eslint-enable -->
        </div>
        <div class="d-flex flex-row justify-content-center">
            <div ref="document" class='p-2 col-lg-5 document'>
            </div>
        </div>
        <div class="card summary">
          <div class="card-header my-header">
              Summary To Be Assessed
          </div>
            <!-- eslint-disable -->
          <div class="card-body">
            <p class="card-text my-text">u.s and european officials may impose a 4th round of sanctions on tehran when the u.n , security council considers the issue of iran 's nuclear energy program most likely in september 2007 .</p>
          </div>
            <!-- eslint-enable -->
        </div>
        <div class="card assessment">
          <div class="card-header my-header">
              Your Assessment
          </div>
            <!-- eslint-disable -->
          <div class="card-body">
            <h5 class="card-title my-title">Information Coverage</h5>
            <p class="card-text my-text">Is the summary missing information from the document?</p>
            <label for="" class="float-left">Everything is missing</label>
              <label for="" class="float-right">Nothing is missing</label>
              <input type="range" min="1" max="100" value=50 class="slider">
          </div>
          <div class="card-body">
            <h5 class="card-title my-title">Information Redundancy</h5>
            <p class="card-text my-text"> How much of the information in the summary is not important?</p>
            <label for="" class="float-left">Everything is not important</label>
              <label for="" class="float-right">Nothing is not importang</label>
              <input type="range" min="1" max="100" value=50 class="slider">
          </div>
            <!-- eslint-enable -->
        </div>
    </div>
</template>

<script>
import Word from '@/components/Component/Word.vue';
import Char from '@/components/Component/Char.vue';
import Vue from 'vue';

// const randomColor = require('randomcolor');
const axios = require('axios');

// const waitTimeForButton = 1;

function createAndMountWord(wordText, wordIndex) {
  const WordClass = Vue.extend(Word);
  const word = new WordClass({
    propsData: {
      word: wordText,
      index: wordIndex,
      type: 'word',
    },
  });
  word.$mount();
  this.words[this.words.length] = word;
  this.$refs.document.appendChild(word.$el);
}

function createAndMountWhitespace(whitespaceIndex) {
  const CharClass = Vue.extend(Char);
  const char = new CharClass({
    propsData: {
      bgColor: '#ffffff',
      type: 'whitespace',
      index: whitespaceIndex,
    },
  });
  char.$slots.default = [' '];
  char.$mount();
  this.whitespaces[whitespaceIndex] = char;
  this.$refs.document.appendChild(char.$el);
}

function parseDoc(textJSON) {
  for (let i = 0; i < textJSON.components.length; i += 1) {
    const comp = textJSON.components[i];
    if (comp.type === 'word') {
      createAndMountWord.call(this, comp.word, i);
    }
    if (comp.type === 'whitespace') {
      createAndMountWhitespace.call(this, comp.word, i);
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
  axios.post('annotation_json')
    .then((response) => {
      parseDoc.call(this, response.data);
      highlightDoc.call(this, response.data);
    })
    .catch((error) => {
      console.log(error);
    });
}

export default {
  name: 'InformativenessEval',
  data() {
    return {
      words: {},
      whitespaces: {},
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
  font-size: 21px;
  line-height: 33px;
}
.summary {
    position: fixed;
    top: 70px;
    left: 1400px;
    width: 450px;
}
.assessment {
    position: fixed;
    top: 300px;
    left: 1400px;
    width: 450px;
}
.instruction {
  position: fixed;
  top: 70px;
  left: 20px;
  width: 450px;
}
.my-header {
  font-size: 20px;
}
.my-title {
    font-size: 18px;
    text-decoration: underline;
}
.my-text {
    font-size: 16px;
}
/* The slider itself */
.slider {
    -webkit-appearance: none;  /* Override default CSS styles */
    appearance: none;
    width: 100%; /* Full-width */
    height: 25px; /* Specified height */
    background: #d3d3d3; /* Grey background */
    outline: none; /* Remove outline */
    opacity: 0.7; /* Set transparency (for mouse-over effects on hover) */
    -webkit-transition: .2s; /* 0.2 seconds transition on hover */
    transition: opacity .2s;
}

/* Mouse-over effects */
.slider:hover {
    opacity: 1; /* Fully shown on mouse-over */
}

.slider::-webkit-slider-thumb {
    -webkit-appearance: none; /* Override default look */
    appearance: none;
    width: 25px; /* Set a specific slider handle width */
    height: 25px; /* Slider handle height */
    background: #4CAF50; /* Green background */
    cursor: pointer; /* Cursor on hover */
}

.slider::-moz-range-thumb {
    width: 25px; /* Set a specific slider handle width */
    height: 25px; /* Slider handle height */
    background: #4CAF50; /* Green background */
    cursor: pointer; /* Cursor on hover */
}
</style>
