 <template>
  <div>
    <div class='row card-deck'>
      <div class='card col-8'>
        <div class='card-header'>Document</div>
        <div class='card-body document'
          v-on:mouseup="captureHighlight"
          v-html="doc.createHTML()"></div>
      </div>
      <div class='card col-4'>
        <div class='card-header'>Guidelines</div>
        <div class='card-body'>
          <p>You have been given a document and guidelines to help you form a summary.
            Please read the document and then highlights fragments of sentences to form a
            100 words summary based on the following guidelines.</p>

          <p>1. The summary tells you who was involved in the document narration and
          the information is correct.</p>

          <p>2. The summary tells you what had happened in the document narration and
          the information is correct.</p>

          <p>3. The summary tells you where the event took place in the document
          narration and the information is correct.</p>

          <p>4. The summary tells you when did the event happen in the document
          narration and the information is correct.</p>

          <p>5. The summary tells you why did the event happen in the document
          narration and the information is correct.</p>

          <p>6. The summary tells you how did the event happen in the document
          narration and the information is correct.</p>
        </div>
      </div>
    </div>
    <div class="row card-deck">
      <div class="card col-11 lower-card">
        <div class="card-header">Summary</div>
        <div class='card-body col highlights' v-html="markedText"></div>
      </div>
      <div class="card col-1 lower-card">
        <div class='card-header'>Words Left</div>
        <div class='card-body'>{{wordsLeft}}</div>
      </div>
    </div>
    <div class="row float-right">
      <router-link
      :to="{ name: 'surveyForm', params: {markedTextIdxs: this.markedTextIdxs}}" tag='button'>
        Submit
      </router-link>
    </div>
  </div>
</template>

<script>
/* eslint no-unused-vars: ["error", { "args": "none" }] */
/* eslint no-continue: "off" */
const randomColor = require('randomcolor');

let highlightId = 0;

function Char(char, idx, wrdIdx) {
  this.idx = idx;
  this.char = char;
  this.wrdIdx = wrdIdx;
  this.isHighlight = false;
  this.fgColor = '#000000';
  this.bgColor = '#ffffff';
}

function Word(word, wrdIdx) {
  this.word = word;
  this.wrdIdx = wrdIdx;
}

function Doc(text) {
  this.chars = [];
  this.words = [];
  let wrdIdx = 0;
  let word = '';
  for (let i = 0; i < text.length; i += 1) {
    if (text[i] === ' ') {
      this.words.push(new Word(word, wrdIdx));
      wrdIdx += 1;
      word = '';
    } else {
      word.push(text[i]);
    }
    this.chars.push(new Char(text[i], i, wrdIdx));
  }
  this.createHTML = function toHTML() {
    const html = '';
    this.chars.forEach((el) => {
      html.push(`<span>${el.chars}</span>`);
    });
    return html;
  };
}

function readFile(file) {
  const d = new XMLHttpRequest();
  let newDoc = null;
  d.open('get', file, false);
  d.onreadystatechange = function readDoc() {
    if (d.readyState === 4) {
      if (d.status === 200 || d.status === 0) {
        newDoc = new Doc(d.responseText);
      }
    }
  };
  d.send(null);
  return newDoc;
}

function wordCounting(sent) {
  const arrMarkedText = sent.trim().split(' ');
  let count = 0;
  for (let i = 0; i < arrMarkedText.length; i += 1) {
    if (arrMarkedText[i] !== '') {
      count += 1;
    }
  }
  return count;
}

export default {
  methods: {
    captureHighlight(event) {
      // Get selection from mouse
      let selection = '';
      let selections = [];
      if (sessionStorage.getItem('selections') != null) {
        selections = JSON.parse(sessionStorage.getItem('selections'));
      }
      if (window.getSelection) {
        selection = window.getSelection();
      } else if (document.getSelection) {
        selection = document.getSelection();
      } else if (document.selection) {
        selection = document.selection.createRange().text;
      }
      // Start making highlights
      if ((this.wordCount + wordCounting(selection.toString())) <= 100) {
        const color = randomColor({
          luminosity: 'light',
        });
        selections.push([selection.anchorOffset, selection.focusOffset]);
        this.index = selections;
        this.markedText = `${this.markedText} <div style='background-color: ${color};'><span class='highlightID' >[${highlightId}]</span> ${selection.toString()}</div>`;
        sessionStorage.setItem('selections', JSON.stringify(selections));

        // Replacement
        const range = selection.getRangeAt(0);
        const iterator = document.createNodeIterator(
          range.commonAncestorContainer,
          NodeFilter.SHOW_ALL, // pre-filter
          {
            // custom filter
            acceptNode(node) {
              return NodeFilter.FILTER_ACCEPT;
            },
          },
        );
        const nodes = [];
        while (iterator.nextNode()) {
          if (nodes.length === 0 && iterator.referenceNode !== range.startContainer) continue;
          nodes.push(iterator.referenceNode);
          if (iterator.referenceNode.parentElement.nodeName === 'SPAN') {
            const parent = iterator.referenceNode.parentElement.parentElement;
            const child = iterator.referenceNode.parentElement;
            this.markedTextIdxs.push(Array.prototype.indexOf.call(parent.children, child));
            iterator.referenceNode.parentElement.setAttribute('style', `background-color: ${color};`);
          }
          if (iterator.referenceNode === range.endContainer) break;
        }
      } else {
        alert('Max words are 100');
      }
      highlightId += 1;
      // Clear selection
      if (window.getSelection) {
        if (window.getSelection().empty) { // Chrome
          window.getSelection().empty();
        } else if (window.getSelection().removeAllRanges) { // Firefox
          window.getSelection().removeAllRanges();
        }
      } else if (document.selection) { // IE?
        document.selection.empty();
      }
    },
  },
  data() {
    return {
      doc: readFile('/static/gold_doc/PROXY_LTW_ENG_20070831_0072'),
      index: [],
      markedText: '',
      markedTextIdxs: [],
      isActive: false,
    };
  },
  computed: {
    wordsLeft() {
      return 100 - this.wordCount;
    },
    wordCount() {
      if (this.markedText) {
        return wordCounting(this.markedText);
      }
      return 0;
    },
    charIndex() {
      if (this.markedTextIdxs) {
        return this.markedTextIdxs;
      }
      return '';
    },
  },
};

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.document {
  overflow: auto;
  height: 450px;
  mark {
    background: aqua;
  }
}
.card {
  margin: 0;
  padding: 0;
}
.lower-card {
  overflow: auto;
  height: 200px;
}
.highlights /deep/ .highlightID {
  vertical-align: super;
  font-size: 70%;
}
.highlights /deep/ .selHighlight{
  background: greenyellow;
}
</style>
