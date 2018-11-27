 <template>
   <div class="container is-fluid home">
     <div class="columns" :style="{ display: display.landing }">
            <div class="column is-8 is-offset-2 box content">
                <LandingHighlight></LandingHighlight>
                <div align="center" style="margin-bottom: 2rem">
                    <a class="button is-primary is-large"
                    v-on:click="closeLanding()">I consent</a>
                </div>
            </div>
        </div>
     <div class="columns" :style="{ display: display.content }">
       <div class="column is-3">
         <div class="box instruction">
           <div class="content">
             <h2>
               Instructions
             </h2>
             <!-- eslint-disable -->
               <p class="my-text">Your task is <strong>to select important phrases</strong> from the document by highlighting them.</p>
               <p class="my-text">Select phrases that are the most informative, use the <a target="_blank" href="https://en.wikipedia.org/wiki/Five_Ws">5W1H principle</a> (who, what, when, where, why and how) to determine the informativeness of a phrase.</p>
               <p class="my-text">The maximum length of the highlighted phrases are <strong>{{ maxTokens }} characters.</strong></p>
               <hr/>
               <p class="my-text"><strong>To highlight, use your mouse to select phrases from the document</strong>, when you have finished, selected words will automatically count as a group of highlight.</p>
               <p class="my-text"><strong>To delete a group of highlights, right click on the highlight </strong>in the document panel.</p>
               <p class="my-text">Clicking on phrases that are colored as blue will show you related phrases that are referring to them.</p>
           </div>
         </div>
       </div>
       <!-- eslint-enable -->
       <div class="column">
         <div class="box document">
           <Document v-on:highlight="updateSummaryBox"
                     v-on:submitSuccess="showMessage('Thank you for submitting!')"
                     v-on:noDocument="showMessage('There are no more documents available!')"
                     :project_id="project_id"
                     :maxTokens="maxTokens"></Document>
         </div>
       </div>
       <div class="column is-3">
         <div class="box summary">
           <div class="content">
             <h2>Summary</h2>
             <h4 class="my-title">Characters left</h4>
             <p>{{tokensLeft}} characters.</p>
             <hr/>
             <h5 class="my-title">Highlighted Phrases:</h5>
             <p v-html="summaries"></p>
           </div>
         </div>
       </div>
     </div>
        <div class="columns" :style="{ display: display.message }">
            <div class="column is-8 is-offset-2 box content">
                <div align="center">
                    <h1>{{ message }}</h1>
                </div>
            </div>
        </div>
   </div>
</template>

<script>
/* eslint no-unused-vars: ["error", { "args": "none" }] */
/* eslint no-continue: "off" */
import Document from '@/components/Annotator/Document.vue';
import LandingHighlight from '@/components/Landing/LandingHighlight.vue';
// const randomColor = require('randomcolor');

const maxTokens = 90;

export default {
  name: 'Annotation',
  components: {
    LandingHighlight,
    Document,
  },
  data() {
    return {
      project_id: this.$route.params.project_id,
      tokensLeft: maxTokens,
      summaries: '',
      display: {
        content: 'none',
        landing: 'block',
        message: 'none',
      },
      maxTokens,
      message: '',
    };
  },
  methods: {
    closeLanding() {
      this.display.content = 'flex';
      this.display.landing = 'none';
      window.scrollTo(0, 0);
    },
    showMessage(message) {
      this.display.landing = 'none';
      this.display.content = 'none';
      this.display.message = 'flex';
      this.message = message;
    },
    updateSummaryBox(data) {
      this.tokensLeft = maxTokens - data.tokens;
      this.summaries = data.summaries;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.document {
  font-family: 'Lora', serif;
  font-size: 1.2rem;
  line-height: 1.5rem;
}
.my-title {
    font-size: 1rem;
}
.my-text {
    font-size: 0.9rem;
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
.home {
  padding-top: 25px;
}
</style>
