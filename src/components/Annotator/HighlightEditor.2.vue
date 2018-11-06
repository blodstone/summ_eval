 <template>
  <div>
    <header>
          <nav class="navbar fixed-top">
            <a class="navbar-brand" href="#">Manual Evaluation</a>
            <a class="words-left">Words Left: {{ wordsLeft }}</a>
          </nav>
    </header>
    <div class='d-flex flex-row justify-content-center'>
      <div class='p-2 col-lg-5'>
        <div class='document'>
          <Document v-on:highlight="countWordsLeft"></Document>
        </div>
      </div>
    </div>

    <div class="row float-right">

    </div>
  </div>
</template>

<script>
/* eslint no-unused-vars: ["error", { "args": "none" }] */
/* eslint no-continue: "off" */
import Document from '@/components/Annotator/Document.vue';


// const randomColor = require('randomcolor');

export default {
  name: 'HighlightEditor',
  components: {
    Document,
  },
  data() {
    return {
      wordsLeft: 100,
    };
  },
  methods: {
    countWordsLeft(words) {
      this.wordsLeft = 100 - words;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.document {
  font-family: 'Lora', serif;
  font-size: 21px;
  line-height: 33px;
}
.words-left {
  font-family: 'Lora', serif;
  font-size: 21px;
  line-height: 33px;
  padding-right: 40px;
}
</style>
