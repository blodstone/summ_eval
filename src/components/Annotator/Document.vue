<template>
    <div>
        <div ref="document" v-on:mouseup="showHighlightMenu"
             @contextmenu.prevent="deleteHighlightGroup" v-on:click="showMentions">
        </div>
        <div v-bind:style="floatMenu">
            <img v-on:click="highlightSelection"
                 src="../../assets/highlight_menu.png"
                 width="35" alt="Highlight">
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

const waitTimeForButton = 5;

function createAndMountWord(sent, token, wordIndex, isSourceAndCorefID) {
  const WordClass = Vue.extend(Word);
  const word = new WordClass({
    propsData: {
      sentIndex: sent.index,
      tokenIndex: token.index,
      word: token.word,
      index: wordIndex,
      compIndex: this.components.length,
      type: 'word',
      // eslint-disable-next-line
      isSource: isSourceAndCorefID.isSource,
    },
  });
  word.$mount();
  if (isSourceAndCorefID.isSource === true) {
    this.words2corefID[wordIndex] = isSourceAndCorefID.corefID;
  }
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

function generateRawHTMLSummaries() {
  this.rawSummariesHTML = '';
  let rawHTML = '';
  for (let i = 0; i < Object.keys(this.groups).length; i += 1) {
    const key = Object.keys(this.groups)[i];
    rawHTML = `<p style='background-color: ${this.group2color[key]}'>${i + 1}: `;
    for (let j = 0; j < this.groups[key].length; j += 1) {
      const component = this.groups[key][j];
      if (component.$props.type === 'word') {
        rawHTML = `${rawHTML} ${component.$props.word}`;
      }
    }
    rawHTML = `${rawHTML}</p>`;
    this.rawSummariesHTML = `${this.rawSummariesHTML}${rawHTML}`;
  }
}

function populateCoref(textJSON) {
  const reverseCorefs = {};
  Object.keys(textJSON.corefs).forEach((ID) => {
    const corefID = parseInt(ID, 10);
    const newCorefID = textJSON.corefs[corefID][0].id;
    if (!(newCorefID in reverseCorefs)) {
      reverseCorefs[newCorefID] = [];
    }
    for (let i = 0; i < textJSON.corefs[corefID].length; i += 1) {
      reverseCorefs[newCorefID].push(textJSON.corefs[corefID][i]);
    }
  });
  Object.keys(reverseCorefs).forEach((ID) => {
    const corefID = parseInt(ID, 10);
    for (let i = 0; i < reverseCorefs[corefID].length; i += 1) {
      const mention = reverseCorefs[corefID][i];
      if (!(corefID in this.srcCorefID2mentionsCorefID)) {
        this.srcCorefID2mentionsCorefID[corefID] = [];
      }
      this.srcCorefID2mentionsCorefID[corefID].push(mention.id);
      if (!(mention.id in this.mentions)) {
        this.mentions[mention.id] = {
          id: mention.id,
          startIndex: mention.startIndex,
          endIndex: mention.endIndex,
          sentIndex: mention.sentNum,
        };
      }
      if (corefID === mention.id) {
        if (!(mention.sentNum in this.sentNum2srcCorefID)) {
          this.sentNum2srcCorefID[mention.sentNum] = [];
        }
        this.sentNum2srcCorefID[mention.sentNum].push(corefID);
      }
    }
  });
}

function getIsSourceAndcorefID(sent, token) {
  if (sent.index + 1 in this.sentNum2srcCorefID) {
    const corefIDs = this.sentNum2srcCorefID[sent.index + 1];
    for (let k = 0; k < corefIDs.length; k += 1) {
      if (token.index >= this.mentions[corefIDs[k]].startIndex &&
          token.index < this.mentions[corefIDs[k]].endIndex) {
        return {
          isSource: true,
          corefID: corefIDs[k],
        };
      }
    }
  }
  return false;
}

function parseDoc(textJSON) {
  let wordIndex = 0;
  let whitespaceIndex = 0;
  const { endSentIndex } = textJSON.paragraph;
  populateCoref.call(this, textJSON);
  for (let i = 0; i < textJSON.sentences.length; i += 1) {
    const sent = textJSON.sentences[i];
    for (let j = 0; j < sent.tokens.length; j += 1) {
      const token = sent.tokens[j];
      const isSourceAndCorefID = getIsSourceAndcorefID.call(this, sent, token);
      createAndMountWord.call(this, sent, token, wordIndex, isSourceAndCorefID);
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
  axios.get(`project/${this.project_id}/single_doc`)
    .then((response) => {
      parseDoc.call(this, JSON.parse(response.data));
    })
    .catch((error) => {
      console.log(error);
    });
}

function sendResult(resultJSON) {
  axios.post('save_annotation', resultJSON)
    .then((response) => {
      console.log(response);
    })
    .catch((error) => {
      console.log(error);
    });
}

function clearSelection(selection) {
  if (selection) {
    if (selection.empty) { // Chrome
      selection.empty();
    } else if (selection.removeAllRanges) { // Firefox
      selection.removeAllRanges();
    }
  }
}

function getSelection() {
  if (window.getSelection) {
    return window.getSelection();
  } else if (document.getSelection) {
    return document.getSelection();
  } else if (document.selection) {
    return document.selection.createRange().text;
  }
  return null;
}

function getTopWhitespaceGroup(index) {
  if (this.whitespaces2Groups[index].length === 0) {
    return -1;
  }
  return this.whitespaces2Groups[index][this.whitespaces2Groups[index].length - 1];
}

function getTopWordGroups(index) {
  if (this.words2Groups[index].length === 0) {
    return -1;
  }
  return this.words2Groups[index][this.words2Groups[index].length - 1];
}

function tempStoreComponent(component, type, groupKey) {
  const components = [];
  let found = false;
  this.groups[groupKey].forEach((aComponent) => {
    if (aComponent === component) {
      found = true;
    }
  });
  if (found === false) {
    components.push(component);
  }
  return components;
}

function highlightAndAddComponentToGroup(
  whitespaceSelectedComponents,
  wordSelectedComponents,
  color, groupKey,
) {
  for (let i = 0; i < whitespaceSelectedComponents.length; i += 1) {
    const component = whitespaceSelectedComponents[i];
    this.groups[groupKey].push(component);
    this.whitespaces2Groups[component.index].push(groupKey);
    component.$data.charStyle['background-color'] = color;
  }
  for (let i = 0; i < wordSelectedComponents.length; i += 1) {
    const component = wordSelectedComponents[i];
    this.groups[groupKey].push(component);
    this.words2Groups[component.index].push(groupKey);
    component.highlight(color);
  }
}

export default {
  name: 'Document',
  props: ['project_id'],
  data() {
    return {
      timer: {
        now: Math.trunc(new Date().getTime() / 1000),
        date: Math.trunc(new Date().getTime() / 1000),
        isRunning: true,
        timer: null,
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
      // A collection of selected Char and Word components
      groups: {},

      floatMenu: {
        display: 'none',
      },

      // Words that are highlighted for mentions
      annotatedWords: [],
      // A mapping of mention's sent index to source's corefID
      sentNum2srcCorefID: {},
      // A mapping of Coref ID to it's properties (Token end, start)
      mentions: {},
      // A mapping of source's coref ID to an array of mentions's Coref ID
      srcCorefID2mentionsCorefID: {},
      // A mapping of Word component to CorefID
      words2corefID: {},
      // A mapping between group Key (this.group index) to color
      group2color: {},
      rawSummariesHTML: '',
    };
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
    saveAnnotation() {
      const resultJSON = {
        highlights: {},
        components: [],
        words: [],
      };
      for (let i = 0; i < Object.keys(this.groups).length; i += 1) {
        const key = Object.keys(this.groups)[i];
        let text = '';
        resultJSON.highlights[key] = {
          indexes: [],
        };
        for (let j = 0; j < this.groups[key].length; j += 1) {
          const component = this.groups[key][j];
          if (component.$props.type === 'word') {
            text = `${text} ${component.$props.word}`.trim();
            resultJSON.highlights[key].indexes.push(component.$props.index);
          }
        }
        resultJSON.highlights[key].text = text;
      }
      for (let i = 0; i < this.components.length; i += 1) {
        if (this.components[i].type === 'word') {
          resultJSON.components.push({
            type: this.components[i].type,
            word: this.components[i].word,
          });
        } else {
          resultJSON.components.push({
            type: this.components[i].type,
            word: ' ',
          });
        }
      }
      for (let i = 0; i < Object.keys(this.words).length; i += 1) {
        const wordIndex = Object.keys(this.words)[i];
        resultJSON.words[wordIndex] = {
          word: this.words[wordIndex].word,
        };
      }
      sendResult.call(this, resultJSON);
    },
    showMentions(event) {
      let corefID = -1;
      if (event.target.parentElement.dataset.type === 'word') {
        corefID = this.words2corefID[event.target.parentElement.dataset.index];
      } else if (event.target.parentElement.dataset.type === 'char') {
        corefID = this.words2corefID[event.target.parentElement.parentElement.dataset.index];
      }
      if (corefID !== -1) {
        for (let i = 0; i < this.annotatedWords.length; i += 1) {
          this.annotatedWords[i].resetAnnotation();
        }
        this.annotatedWords = [];
        const mentions = this.srcCorefID2mentionsCorefID[corefID];
        for (let i = 0; i < Object.keys(this.words).length; i += 1) {
          const index = Object.keys(this.words)[i];
          const { tokenIndex } = this.words[index];
          for (let j = 0; j < mentions.length; j += 1) {
            if (this.words[index].sentIndex + 1 === this.mentions[mentions[j]].sentIndex &&
              tokenIndex >= this.mentions[mentions[j]].startIndex &&
              tokenIndex < this.mentions[mentions[j]].endIndex) {
              this.words[index].annotate();
              if (j === 1) {
                this.words[index].$refs.word.scrollIntoView();
                window.scrollBy(0, -1 * (window.innerHeight / 10));
              }
              this.annotatedWords.push(this.words[index]);
            }
          }
        }
      }
    },
    deleteHighlightGroup(event) {
      let groupIndex = -1;
      if (event.target.parentElement.dataset.type === 'whitespace') {
        groupIndex = getTopWhitespaceGroup.call(this, event.target.parentElement.dataset.index);
      } else if (event.target.parentElement.dataset.type === 'word') {
        groupIndex = getTopWordGroups.call(this, event.target.parentElement.dataset.index);
      } else if (event.target.parentElement.dataset.type === 'char') {
        groupIndex = getTopWordGroups.call(
          this,
          event.target.parentElement.parentElement.dataset.index,
        );
      }
      if (groupIndex !== -1) {
        this.$dialog.confirm({
          message: 'Do you want to delete the highlights?',
          onConfirm: () => {
            this.groups[groupIndex].forEach((component) => {
              if (component.$props.type === 'whitespace') {
                for (let i = 0;
                  i < this.whitespaces2Groups[component.$props.index].length;
                  i += 1) {
                  if (this.whitespaces2Groups[component.$props.index][i] === groupIndex) {
                    this.whitespaces2Groups[component.$props.index].splice(i, 1);
                    if (this.whitespaces2Groups[component.$props.index].length === 0) {
                    // eslint-disable-next-line
                    component.$data.charStyle['background-color'] = '#ffffff';
                    }
                    break;
                  }
                }
              } else if (component.$props.type === 'word') {
                for (let i = 0; i < this.words2Groups[component.$props.index].length; i += 1) {
                  if (this.words2Groups[component.$props.index][i] === groupIndex) {
                    this.words2Groups[component.$props.index].splice(i, 1);
                    if (this.words2Groups[component.$props.index].length === 0) {
                    // eslint-disable-next-line
                    component.rmHighlight();
                    }
                    break;
                  }
                }
              }
            });
            if (groupIndex in this.groups) {
              delete this.groups[groupIndex];
            }
            let sumOfWords = 0;
            // eslint-disable-next-line
          for (const key in this.words2Groups) {
              if (this.words2Groups[key].length > 0) {
                sumOfWords += 1;
              }
            }
            generateRawHTMLSummaries.call(this);
            this.$emit('highlight', {
              words: sumOfWords,
              summaries: this.rawSummariesHTML,
            });
          },
        });
      }
    },
    highlightSelection() {
      // Generate new group key
      let groupKey = 0;
      Object.keys(this.groups).forEach((key) => {
        groupKey = parseInt(key, 10) + 1;
      });
      this.groups[groupKey] = [];
      // const color = randomColor({
      //   luminosity: 'light',
      // });
      const color = '#77e529';
      this.group2color[groupKey] = color;
      const selection = getSelection();
      const range = selection.getRangeAt(0);
      const iterator = document.createNodeIterator(
        range.commonAncestorContainer,
        NodeFilter.SHOW_ALL, // pre-filter
        {
          acceptNode() {
            return NodeFilter.FILTER_ACCEPT;
          },
        },
      );
      const nodes = [];
      // Add selected component to storage
      let whitespaceSelectedComponents = [];
      let wordSelectedComponents = [];
      while (iterator.nextNode()) {
        // eslint-disable-next-line
        if (nodes.length === 0 && iterator.referenceNode !== range.startContainer) continue;
        nodes.push(iterator.referenceNode);
        if (iterator.referenceNode.parentElement.dataset.type === 'whitespace') {
          // eslint-disable-next-line
          const index = iterator.referenceNode.parentElement.dataset.index;
          whitespaceSelectedComponents =
            whitespaceSelectedComponents.concat(tempStoreComponent.call(this, this.whitespaces[index], 'char', groupKey));
        }
        if (iterator.referenceNode.parentElement.dataset.type === 'word') {
          // eslint-disable-next-line
          const index = iterator.referenceNode.parentElement.dataset.index;
          if (!(wordSelectedComponents.includes(this.words[index]))) {
            wordSelectedComponents =
              wordSelectedComponents.concat(tempStoreComponent.call(this, this.words[index], 'word', groupKey));
          }
        }
        if (iterator.referenceNode === range.endContainer) break;
      }
      let sumOfWords = 0;
      // eslint-disable-next-line
      for (const key in this.words2Groups) {
        if (this.words2Groups[key].length > 0) {
          sumOfWords += 1;
        }
      }
      for (let i = 0; i < wordSelectedComponents.length; i += 1) {
        const word = wordSelectedComponents[i];
        if (this.words2Groups[word.index].length === 0) {
          sumOfWords += 1;
        }
      }
      if (sumOfWords <= 100) {
        highlightAndAddComponentToGroup.call(
          this, whitespaceSelectedComponents, wordSelectedComponents,
          color, groupKey,
        );
        generateRawHTMLSummaries.call(this);
        this.$emit('highlight', {
          words: sumOfWords,
          summaries: this.rawSummariesHTML,
        });
      } else {
        this.$toast.open({
          message: 'Your highlights have passed the 100 words limit. Remove previous highlights or shorten the highlights.',
          type: 'is-danger',
        });
        delete this.group2color[groupKey];
        delete this.groups[groupKey];
      }

      // Clear selection
      this.floatMenu.display = 'none';
      clearSelection(selection);
    },
    showHighlightMenu(event) {
      const selection = getSelection();
      if (!(selection.toString() === '')) {
        this.floatMenu.display = 'block';
        this.floatMenu.position = 'fixed';
        this.$set(this.floatMenu, 'left', `${event.pageX - 10}px`);
        this.$set(this.floatMenu, 'top', `${event.pageY - (window.scrollY - 20)}px`);
      } else {
        this.floatMenu.display = 'none';
      }
    },
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
</style>
