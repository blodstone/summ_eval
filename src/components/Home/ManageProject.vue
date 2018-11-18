<template>
    <div class="container">
        <div>
            <b-table :data="projects">
                <template slot-scope="props">
                    <b-table-column field="no" label="No." width="40">
                        {{ props.row.no }}
                    </b-table-column>
                    <b-table-column field="name" label="Name">
                        {{ props.row.name }}
                    </b-table-column>
                    <b-table-column field="dataset_name" label="Dataset">
                        {{ props.row.dataset_name }}
                    </b-table-column>
                    <b-table-column field="created_at"
                                    label="Created at" centered>
                        {{ new Date(props.row.created_at).toLocaleDateString() }}
                    </b-table-column>
                    <b-table-column field="progress is-success" label="Progress">
                        <progress
                                class="progress"
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
  beforeCreate() {
    axios.get('project/progress')
      .then((response) => {
        if (response.status === 204) {
          this.$toast.open({
            message: 'There is no project in database. Please create project first!',
            type: 'is-danger',
          });
        } else {
          this.projects = response.data.projects;
        }
      })
      .catch((error) => {
        console.log(error);
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
