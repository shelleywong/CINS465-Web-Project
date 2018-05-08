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

  methods: {
    fetchStudentList: function() {
      $.get('/people/students/',function(user_list) {
        this.users = user_list.users;
        console.log(this.selected);
      }.bind(this));
    },
  },

  // adapted from:
  //https://stackoverflow.com/questions/42883835/sort-an-array-in-vue-js?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
  computed: {
    orderedUsers: function () {
      if(this.selected == "First Name"){
        return this.users.sort((a, b) => a.first_name > b.first_name);
      }
      else if(this.selected == "Last Name"){
        return this.users.sort((a, b) => a.last_name > b.last_name);
      }
      {
        return this.users.sort((a, b) => a.username > b.username);
      }
      else{
        return this.users;
      }
    }
  },
})
