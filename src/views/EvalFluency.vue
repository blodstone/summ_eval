<template>
  <div class="container home">
        <div class="columns">
            <div class="column is-5 is-offset-3">
                <div class="box summary">
                    <div class="content">
                        <h1>Assessment</h1>
                        <h5 class="my-header">Summary to be assessed</h5>
                        <p class="my-summary">{{ system_text }}</p>
                        <hr>
                        <h5 class="my-header">
                            Your Assessment
                        </h5>
                        <h5 class="my-title">Fluency</h5>
                        <p class="my-text"> Is there any grammatical mistake in the text?</p>
                        <p class="my-text">
                            <strong>{{ fluency }} % </strong> of text has grammatical mistake
                        </p>
                        <div class="level" align="center">
                            <span class="level-left">
                                <label class="label is-small">No grammatical <br> mistake</label>
                            </span>
                            <span class="level-item">
                            <input type="range" min="0" max="100"
                                   v-model="fluency" class="my-slider slider is-info is-fullwidth">
                            </span>
                            <span class="level-right">
                                <label class="label is-small">
                                   Too many <br> grammatical mistake</label>
                            </span>
                        </div>
                        <a class="button is-primary" :disabled="timer.isRunning"
                    v-on:click="saveEvaluation()">{{ timenow }}</a>
                    </div>
                </div>
            </div>
            <!-- eslint-enable -->
        </div>
    </div>
</template>

<script>
// @ is an alias to /src
const axios = require('axios');

const waitTimeForButton = 5;

function getFile() {
  axios.get(`project/evaluation/fluency/${this.project_id}/single_doc`)
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
    })
    .catch((error) => {
      this.$toast.open({
        message: `${error}`,
        type: 'is-danger',
      });
    });
}

export default {
  data() {
    return {
      system_text: '',
      ref_text: '',
      fluency: 50,
      project_id: this.$route.params.project_id,
      timer: {
        now: Math.trunc(new Date().getTime() / 1000),
        date: Math.trunc(new Date().getTime() / 1000),
        isRunning: true,
        timer: null,
      },
    };
  },
  methods: {
    saveEvaluation() {
      const resultJSON = {
        project_id: this.project_id,
        status_id: this.summ_status_id,
        fluency: this.fluency,
        category: 'fluency',
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
