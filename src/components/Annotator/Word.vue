<template>
    <span ref="word" v-bind:data-type="type" v-bind:data-index="index"></span>
</template>
<script>
import Char from '@/components/Annotator/Char.vue';
import Vue from 'vue';

const CharClass = Vue.extend(Char);

export default {
  name: 'Word',
  props: ['index', 'sentIndex', 'tokenIndex', 'word', 'type', 'isSource'],
  data() {
    return {
      chars: [],
    };
  },
  methods: {
    annotate() {
      this.chars.forEach((char, idx) => {
        this.chars[idx].$data.charStyle.color = '#ff00ff';
        this.chars[idx].$data.charStyle['font-weight'] = 'normal';
      });
    },
    resetAnnotation() {
      if (this.isSource) {
        this.chars.forEach((char, idx) => {
          this.chars[idx].$data.charStyle.color = '#3878E5';
          this.chars[idx].$data.charStyle.cursor = 'pointer';
          this.chars[idx].$data.charStyle['font-weight'] = 'bold';
        });
      } else {
        this.chars.forEach((char, idx) => {
          this.chars[idx].$data.charStyle.color = '#000000';
          this.chars[idx].$data.charStyle.cursor = 'text';
          this.chars[idx].$data.charStyle['font-weight'] = 'normal';
        });
      }
    },
    highlight(color) {
      this.chars.forEach((char, idx) => {
        this.chars[idx].$data.charStyle['background-color'] = color;
      });
    },
    rmHighlight() {
      this.chars.forEach((char, idx) => {
        this.chars[idx].$data.charStyle['background-color'] = '#ffffff';
      });
    },
  },
  mounted: function onMounted() {
    for (let i = 0; i < this.word.length; i += 1) {
      let fgColor = '#000000';
      let fontWeight = 'normal';
      let cursor = 'text';
      if (this.isSource === true) {
        fgColor = '#3878E5';
        fontWeight = 'bold';
        cursor = 'pointer';
      }
      const char = new CharClass({
        propsData: {
          bgColor: '#ffffff',
          fgColor,
          fontWeight,
          type: 'char',
          cursor,
        },
      });
      char.$slots.default = [this.word[i]];
      this.chars.push(char);
      char.$mount();
      this.$refs.word.appendChild(char.$el);
    }
  },
};
</script>

<style scoped>

</style>
