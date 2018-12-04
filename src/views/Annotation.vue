 <template>
   <div class="container is-fluid home">
     <div class="columns" :style="{ display: display.landing }">
            <div class="column is-8 is-offset-2 box content">
                <component :is="dynamicLanding"></component>
                <div align="center" style="margin-bottom: 2rem">
                    <button class="button is-primary is-large"
                    v-on:click="closeLanding()">I consent</button>
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
               <p class="my-text">Select phrases that are the most informative, <strong>use the <a target="_blank" href="https://en.wikipedia.org/wiki/Five_Ws">5W1H principle</a> (who, what, when, where, why and how) to determine the informativeness of a phrase.</strong></p>
               <p class="my-text">The maximum length of the highlighted phrases is <strong>{{ maxTokens }} words.</strong></p>
               <hr/>
               <p class="my-text"><strong>To highlight, use your mouse to select phrases from the document</strong>, when you have finished, selected words will automatically count as a group of highlight.</p>
               <p class="my-text"><strong>To delete a group of highlights, right click on the highlight </strong>in the document panel.</p>
               <p class="my-text"><strong>Clicking on phrases that are colored as blue</strong> will show you related phrases that are referring to them.</p>
           </div>
         </div>
       </div>
       <!-- eslint-enable -->
       <div class="column">
         <div class="box document">
           <Document v-on:highlight="updateSummaryBox"
                     v-on:noDocument="showMessage(
                     '<h1>There are no more documents available!</h1>')"
                     v-on:annotationDone="showTest"
                     :project_id="project_id"
                     :maxTokens="maxTokens"></Document>
         </div>
       </div>
       <div class="column is-3">
         <div class="box summary">
           <div class="content">
             <h2>Summary</h2>
             <h4 class="my-title">Words left</h4>
             <p>{{tokensLeft}} words.</p>
             <hr/>
             <h5 class="my-title">Highlighted Phrases:</h5>
             <p v-html="summaries"></p>
           </div>
         </div>
       </div>
     </div>
     <div class="columns" :style="{ display: display.message }">
        <div class="column is-8 is-offset-2 box content">
            <div align="center" v-html="message">
            </div>
        </div>
     </div>
     <div class="columns" :style="{ display: display.test }">
        <div class="column is-8 is-offset-2 box content">
            <div align="center">
                <h3>Please Answer the Following Question</h3>
                <div v-html="test_sentence">
                </div>
                <div class="block">
                    <b-radio v-model="radio"
                        native-value="True">
                        True
                    </b-radio>
                    <b-radio v-model="radio"
                        native-value="False">
                        False
                    </b-radio>
                </div>
                <hr/>
                <div :style="{ display: mTurkDisplay }">
                    <p>
                        Please enter an email to be included in a lucky draw
                        or leave it blank to opt out:
                    </p>
                    <b-field>
                        <b-input v-model="email"
                                 placeholder="Your email"
                                 icon-pack="fas"
                                 icon="envelope" style="width: 250px;" ></b-input>
                    </b-field>
                </div>
                <div style="margin-top: 5px;">
                    <button class="button is-primary" v-on:click="sendResult">Submit</button>
                </div>
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
import LandingHighlightMturk from '@/components/LandingMTurk/LandingHighlight.vue';

// const randomColor = require('randomcolor');
const axios = require('axios');

const maxTokens = 30;

export default {
  name: 'Annotation',
  components: {
    LandingHighlight,
    LandingHighlightMturk,
    Document,
  },
  data() {
    return {
      project_id: this.$route.params.project_id,
      is_mturk: this.$route.params.mturk,
      tokensLeft: maxTokens,
      summaries: '',
      display: {
        content: 'none',
        landing: 'block',
        message: 'none',
        test: 'none',
      },
      resultJSON: {},
      maxTokens,
      message: '',
      test_sentence: '',
      radio: '',
      answer: '',
      email: '',
    };
  },
  computed: {
    dynamicLanding() {
      if (this.is_mturk === '0') {
        return 'LandingHighlight';
      }
      return 'LandingHighlightMturk';
    },
    mTurkDisplay() {
      if (this.is_mturk === '0') {
        return 'block';
      }
      return 'none';
    },
  },
  methods: {
    sendResult() {
      this.resultJSON.email = this.email;
      if (this.is_mturk === '1') {
        this.resultJSON.mturk_code = this.turkCode;
      } else {
        this.resultJSON.mturk_code = null;
      }
      if ((this.radio === 'True') === this.answer) {
        this.resultJSON.validity = true;
      } else {
        this.resultJSON.validity = false;
      }
      axios.post('project/save_result/annotation', this.resultJSON)
        .then(() => {
          this.$toast.open({
            message: 'Submission successful.',
            type: 'is-success',
          });
          let text = '';
          if (this.is_mturk === '1') {
            text = '<p>Please enter this code:</p>' +
              `<blockquote>${this.turkCode}</blockquote>`;
          } else {
            text = '<p>Please refresh the page to do another highlighting. You need to do at least twice to be eligible for the lucky draw.</p>';
          }
          this.showMessage(`<h3>Thank you for submitting!</h3><br/> ${text}`);
        })
        .catch((error) => {
          this.$toast.open({
            message: `${error}`,
            type: 'is-danger',
          });
        });
    },
    closeLanding() {
      this.display.content = 'flex';
      this.display.landing = 'none';
      window.scrollTo(0, 0);
    },
    showTest(arg) {
      this.display.landing = 'none';
      this.display.content = 'none';
      this.display.message = 'none';
      this.display.test = 'flex';
      this.resultJSON = arg.resultJSON;
      this.test_sentence = arg.test_sentence;
      this.answer = arg.answer;
      this.turkCode = arg.turkCode;
    },
    showMessage(message) {
      this.display.landing = 'none';
      this.display.content = 'none';
      this.display.message = 'flex';
      this.display.test = 'none';
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
