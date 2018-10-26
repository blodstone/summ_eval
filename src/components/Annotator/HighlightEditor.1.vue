 <template>
  <div>
    <div class='row card-deck'>
      <div class='card col-8'>
        <div class='card-header'>Document</div>
        <div class='card-body document'
          v-on:mouseup="captureHighlight"
          v-html="createHTML"></div>
        <button v-bind:style="floatMenu">Highlight</button>
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
  this.isLink = false;
  this.isCoref = false;
  this.corefColor = '#ffffff';
  this.ulColor = '#ffffff';
  this.bgColor = '#ffffff';
  this.highlight = function highlight(color) {
    this.isHighlight = true;
    this.bgColor = color;
  };
  this.setlink = function setLink(color) {
    this.isLink = true;
    this.uColor = color;
  };
  this.setCoref = function setCoref(color) {
    this.isCoref = true;
    this.corefColor = color;
  };
}

function WordIdx(idx, sntIdx, posIdx) {
  this.idx = idx;
  this.sntIdx = sntIdx;
  this.posIdx = posIdx;
}

function Word(word, wrdIdx, isSourceLink) {
  this.word = word;
  this.wrdIdx = wrdIdx;
  this.wrdIdxLink = [];
  this.isSourceLink = isSourceLink;
}

function Doc(textJSON) {
  this.chars = {};
  this.words = [];
  this.pos2corefkey = {};
  this.charIdx2wrdIdx = {};
  let wrdIdx = 0;
  let charIdx = 0;
  let text = '';
  this.corefs = textJSON.corefs;
  Object.keys(textJSON.corefs).forEach((key) => {
    textJSON.corefs[key].forEach((coref) => {
      if (coref.id.toString() === key) {
        this.pos2corefkey[`${coref.sentNum} ${coref.startIndex} ${coref.endIndex}`] = key;
      }
    });
  });
  textJSON.sentences.forEach((sent) => {
    sent.tokens.forEach((token) => {
      let isSourceLink = false;
      Object.keys(this.pos2corefkey).forEach((key) => {
        const corefIdxs = key.split(' ');
        if (sent.index + 1 === parseInt(corefIdxs[0], 10)) {
          if (token.index >= parseInt(corefIdxs[1], 10) &&
          token.index < parseInt(corefIdxs[2], 10)) {
            isSourceLink = true;
          }
        }
      });
      this.words.push(new Word(token, new WordIdx(wrdIdx, sent.index, token.index), isSourceLink));
      wrdIdx += 1;
      text = `${text} ${token.word}`.trim();
      charIdx = token.characterOffsetBegin;
      for (let i = 0; i < token.word.length; i += 1) {
        const newChar = new Char(token.word[i], charIdx, wrdIdx);
        if (isSourceLink === true) {
          newChar.setlink('#00ff00');
        }
        this.chars[charIdx] = newChar;
        charIdx += 1;
      }
    });
  });
  for (let i = 0; i < text.length; i += 1) {
    if (!(i in this.chars)) {
      this.chars[i] = new Char(' ', i, -1);
    }
  }
  this.getChar = function getChar(idx) {
    return this.chars[idx];
  };
}

function readFile(file) {
  const d = new XMLHttpRequest();
  let newDoc = null;
  d.open('get', file, false);
  d.onreadystatechange = function readDoc() {
    if (d.readyState === 4) {
      if (d.status === 200 || d.status === 0) {
        const textJSON = JSON.parse(d.responseText);
        newDoc = new Doc(textJSON);
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
      // Shows text
      this.floatMenu.display = 'block';
      this.floatMenu.position = 'absolute';
      this.$set(this.floatMenu, 'left', `${event.pageX}px`);
      this.$set(this.floatMenu, 'top', `${event.pageY - 70}px`);
      // Start making highlights
      if ((this.wordCount + wordCounting(selection.toString())) <= 100 && false) {
        const color = randomColor({
          luminosity: 'light',
        });
        selections.push([selection.anchorOffset, selection.focusOffset]);
        this.index = selections;
        this.markedText = `${this.markedText} <div style='background-color: ${color};'><span class='highlightID' >[${highlightId}]</span> ${selection.toString()}</div>`;
        sessionStorage.setItem('selections', JSON.stringify(selections));
        highlightId += 1;

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
            const clickedChar = this.doc.getChar(iterator.referenceNode.parentElement.dataset.idx);
            // clickedChar.highlight(color);
            // const clickedWord = this.doc.words[clickedChar.wrdIdx];
            /* eslint-disable */
            // const corefKey = this.doc.pos2corefkey[`${clickedWord.sntIdx} ${clickedWord.posIdx}`];
            Object.keys(this.pos2corefkey).forEach((key) => {
              const corefIdxs = key.split(' ');
              if (clickedChar.wrdIdx === parseInt(corefIdxs[0], 10)) {
                if (token.index >= parseInt(corefIdxs[1], 10) &&
                token.index < parseInt(corefIdxs[2], 10)) {
                  Object.keys(textJSON.corefs).forEach((key) => {
                  textJSON.corefs[key].forEach((coref) => {
                    if (coref.id.toString() !== key) {
                      this.markedText += coref.text; 
                    }
                  });
                });
                }
              }
            });
            /* eslint-enable */
          }
          if (iterator.referenceNode === range.endContainer) break;
        }
      }
      // // Clear selection
      // if (window.getSelection) {
      //   if (window.getSelection().empty) { // Chrome
      //     window.getSelection().empty();
      //   } else if (window.getSelection().removeAllRanges) { // Firefox
      //     window.getSelection().removeAllRanges();
      //   }
      // } else if (document.selection) { // IE?
      //   document.selection.empty();
      // }
    },
  },
  data() {
    return {
      doc: readFile('/static/gold_doc/doc.json'),
      index: [],
      markedText: '',
      markedTextIdxs: [],
      isActive: false,
      floatMenu: {
        display: 'none',
      },
    };
  },
  computed: {
    createHTML() {
      let html = '';
      Object.keys(this.doc.chars).forEach((key) => {
        const el = this.doc.chars[key];
        let styleTag = '';
        if (el.isHighlight === true) {
          styleTag = `background-color: ${el.bgColor};`;
        }
        if (el.isLink === true) {
          styleTag = `${styleTag}background-image: linear-gradient(to bottom, red 66%, transparent 66%, transparent 66%, red 66%, red);
          background-position: 0 1.03em;background-repeat: repeat-x;background-size: 2px 8px;`;
        }
        html += `<span style='${styleTag}' data-idx="${el.idx}">${el.char}</span>`;
      });
      return html;
    },
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
.source-links {
  background: green;
  text-decoration: none;
  border-bottom: 2px solid currentColor;
  display: inline-block;
  line-height: 0.85;
  text-shadow:
    2px 2px white,
    2px -2px white,
    -2px 2px white,
    -2px -2px white;
}
</style>
