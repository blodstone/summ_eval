<template>
  <div>
    <div class='row card-deck'>
      <div class='card col-8'>
        <div class='card-header'>Document</div>
        <div class='card-body document' v-on:mouseup="captureHighlight" v-html="message"></div>
      </div>
      <div class='card col-4'>
        <div class='card-header'>Guidelines</div>
        <div class='card-body'>
          <p>You have been given a document and several summaries that are extracted
from the document. Please read the document and then highlights fragments of sentences to form a 100 words summary based on the following guidelines.</p>

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
        <div class='card-body col'>{{markedText}}</div>
      </div>
      <div class="card col-1 lower-card">
        <div class='card-header'>Words Left</div>
        <div class='card-body'>{{wordsLeft}}</div>
      </div>
    </div>
    <div class="row float-right">
      <router-link :to="{ name: 'surveyForm', params: {markedTextIdxs: this.markedTextIdxs}}" tag='button'>Submit</router-link>
    </div>
  </div>
</template>

<script>
let docContent = '';
function readFile(file) {
  const d = new XMLHttpRequest();
  d.open('get', file, false);
  d.onreadystatechange = function () {
    if (d.readyState === 4) {
      if (d.status === 200 || d.status === 0) {
        docContent = d.responseText;
      }
    }
  };
  d.send(null);
}

function wordCounting(sent) {
  const arrMarkedText = sent.trim().split(' ');
  let count = 0;
  for (let i = 0; i < arrMarkedText.length; i++) {
    if (arrMarkedText[i] !== '') {
      count += 1;
    }
  }
  return count;
}

export default {
  methods: {
    submitHandler(event) {
      this.$route.push({ path: '/foo', name: 'home2' });
    },

    captureHighlight(event) {
      // Save highlight
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
      if ((this.wordCount + wordCounting(selection.toString())) <= 100) {
        selections.push([selection.anchorOffset, selection.focusOffset]);
        this.index = selections;
        this.markedText = `${this.markedText} ${selection.toString()}`;
        sessionStorage.setItem('selections', JSON.stringify(selections));

        // Replacement
        const range = selection.getRangeAt(0);
        const _iterator = document.createNodeIterator(
          range.commonAncestorContainer,
          NodeFilter.SHOW_ALL, // pre-filter
          {
            // custom filter
            acceptNode(node) {
              return NodeFilter.FILTER_ACCEPT;
            },
          },
        );
        const _nodes = [];
        while (_iterator.nextNode()) {
          if (_nodes.length === 0 && _iterator.referenceNode !== range.startContainer) continue;
          _nodes.push(_iterator.referenceNode);
          if (_iterator.referenceNode.parentElement.nodeName === 'SPAN') {
            const parent = _iterator.referenceNode.parentElement.parentElement;
            const child = _iterator.referenceNode.parentElement;
            this.markedTextIdxs.push(Array.prototype.indexOf.call(parent.children, child));
            _iterator.referenceNode.parentElement.setAttribute('style', 'background-color: yellow;');
          }
          if (_iterator.referenceNode === range.endContainer) break;
        }
      } else {
        alert('Max words are 100');
      }
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
    readFile('/static/gold_doc/PROXY_LTW_ENG_20070831_0072');
    let markedDocContent = '';
    for (let i = 0; i < docContent.length; i += 1) {
      markedDocContent += `<span>${docContent[i]}</span>`;
    }
    this.message = markedDocContent;
    return {
      message: this.message,
      index: [],
      markedText: '',
      markedTextIdxs: [],
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
.lower-card{
  overflow: auto;
  height: 200px;
}
</style>
