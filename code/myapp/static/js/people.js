var app_student = new Vue({
  el: '#app-student',

  data: {
    users: []
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
        console.log(user_list);
      }.bind(this));
    },
  },
})
