// import _ from 'lodash';

var app_roster = new Vue({
  el: '#app-roster',

  data: {
    users: [],
    selected: '',
  },

  //Adapted from:
  //https://stackoverflow.com/questions/36572540/vue-js-auto-reload-refresh-data-with-timer
  created: function() {
    this.fetchStudentList();
  },

  // adapted from:
  //https://stackoverflow.com/questions/42883835/sort-an-array-in-vue-js?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
  computed: {
    orderedUsers: function () {
      if(this.selected == "First Name"){
        // return _.orderBy(this.users, 'first_name')
        return this.users.sort((a, b) => a.first_name.toLowerCase() > b.first_name.toLowerCase());
      }
      else if(this.selected == "Last Name"){
        // return _.orderBy(this.users, 'last_name')
        return this.users.sort((a, b) => a.last_name.toLowerCase() > b.last_name.toLowerCase());
      }
      else if(this.selected == "Username"){
        // return _.orderBy(this.users, 'username')
        return this.users.sort((a, b) => a.username.toLowerCase() > b.username.toLowerCase());
      }
      else{
        return this.users;
      }
    },
  },

  methods: {
    fetchStudentList: function() {
      $.get('/people/students/',function(user_list) {
        this.users = user_list.users;
        console.log(this.selected);
      }.bind(this));
    },
  },

})
