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
  //https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter
  //https://stackoverflow.com/questions/42883835/sort-an-array-in-vue-js?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
  computed: {
    orderedUsers: function () {
      if(this.selected == "First Names A-M"){
        return this.users.filter(
          (word) => word.first_name.toLowerCase() < 'n').sort(
          (a, b) => a.first_name.toLowerCase() > b.first_name.toLowerCase()
        );
      }
      else if(this.selected == "First Names N-Z"){
        return this.users.filter(
          (word) => word.first_name.toLowerCase() > 'n').sort(
          (a, b) => a.first_name.toLowerCase() > b.first_name.toLowerCase()
        );
      }
      else if(this.selected == "Last Names A-M"){
        return this.users.filter(
          (word) => word.last_name.toLowerCase() < 'n').sort(
          (a, b) => a.last_name.toLowerCase() > b.last_name.toLowerCase()
        );
      }
      else if(this.selected == "Last Names N-Z"){
        return this.users.filter(
          (word) => word.last_name.toLowerCase() > 'n').sort(
          (a, b) => a.last_name.toLowerCase() > b.last_name.toLowerCase()
        );
      }
      else if(this.selected == "Usernames A-M"){
        return this.users.filter(
          (word) => word.username.toLowerCase() < 'n').sort(
          (a, b) => a.username.toLowerCase() > b.username.toLowerCase()
        );
      }
      else if(this.selected == "Usernames N-Z"){
        return this.users.filter(
          (word) => word.username.toLowerCase() > 'n').sort(
          (a, b) => a.username.toLowerCase() > b.username.toLowerCase()
        );
      }
      else if(this.selected == "Show All" || this.selected == ""){
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
