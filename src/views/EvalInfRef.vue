<template>
  <div class="container home">
        <div class="columns" :style="{ display: display.landing }">
            <div class="column is-8 is-offset-2 box content">
                <LandingInfRef></LandingInfRef>
                <div align="center">
                    <a class="button is-primary is-large" style="margin-bottom: 2rem"
                    v-on:click="closeLanding()">I consent</a>
                </div>
            </div>
        </div>
        <div class="columns" :style="{ display: display.content }">
            <div class="column is-5 is-offset-1">
                <div class="box document">
                    <div class="content">
                        <h1>Read This Text</h1>
                        <p class="my-summary">{{ ref_text }}</p>
                    </div>
                </div>
            </div>
            <div class="column is-5">
                <div class="box summary">
                    <div class="content">
                        <h1>Assessment</h1>
                        <h5 class="my-header">Assess the following summary.</h5>
                        <p class="my-summary">{{ system_text }}</p>
                        <hr>
                        <h5 class="my-header">
                        <strong>How strongly agree are you on the following statements?</strong>
                        </h5>
                        <p class="my-text">
                            <strong>All important information
                            </strong> from the left panel's sentence is present in the summary
                        </p>
                        <div class="level" align="center"
                             style="margin-bottom: 1.8rem; margin-top: 1.8rem;">
                            <span class="level-left">
                                <label class="label is-small">Strongly <br/> disagree</label>
                            </span>
                            <span class="level-item">
                            <vue-slider min="1" max="100" v-model="recall"
                                        v-if="show" width="100%"></vue-slider>
                            </span>
                            <span class="level-right">
                                <label class="label is-small">Strongly <br/> agree</label>
                            </span>
                        </div>
                        <p class="my-text">
                            <strong>Only important information</strong>
                            from the left panel's sentence is present in the summary.</p>
                        <div class="level" align="center"
                             style="margin-bottom: 1.8rem; margin-top: 1.8rem;">
                            <span class="level-left">
                                <label class="label is-small">Strongly <br/> disagree</label>
                            </span>
                            <span class="level-item">
                           <vue-slider min="1" max="100" v-model="precision"
                                       v-if="show" width="100%"></vue-slider>
                            </span>
                            <span class="level-right">
                                <label class="label is-small">Strongly <br/> agree</label>
                            </span>
                        </div>
                        <a class="button is-primary" :disabled="timer.isRunning"
                    v-on:click="saveEvaluation()">{{ timenow }}</a>
                    </div>
                </div>
            </div>
            <!-- eslint-enable -->
        </div>
        <div class="columns" :style="{ display: display.closing }">
            <div class="column is-8 is-offset-2 box content">
                <div align="center">
                    <h1>Thank you for submitting!</h1>
                </div>
            </div>
        </div>
  </div>
</template>

<script>
// @ is an alias to /src
import LandingInfRef from '@/components/Landing/LandingInfRef.vue';
import vueSlider from 'vue-slider-component';

const axios = require('axios');

const waitTimeForButton = 5;

function getFile() {
  axios.get(`project/evaluation/informativeness_ref/${this.project_id}/single_doc`)
    .then((response) => {
      this.system_text = response.data.system_text;
      this.ref_text = response.data.ref_text;
      this.summ_status_id = response.data.summ_status_id;
    })
    .catch((error) => {
      this.$toast.open({
        message: `${error}`,
        type: 'is-danger',
      });
    });
}

function sendResult(resultJSON) {
  axios.post('project/save_result/evaluation', resultJSON)
    .then(() => {
      this.$toast.open({
        message: 'Submission successful.',
        type: 'is-success',
      });
      this.display.content = 'none';
      this.display.closing = 'flex';
    })
    .catch((error) => {
      this.$toast.open({
        message: `${error}`,
        type: 'is-danger',
      });
    });
}

export default {
  components: {
    LandingInfRef,
    vueSlider,
  },
  data() {
    return {
      show: false,
      system_text: '',
      ref_text: '',
      timer: {
        now: Math.trunc(new Date().getTime() / 1000),
        date: Math.trunc(new Date().getTime() / 1000),
        isRunning: true,
        timer: null,
      },
      precision: 50,
      recall: 50,
      project_id: this.$route.params.project_id,
      summ_status_id: '',
      display: {
        content: 'none',
        landing: 'block',
        closing: 'none',
      },
    };
  },
  methods: {
    closeLanding() {
      this.display.content = 'flex';
      this.display.landing = 'none';
      window.scrollTo(0, 0);
      this.show = true;
    },
    saveEvaluation() {
      const resultJSON = {
        project_id: this.project_id,
        status_id: this.summ_status_id,
        precision: this.precision,
        recall: this.recall,
        category: 'Informativeness_Ref',
      };
      sendResult.call(this, resultJSON);
    },
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
  mounted: function onMounted() {
    getFile.call(this);
    this.timer.timer = window.setInterval(() => {
      this.timer.now = Math.trunc((new Date()).getTime() / 1000);
    }, 1000);
  },
};
</script>

<style lang="scss">
.home {
  padding-top: 25px;
}
</style>
