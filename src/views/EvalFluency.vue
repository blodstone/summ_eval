<template>
  <div class="container">
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
                            <strong>{{ mistake }} % </strong> of text has grammatical mistake
                        </p>
                        <div class="level" align="center">
                            <span class="level-left">
                                <label class="label is-small">No grammatical <br> mistake</label>
                            </span>
                            <span class="level-item">
                            <input type="range" min="0" max="100"
                                   v-model="mistake" class="my-slider slider is-info is-fullwidth">
                            </span>
                            <span class="level-right">
                                <label class="label is-small">
                                   Too many <br> grammatical mistake</label>
                            </span>
                        </div>

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

function getFile() {
  axios.get(`project/evaluation/fluency/${this.project_id}/single_doc`)
    .then((response) => {
      this.system_text = response.data.system_text;
      this.ref_text = response.data.ref_text;
      // this.doc_status_id = response.data.doc_status_id;
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
      mistake: 50,
      project_id: this.$route.params.project_id,
    };
  },
  mounted: function onMounted() {
    getFile.call(this);
  },
};
</script>

<style lang="scss">
.home {
  padding-top: 25px;
}
</style>
