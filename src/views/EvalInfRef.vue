<template>
  <div class="container">
        <div class="columns is-2 is-variable">
            <div class="column is-5 is-offset-1">
                <div class="box document">
                    <div class="content">
                        <h1>Reference Text</h1>
                        <h5 class="my-header">Read this text</h5>
                        <p class="my-summary">{{ ref_text }}</p>
                    </div>
                </div>
            </div>
            <div class="column is-5">
                <div class="box summary">
                    <div class="content">
                        <h1>Assessment</h1>
                        <h5 class="my-header">Summary to be assessed</h5>
                        <p class="my-summary">{{ system_text }}</p>
                        <hr>
                        <h5 class="my-header">
                            Your Assessment
                        </h5>
                        <h5 class="my-title">Question #1</h5>
                        <p class="my-text"> Is the summary missing important information?</p>
                        <p class="my-text">
                            <strong>{{ recall }} % </strong> of information is missing
                        </p>
                        <div class="level" align="center">
                            <span class="level-left">
                                <label class="label is-small">Nothing <br/> is <br/> missing</label>
                            </span>
                            <span class="level-item">
                            <input type="range" min="0" max="100"
                                   v-model="recall" class="my-slider slider is-info is-fullwidth">
                            </span>
                            <span class="level-right">
                                <label class="label is-small">
                                    Everything <br/> is <br/> missing</label>
                            </span>
                        </div>
                        <h5 class="my-title">Question #2</h5>
                        <p class="my-text"> Does the summary contain only important information?</p>
                        <p class="my-text">
                            <strong>{{ precision }} % </strong> of information is important
                        </p>
                        <div class="level" align="center">
                            <span class="level-left">
                                <label class="label is-small">
                                    Nothing <br/> is <br/> important
                                </label>
                            </span>
                            <span class="level-item">
                            <input type="range" min="0" max="100"
                                   v-model="precision"
                                   class="my-slider slider is-info is-fullwidth">
                            </span>
                            <span class="level-right">
                                <label class="label is-small">
                                    Everything <br/> is <br/> important</label>
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
  axios.get(`project/evaluation/informativeness_ref/${this.project_id}/single_doc`)
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
      precision: 50,
      recall: 50,
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
