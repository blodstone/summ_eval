<template>
    <div class="container">
        <div>
            <b-table :data="projects">
                <template slot-scope="props">
                    <b-table-column field="no" label="No." width="40">
                        {{ props.row.no }}
                    </b-table-column>
                    <b-table-column field="id" label="ID" width="40">
                        {{ props.row.id }}
                    </b-table-column>
                    <b-table-column field="name" label="Name">
                        {{ props.row.name }}
                    </b-table-column>
                    <b-table-column field="type" label="Type">
                        {{ props.row.type }}
                    </b-table-column>
                    <b-table-column field="dataset_name" label="Dataset">
                        {{ props.row.dataset_name }}
                    </b-table-column>
                    <b-table-column field="created_at"
                                    label="Created at" centered>
                        {{ new Date(props.row.created_at).toLocaleDateString() }}
                    </b-table-column>
                    <b-table-column field="progress" label="Progress">
                        <progress
                                class="progress is-success"
                                :value="props.row.progress" max="1">
                        </progress>
                        {{
                          props.row.progress
                          .toLocaleString(
                            "en",
                            {style: "percent", maximumSignificantDigits: 2},
                          )
                        }}
                    </b-table-column>
                    <b-table-column label="Link for Participants">
                        <b-field>
                            <b-input icon-pack="fas" icon="link"
                                :value="props.row.link"
                                readonly size="is-small">
                            </b-input>
                            <!--<p class="control">-->
                                <!--<button size="icon is-small is-primary">-->
                                    <!--<i class="fas fa-clipboard"></i>-->
                                <!--</button>-->
                            <!--</p>-->
                        </b-field>
                    </b-table-column>
                    <b-table-column field="id" label="Close Project">
                        <a class="button is-danger is-outlined is-small"
                           v-on:click="close_project(props.row.id)">
                            <span>Close</span>
                            <span class="icon is-small">
                                <i class="fas fa-times"></i>
                            </span>
                        </a>
                    </b-table-column>
                </template>
            </b-table>
        </div>
    </div>
</template>

<script>
import BTable from 'buefy/src/components/table/Table.vue';
import BTableColumn from 'buefy/src/components/table/TableColumn.vue';

const axios = require('axios');

export default {
  name: 'ManageProject',
  components: { BTableColumn, BTable },
  data() {
    return {
      projects: [],
    };
  },
  methods: {
    close_project(id) {
      this.$dialog.confirm({
        message: `Do you want to close project ${id}?`,
        onConfirm: () => {
          axios.post(`project/${id}/close`)
            .then(() => {
              this.$toast.open({
                message: `Project ${id} has been closed`,
                type: 'is-success',
              });
            })
            .catch((error) => {
              this.$toast.open({
                message: `${error}`,
                type: 'is-danger',
              });
            });
        },
      });
    },
  },
  beforeCreate() {
    axios.get('project/all_progress')
      .then((response) => {
        if (response.status === 204) {
          this.$toast.open({
            message: 'There is no active project in database. ' +
              'Please create project first!',
            type: 'is-danger',
          });
        } else {
          this.projects = response.data.projects;
        }
      })
      .catch((error) => {
        this.$toast.open({
          message: `${error}`,
          type: 'is-danger',
        });
      });
  },
};
</script>

<style scoped>
progress {
    display: inline;
    width: 80%;
}
</style>
